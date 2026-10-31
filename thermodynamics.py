"""Termodinamik yolculuğu — ilk beş bölüm.

Önizleme:
    manim -pql thermodynamics.py Chapter1
    manim -pql thermodynamics.py Chapter2
    manim -pql thermodynamics.py Chapter3 Chapter4 Chapter5
"""

from __future__ import annotations

import numpy as np
from manim import *


FONT = "Arial"


NARRATION = {
    "chapter_1": [
        "Gözünle göremediğin bu dünyada, gaz molekülleri sürekli hareket eder.",
        "Benim adım Mola. Bir gaz molekülüyüm; duvarlara çarpar, yön değiştiririm.",
        "Sen artık bir moleküldün. Şimdi sistemin tamamına dışarıdan bakalım.",
        "Basınç, hacim, madde miktarı ve mutlak sıcaklık: gazı anlatan dört değişken.",
    ],
    "chapter_2": [
        "Bir molekülün enerjisi, farklı hareket biçimlerinden oluşabilir.",
        "Bu katkıları topladığımızda molekülün enerjisini; bütün molekülleri topladığımızda iç enerjiyi buluruz.",
        "İdeal gaz modelinde moleküller arası potansiyel enerjiyi ihmal ederiz.",
        "Isı, depolanan bir şey değil; sıcaklık farkı nedeniyle sistemler arasında aktarılan enerjidir.",
        "Enerji sıcak kaptan soğuk kaba aktarılır. Soğuk kabın iç enerjisi artar.",
    ],
    "chapter_3": [
        "Gazdaki moleküllerin hızları birbirinden farklıdır; sıcaklık tek bir molekülün hızını göstermez.",
        "Sıcaklık, moleküllerin ortalama öteleme kinetik enerjisiyle ilişkilidir.",
        "İki kap aynı sıcaklıkta olabilir; daha çok molekül içeren kapta toplam iç enerji daha büyüktür.",
    ],
    "chapter_4": [
        "Mola duvara çarptığında momentumu değişir; duvar da bir itme alır.",
        "Çarpışmaların duvara aktardığı momentum, kuvveti; kuvvetin yüzeye dağılımı basıncı oluşturur.",
    ],
    "chapter_5": [
        "Sıcaklık ve mol sayısı sabitken pistonu aşağı indirirsek aynı gaz daha küçük bir hacme sıkışır.",
        "Moleküller duvarlara daha sık çarpar. Böylece basınç yükselir ve PV çarpımı sabit kalır.",
    ],
}


def _precompute_paths(
    count: int,
    duration: float,
    samples_per_second: int = 24,
    radius: float = 1.38,
    half_height: float = 1.78,
    seed: int = 24,
) -> np.ndarray:
    """Silindirin içinde yansıyan molekül yollarını bir kez hesapla."""
    rng = np.random.default_rng(seed)
    sample_count = int(duration * samples_per_second) + 1
    dt = 1 / samples_per_second

    radial_distance = radius * np.sqrt(rng.random(count))
    angle = rng.uniform(0, TAU, count)
    positions = np.column_stack(
        (
            radial_distance * np.cos(angle),
            rng.uniform(-half_height, half_height, count),
            radial_distance * np.sin(angle),
        )
    )
    velocities = rng.normal(size=(count, 3))
    velocities /= np.linalg.norm(velocities, axis=1, keepdims=True)
    speeds = rng.uniform(0.65, 1.45, count)
    velocities *= speeds[:, np.newaxis]

    paths = np.empty((sample_count, count, 3), dtype=float)
    paths[0] = positions
    for frame in range(1, sample_count):
        positions += velocities * dt

        radial = np.linalg.norm(positions[:, (0, 2)], axis=1)
        outside = radial > radius
        if np.any(outside):
            normals = positions[outside][:, (0, 2)] / radial[outside, np.newaxis]
            radial_velocity = np.sum(velocities[outside][:, (0, 2)] * normals, axis=1)
            velocities[outside, 0] -= 2 * radial_velocity * normals[:, 0]
            velocities[outside, 2] -= 2 * radial_velocity * normals[:, 1]
            positions[outside, 0] *= radius / radial[outside]
            positions[outside, 2] *= radius / radial[outside]

        top = positions[:, 1] > half_height
        bottom = positions[:, 1] < -half_height
        positions[top, 1] = 2 * half_height - positions[top, 1]
        velocities[top, 1] *= -1
        positions[bottom, 1] = -2 * half_height - positions[bottom, 1]
        velocities[bottom, 1] *= -1

        paths[frame] = positions
    return paths


def _sample_path(path: np.ndarray, time: float, samples_per_second: int = 24) -> np.ndarray:
    index = min(int(time * samples_per_second), len(path) - 1)
    next_index = min(index + 1, len(path) - 1)
    fraction = min(max(time * samples_per_second - index, 0.0), 1.0)
    return path[index] * (1 - fraction) + path[next_index] * fraction


