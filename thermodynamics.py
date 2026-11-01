"""Termodinamik yolculuğu — ilk sekiz bölüm.

Önizleme:
    manim -pql thermodynamics.py Chapter1
    manim -pql thermodynamics.py Chapter2
    manim -pql thermodynamics.py Chapter3 Chapter4 Chapter5
    manim -pql thermodynamics.py Chapter6 Chapter7 Chapter8
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
    "chapter_6": [
        "Kabın hacmi ve gaz miktarı sabit. Isıtınca moleküllerin ortalama kinetik enerjisi yükselir.",
        "Isıtıcı enerji aktarır. Moleküller hızlanır; duvara çarptıklarında daha büyük momentum değişimi oluştururlar.",
        "Bir moleküle yakından bakalım: aynı sürede daha uzun yol alır ve duvara daha sık çarpar.",
        "Mutlak sıcaklık Kelvin cinsinden ölçülür. Hacim sabitken basınç sıcaklıkla doğru orantılıdır.",
    ],
    "chapter_7": [
        "Pistonun üstündeki ağırlık değişmediği için dış basınç sabit kalır.",
        "Gazı ısıtınca moleküller hızlanır; piston yükselerek gazın daha büyük bir hacme yayılmasına izin verir.",
        "Basınç ve gaz miktarı sabitken hacim, Kelvin cinsinden sıcaklıkla doğru orantılıdır.",
    ],
    "chapter_8": [
        "Sıcaklık ve hacim sabitken kaba daha fazla gaz molekülü ekliyoruz.",
        "Daha çok molekül, duvarlara aynı sürede daha çok çarpışma demektir; basınç artar.",
        "N, gazdaki toplam tanecik sayısıdır. n ise madde miktarıdır ve mol cinsinden ölçülür.",
        "N alt A, Avogadro sabitidir; bir moldaki tanecik sayısını verir. Değeri yaklaşık 6,022 × 10 üzeri 23 bölü moldür.",
        "Bu yüzden toplam tanecik sayısı N, mol miktarı n ile Avogadro sabiti N alt A'nın çarpımına eşittir.",
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
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray], np.ndarray]:
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
    collision_times: list[list[float]] = [[] for _ in range(len(positions))]
    piston_hit_times: list[list[float]] = [[] for _ in range(len(positions))]
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
            for molecule_index in np.flatnonzero(side_hit):
                collision_times[molecule_index].append(elapsed)
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
            for molecule_index in np.flatnonzero(top_hit | bottom_hit):
                collision_times[molecule_index].append(elapsed)
            positions[top_hit, 1] = 2 * current_upper - positions[top_hit, 1]
            velocities[top_hit, 1] = 2 * wall_velocity - velocities[top_hit, 1]
            positions[bottom_hit, 1] = 2 * lower - positions[bottom_hit, 1]
            velocities[bottom_hit, 1] *= -1
            for molecule_index in np.flatnonzero(top_hit):
                piston_hit_times[molecule_index].append(elapsed)
            hits += int(np.count_nonzero(top_hit))

        paths[frame] = positions
        hit_totals[frame] = hits

    return (
        paths,
        hit_totals,
        [np.asarray(events) for events in collision_times],
        [np.asarray(events) for events in piston_hit_times],
        velocities,
    )


def _text(content: str, size: float = 30, color=WHITE) -> Text:
    return Text(content, font=FONT, font_size=size, color=color)


def _prediction_prompt(
    scene: ThreeDScene,
    question: str,
    correct: str,
    choice_buff: float = 0.7,
    labeled_choices: bool = False,
):
    question_text = _text(question, 30, YELLOW).to_edge(UP, buff=0.42)
    choice_labels = ("ARTAR", "AZALIR", "DEĞİŞMEZ")
    displayed_choices = (
        tuple(f"{letter}) {choice}" for letter, choice in zip("ABC", choice_labels))
        if labeled_choices
        else choice_labels
    )
    choices = VGroup(
        *[_text(choice, 28, WHITE) for choice in displayed_choices]
    ).arrange(RIGHT, buff=choice_buff)
    choices.to_edge(DOWN, buff=0.55)
    card = VGroup(question_text, choices)
    scene.add_fixed_in_frame_mobjects(card)
    scene.wait(5)
    return card, choices[choice_labels.index(correct)]


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
        vessel_center_x = 0.0
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
        ).move_to(np.array([vessel_center_x, -0.2, 0]))
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

        graph_center = RIGHT * 4.07 + DOWN * 0.25
        graph_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=3.7,
            y_length=2.8,
            axis_config={"color": GREY_B, "include_tip": True, "stroke_width": 2},
        ).move_to(graph_center)
        curve = graph_axes.plot(
            lambda volume: 4 / volume,
            x_range=[0.8, 4.5],
            color=YELLOW,
            stroke_width=4,
        )
        invariant_label = _text("Boyle: PV = sabit", 30, YELLOW)
        volume_label = _text("Hacim V", 17, GREY_A).move_to(
            graph_center + DOWN * 1.75
        )
        pressure_label = _text("P", 17, GREY_A).move_to(
            graph_center + LEFT * 1.9 + UP * 0.15
        )
        pressure_label.rotate(90 * DEGREES)
        volume_point = Dot(graph_axes.c2p(3, 4 / 3), color=ORANGE, radius=0.09)
        graph_group = VGroup(
            graph_axes,
            curve,
            volume_label,
            pressure_label,
            volume_point,
        )
        graph_group.scale(
            0.7,
            about_point=graph_center + RIGHT * 1.95,
        )
        graph_center_after_scale = graph_axes.get_center()
        invariant_label.move_to(
            [graph_center_after_scale[0], 1.55, graph_center_after_scale[2]]
        )
        volume_label.move_to(
            [graph_center_after_scale[0], -1.78, graph_center_after_scale[2]]
        )
        VGroup(graph_axes, curve, pressure_label, volume_point).shift(DOWN * 0.25)
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
        table_width = 2.45
        table_height = 1.8
        table_center = LEFT * 4.75 + DOWN * 0.88
        table_left = table_center[0] - table_width / 2
        table_right = table_center[0] + table_width / 2
        table_top = table_center[1] + table_height / 2
        table_row_height = table_height / 6
        column_divider = table_center[0] + 0.32
        measurement_table = VGroup(
            Rectangle(
                width=table_width,
                height=table_height,
                fill_color=BLUE_E,
                fill_opacity=0.3,
                stroke_color=BLUE_A,
                stroke_width=1.2,
            ).move_to(table_center),
            Rectangle(
                width=table_width - 0.04,
                height=table_row_height - 0.02,
                fill_color=BLUE_D,
                fill_opacity=0.75,
                stroke_width=0,
            ).move_to(
                [table_center[0], table_top - table_row_height / 2, 0]
            ),
            Line(
                [column_divider, table_top - table_height, 0],
                [column_divider, table_top, 0],
                color=BLUE_A,
                stroke_width=1,
            ),
            *[
                Line(
                    [table_left, table_top - row * table_row_height, 0],
                    [table_right, table_top - row * table_row_height, 0],
                    color=BLUE_A,
                    stroke_width=0.8,
                )
                for row in range(1, 6)
            ],
            _text("Ölçüm", 13, WHITE).move_to(
                [table_center[0] - 0.62, table_top - table_row_height / 2, 0]
            ),
            _text("Çarpma", 13, YELLOW).move_to(
                [table_center[0] + 0.76, table_top - table_row_height / 2, 0]
            ),
            *[
                _text(label, 12, GREY_A).move_to(
                    [
                        table_center[0] - 0.62,
                        table_top - (row + 1.5) * table_row_height,
                        0,
                    ]
                )
                for row, label in enumerate(
                    ["Başlangıç", "1. kademe", "2. kademe", "3. kademe", "4. kademe"]
                )
            ],
        )
        self.add_fixed_in_frame_mobjects(
            phase_label,
            counter_heading,
            counter,
            measurement_label,
            measurement_table,
        )
        self.play(
            FadeIn(phase_label),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(measurement_label),
            FadeIn(measurement_table),
            run_time=0.6,
        )

        def record_collision_count(count: int, row: int) -> None:
            cell_position = np.array(
                [
                    table_center[0] + 0.76,
                    table_top - (row + 1.5) * table_row_height,
                    0,
                ]
            )
            count_copy = counter.copy()
            count_copy.clear_updaters()
            count_copy.become(_text(str(count), 34, YELLOW).move_to(counter_position))
            self.add_fixed_in_frame_mobjects(count_copy)
            self.play(
                count_copy.animate.move_to(cell_position).scale(0.5),
                rate_func=smooth,
                run_time=0.65,
            )

        def animate_gas_interval(
            positions: np.ndarray,
            velocities: np.ndarray | None,
            duration: float,
            wall_start: float,
            wall_end: float,
            label: str,
        ) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], np.ndarray]:
            paths, totals, events, piston_events, final_velocities = _simulate_gas_paths(
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
                np.sort(np.concatenate(piston_events))
                if any(len(entry) for entry in piston_events)
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
                    active = age < 0.05
                    pulse = np.sin(np.pi * age / 0.05) if active else 0.0
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
        record_collision_count(baseline_hits, 0)

        question = "Pistonu yavaşça aşağı indirirsem ne değişir?"
        card, correct = _prediction_prompt(
            self, question, "ARTAR", choice_buff=0.4, labeled_choices=True
        )

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
            record_collision_count(stage_counts[-1], stage_number)

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


def _gas_particles(
    positions: np.ndarray,
    colors: list,
    radius: float = 0.065,
) -> VGroup:
    return VGroup(
        *[
            Dot(point=point, radius=radius, color=colors[index], fill_opacity=0.95)
            for index, point in enumerate(positions)
        ]
    )


def _gas_positions(
    count: int,
    center_x: float,
    radius: float,
    lower: float,
    upper: float,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    radial = radius * 0.72 * np.sqrt(rng.random(count))
    angles = rng.uniform(0, TAU, count)
    return np.column_stack(
        (
            center_x + radial * np.cos(angles),
            rng.uniform(lower + 0.18, upper - 0.18, count),
            radial * np.sin(angles),
        )
    )


def _gas_vessel(
    center_x: float,
    radius: float,
    bottom: float,
    top: float,
    visual_top: float | None = None,
) -> Cylinder:
    visual_top = top if visual_top is None else visual_top
    return Cylinder(
        radius=radius,
        height=visual_top - bottom,
        direction=UP,
        resolution=(20, 12),
        fill_color=BLUE_E,
        fill_opacity=0.08,
        stroke_color=BLUE_A,
        stroke_opacity=0.2,
        stroke_width=0.65,
    ).move_to(np.array([center_x, (visual_top + bottom) / 2, 0]))


def _gas_piston(center_x: float, radius: float, top: float) -> Cylinder:
    return Cylinder(
        radius=radius * 0.96,
        height=0.13,
        direction=UP,
        resolution=(20, 12),
        fill_color=GREY_B,
        fill_opacity=0.95,
        stroke_color=WHITE,
    ).move_to(np.array([center_x, top, 0]))


def _play_gas_measurement(
    scene: ThreeDScene,
    gas: VGroup,
    positions: np.ndarray,
    velocities: np.ndarray | None,
    *,
    duration: float,
    radius: float,
    lower: float,
    upper_start: float,
    upper_end: float,
    center_x: float,
    counter: Text,
    moving_objects: list[Mobject] | None = None,
    seed: int = 81,
) -> tuple[np.ndarray, np.ndarray, int]:
    paths, totals, collision_events, _, final_velocities = _simulate_gas_paths(
        positions,
        duration,
        radius,
        lower,
        upper_start,
        seed=seed,
        center_x=center_x,
        upper_end=upper_end,
        initial_velocities=velocities,
    )
    clock = ValueTracker(0)
    original_colors = [molecule.get_color() for molecule in gas]
    pulse_states = [
        {"scale": 1.0, "active": False} for _ in range(len(gas))
    ]

    def last_collision_age(event_times: np.ndarray, now: float) -> float:
        previous = np.searchsorted(event_times, now, side="right") - 1
        return now - event_times[previous] if previous >= 0 else duration

    for index, molecule in enumerate(gas):
        molecule.clear_updaters()
        path = paths[:, index, :]
        events = collision_events[index]
        state = pulse_states[index]
        base_color = original_colors[index]

        def update_molecule(
            mob,
            _dt=0,
            p=path,
            timer=clock,
            hits=events,
            pulse_state=state,
            molecule_color=base_color,
        ):
            now = timer.get_value()
            age = last_collision_age(hits, now)
            active = age < 0.05
            pulse = np.sin(np.pi * age / 0.05) if active else 0.0
            scale = 1 + 0.7 * pulse
            mob.scale(scale / pulse_state["scale"])
            pulse_state["scale"] = scale
            if active != pulse_state["active"]:
                mob.set_color(RED if active else molecule_color)
                pulse_state["active"] = active
            mob.move_to(_sample_path(p, now))

        molecule.add_updater(update_molecule)

    counter.clear_updaters()
    counter_state = {"count": None}
    counter_position = counter.get_center().copy()

    def update_counter(mob, _dt=0):
        frame = min(int(clock.get_value() * 24), len(totals) - 1)
        count = int(totals[frame])
        if count != counter_state["count"]:
            mob.become(_text(str(count), 34, YELLOW))
            counter_state["count"] = count
        mob.move_to(counter_position)

    counter.add_updater(update_counter)
    animations = [clock.animate.set_value(duration)]
    if moving_objects:
        shift = UP * (upper_end - upper_start)
        animations.extend(obj.animate.shift(shift) for obj in moving_objects)
    scene.play(*animations, run_time=duration, rate_func=linear)

    for molecule in gas:
        molecule.clear_updaters()
    for molecule, color, state in zip(gas, original_colors, pulse_states):
        if state["scale"] != 1.0:
            molecule.scale(1 / state["scale"])
        molecule.set_color(color)
    counter.clear_updaters()
    return paths[-1], final_velocities, int(totals[-1])


class Chapter6(ThreeDScene):
    """Bölüm 6 — Gay-Lussac yasası: hacim ve mol sayısı sabit."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("GAY-LUSSAC YASASI", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("Hacim V ve mol sayısı n sabit", 20, GREY_A).next_to(
            title, DOWN, buff=0.1
        )
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.8)

        center_x, radius = -2.15, 0.96
        lower, upper = -1.55, 1.15
        vessel = _gas_vessel(center_x, radius, lower, upper)
        piston = _gas_piston(center_x, radius, upper)
        positions = _gas_positions(30, center_x, radius, lower, upper, 606)
        colors = [ORANGE if i == 0 else BLUE_C for i in range(len(positions))]
        gas = _gas_particles(positions, colors)
        self.play(Create(vessel), FadeIn(piston), FadeIn(gas), run_time=1.2)

        heater = VGroup(
            RoundedRectangle(
                width=1.65,
                height=0.42,
                corner_radius=0.08,
                fill_color=ORANGE,
                fill_opacity=0.85,
                stroke_color=YELLOW,
            ).move_to([center_x, -2.05, 0]),
            _text("ISITICI", 16, BLACK).move_to([center_x, -2.05, 0]),
        )
        heater_arrows = VGroup(
            *[
                Arrow(
                    [center_x + offset, -1.78, 0],
                    [center_x + offset, -1.48, 0],
                    buff=0,
                    color=ORANGE,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.3,
                )
                for offset in (-0.45, 0, 0.45)
            ]
        )
        phase = _text("ÖNCE — 3 s ölçüm", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Piston çarpması", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Aynı süre", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        formula = _text("P / T = sabit", 30, YELLOW).move_to([3.35, 1.25, 0])
        explanation = _text(
            "V ve n sabit\nT (Kelvin) artar → P artar",
            20,
            WHITE,
        ).move_to([3.35, 0.25, 0])
        temperature = _text("T: 300 K", 20, ORANGE).move_to([3.35, -0.75, 0])
        self.add_fixed_in_frame_mobjects(
            phase, counter_heading, counter, counter_note, formula, explanation, temperature
        )
        self.play(
            FadeIn(phase),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(counter_note),
            FadeIn(formula),
            FadeIn(explanation),
            FadeIn(temperature),
            run_time=0.7,
        )

        observation_time = 3.0
        inner_radius, inner_lower, inner_upper = radius - 0.15, lower + 0.15, upper - 0.15
        positions, velocities, before_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            None,
            duration=observation_time,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=inner_upper,
            upper_end=inner_upper,
            center_x=center_x,
            counter=counter,
            seed=606,
        )

        self.remove_fixed_in_frame_mobjects(title, condition)
        self.remove(title, condition)
        card, correct = _prediction_prompt(
            self,
            "Hacim sabitken gazı ısıtırsam basınç ne olur?",
            "ARTAR",
            choice_buff=0.4,
            labeled_choices=True,
        )
        hot_temperature = 450
        correct.set_color(GREEN)
        self.play(Indicate(correct, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.remove_fixed_in_frame_mobjects(card)
        self.remove(card)

        self.play(
            FadeOut(phase),
            FadeOut(counter_heading),
            FadeOut(counter),
            FadeOut(counter_note),
            FadeOut(formula),
            FadeOut(explanation),
            FadeOut(temperature),
            run_time=0.5,
        )
        self.remove_fixed_in_frame_mobjects(
            phase,
            counter_heading,
            counter,
            counter_note,
            formula,
            explanation,
            temperature,
        )
        self.remove(
            phase,
            counter_heading,
            counter,
            counter_note,
            formula,
            explanation,
            temperature,
        )

        mola = gas[0]
        mola_start = positions[0].copy()
        hot_velocity = velocities[0] * np.sqrt(hot_temperature / 300)
        closeup_duration = 2.4
        closeup_paths, _, closeup_events, _, _ = _simulate_gas_paths(
            mola_start.reshape(1, 3),
            closeup_duration,
            inner_radius,
            inner_lower,
            inner_upper,
            seed=612,
            center_x=center_x,
            initial_velocities=hot_velocity.reshape(1, 3),
            samples_per_second=60,
            substeps=4,
        )
        closeup_path = closeup_paths[:, 0, :]
        closeup_hits = closeup_events[0]
        closeup_clock = ValueTracker(0)
        closeup_state = {"scale": 1.0, "active": False}
        original_mola_color = colors[0]

        def animate_closeup_mola(mob, _dt=0):
            now = closeup_clock.get_value()
            hit_index = np.searchsorted(closeup_hits, now, side="right") - 1
            age = now - closeup_hits[hit_index] if hit_index >= 0 else closeup_duration
            active = age < 0.05
            pulse = np.sin(np.pi * age / 0.05) if active else 0.0
            scale = 1 + 0.7 * pulse
            mob.scale(scale / closeup_state["scale"])
            closeup_state["scale"] = scale
            if active != closeup_state["active"]:
                mob.set_color(RED if active else original_mola_color)
                closeup_state["active"] = active
            mob.move_to(_sample_path(closeup_path, now, samples_per_second=60))

        mola.add_updater(animate_closeup_mola)
        dim_others = [molecule.animate.set_opacity(0.12) for molecule in gas[1:]]
        self.play(*dim_others, run_time=1.1)
        self.move_camera(zoom=2.2, frame_center=mola_start, run_time=1.1)
        heat_caption = _text("ISI GAZA AKTARILIYOR", 22, ORANGE).to_corner(
            UL, buff=0.35
        )
        energy_label = _text("Mola'nın kinetik enerjisi", 17, WHITE).move_to(
            [3.8, 1.0, 0]
        )
        energy_before = _text("300 K", 17, BLUE_A).move_to([3.8, 0.58, 0])
        energy_after = _text("450 K", 17, ORANGE).move_to([3.8, -0.55, 0])
        energy_outline = RoundedRectangle(
            width=2.1,
            height=0.34,
            corner_radius=0.08,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_opacity=0,
        ).move_to([3.8, 0, 0])
        energy_fill = Rectangle(
            width=0.68,
            height=0.23,
            stroke_width=0,
            fill_color=BLUE_C,
            fill_opacity=0.95,
        ).move_to([3.18, 0, 0])
        heat_note = _text(
            "Isıtıcıdan alınan enerji\nortalama kinetik enerjiyi artırır.",
            17,
            WHITE,
        ).move_to([3.8, -1.15, 0])
        self.add_fixed_in_frame_mobjects(
            heat_caption,
            energy_label,
            energy_before,
            energy_after,
            energy_outline,
            energy_fill,
            heat_note,
        )
        self.play(
            FadeIn(heat_caption),
            FadeIn(energy_label),
            FadeIn(energy_before),
            FadeIn(energy_after),
            Create(energy_outline),
            FadeIn(energy_fill),
            FadeIn(heat_note),
            FadeIn(heater),
            FadeIn(heater_arrows),
            run_time=0.7,
        )

        start = mola.get_center()
        incoming_heat = VGroup(
            *[
                Dot(point=start + DOWN * (0.75 + index * 0.16), radius=0.09, color=ORANGE)
                for index in range(4)
            ]
        )
        self.add(incoming_heat)
        self.play(
            *[
                packet.animate.move_to(start + DOWN * 0.12)
                for packet in incoming_heat
            ],
            energy_fill.animate.set_color(ORANGE).stretch_to_fit_width(1.38).move_to(
                [3.45, 0, 0]
            ),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(FadeOut(incoming_heat), run_time=0.2)
        speed_before = Arrow(
            start,
            start + velocities[0] / np.linalg.norm(velocities[0]) * 0.42,
            buff=0,
            color=BLUE_A,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.35,
        )
        speed_after = Arrow(
            start,
            start + hot_velocity / np.linalg.norm(hot_velocity) * 1.05,
            buff=0,
            color=ORANGE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
        )
        speed_note = _text("Hız vektörü uzar", 16, ORANGE).move_to(
            [3.8, -1.72, 0]
        )
        self.add(speed_before)
        self.add_fixed_in_frame_mobjects(speed_note)
        self.play(
            Transform(speed_before, speed_after),
            FadeIn(speed_note),
            run_time=0.7,
        )
        self.play(closeup_clock.animate.set_value(closeup_duration), run_time=closeup_duration, rate_func=linear)
        mola.clear_updaters()
        if closeup_state["scale"] != 1.0:
            mola.scale(1 / closeup_state["scale"])
        mola.set_color(original_mola_color)
        mola.move_to(mola_start)

        self.play(
            FadeOut(speed_before),
            FadeOut(heater),
            FadeOut(heater_arrows),
            FadeOut(heat_caption),
            FadeOut(energy_label),
            FadeOut(energy_before),
            FadeOut(energy_after),
            FadeOut(energy_outline),
            FadeOut(energy_fill),
            FadeOut(heat_note),
            FadeOut(speed_note),
            *[molecule.animate.set_opacity(1) for molecule in gas[1:]],
            run_time=1.1,
        )
        self.move_camera(zoom=1.0, frame_center=ORIGIN, run_time=1.1)
        self.remove_fixed_in_frame_mobjects(
            heat_caption,
            energy_label,
            energy_before,
            energy_after,
            energy_outline,
            energy_fill,
            heat_note,
            speed_note,
        )
        self.remove(
            heat_caption,
            energy_label,
            energy_before,
            energy_after,
            energy_outline,
            energy_fill,
            heat_note,
            speed_note,
        )

        hot_label = _text(f"T: {hot_temperature} K", 20, ORANGE).move_to(
            temperature.get_center()
        )
        self.add_fixed_in_frame_mobjects(hot_label)
        self.play(FadeIn(phase), FadeIn(counter_heading), FadeIn(counter), FadeIn(counter_note), FadeIn(formula), FadeIn(explanation), FadeIn(hot_label), run_time=0.5)
        self.play(
            *[molecule.animate.set_color(ORANGE) for molecule in gas],
            run_time=0.45,
        )
        phase.become(
            _text("SONRA — 3 s ölçüm", 18, ORANGE).move_to(phase.get_center())
        )

        positions, velocities, after_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            velocities * np.sqrt(hot_temperature / 300),
            duration=observation_time,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=inner_upper,
            upper_end=inner_upper,
            center_x=center_x,
            counter=counter,
            seed=607,
        )
        result = _text(
            f"Aynı sürede piston çarpması: {before_hits} → {after_hits}. "
            "Moleküller daha hızlı ve daha sert çarpar.",
            18,
            WHITE,
        )
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("V ve n sabit  →  T artarsa P artar", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)


class Chapter7(ThreeDScene):
    """Bölüm 7 — Charles yasası: basınç ve mol sayısı sabit."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("CHARLES YASASI", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("Basınç P ve mol sayısı n sabit", 20, GREY_A).next_to(
            title, DOWN, buff=0.1
        )
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.8)

        center_x, radius = -2.15, 0.96
        lower, upper_start, upper_end = -1.55, -0.15, 0.4
        vessel = _gas_vessel(
            center_x, radius, lower, upper_start, visual_top=0.8
        )
        piston = _gas_piston(center_x, radius, upper_start)
        weight = Cube(
            side_length=0.48,
            fill_color=GREY_B,
            fill_opacity=0.95,
            stroke_color=WHITE,
        ).move_to([center_x, upper_start + 0.42, 0])
        positions = _gas_positions(30, center_x, radius, lower, upper_start, 707)
        colors = [ORANGE if i == 0 else BLUE_C for i in range(len(positions))]
        gas = _gas_particles(positions, colors)
        self.play(
            Create(vessel),
            FadeIn(piston),
            FadeIn(weight),
            FadeIn(gas),
            run_time=1.2,
        )

        phase = _text("ÖNCE — 3 s ölçüm", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Piston çarpması", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Aynı süre", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        formula = _text("V / T = sabit", 30, YELLOW).move_to([3.35, 1.25, 0])
        weight_note = _text(
            "Üstteki ağırlık hep aynı,\nbu yüzden içerideki basınç da aynı kalıyor.",
            18,
            WHITE,
        ).move_to([3.35, 0.2, 0])
        temperature = _text("T: 400 K", 20, ORANGE).move_to([3.35, -0.85, 0])
        self.add_fixed_in_frame_mobjects(
            phase, counter_heading, counter, counter_note, formula, weight_note, temperature
        )
        self.play(
            FadeIn(phase),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(counter_note),
            FadeIn(formula),
            FadeIn(weight_note),
            FadeIn(temperature),
            run_time=0.7,
        )

        observation_time = 3.0
        inner_radius, inner_lower = radius - 0.15, lower + 0.15
        current_upper = upper_start - 0.15
        positions, velocities, before_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            None,
            duration=observation_time,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=current_upper,
            upper_end=current_upper,
            center_x=center_x,
            counter=counter,
            seed=707,
        )

        self.remove_fixed_in_frame_mobjects(title, condition)
        self.remove(title, condition)
        card, correct = _prediction_prompt(
            self,
            "Aynı ağırlık altındaki gazı ısıtırsam piston ne yapar?",
            "ARTAR",
            choice_buff=0.4,
            labeled_choices=True,
        )
        hot_temperature = 600
        hot_label = _text(f"T: {hot_temperature} K", 20, ORANGE).move_to(
            temperature.get_center()
        )
        self.add_fixed_in_frame_mobjects(hot_label)
        self.remove_fixed_in_frame_mobjects(temperature)
        self.remove(temperature)
        counter_note.become(
            _text("Isıtma sırasında", 15, GREY_A).move_to(counter_note.get_center())
        )
        self.play(
            *[molecule.animate.set_color(ORANGE) for molecule in gas],
            run_time=0.45,
        )
        phase.become(
            _text("PİSTON YÜKSELİYOR", 18, ORANGE).move_to(phase.get_center())
        )

        positions, velocities, _ = _play_gas_measurement(
            self,
            gas,
            positions,
            velocities * np.sqrt(hot_temperature / 400),
            duration=4.0,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=current_upper,
            upper_end=upper_end - 0.15,
            center_x=center_x,
            counter=counter,
            moving_objects=[piston, weight],
            seed=708,
        )
        phase.become(_text("SONRA — V arttı", 18, GREEN_A).move_to(phase.get_center()))
        volume_note = _text("Piston yükselir → V artar", 19, GREEN_A).move_to(
            [3.35, -1.45, 0]
        )
        self.add_fixed_in_frame_mobjects(volume_note)
        self.play(FadeIn(volume_note), run_time=0.5)
        result = _text(
            "Ağırlık aynı kaldı: basınç sabit. "
            "Gaz ısınınca piston yükseldi.",
            18,
            WHITE,
        )
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("P ve n sabit  →  T artarsa V artar", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)


class Chapter8(ThreeDScene):
    """Bölüm 8 — sıcaklık ve hacim sabitken mol sayısının etkisi."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("MADDE MİKTARI VE BASINÇ", 34, BLUE_A).to_edge(
            UP, buff=0.3
        )
        condition = _text("Sıcaklık T ve hacim V sabit", 20, GREY_A).next_to(
            title, DOWN, buff=0.1
        )
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.8)

        center_x, radius = -2.15, 0.96
        lower, upper = -1.55, 1.15
        vessel = _gas_vessel(center_x, radius, lower, upper)
        piston = _gas_piston(center_x, radius, upper)
        initial_count = 18
        positions = _gas_positions(
            initial_count, center_x, radius, lower, upper, 808
        )
        colors = [ORANGE if i == 0 else BLUE_C for i in range(initial_count)]
        gas = _gas_particles(positions, colors)
        self.play(Create(vessel), FadeIn(piston), FadeIn(gas), run_time=1.2)

        phase = _text("ÖNCE — 3 s ölçüm", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Piston çarpması", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Aynı süre", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        formula = MathTex(r"N = n \times N_A", font_size=34, color=YELLOW).move_to(
            [3.35, 1.35, 0]
        )
        symbol_definitions = _text(
            "N: toplam tanecik sayısı\nn: madde miktarı (mol)",
            15,
            WHITE,
        ).move_to([3.35, 0.55, 0])
        avogadro = MathTex(
            r"N_A = 6{,}022 \times 10^{23}\ \mathrm{mol}^{-1}",
            font_size=23,
            color=WHITE,
        ).move_to([3.35, -0.15, 0])
        avogadro_note = _text(
            "Avogadro sabiti: 1 moldaki tanecik sayısı",
            14,
            GREY_A,
        ).move_to([3.35, -0.62, 0])
        relation = _text("T ve V sabit → n artarsa P artar", 18, GREEN_A).move_to(
            [3.35, -1.1, 0]
        )
        model_note = _text(
            "Her nokta çok sayıda molekülü temsil eder.",
            16,
            GREY_A,
        ).move_to([3.35, -1.55, 0])
        self.add_fixed_in_frame_mobjects(
            phase,
            counter_heading,
            counter,
            counter_note,
            formula,
            symbol_definitions,
            avogadro,
            avogadro_note,
            relation,
            model_note,
        )
        self.play(
            FadeIn(phase),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(counter_note),
            FadeIn(formula),
            FadeIn(symbol_definitions),
            FadeIn(avogadro),
            FadeIn(avogadro_note),
            FadeIn(relation),
            FadeIn(model_note),
            run_time=0.7,
        )

        observation_time = 3.0
        inner_radius, inner_lower, inner_upper = radius - 0.15, lower + 0.15, upper - 0.15
        positions, velocities, before_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            None,
            duration=observation_time,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=inner_upper,
            upper_end=inner_upper,
            center_x=center_x,
            counter=counter,
            seed=808,
        )

        self.remove_fixed_in_frame_mobjects(title, condition)
        self.remove(title, condition)
        card, correct = _prediction_prompt(
            self,
            "T ve V sabitken kaba daha fazla gaz eklersem basınç ne olur?",
            "ARTAR",
            choice_buff=0.4,
            labeled_choices=True,
        )
        added_count = 18
        added_positions = _gas_positions(
            added_count, center_x, radius, lower, upper, 809
        )
        added_colors = [GREEN_C] * added_count
        added_gas = _gas_particles(added_positions, added_colors, radius=0.06)
        valve = Circle(radius=0.16, color=GREEN_A, stroke_width=3).move_to(
            [center_x + 0.7, 1.65, 0]
        )
        valve_label = _text("VANA AÇIK", 15, GREEN_A).next_to(valve, UP, buff=0.12)
        self.add_fixed_in_frame_mobjects(valve, valve_label)
        self.add(added_gas)
        for molecule in added_gas:
            molecule.move_to(valve.get_center())
        self.play(
            FadeIn(valve_label),
            *[
                molecule.animate.move_to(target)
                for molecule, target in zip(added_gas, added_positions)
            ],
            run_time=1.3,
            rate_func=smooth,
        )
        gas.add(*added_gas)
        self.remove(added_gas)
        positions = np.vstack((positions, added_positions))
        rng = np.random.default_rng(809)
        added_velocities = rng.normal(size=(added_count, 3))
        added_velocities[:, 2] = 0
        added_velocities /= np.linalg.norm(
            added_velocities, axis=1, keepdims=True
        )
        added_velocities *= rng.uniform(0.9, 1.45, size=(added_count, 1))
        velocities = np.vstack((velocities, added_velocities))
        self.play(FadeOut(valve_label), run_time=0.3)
        phase.become(
            _text("SONRA — 3 s ölçüm", 18, GREEN_A).move_to(phase.get_center())
        )

        positions, velocities, after_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            velocities,
            duration=observation_time,
            radius=inner_radius,
            lower=inner_lower,
            upper_start=inner_upper,
            upper_end=inner_upper,
            center_x=center_x,
            counter=counter,
            seed=810,
        )
        self.remove_fixed_in_frame_mobjects(valve, valve_label)
        self.play(FadeOut(valve), run_time=0.35)
        result = _text(
            f"Aynı sürede çarpma sayısı: {before_hits} → {after_hits}. "
            "Molekül sayısı artınca basınç yükselir.",
            18,
            WHITE,
        )
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("T ve V sabit  →  n artarsa P artar", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)