def _simulate_gas_paths(
    initial_positions: np.ndarray,
    duration: float,
    radius: float,
    lower: float,
    upper_start: float,
    seed: int,
    center_x: float = 0.0,
    upper_end: float | None = None,
    initial_velocities: np.ndarray | None = None,
    samples_per_second: int = 24,
    substeps: int = 4,
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], np.ndarray]:
    """Önceden hesaplanan yolları, çarpışma sayılarını ve olay zamanlarını üret."""
    rng = np.random.default_rng(seed)
    positions = initial_positions.copy()
    if initial_velocities is None:
        velocities = rng.normal(size=positions.shape)
        velocities[:, 2] = 0
        velocities /= np.linalg.norm(velocities, axis=1, keepdims=True)
        velocities *= rng.uniform(0.9, 1.45, size=(len(positions), 1))
    else:
        velocities = initial_velocities.copy()

    frame_count = int(duration * samples_per_second) + 1
    paths = np.empty((frame_count, len(positions), 3), dtype=float)
    hit_totals = np.zeros(frame_count, dtype=int)
    hit_times: list[list[float]] = [[] for _ in range(len(positions))]
    paths[0] = positions
    hits = 0
    dt = 1 / (samples_per_second * substeps)
    upper_end = upper_start if upper_end is None else upper_end
    wall_velocity = (upper_end - upper_start) / duration

    for frame in range(1, frame_count):
        for substep in range(substeps):
            elapsed = ((frame - 1) * substeps + substep + 1) * dt
            current_upper = upper_start + wall_velocity * elapsed
            positions += velocities * dt

            radial_positions = positions[:, (0, 2)].copy()
            radial_positions[:, 0] -= center_x
            radial = np.linalg.norm(radial_positions, axis=1)
            side_hit = radial > radius
            if np.any(side_hit):
                normals = radial_positions[side_hit] / radial[side_hit, np.newaxis]
                radial_speed = np.sum(velocities[side_hit][:, (0, 2)] * normals, axis=1)
                velocities[side_hit, 0] -= 2 * radial_speed * normals[:, 0]
                velocities[side_hit, 2] -= 2 * radial_speed * normals[:, 1]
                positions[side_hit, 0] = center_x + radial_positions[side_hit, 0] * (
                    radius / radial[side_hit]
                )
                positions[side_hit, 2] *= radius / radial[side_hit]

            top_hit = positions[:, 1] > current_upper
            bottom_hit = positions[:, 1] < lower
            positions[top_hit, 1] = 2 * current_upper - positions[top_hit, 1]
            velocities[top_hit, 1] = 2 * wall_velocity - velocities[top_hit, 1]
            positions[bottom_hit, 1] = 2 * lower - positions[bottom_hit, 1]
            velocities[bottom_hit, 1] *= -1
            for molecule_index in np.flatnonzero(top_hit):
                hit_times[molecule_index].append(elapsed)
            hits += int(np.count_nonzero(top_hit))

        paths[frame] = positions
        hit_totals[frame] = hits

    return (
        paths,
        hit_totals,
        [np.asarray(events) for events in hit_times],
        velocities,
    )


def _text(content: str, size: float = 30, color=WHITE) -> Text:
    return Text(content, font=FONT, font_size=size, color=color)


def _prediction_prompt(scene: ThreeDScene, question: str, correct: str):
    question_text = _text(question, 30, YELLOW).to_edge(UP, buff=0.42)
    choices = VGroup(
        *[_text(choice, 28, WHITE) for choice in ("ARTAR", "AZALIR", "DEĞİŞMEZ")]
    ).arrange(RIGHT, buff=0.7)
    choices.to_edge(DOWN, buff=0.55)
    card = VGroup(question_text, choices)
    scene.add_fixed_in_frame_mobjects(card)
    scene.wait(5)
    return card, choices[("ARTAR", "AZALIR", "DEĞİŞMEZ").index(correct)]


def _close_prediction(scene: ThreeDScene, card: VGroup, correct: Text, explanation: Text):
    correct.set_color(GREEN)
    scene.play(Indicate(correct, color=GREEN, scale_factor=1.12), run_time=0.8)
    scene.remove_fixed_in_frame_mobjects(card)
    scene.remove(card)
    explanation.to_edge(DOWN, buff=0.12)
    scene.add_fixed_in_frame_mobjects(explanation)
    scene.play(FadeIn(explanation), run_time=0.5)
    scene.wait(3)
    scene.remove_fixed_in_frame_mobjects(explanation)
    scene.remove(card, explanation)


class Chapter1(ThreeDScene):
    """Bölüm 1 — molekül perspektifiyle gaz sistemine giriş."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=68 * DEGREES, theta=-48 * DEGREES, zoom=0.9)

        title = _text("THE PHYSICS OF GASES", 38, BLUE_A).to_edge(UP, buff=0.35)
        subtitle = _text("Görünmeyen dünyaya yolculuk", 24, GREY_A).next_to(
            title, DOWN, buff=0.15
        )
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=1.5)
        self.wait(1)

        radius = 1.65
        height = 4.2
        chamber = Cylinder(
            radius=radius,
            height=height,
            direction=UP,
            resolution=(24, 16),
            fill_color=BLUE_E,
            fill_opacity=0.08,
            stroke_color=BLUE_A,
            stroke_opacity=0.7,
            stroke_width=1.5,
        )
        rings = VGroup(
            *[
                Circle(radius=radius, color=BLUE_B, stroke_width=1.5)
                .rotate(90 * DEGREES, axis=RIGHT)
                .move_to(UP * y)
                for y in (-height / 2, height / 2)
            ]
        )

        duration = 9
        paths = _precompute_paths(40, duration)
        tracker = ValueTracker(0)
        molecules = VGroup()
        for i, path in enumerate(paths.transpose(1, 0, 2)):
            speed_fraction = (i % 7) / 6
            color = interpolate_color(BLUE_C, ORANGE, speed_fraction)
            molecule = Dot3D(
                radius=0.075 if i == 0 else 0.045,
                resolution=(8, 8),
                color=color,
                fill_opacity=0.95,
                stroke_width=0,
            )
            molecule.move_to(path[0])
            molecule.add_updater(
                lambda mob, _dt=0, p=path, clock=tracker: mob.move_to(
                    _sample_path(p, clock.get_value())
                )
            )
            molecules.add(molecule)

        self.play(Create(chamber), Create(rings), run_time=2)
        self.play(FadeIn(molecules), run_time=1.2)
        self.play(tracker.animate.set_value(2.5), run_time=2.5, rate_func=linear)

        mola = molecules[0]
        mola_label = _text("Mola", 24, ORANGE).to_corner(UL, buff=0.35)
        self.add_fixed_in_frame_mobjects(mola_label)
        self.move_camera(frame_center=mola.get_center(), zoom=1.35, run_time=2)

        follow_anchor = VectorizedPoint(mola.get_center())

        def follow_mola(_mob, _dt=0):
            self.camera.frame_center = mola.get_center()

        follow_anchor.add_updater(follow_mola)
        self.add(follow_anchor)
        self.play(tracker.animate.set_value(5), run_time=2.5, rate_func=linear)
        follow_anchor.clear_updaters()
        self.remove(follow_anchor)
        self.wait(1)

        self.move_camera(frame_center=ORIGIN, zoom=0.9, run_time=2)
        self.play(tracker.animate.set_value(7), run_time=2, rate_func=linear)
        intro = _text("Sen artık bir moleküldün…", 30, YELLOW).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(intro)
        self.play(FadeIn(intro), run_time=0.8)
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(intro, mola_label, title, subtitle)
        self.remove(intro, mola_label, title, subtitle)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(tracker.animate.set_value(duration), run_time=2, rate_func=linear)
        self.stop_ambient_camera_rotation()
        molecules.clear_updaters()

        heading = _text("Bir gazı dört değişkenle anlatırız", 30, WHITE).to_edge(UP, buff=0.4)
        indicators = VGroup(
            _text("P  Basınç", 26, BLUE_A),
            _text("V  Hacim", 26, GREEN_A),
            _text("n  Madde miktarı", 26, YELLOW),
            _text("T  Mutlak sıcaklık", 26, ORANGE),
        ).arrange(RIGHT, buff=0.48).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(heading, indicators)
        self.play(FadeIn(heading), LaggedStart(*[FadeIn(item) for item in indicators], lag_ratio=0.2))
        self.wait(4)


class Chapter2(ThreeDScene):
    """Bölüm 2 — iç enerji ve ısının aktarımı."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.0)

        heading = _text("ENERJİ: MOLEKÜLDEN SİSTEME", 34, BLUE_A).to_edge(UP, buff=0.35)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), run_time=1)

        mola = Dot3D(
            radius=0.24,
            resolution=(8, 8),
            color=BLUE_C,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 2.7 + DOWN * 0.1)
        mola_name = _text("Mola", 23, ORANGE).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(mola_name)
        self.play(FadeIn(mola), FadeIn(mola_name), run_time=1)

        labels = [
            "Öteleme kinetik enerjisi",
            "Dönme kinetik enerjisi",
            "Titreşim kinetik enerjisi",
            "Potansiyel enerji (gerçek gaz)",
        ]
        colors = [BLUE_C, GREEN_C, YELLOW, ORANGE]
        segments = VGroup()
        for i, (label, color) in enumerate(zip(labels, colors)):
            block = Cube(
                side_length=0.62,
                fill_color=color,
                fill_opacity=0.88,
                stroke_color=WHITE,
                stroke_width=0.5,
            ).move_to(RIGHT * 1.5 + UP * (1.1 - i * 0.68))
            label_text = _text(label, 21, color).move_to(RIGHT * 3.2 + UP * (1.1 - i * 0.68))
            segments.add(VGroup(block, label_text))

        for segment in segments:
            self.play(FadeIn(segment), run_time=0.55)
        self.play(mola.animate.set_color(ORANGE), run_time=1)

        total_bar = SurroundingRectangle(
            VGroup(*[segment[0] for segment in segments]),
            color=WHITE,
            buff=0.12,
            stroke_width=1.5,
        )
        total_label = _text("Bir molekülün toplam enerjisi", 23, WHITE).next_to(
            total_bar, DOWN, buff=0.18
        )
        self.play(Create(total_bar), FadeIn(total_label), run_time=1)
        ideal_note = _text(
            "İdeal gazda moleküller arası potansiyel enerji ihmal edilir.",
            22,
            GREY_A,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(ideal_note)
        self.play(FadeIn(ideal_note), run_time=0.6)
        self.wait(3)

        other_molecules = VGroup(
            *[
                Dot3D(
                    radius=0.07,
                    resolution=(8, 8),
                    color=interpolate_color(BLUE_C, ORANGE, i / 17),
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(
                    LEFT * 2.7
                    + RIGHT * ((i % 6) * 0.22 - 0.55)
                    + UP * ((i // 6) * 0.22 - 0.3)
                )
                for i in range(18)
            ]
        )
        sum_label = _text("Bütün moleküllerin enerjileri toplanır", 24, WHITE).to_edge(
            UP, buff=1.1
        )
        internal_energy = _text(
            "İÇ ENERJİ  U = Σ (E öteleme + E dönme + E titreşim + E potansiyel)",
            25,
            YELLOW,
        ).to_edge(DOWN, buff=0.85)
        self.play(FadeIn(other_molecules), FadeIn(sum_label), run_time=1.2)
        self.add_fixed_in_frame_mobjects(sum_label, internal_energy)
        self.play(FadeIn(internal_energy), run_time=1)
        self.wait(3)

        # Isı aktarımı, iç enerjinin kendisi değil iki sistem arasındaki enerji akışıdır.
        self.play(
            FadeOut(other_molecules),
            FadeOut(segments),
            FadeOut(total_bar),
            FadeOut(total_label),
            FadeOut(mola),
            FadeOut(sum_label),
            FadeOut(internal_energy),
            FadeOut(ideal_note),
            run_time=1,
        )
        self.remove_fixed_in_frame_mobjects(
            heading, mola_name, sum_label, internal_energy, ideal_note
        )
        self.remove(heading, mola_name, sum_label, internal_energy, ideal_note)
        hot_vessel = Cylinder(
            radius=0.62,
            height=1.45,
            direction=UP,
            resolution=(20, 12),
            fill_color=RED_E,
            fill_opacity=0.45,
            stroke_color=RED_A,
            stroke_width=1.5,
        ).move_to(LEFT * 2)
        cold_vessel = Cylinder(
            radius=0.62,
            height=1.45,
            direction=UP,
            resolution=(20, 12),
            fill_color=BLUE_E,
            fill_opacity=0.45,
            stroke_color=BLUE_A,
            stroke_width=1.5,
        ).move_to(RIGHT * 2)
        hot_label = _text("SICAK SİSTEM", 22, RED_A).move_to(LEFT * 2 + DOWN * 1.25)
        cold_label = _text("SOĞUK SİSTEM", 22, BLUE_A).move_to(RIGHT * 2 + DOWN * 1.25)
        self.play(
            FadeIn(hot_vessel),
            FadeIn(cold_vessel),
            FadeIn(hot_label),
            FadeIn(cold_label),
            run_time=1.2,
        )

        question = "Soğuk sisteme enerji aktarılırsa iç enerjisi ne olur?"
        card, correct = _prediction_prompt(self, question, "ARTAR")

        transfer_dots = VGroup(
            *[
                Dot3D(
                    radius=0.075,
                    resolution=(8, 8),
                    color=interpolate_color(RED_C, YELLOW, i / 5),
                    fill_opacity=1,
                    stroke_width=0,
                ).move_to(LEFT * 1.25 + UP * ((i - 2.5) * 0.18))
                for i in range(6)
            ]
        )
        self.add(transfer_dots)
        self.play(
            *[
                dot.animate.move_to(RIGHT * 1.25 + UP * ((i - 2.5) * 0.18))
                for i, dot in enumerate(transfer_dots)
            ],
            run_time=2.5,
            rate_func=linear,
        )
        explanation = _text(
            "Isı Q: sıcaklık farkıyla aktarılan enerjidir; bir enerji deposu değildir.",
            22,
            WHITE,
        )
        _close_prediction(self, card, correct, explanation)
        self.play(FadeOut(transfer_dots), run_time=0.6)

        heat_formula = _text("ΔU = Q + W", 40, YELLOW).to_edge(UP, buff=1.05)
        sign_note = _text(
            "W: sisteme yapılan iş  •  Isı: sıcak olandan soğuk olana aktarım",
            21,
            GREY_A,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(heat_formula, sign_note)
        self.play(FadeIn(heat_formula), FadeIn(sign_note), run_time=1)
        self.wait(5)


class Chapter3(ThreeDScene):
    """Bölüm 3 — sıcaklığın ortalama kinetik enerjiyle ilişkisi."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("SICAKLIK: ENERJİLERİN ORTALAMASI", 32, BLUE_A).to_edge(
            UP, buff=0.35
        )
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.8)

        x_left, x_right, baseline = -3.2, 3.2, -1.05
        axes = VGroup(
            Line(
                np.array([x_left, baseline, 0]),
                np.array([x_right, baseline, 0]),
                color=GREY_B,
                stroke_width=2,
            ),
            Line(
                np.array([x_left, baseline, 0]),
                np.array([x_left, 1.55, 0]),
                color=GREY_B,
                stroke_width=2,
            ),
        )
        counts = np.array([0.2, 0.42, 0.75, 1.1, 1.38, 1.18, 0.82, 0.46, 0.21])
        x_values = np.linspace(-2.8, 2.8, len(counts))
        bars = VGroup()
        for x, height in zip(x_values, counts):
            bar = Cube(
                side_length=1,
                fill_color=BLUE_C,
                fill_opacity=0.88,
                stroke_color=BLUE_A,
                stroke_width=0.5,
            )
            bar.stretch_to_fit_width(0.42)
            bar.stretch_to_fit_depth(0.42)
            bar.stretch_to_fit_height(float(height))
            bar.move_to(np.array([x, baseline + height / 2, 0]))
            bars.add(bar)
        mean_x = float(np.average(x_values, weights=counts))
        average_line = DashedLine(
            np.array([mean_x, baseline, 0]),
            np.array([mean_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=3,
        )
        average_label = _text("Ortalama", 20, YELLOW).move_to(
            np.array([mean_x, 1.92, 0])
        )
        labels = VGroup(
            _text("Düşük enerji", 18, GREY_A).move_to(np.array([-2.45, -1.38, 0])),
            _text("Yüksek enerji", 18, GREY_A).move_to(np.array([2.35, -1.38, 0])),
        )
        count_label = _text("Molekül sayısı", 18, GREY_A).rotate(90 * DEGREES)
        count_label.move_to(np.array([-3.65, 0.1, 0]))
        for fixed_object in (axes, bars, average_line, average_label, labels, count_label):
            self.add_fixed_in_frame_mobjects(fixed_object)
        self.play(
            Create(axes),
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.08),
            run_time=2,
        )
        self.play(
            Create(average_line),
            FadeIn(average_label),
            FadeIn(labels),
            FadeIn(count_label),
            run_time=0.8,
        )

        explanation = _text(
            "Çubuklar moleküllerin kinetik enerjilerini gösterir; çoğu orta enerjidedir.",
            22,
            WHITE,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(FadeIn(explanation), run_time=0.7)
        self.wait(2)

        heat_label = _text("Isıtma", 23, ORANGE).to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(heat_label)
        self.play(
            bars.animate.shift(RIGHT * 0.55).set_color(ORANGE),
            average_line.animate.shift(RIGHT * 0.55).set_color(ORANGE),
            average_label.animate.shift(RIGHT * 0.55).set_color(ORANGE),
            FadeIn(heat_label),
            run_time=1.8,
        )
        formula = _text("Ortalama E_kin = (3/2) k_B T", 29, YELLOW).to_edge(
            DOWN, buff=0.35
        )
        average_note = _text(
            "Sıcaklık, öteleme kinetik enerjisinin ortalamasıyla ilişkilidir; tüm enerji türlerinin değil.",
            18,
            WHITE,
        ).next_to(formula, UP, buff=0.12)
        self.remove_fixed_in_frame_mobjects(explanation)
        self.remove(explanation)
        self.add_fixed_in_frame_mobjects(formula, average_note)
        self.play(FadeIn(formula), FadeIn(average_note), run_time=0.8)
        self.wait(3)

        self.play(
            FadeOut(axes),
            FadeOut(bars),
            FadeOut(average_line),
            FadeOut(average_label),
            FadeOut(labels),
            FadeOut(count_label),
            FadeOut(heat_label),
            FadeOut(formula),
            FadeOut(average_note),
            run_time=0.8,
        )
        self.remove_fixed_in_frame_mobjects(
            title,
            axes,
            bars,
            average_line,
            average_label,
            labels,
            count_label,
            heat_label,
            formula,
            average_note,
        )
        self.remove(
            title, axes, bars, average_line, average_label, labels, count_label,
            heat_label, formula, average_note,
        )

        vessel_left = Cylinder(
            radius=0.82,
            height=1.8,
            direction=UP,
            resolution=(16, 10),
            fill_color=BLUE_E,
            fill_opacity=0.16,
            stroke_color=BLUE_A,
            stroke_opacity=0.16,
            stroke_width=0.5,
        ).move_to(LEFT * 2.0)
        vessel_right = vessel_left.copy().set_color(GREEN_A).move_to(RIGHT * 2.0)
        many = VGroup()
        few = VGroup()
        rng = np.random.default_rng(303)
        for group, center, amount, color in (
            (many, LEFT * 2.0, 16, BLUE_C),
            (few, RIGHT * 2.0, 5, GREEN_C),
        ):
            for _ in range(amount):
                angle = rng.uniform(0, TAU)
                radial = rng.uniform(0.12, 0.56)
                point = center + np.array(
                    [
                        radial * np.cos(angle),
                        rng.uniform(-0.65, 0.65),
                        radial * np.sin(angle),
                    ]
                )
                group.add(
                    Dot3D(
                        point=point,
                        radius=0.07,
                        resolution=(8, 8),
                        color=color,
                        fill_opacity=0.95,
                    )
                )
        comparison = _text(
            "Aynı sıcaklık: ortalama kinetik enerji aynı",
            24,
            YELLOW,
        ).to_edge(UP, buff=0.85)
        labels = VGroup(
            _text("Çok molekül", 22, BLUE_A).move_to(np.array([-2.0, -1.4, 0])),
            _text("Az molekül", 22, GREEN_A).move_to(np.array([2.0, -1.4, 0])),
        )
        total_energy = _text(
            "Molekül sayısı fazla → toplam iç enerji U daha büyük",
            23,
            WHITE,
        ).move_to(np.array([0, -3.05, 0]))
        comparison.move_to(np.array([0, 2.8, 0]))
        self.add_fixed_in_frame_mobjects(comparison, labels, total_energy)
        self.play(
            FadeIn(vessel_left),
            FadeIn(vessel_right),
            FadeIn(many),
            FadeIn(few),
            FadeIn(labels),
            run_time=1.5,
        )
        self.play(FadeIn(comparison), FadeIn(total_energy), run_time=0.8)
        self.wait(4)


class Chapter4(ThreeDScene):
    """Bölüm 4 — basınç, duvar çarpışmalarından doğar."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=68 * DEGREES, theta=-38 * DEGREES, zoom=1.0)

        title = _text("BASINÇ: DUVARA ÇARPIŞMALAR", 32, BLUE_A).to_edge(
            UP, buff=0.35
        )
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.8)

        chamber = Cube(
            side_length=1,
            fill_color=BLUE_E,
            fill_opacity=0.045,
            stroke_color=BLUE_A,
            stroke_opacity=0.8,
            stroke_width=1.5,
        )
        chamber.stretch_to_fit_width(3.6)
        chamber.stretch_to_fit_height(2.6)
        chamber.stretch_to_fit_depth(2.3)
        self.play(Create(chamber), run_time=1.2)

        time = ValueTracker(0)
        xmin, xmax = -1.52, 1.52
        speed = 2.0

        def position_at(t: float) -> np.ndarray:
            phase = (speed * t) % (2 * (xmax - xmin))
            x = xmin + phase if phase <= xmax - xmin else xmax - (
                phase - (xmax - xmin)
            )
            return np.array([x, 0.0, 0.0])

        def hit_count(t: float) -> int:
            return int(np.floor((speed * t + 1e-8) / (xmax - xmin)))

        mola = Dot3D(
            radius=0.13,
            resolution=(10, 10),
            color=ORANGE,
            fill_opacity=1,
        ).move_to(position_at(0))
        mola.add_updater(lambda mob: mob.move_to(position_at(time.get_value())))
        self.add(mola)

        label = _text("Mola", 22, ORANGE).to_corner(UL, buff=0.4)
        counter_label = _text("Duvar çarpması:", 23, WHITE).to_corner(UR, buff=0.55)
        counter = _text("0", 30, YELLOW).next_to(counter_label, DOWN, buff=0.15)
        counter_position = counter.get_center().copy()
        counter.add_updater(
            lambda mob: mob.become(
                _text(str(hit_count(time.get_value())), 30, YELLOW).move_to(
                    counter_position
                )
            )
        )
        self.add_fixed_in_frame_mobjects(label, counter_label, counter)
        self.play(FadeIn(label), FadeIn(counter_label), FadeIn(counter), run_time=0.6)

        self.play(time.animate.set_value(1.52), run_time=1.52, rate_func=linear)
        contact = Dot3D(
            point=np.array([xmax, 0, 0]),
            radius=0.21,
            resolution=(8, 8),
            color=YELLOW,
            fill_opacity=0.8,
        )
        self.play(FadeIn(contact), mola.animate.scale(1.35), run_time=0.18)
        self.move_camera(frame_center=UP * 0.08, run_time=0.08)
        self.move_camera(frame_center=ORIGIN, run_time=0.08)
        self.play(FadeOut(contact), mola.animate.scale(1 / 1.35), run_time=0.2)

        vector_before = Arrow(
            np.array([-4.1, -2.5, 0]),
            np.array([-2.25, -2.5, 0]),
            color=YELLOW,
            buff=0,
            stroke_width=7,
        )
        vector_after = Arrow(
            np.array([4.1, -2.5, 0]),
            np.array([2.25, -2.5, 0]),
            color=BLUE_B,
            buff=0,
            stroke_width=7,
        )
        vectors_text = VGroup(
            _text("Çarpmadan önce", 19, YELLOW).move_to(np.array([-3.2, -2.12, 0])),
            _text("Çarpmadan sonra", 19, BLUE_B).move_to(np.array([3.2, -2.12, 0])),
        )
        self.add_fixed_in_frame_mobjects(vector_before, vector_after, vectors_text)
        self.wait(0.7)
        self.play(time.animate.set_value(5.2), run_time=3.68, rate_func=linear)

        explanation = _text(
            "Mola'nın momentumu değişir; duvar, gelen her çarpışmada kuvvet alır.",
            21,
            WHITE,
        ).to_edge(DOWN, buff=0.9)
        formula = _text("Basınç P = Kuvvet F / Yüzey alanı A", 27, YELLOW).to_edge(
            DOWN, buff=0.28
        )
        self.add_fixed_in_frame_mobjects(explanation, formula)
        self.play(FadeIn(explanation), FadeIn(formula), run_time=0.8)
        self.wait(3)
        mola.clear_updaters()
        counter.clear_updaters()


class Chapter5(ThreeDScene):
    """Bölüm 5 — Boyle yasası: sıcaklık ve mol sayısı sabit."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("BOYLE YASASI", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("T ve n sabit", 21, GREY_A).next_to(title, DOWN, buff=0.1)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.8)

        radius = 1.12
        lower = -1.7
        upper_initial = 1.3
        upper_compressed = -0.2
        vessel = Cylinder(
            radius=radius,
            height=3.0,
            direction=UP,
            resolution=(20, 12),
            fill_color=BLUE_E,
            fill_opacity=0.08,
            stroke_color=BLUE_A,
            stroke_opacity=0.16,
            stroke_width=0.5,
        ).move_to(np.array([-2.35, -0.2, 0]))
        vessel_center_x = -2.35
        self.play(Create(vessel), run_time=1)

        piston = Cylinder(
            radius=radius * 0.96,
            height=0.14,
            direction=UP,
            resolution=(20, 12),
            fill_color=GREY_B,
            fill_opacity=0.95,
            stroke_color=WHITE,
        ).move_to(np.array([vessel_center_x, upper_initial, 0]))
        gas = VGroup()
        rng = np.random.default_rng(55)
        for index in range(40):
            horizontal = rng.uniform(-radius * 0.72, radius * 0.72)
            point = np.array(
                [
                    vessel_center_x + horizontal,
                    rng.uniform(lower + 0.18, upper_initial - 0.18),
                    0.0,
                ]
            )
            gas.add(
                Dot(
                    point=point,
                    radius=0.11 if index == 0 else 0.055,
                    color=ORANGE if index == 0 else BLUE_C,
                    fill_opacity=0.95,
                )
            )
        self.play(FadeIn(piston), FadeIn(gas), run_time=1)

        graph_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=3.7,
            y_length=2.8,
            axis_config={"color": GREY_B, "include_tip": True, "stroke_width": 2},
        ).move_to(RIGHT * 2.35 + DOWN * 0.25)
        curve = graph_axes.plot(
            lambda volume: 4 / volume,
            x_range=[0.8, 4.5],
            color=YELLOW,
            stroke_width=4,
        )
        invariant_label = _text("Boyle: PV = sabit", 23, YELLOW).move_to(
            RIGHT * 2.35 + UP * 2.0
        )
        volume_label = _text("Hacim V", 17, GREY_A).move_to(
            RIGHT * 2.35 + DOWN * 2.0
        )
        pressure_label = _text("P", 17, GREY_A).move_to(
            RIGHT * 0.45 + DOWN * 0.1
        )
        pressure_label.rotate(90 * DEGREES)
        self.add_fixed_in_frame_mobjects(
            graph_axes, curve, invariant_label, volume_label, pressure_label
        )
        self.play(
            Create(graph_axes),
            Create(curve),
            FadeIn(invariant_label),
            FadeIn(volume_label),
            FadeIn(pressure_label),
            run_time=1.2,
        )

        volume_point = Dot(graph_axes.c2p(3, 4 / 3), color=ORANGE, radius=0.09)
        self.add_fixed_in_frame_mobjects(volume_point)
        self.play(FadeIn(volume_point))
        self.remove_fixed_in_frame_mobjects(title, condition)
        self.remove(title, condition)

        observation_time = 4.0
        compression_time = 1.25
        initial_positions = np.array([molecule.get_center() for molecule in gas])
        inner_radius = radius - 0.12
        inner_lower = lower + 0.12
        inner_upper_initial = upper_initial - 0.12
        original_colors = [BLUE_C if index else ORANGE for index in range(len(gas))]

        phase_label = _text("PİSTON SABİT", 20, GREEN_A).move_to(LEFT * 4.65 + UP * 2.1)
        counter_heading = _text("Piston çarpması", 19, WHITE).move_to(
            LEFT * 4.65 + UP * 1.55
        )
        counter_position = LEFT * 4.65 + UP * 0.95
        counter = _text("0", 34, YELLOW).move_to(counter_position)
        measurement_label = _text(f"Son {observation_time:.0f} saniyede", 17, GREY_A).move_to(
            LEFT * 4.65 + UP * 0.42
        )
        self.add_fixed_in_frame_mobjects(
            phase_label, counter_heading, counter, measurement_label
        )
        self.play(
            FadeIn(phase_label),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(measurement_label),
            run_time=0.6,
        )

        def animate_gas_interval(
            positions: np.ndarray,
            velocities: np.ndarray | None,
            duration: float,
            wall_start: float,
            wall_end: float,
            label: str,
        ) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], np.ndarray]:
            paths, totals, events, final_velocities = _simulate_gas_paths(
                positions,
                duration,
                inner_radius,
                inner_lower,
                wall_start,
                seed=81,
                center_x=vessel_center_x,
                upper_end=wall_end,
                initial_velocities=velocities,
            )
            clock = ValueTracker(0)
            all_events = (
                np.sort(np.concatenate(events))
                if any(len(entry) for entry in events)
                else np.array([])
            )

            def last_event_age(event_times: np.ndarray, now: float) -> float:
                previous = np.searchsorted(event_times, now, side="right") - 1
                return now - event_times[previous] if previous >= 0 else duration

            for index, molecule in enumerate(gas):
                molecule.clear_updaters()
                event_times = events[index]
                path = paths[:, index, :]
                pulse_state = {"scale": 1.0, "active": False}

                def update_molecule(
                    mob,
                    _dt=0,
                    molecule_path=path,
                    collisions=event_times,
                    source_index=index,
                    state=pulse_state,
                    timer=clock,
                ):
                    now = timer.get_value()
                    age = last_event_age(collisions, now)
                    active = age < 0.1
                    pulse = np.sin(np.pi * age / 0.1) if active else 0.0
                    scale = 1 + 0.7 * pulse
                    mob.scale(scale / state["scale"])
                    state["scale"] = scale
                    if active != state["active"]:
                        mob.set_color(
                            RED if active else original_colors[source_index]
                        )
                        state["active"] = active
                    mob.move_to(_sample_path(molecule_path, now))

                molecule.add_updater(update_molecule)

            counter.clear_updaters()
            counter_state = {"count": None, "scale": 1.0}

            def update_counter(mob, _dt=0):
                now = clock.get_value()
                frame = min(int(now * 24), len(totals) - 1)
                age = last_event_age(all_events, now)
                active = age < 0.1
                pulse = np.sin(np.pi * age / 0.1) if active else 0.0
                scale = 1 + 0.65 * pulse
                count = int(totals[frame])
                if count != counter_state["count"]:
                    mob.become(_text(str(count), 34, YELLOW))
                    counter_state["count"] = count
                    counter_state["scale"] = 1.0
                mob.scale(scale / counter_state["scale"])
                counter_state["scale"] = scale
                mob.move_to(counter_position)

            counter.add_updater(update_counter)
            phase_label.become(_text(label, 20, GREEN_A if wall_start == wall_end else ORANGE).move_to(
                phase_label.get_center()
            ))
            self.play(
                clock.animate.set_value(duration),
                piston.animate.shift(UP * (wall_end - wall_start)),
                volume_point.animate.move_to(
                    graph_axes.c2p(
                        3 * (wall_end - lower) / (upper_initial - lower),
                        4 / (3 * (wall_end - lower) / (upper_initial - lower)),
                    )
                ),
                run_time=duration,
                rate_func=linear,
            )
            for molecule in gas:
                molecule.clear_updaters()
            counter.clear_updaters()
            return paths[-1], final_velocities, events, totals

        current_positions = initial_positions
        current_velocities = None
        current_upper = inner_upper_initial
        baseline_paths, current_velocities, baseline_events, baseline_totals = animate_gas_interval(
            current_positions,
            current_velocities,
            observation_time,
            current_upper,
            current_upper,
            f"ÖNCE — {observation_time:.1f} s ölçüm",
        )
        baseline_hits = int(baseline_totals[-1])
        current_positions = baseline_paths

        question = "Pistonu yavaşça aşağı indirirsem ne değişir?"
        card, correct = _prediction_prompt(self, question, "ARTAR")

        stage_upper_levels = np.linspace(
            inner_upper_initial, upper_compressed - 0.12, 5
        )[1:]
        stage_counts = []
        for stage_number, next_upper in enumerate(stage_upper_levels, start=1):
            transition_start = current_upper
            moved_positions, current_velocities, _, _ = animate_gas_interval(
                current_positions,
                current_velocities,
                compression_time,
                transition_start,
                float(next_upper),
                f"PİSTON İNİYOR — KADEME {stage_number}/4",
            )
            current_positions = moved_positions
            current_upper = float(next_upper)

            measured_positions, current_velocities, _, measured_totals = animate_gas_interval(
                current_positions,
                current_velocities,
                observation_time,
                current_upper,
                current_upper,
                f"KADEME {stage_number}/4 — {observation_time:.1f} s ölçüm",
            )
            stage_counts.append(int(measured_totals[-1]))
            current_positions = measured_positions

        explanation = _text(
            f"Aynı 4 saniyede piston çarpması: {baseline_hits} → {stage_counts[-1]}. "
            "Hacim küçüldükçe çarpışmalar sıklaşır, basınç artar.",
            19,
            WHITE,
        )
        _close_prediction(self, card, correct, explanation)

        summary = _text("V azalır  →  P artar", 25, YELLOW).to_edge(DOWN, buff=0.65)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.7)
        self.wait(4)
