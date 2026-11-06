"""Reise durch die Thermodynamik: elf Kapitel.

Vorschau:
    manim -pql thermodynamics.py Chapter1
    manim -pql thermodynamics.py Chapter2
    manim -pql thermodynamics.py Chapter3 Chapter4 Chapter5
    manim -pql thermodynamics.py Chapter6 Chapter7 Chapter8
    manim -pql thermodynamics.py Chapter9 Chapter10a Chapter10b Chapter10c
    manim -pql thermodynamics.py Chapter11

Alle Formeln sind mit MarkupText gesetzt; LaTeX (MiKTeX) wird nicht benötigt.
"""

from __future__ import annotations

import numpy as np
from manim import *
from manim.utils.color import color_to_rgb


FONT = "Arial"
MAX_TEXT_WIDTH = 13.0


NARRATION = {
    "chapter_1": [
        "In dieser Welt, die du mit bloßem Auge nicht sehen kannst, sind Gasmoleküle ständig in Bewegung.",
        "Ich heiße Mola. Ich bin ein Gasmolekül; ich stoße gegen Wände und ändere meine Richtung.",
        "Eben warst du ein Molekül. Jetzt betrachten wir das ganze System von außen.",
        "Druck, Volumen, Stoffmenge und absolute Temperatur: vier Größen, die ein Gas beschreiben.",
    ],
    "chapter_2": [
        "Die Energie eines Moleküls kann aus verschiedenen Bewegungsformen bestehen.",
        "Addieren wir diese Beiträge, erhalten wir die Energie eines Moleküls; addieren wir über alle Moleküle, erhalten wir die innere Energie.",
        "Im Modell des idealen Gases vernachlässigen wir die potenzielle Energie zwischen den Molekülen.",
        "Wärme ist nichts, was gespeichert wird; sie ist Energie, die wegen eines Temperaturunterschieds zwischen Systemen übertragen wird.",
        "Energie fließt vom heißen zum kalten Gefäß. Die innere Energie des kalten Gefäßes nimmt zu.",
    ],
    "chapter_3": [
        "Die Moleküle eines Gases sind unterschiedlich schnell; die Temperatur gibt nicht die Geschwindigkeit eines einzelnen Moleküls an.",
        "Die Temperatur hängt mit der mittleren kinetischen Energie der Translationsbewegung der Moleküle zusammen.",
        "Beim Erwärmen wird die Verteilung breiter und flacher, und der Mittelwert wandert zu höheren Energien.",
        "Zwei Gefäße können dieselbe Temperatur haben; im Gefäß mit mehr Molekülen ist die gesamte innere Energie größer.",
    ],
    "chapter_4": [
        "Wenn Mola gegen die Wand stößt, ändert sich sein Impuls; auch die Wand erhält einen Kraftstoß.",
        "Der Impuls, den die Stöße auf die Wand übertragen, erzeugt eine Kraft; die Kraft verteilt auf die Fläche ergibt den Druck.",
    ],
    "chapter_5": [
        "Bei konstanter Temperatur und Stoffmenge drücken wir den Kolben nach unten; dasselbe Gas wird auf ein kleineres Volumen zusammengedrückt.",
        "Die Moleküle treffen häufiger auf die Wände. Dadurch steigt der Druck, und das Produkt p mal V bleibt konstant.",
    ],
    "chapter_6": [
        "Volumen und Gasmenge im Gefäß sind konstant. Beim Erwärmen steigt die mittlere kinetische Energie der Moleküle.",
        "Der Heizer überträgt Energie. Die Moleküle werden schneller; beim Stoß gegen die Wand erzeugen sie eine größere Impulsänderung.",
        "Schauen wir uns ein Molekül genauer an: In derselben Zeit legt es einen längeren Weg zurück und trifft häufiger auf die Wand.",
        "Die absolute Temperatur wird in Kelvin gemessen. Bei konstantem Volumen ist der Druck proportional zur Temperatur.",
    ],
    "chapter_7": [
        "Da sich das Gewicht auf dem Kolben nicht ändert, bleibt der äußere Druck konstant.",
        "Erwärmen wir das Gas, werden die Moleküle schneller; der Kolben steigt und lässt das Gas sich auf ein größeres Volumen ausdehnen.",
        "Bei konstantem Druck und konstanter Gasmenge ist das Volumen proportional zur Temperatur in Kelvin.",
    ],
    "chapter_8": [
        "Bei konstanter Temperatur und konstantem Volumen geben wir mehr Gasmoleküle in das Gefäß.",
        "Mehr Moleküle bedeuten in derselben Zeit mehr Stöße gegen die Wände; der Druck steigt.",
        "N ist die Gesamtzahl der Teilchen im Gas. n ist die Stoffmenge und wird in Mol gemessen.",
        "N A ist die Avogadro-Konstante; sie gibt die Anzahl der Teilchen in einem Mol an. Ihr Wert beträgt etwa 6,022 mal 10 hoch 23 pro Mol.",
        "Deshalb ist die Gesamtzahl der Teilchen N gleich dem Produkt aus der Stoffmenge n und der Avogadro-Konstante N A.",
    ],
    "chapter_9": [
        "Zuerst die Symbole: p ist der Druck, V das Volumen, n die Stoffmenge in Mol und T die absolute Temperatur. R ist die universelle Gaskonstante.",
        "Der Druck entsteht durch Stöße der Moleküle gegen die Wände. Prallt ein Molekül in einem Würfel gegen eine Wand, ändert sich sein Impuls in x-Richtung um 2 m v x.",
        "Die Zeit zwischen zwei Stößen ist die Zeit für den Weg zur gegenüberliegenden Wand und zurück. Die Kraft ist die Impulsänderung pro Zeit.",
        "Die Bewegung verteilt sich gleichmäßig auf die drei Raumrichtungen. Deshalb ist der Mittelwert von v x Quadrat ein Drittel des Mittelwerts von v Quadrat. Daher kommt das Drittel.",
        "Die Translationsenergie eines Moleküls ist ein halb m v Quadrat. Die Summe über alle N Moleküle ist U kin; das Halbe stammt aus der Definition der kinetischen Energie.",
        "So erhalten wir p V gleich zwei Drittel U kin. Der Faktor zwei Drittel ist das Verhältnis aus dem Drittel in der Druckgleichung und dem Halben in der kinetischen Energie.",
        "Nach dem Gleichverteilungssatz trägt im Gleichgewicht jede der Richtungen x, y und z im Mittel ein halb k B T. Drei Richtungen ergeben den Faktor drei Halbe.",
        "k B ist die Boltzmann-Konstante: Sie verknüpft die Temperatur mit der Energie einzelner Teilchen. Ihre Einheit ist Joule pro Kelvin.",
        "N ist die Gesamtzahl der Teilchen. Ein Mol enthält N A Teilchen; deshalb gilt N gleich n mal N A.",
        "Setzen wir alles ein, kürzen sich zwei Drittel und drei Halbe weg: p V gleich N k B T, also p V gleich n mal N A mal k B mal T.",
        "Das Produkt N A mal k B ist die universelle Gaskonstante R, etwa 8,314 Joule pro Mol und Kelvin.",
        "Ergebnis: p V gleich n R T. T ist die absolute Temperatur in Kelvin, deren Nullpunkt der absolute Nullpunkt ist. Aus Grad Celsius rechnet man T gleich t plus 273,15.",
        "Die Gesetze von Boyle-Mariotte, Amontons und Gay-Lussac folgen aus p V gleich n R T, wenn man einige Größen konstant hält.",
    ],
    "chapter_10a": [
        "Wärmeleitung, also Konduktion: Wir tauchen einen Metalllöffel in ein schlankes türkisches Teeglas.",
        "Das Ende im Tee wird heiß. Die Atome im Kristallgitter des Metalls schwingen um ihre Ruhelagen.",
        "Am heißen Ende schwingen sie stärker. Über die Kopplung an die Nachbaratome breitet sich diese Energie durch das Gitter aus.",
        "Wir zeigen etwa 1.500 Atome stark vergrößert. Das ist ein Modell: Atome und Abstände sind nicht maßstabsgetreu.",
        "Die Atome wandern nicht den Löffel entlang; jedes schwingt um seine eigene Ruhelage. Was sich ausbreitet, ist die Energie.",
        "In Metallen transportieren freie Elektronen sogar den größten Teil der Wärme. In dieser Nahaufnahme betrachten wir nur die Gitterschwingungen.",
        "Die Energie fließt vom heißen Tee zum kälteren Stiel. Das Ende des Stiels wird mit der Zeit warm; der Löffel selbst bewegt sich nicht.",
    ],
    "chapter_10b": [
        "Wärmeströmung, also Konvektion, entsteht in Flüssigkeiten und Gasen durch die Bewegung der Materie selbst.",
        "Von unten erwärmtes Wasser dehnt sich aus und wird weniger dicht; deshalb steigt es nach oben.",
        "Kälteres, dichteres Wasser sinkt nach unten. So entsteht im Gefäß ein Strömungskreislauf.",
        "Auch Mola wird mit dem strömenden Wasser mitgetragen; die Energie wird mit dem Fluid transportiert.",
    ],
    "chapter_10c": [
        "Wärmestrahlung ist Energieübertragung durch elektromagnetische Wellen.",
        "Die Strahlung der Sonne durchquert den leeren Weltraum; dazwischen braucht es weder Luft noch einen anderen Stoff.",
        "In einer elektromagnetischen Welle stehen elektrisches und magnetisches Feld senkrecht aufeinander und senkrecht zur Ausbreitungsrichtung.",
        "Trifft die Welle auf eine Oberfläche, kann sie absorbiert werden. Die Energie geht auf die Teilchen der Oberfläche über; sie erwärmt sich.",
        "Auch Mola bewegt sich schneller.",
        "Leitung geschieht von Atom zu Atom, Strömung mit dem bewegten Fluid und Strahlung mit elektromagnetischen Wellen.",
    ],
    "chapter_11": [
        "Fassen wir die ganze Reise zusammen: Der Zustand eines Gases wird durch Druck, Volumen, Stoffmenge und absolute Temperatur beschrieben.",
        "Der Druck entsteht durch Stöße der Moleküle gegen die Wände. Die Temperatur hängt mit der mittleren kinetischen Energie der Translation zusammen.",
        "In der Zustandsgleichung des idealen Gases steht die Temperatur immer in Kelvin.",
        "Die Gesetze von Boyle-Mariotte, Amontons und Gay-Lussac folgen aus p V gleich n R T, wenn einige Größen konstant bleiben.",
        "Energie wird durch Leitung von Atom zu Atom, durch Strömung mit dem Fluid und durch Strahlung mit elektromagnetischen Wellen übertragen.",
        "Merke: Die Temperatur ist ein Mittelwert, die innere Energie eine Summe. Wärme ist der Vorgang der Energieübertragung.",
    ],
}


def _precompute_paths(
    count: int,
    duration: float,
    samples_per_second: int = 24,
    radius: float = 1.38,
    half_height: float = 1.78,
    seed: int = 24,
) -> tuple[np.ndarray, np.ndarray]:
    """Berechnet einmal die Bahnen der Moleküle, die im Zylinder reflektiert werden.

    Gibt die Bahnen und die (bei elastischen Stößen konstanten) Geschwindigkeitsbeträge zurück.
    """
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
    return paths, speeds


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
    thermostat: bool = False,
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray], np.ndarray]:
    """Erzeugt vorab berechnete Bahnen, Stoßzahlen und Ereigniszeiten.

    Ein bewegter Kolben verrichtet Arbeit am Gas: Beim Zusammendrücken werden die
    Moleküle schneller, beim Ausdehnen langsamer. Mit thermostat=True wird die
    gesamte kinetische Energie konstant gehalten (Wärmeaustausch mit der Umgebung
    bzw. dem Heizer), damit die Temperatur wie in der Erzählung konstant bleibt.
    """
    rng = np.random.default_rng(seed)
    positions = initial_positions.copy()
    if initial_velocities is None:
        velocities = rng.normal(size=positions.shape)
        velocities[:, 2] = 0
        velocities /= np.linalg.norm(velocities, axis=1, keepdims=True)
        velocities *= rng.uniform(0.9, 1.45, size=(len(positions), 1))
    else:
        velocities = initial_velocities.copy()
    target_energy = float(np.sum(velocities**2))

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

            if thermostat:
                current_energy = float(np.sum(velocities**2))
                if current_energy > 0:
                    velocities *= np.sqrt(target_energy / current_energy)

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
    text = Text(content, font=FONT, font_size=size, color=color)
    # Deutsche Texte sind oft länger: zu breite Zeilen auf Bildbreite begrenzen.
    if text.width > MAX_TEXT_WIDTH:
        text.scale_to_fit_width(MAX_TEXT_WIDTH)
    return text


def _prediction_prompt(
    scene: ThreeDScene,
    question: str,
    correct: str,
    choice_buff: float = 0.7,
    labeled_choices: bool = False,
):
    question_text = _text(question, 30, YELLOW).to_edge(UP, buff=0.42)
    choice_labels = ("NIMMT ZU", "NIMMT AB", "BLEIBT GLEICH")
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
    """Kapitel 1: Einführung in das Gassystem aus der Sicht eines Moleküls."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=68 * DEGREES, theta=-48 * DEGREES, zoom=0.9)

        title = _text("DIE PHYSIK DER GASE", 38, BLUE_A).to_edge(UP, buff=0.35)
        subtitle = _text("Reise in die unsichtbare Welt", 24, GREY_A).next_to(
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
        paths, speeds = _precompute_paths(40, duration)
        tracker = ValueTracker(0)
        molecules = VGroup()
        for i, path in enumerate(paths.transpose(1, 0, 2)):
            # Farbe zeigt die tatsächliche Geschwindigkeit: blau = langsam, orange = schnell.
            speed_fraction = (speeds[i] - 0.65) / (1.45 - 0.65)
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
        intro = _text("Eben warst du ein Molekül …", 30, YELLOW).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(intro)
        self.play(FadeIn(intro), run_time=0.8)
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(intro, mola_label, title, subtitle)
        self.remove(intro, mola_label, title, subtitle)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(tracker.animate.set_value(duration), run_time=2, rate_func=linear)
        self.stop_ambient_camera_rotation()
        molecules.clear_updaters()

        heading = _text("Ein Gas beschreiben wir mit vier Größen", 30, WHITE).to_edge(UP, buff=0.4)
        indicators = VGroup(
            _text("p  Druck", 26, BLUE_A),
            _text("V  Volumen", 26, GREEN_A),
            _text("n  Stoffmenge", 26, YELLOW),
            _text("T  Absolute Temperatur", 26, ORANGE),
        ).arrange(RIGHT, buff=0.48).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(heading, indicators)
        self.play(FadeIn(heading), LaggedStart(*[FadeIn(item) for item in indicators], lag_ratio=0.2))
        self.wait(4)


class Chapter2(ThreeDScene):
    """Kapitel 2: Innere Energie und Wärmeübertragung."""

    def construct(self):
        self.camera.background_color = BLACK
        # Frontansicht: Bei der früheren flachen Kamera (phi=70°) lagen alle Beschriftungen
        # in der Bodenebene und waren stark verzerrt. Die 3D-Wirkung kommt jetzt durch
        # leicht gedrehte Körper.
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        heading = _text("ENERGIE: VOM MOLEKÜL ZUM SYSTEM", 34, BLUE_A).to_edge(UP, buff=0.35)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(FadeIn(heading), run_time=1)

        mola_center = LEFT * 3.6 + UP * 0.1
        mola = Dot3D(
            radius=0.24,
            resolution=(8, 8),
            color=BLUE_C,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(mola_center)
        mola_name = _text("Mola", 23, ORANGE).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(mola_name)
        self.play(FadeIn(mola), FadeIn(mola_name), run_time=1)

        labels = [
            "Translationsenergie (kinetisch)",
            "Rotationsenergie (kinetisch)",
            "Schwingungsenergie",
            "Wechselwirkungsenergie (reales Gas)",
        ]
        colors = [BLUE_C, GREEN_C, YELLOW, ORANGE]
        segments = VGroup()
        for i, (label, color) in enumerate(zip(labels, colors)):
            y = 1.25 - i * 0.78
            block = (
                Cube(
                    side_length=0.52,
                    fill_color=color,
                    fill_opacity=0.88,
                    stroke_color=WHITE,
                    stroke_width=0.5,
                )
                .rotate(-30 * DEGREES, axis=UP)
                .rotate(20 * DEGREES, axis=RIGHT)
                .move_to(RIGHT * 0.1 + UP * y)
            )
            label_text = _text(label, 21, color)
            label_text.next_to(np.array([0.75, y, 0]), RIGHT, buff=0)
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
        total_label = _text("Gesamtenergie eines Moleküls", 23, WHITE).next_to(
            total_bar, DOWN, buff=0.18
        )
        self.play(Create(total_bar), FadeIn(total_label), run_time=1)
        ideal_note = _text(
            "Beim idealen Gas wird die potenzielle Energie zwischen den Molekülen vernachlässigt.",
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
                    mola_center
                    + RIGHT * ((i % 6) * 0.22 - 0.55)
                    + UP * ((i // 6) * 0.22 - 0.3)
                )
                for i in range(18)
            ]
        )
        sum_label = _text("Die Energien aller Moleküle werden addiert", 24, WHITE).to_edge(
            UP, buff=1.1
        )
        internal_energy = _text(
            "INNERE ENERGIE  U = Σ (E_trans + E_rot + E_schw + E_pot)",
            25,
            YELLOW,
        ).to_edge(DOWN, buff=0.85)
        # Erst im Bild fixieren, dann einblenden (sonst springt der Text nach dem Einblenden).
        self.add_fixed_in_frame_mobjects(sum_label, internal_energy)
        self.play(FadeIn(other_molecules), FadeIn(sum_label), run_time=1.2)
        self.play(FadeIn(internal_energy), run_time=1)
        self.wait(3)

        # Wärme ist nicht die innere Energie selbst, sondern ein Energiefluss zwischen zwei Systemen.
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
        ).rotate(20 * DEGREES, axis=RIGHT).move_to(LEFT * 2)
        cold_vessel = Cylinder(
            radius=0.62,
            height=1.45,
            direction=UP,
            resolution=(20, 12),
            fill_color=BLUE_E,
            fill_opacity=0.45,
            stroke_color=BLUE_A,
            stroke_width=1.5,
        ).rotate(20 * DEGREES, axis=RIGHT).move_to(RIGHT * 2)
        hot_label = _text("HEISSES SYSTEM", 22, RED_A).move_to(LEFT * 2 + DOWN * 1.3)
        cold_label = _text("KALTES SYSTEM", 22, BLUE_A).move_to(RIGHT * 2 + DOWN * 1.3)
        self.play(
            FadeIn(hot_vessel),
            FadeIn(cold_vessel),
            FadeIn(hot_label),
            FadeIn(cold_label),
            run_time=1.2,
        )

        question = "Das kalte System erhält Energie: Was passiert mit seiner inneren Energie?"
        card, correct = _prediction_prompt(self, question, "NIMMT ZU")

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
            "Wärme Q: Energie, die wegen eines Temperaturunterschieds übertragen wird; kein Energiespeicher.",
            22,
            WHITE,
        )
        _close_prediction(self, card, correct, explanation)
        self.play(FadeOut(transfer_dots), run_time=0.6)

        heat_formula = _text("ΔU = Q + W", 40, YELLOW).to_edge(UP, buff=1.05)
        sign_note = _text(
            "W: am System verrichtete Arbeit  •  Wärme fließt vom heißeren zum kälteren System",
            21,
            GREY_A,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(heat_formula, sign_note)
        self.play(FadeIn(heat_formula), FadeIn(sign_note), run_time=1)
        self.wait(5)


class Chapter3(ThreeDScene):
    """Kapitel 3: Zusammenhang zwischen Temperatur und mittlerer kinetischer Energie."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("TEMPERATUR: MITTELWERT DER ENERGIEN", 32, BLUE_A).to_edge(
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

        # Maxwell-Boltzmann-Verteilung der kinetischen Energie: unsymmetrisch, mit langem
        # Ausläufer zu hohen Energien. Maximum bei k_B T / 2, Mittelwert bei 3/2 k_B T.
        bin_energies = np.linspace(0.25, 4.25, 9)  # in Einheiten von k_B · T (kaltes Gas)

        def energy_to_x(energy: float) -> float:
            return -2.8 + (energy - bin_energies[0]) * 1.4

        def maxwell_boltzmann(k_t: float) -> np.ndarray:
            return (
                2 / np.sqrt(np.pi)
                * np.sqrt(bin_energies)
                / k_t**1.5
                * np.exp(-bin_energies / k_t)
            )

        cold_density = maxwell_boltzmann(1.0)
        hot_density = maxwell_boltzmann(1.5)
        height_scale = 1.38 / cold_density.max()

        def energy_bars(density: np.ndarray, color, stroke_color) -> VGroup:
            group = VGroup()
            for energy, value in zip(bin_energies, density):
                height = float(value * height_scale)
                bar = Cube(
                    side_length=1,
                    fill_color=color,
                    fill_opacity=0.88,
                    stroke_color=stroke_color,
                    stroke_width=0.5,
                )
                bar.stretch_to_fit_width(0.42)
                bar.stretch_to_fit_depth(0.42)
                bar.stretch_to_fit_height(height)
                bar.move_to(np.array([energy_to_x(energy), baseline + height / 2, 0]))
                group.add(bar)
            return group

        bars = energy_bars(cold_density, BLUE_C, BLUE_A)
        hot_bars = energy_bars(hot_density, ORANGE, YELLOW)
        mean_x = energy_to_x(1.5)
        hot_mean_x = energy_to_x(1.5 * 1.5)
        average_line = DashedLine(
            np.array([mean_x, baseline, 0]),
            np.array([mean_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=3,
        )
        average_label = _text("Mittelwert", 20, YELLOW).move_to(
            np.array([mean_x, 1.92, 0])
        )
        labels = VGroup(
            _text("Niedrige Energie", 18, GREY_A).move_to(np.array([-2.4, -1.38, 0])),
            _text("Hohe Energie", 18, GREY_A).move_to(np.array([2.4, -1.38, 0])),
        )
        count_label = _text("Anzahl der Moleküle", 18, GREY_A).rotate(90 * DEGREES)
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
            "Balken: Anzahl der Moleküle pro Energiebereich. Viele sind eher langsam, wenige sehr schnell.",
            22,
            WHITE,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(FadeIn(explanation), run_time=0.7)
        self.wait(2)

        heat_label = _text("Erwärmen", 23, ORANGE).to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(heat_label)
        # Beim Erwärmen wird die Verteilung breiter und flacher; sie verschiebt sich nicht einfach.
        self.play(
            Transform(bars, hot_bars),
            average_line.animate.shift(RIGHT * (hot_mean_x - mean_x)).set_color(ORANGE),
            average_label.animate.shift(RIGHT * (hot_mean_x - mean_x)).set_color(ORANGE),
            FadeIn(heat_label),
            run_time=1.8,
        )
        formula = _text("Mittlere E_kin = (3/2) k_B T", 29, YELLOW).to_edge(
            DOWN, buff=0.35
        )
        average_note = _text(
            "Die Temperatur hängt mit der mittleren kinetischen Energie der Translation zusammen, nicht mit allen Energieformen.",
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
            "Gleiche Temperatur: gleiche mittlere kinetische Energie",
            24,
            YELLOW,
        ).to_edge(UP, buff=0.85)
        labels = VGroup(
            _text("Viele Moleküle", 22, BLUE_A).move_to(np.array([-2.0, -1.4, 0])),
            _text("Wenige Moleküle", 22, GREEN_A).move_to(np.array([2.0, -1.4, 0])),
        )
        total_energy = _text(
            "Mehr Moleküle → größere gesamte innere Energie U",
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
    """Kapitel 4: Druck entsteht durch Stöße gegen die Wand."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=68 * DEGREES, theta=-38 * DEGREES, zoom=1.0)

        title = _text("DRUCK: STÖSSE GEGEN DIE WAND", 32, BLUE_A).to_edge(
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
        counter_label = _text("Wandstöße:", 23, WHITE).to_corner(UR, buff=0.55)
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
            _text("Vor dem Stoß", 19, YELLOW).move_to(np.array([-3.2, -2.12, 0])),
            _text("Nach dem Stoß", 19, BLUE_B).move_to(np.array([3.2, -2.12, 0])),
        )
        self.add_fixed_in_frame_mobjects(vector_before, vector_after, vectors_text)
        self.wait(0.7)
        self.play(time.animate.set_value(5.2), run_time=3.68, rate_func=linear)

        explanation = _text(
            "Molas Impuls ändert sich; bei jedem Stoß wirkt eine Kraft auf die Wand.",
            21,
            WHITE,
        ).to_edge(DOWN, buff=0.9)
        formula = _text("Druck p = Kraft F / Fläche A", 27, YELLOW).to_edge(
            DOWN, buff=0.28
        )
        self.add_fixed_in_frame_mobjects(explanation, formula)
        self.play(FadeIn(explanation), FadeIn(formula), run_time=0.8)
        self.wait(3)
        mola.clear_updaters()
        counter.clear_updaters()


class Chapter5(ThreeDScene):
    """Kapitel 5: Gesetz von Boyle-Mariotte: Temperatur und Stoffmenge konstant."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("GESETZ VON BOYLE-MARIOTTE", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("isotherm: T und n konstant", 21, GREY_A).next_to(title, DOWN, buff=0.1)
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
        invariant_label = _text("p · V = konstant", 30, YELLOW)
        volume_label = _text("Volumen V", 17, GREY_A).move_to(
            graph_center + DOWN * 1.75
        )
        pressure_label = _text("p", 17, GREY_A).move_to(
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

        def graph_volume(wall: float) -> float:
            # Dieselben (inneren) Grenzen wie in der Simulation, damit der Punkt bei V = 3 startet.
            return 3 * (wall - inner_lower) / (inner_upper_initial - inner_lower)

        phase_label = _text("KOLBEN FEST", 20, GREEN_A).move_to(LEFT * 4.65 + UP * 2.1)
        counter_heading = _text("Stöße am Kolben", 19, WHITE).move_to(
            LEFT * 4.65 + UP * 1.55
        )
        counter_position = LEFT * 4.65 + UP * 0.95
        counter = _text("0", 34, YELLOW).move_to(counter_position)
        measurement_label = _text(
            f"In den letzten {observation_time:.0f} Sekunden", 17, GREY_A
        ).move_to(LEFT * 4.65 + UP * 0.42)
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
            _text("Messung", 13, WHITE).move_to(
                [table_center[0] - 0.62, table_top - table_row_height / 2, 0]
            ),
            _text("Stöße", 13, YELLOW).move_to(
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
                    ["Anfang", "Stufe 1", "Stufe 2", "Stufe 3", "Stufe 4"]
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
                # Isotherm: Die Arbeit des Kolbens geht als Wärme an die Umgebung,
                # die Teilchen werden also nicht schneller.
                thermostat=True,
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
            end_volume = graph_volume(wall_end)
            self.play(
                clock.animate.set_value(duration),
                piston.animate.shift(UP * (wall_end - wall_start)),
                volume_point.animate.move_to(graph_axes.c2p(end_volume, 4 / end_volume)),
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
            f"VORHER: {observation_time:.0f} s Messung",
        )
        baseline_hits = int(baseline_totals[-1])
        current_positions = baseline_paths
        record_collision_count(baseline_hits, 0)

        question = "Kolben langsam nach unten: Was passiert mit dem Druck?"
        card, correct = _prediction_prompt(
            self, question, "NIMMT ZU", choice_buff=0.4, labeled_choices=True
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
                f"KOLBEN SINKT: STUFE {stage_number}/4",
            )
            current_positions = moved_positions
            current_upper = float(next_upper)

            measured_positions, current_velocities, _, measured_totals = animate_gas_interval(
                current_positions,
                current_velocities,
                observation_time,
                current_upper,
                current_upper,
                f"STUFE {stage_number}/4: {observation_time:.0f} s Messung",
            )
            stage_counts.append(int(measured_totals[-1]))
            current_positions = measured_positions
            record_collision_count(stage_counts[-1], stage_number)

        explanation = _text(
            f"Stöße am Kolben in jeweils {observation_time:.0f} s: {baseline_hits} → {stage_counts[-1]}. "
            "Kleineres Volumen, häufigere Stöße, höherer Druck.",
            19,
            WHITE,
        )
        _close_prediction(self, card, correct, explanation)

        summary = _text("V nimmt ab  →  p nimmt zu", 25, YELLOW).to_edge(DOWN, buff=0.65)
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
    thermostat: bool = False,
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
        thermostat=thermostat,
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
    """Kapitel 6: Gesetz von Amontons (isochor): Volumen und Stoffmenge konstant."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        # Im Deutschen heißt p ~ T bei konstantem V "Gesetz von Amontons"
        # (auch 2. Gesetz von Gay-Lussac). V ~ T bei konstantem p ist Kapitel 7.
        title = _text("GESETZ VON AMONTONS", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("isochor: Volumen V und Stoffmenge n konstant", 20, GREY_A).next_to(
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
            _text("HEIZER", 16, BLACK).move_to([center_x, -2.05, 0]),
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
        phase = _text("VORHER: 3 s Messung", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Stöße am Kolben", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Gleiche Dauer", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        formula = _text("p / T = konstant", 30, YELLOW).move_to([3.35, 1.25, 0])
        explanation = _text(
            "V und n konstant\nT (Kelvin) steigt → p steigt",
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
            "Gas bei konstantem Volumen erwärmen: Was passiert mit dem Druck?",
            "NIMMT ZU",
            choice_buff=0.4,
            labeled_choices=True,
        )
        hot_temperature = 450
        # Frage ausblenden, ohne die Lösung vorwegzunehmen; sie wird erst nach dem Versuch aufgelöst.
        self.play(FadeOut(card), run_time=0.4)
        self.remove_fixed_in_frame_mobjects(card)

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
        speed_factor = np.sqrt(hot_temperature / 300)  # v ~ √T
        hot_velocity = velocities[0] * speed_factor
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
        heat_caption = _text("WÄRME WIRD AUF DAS GAS ÜBERTRAGEN", 22, ORANGE).to_corner(
            UL, buff=0.35
        )
        # Temperatur ist eine Eigenschaft des ganzen Gases, nicht eines einzelnen Moleküls.
        # Der Balken zeigt deshalb die mittlere kinetische Energie, die proportional zu T ist.
        energy_label = _text("Mittlere kinetische Energie", 17, WHITE).move_to(
            [3.8, 1.0, 0]
        )
        energy_before = _text("300 K", 17, BLUE_A).move_to([3.8, 0.58, 0])
        energy_after = _text(f"{hot_temperature} K", 17, ORANGE).move_to([3.8, -0.55, 0])
        energy_outline = RoundedRectangle(
            width=2.1,
            height=0.34,
            corner_radius=0.08,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_opacity=0,
        ).move_to([3.8, 0, 0])
        bar_left = 2.84
        cold_bar_width = 0.68
        hot_bar_width = cold_bar_width * hot_temperature / 300  # <E_kin> ~ T
        energy_fill = Rectangle(
            width=cold_bar_width,
            height=0.23,
            stroke_width=0,
            fill_color=BLUE_C,
            fill_opacity=0.95,
        ).move_to([bar_left + cold_bar_width / 2, 0, 0])
        heat_note = _text(
            "Die Energie vom Heizer erhöht\ndie mittlere kinetische Energie.",
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
            energy_fill.animate.set_color(ORANGE).stretch_to_fit_width(hot_bar_width).move_to(
                [bar_left + hot_bar_width / 2, 0, 0]
            ),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(FadeOut(incoming_heat), run_time=0.2)
        arrow_length = 0.6
        speed_before = Arrow(
            start,
            start + velocities[0] / np.linalg.norm(velocities[0]) * arrow_length,
            buff=0,
            color=BLUE_A,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.35,
        )
        speed_after = Arrow(
            start,
            start + hot_velocity / np.linalg.norm(hot_velocity) * arrow_length * speed_factor,
            buff=0,
            color=ORANGE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.3,
        )
        speed_note = _text("Geschwindigkeitspfeil wird länger", 16, ORANGE).move_to(
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
        # Die Anzeigen wieder im Bild fixieren, bevor sie eingeblendet werden.
        self.add_fixed_in_frame_mobjects(
            phase, counter_heading, counter, counter_note, formula, explanation, hot_label
        )
        self.play(
            FadeIn(phase),
            FadeIn(counter_heading),
            FadeIn(counter),
            FadeIn(counter_note),
            FadeIn(formula),
            FadeIn(explanation),
            FadeIn(hot_label),
            run_time=0.5,
        )
        self.play(
            *[molecule.animate.set_color(ORANGE) for molecule in gas],
            run_time=0.45,
        )
        phase.become(
            _text("NACHHER: 3 s Messung", 18, ORANGE).move_to(phase.get_center())
        )

        positions, velocities, after_hits = _play_gas_measurement(
            self,
            gas,
            positions,
            velocities * speed_factor,
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
            f"Stöße am Kolben in gleicher Zeit: {before_hits} → {after_hits}. "
            "Die Moleküle treffen öfter und härter.",
            18,
            WHITE,
        )
        # Erst jetzt die Frage wieder zeigen und auflösen.
        self.add_fixed_in_frame_mobjects(card)
        self.play(FadeIn(card), run_time=0.4)
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("V und n konstant  →  T steigt, also steigt p", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)


class Chapter7(ThreeDScene):
    """Kapitel 7: Gesetz von Gay-Lussac (isobar): Druck und Stoffmenge konstant."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        # Im Deutschen heißt V ~ T bei konstantem p "Gesetz von Gay-Lussac"
        # (im Englischen und Türkischen "Gesetz von Charles").
        title = _text("GESETZ VON GAY-LUSSAC", 34, BLUE_A).to_edge(UP, buff=0.3)
        condition = _text("isobar: Druck p und Stoffmenge n konstant", 20, GREY_A).next_to(
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

        phase = _text("VORHER: 3 s Messung", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Stöße am Kolben", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Gleiche Dauer", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        formula = _text("V / T = konstant", 30, YELLOW).move_to([3.35, 1.25, 0])
        weight_note = _text(
            "Das Gewicht oben bleibt immer gleich,\ndeshalb bleibt auch der Druck innen gleich.",
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
            "Gas unter demselben Gewicht erwärmen: Was passiert mit dem Volumen?",
            "NIMMT ZU",
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
            _text("Während des Erwärmens", 15, GREY_A).move_to(counter_note.get_center())
        )
        self.play(
            *[molecule.animate.set_color(ORANGE) for molecule in gas],
            run_time=0.45,
        )
        phase.become(
            _text("KOLBEN STEIGT", 18, ORANGE).move_to(phase.get_center())
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
            # Beim Ausdehnen verrichtet das Gas Arbeit und würde abkühlen; der Heizer
            # ersetzt diese Energie, damit T bei 600 K bleibt.
            thermostat=True,
        )
        phase.become(_text("NACHHER: V ist größer", 18, GREEN_A).move_to(phase.get_center()))
        volume_note = _text("Kolben steigt → V nimmt zu", 19, GREEN_A).move_to(
            [3.35, -1.45, 0]
        )
        self.add_fixed_in_frame_mobjects(volume_note)
        self.play(FadeIn(volume_note), run_time=0.5)
        result = _text(
            "Das Gewicht blieb gleich: Druck konstant. "
            "Beim Erwärmen ist der Kolben gestiegen.",
            18,
            WHITE,
        )
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("p und n konstant  →  T steigt, also steigt V", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)


class Chapter8(ThreeDScene):
    """Kapitel 8: Einfluss der Stoffmenge bei konstanter Temperatur und konstantem Volumen."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("STOFFMENGE UND DRUCK", 34, BLUE_A).to_edge(
            UP, buff=0.3
        )
        condition = _text("Temperatur T und Volumen V konstant", 20, GREY_A).next_to(
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

        phase = _text("VORHER: 3 s Messung", 18, GREEN_A).move_to([-5.25, 2.15, 0])
        counter_heading = _text("Stöße am Kolben", 18, WHITE).move_to(
            [-5.25, 1.55, 0]
        )
        counter = _text("0", 34, YELLOW).move_to([-5.25, 0.95, 0])
        counter_note = _text("Gleiche Dauer", 15, GREY_A).next_to(counter, DOWN, buff=0.08)
        # MarkupText statt MathTex: braucht kein LaTeX (MiKTeX) auf dem Rechner.
        formula = MarkupText(
            "<i>N</i> = <i>n</i> × <i>N</i><sub>A</sub>", font=FONT, font_size=34, color=YELLOW
        ).move_to([3.35, 1.35, 0])
        symbol_definitions = _text(
            "N: Gesamtzahl der Teilchen\nn: Stoffmenge (mol)",
            15,
            WHITE,
        ).move_to([3.35, 0.55, 0])
        avogadro = MarkupText(
            "<i>N</i><sub>A</sub> = 6,022 × 10<sup>23</sup> mol<sup>−1</sup>",
            font=FONT,
            font_size=23,
            color=WHITE,
        ).move_to([3.35, -0.15, 0])
        avogadro_note = _text(
            "Avogadro-Konstante: Anzahl der Teilchen in 1 mol",
            14,
            GREY_A,
        ).move_to([3.35, -0.62, 0])
        relation = _text("T und V konstant → n steigt, also steigt p", 18, GREEN_A).move_to(
            [3.35, -1.1, 0]
        )
        model_note = _text(
            "Jeder Punkt steht für sehr viele Moleküle.",
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
            "T und V konstant, mehr Gas hinein: Was passiert mit dem Druck?",
            "NIMMT ZU",
            choice_buff=0.4,
            labeled_choices=True,
        )
        added_count = 18
        added_positions = _gas_positions(
            added_count, center_x, radius, lower, upper, 809
        )
        added_colors = [GREEN_C] * added_count
        added_gas = _gas_particles(added_positions, added_colors, radius=0.06)
        # Ventil an der Seitenwand unterhalb des Kolbens (vorher lag es über dem Kolben,
        # die Teilchen wären also durch den Kolben hindurch ins Gas geflogen).
        valve = Circle(radius=0.16, color=GREEN_A, stroke_width=3).move_to(
            [center_x + radius + 0.22, 0.2, 0]
        )
        valve_label = _text("VENTIL OFFEN", 15, GREEN_A).next_to(valve, RIGHT, buff=0.12)
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
            _text("NACHHER: 3 s Messung", 18, GREEN_A).move_to(phase.get_center())
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
            f"Stöße in gleicher Zeit: {before_hits} → {after_hits}. "
            "Mehr Moleküle, höherer Druck.",
            18,
            WHITE,
        )
        _close_prediction(self, card, correct, result)
        self.add_fixed_in_frame_mobjects(title, condition)
        self.play(FadeIn(title), FadeIn(condition), run_time=0.5)
        summary = _text("T und V konstant  →  n steigt, also steigt p", 23, YELLOW).to_edge(
            DOWN, buff=0.55
        )
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(3)


# ---------------------------------------------------------------------------
# Formeln ohne LaTeX: MarkupText-Bausteine (funktioniert ohne MiKTeX)
# ---------------------------------------------------------------------------


def _frac(numerator, denominator, size: float = 32, color=WHITE) -> VGroup:
    """Bruch aus zwei Markup-Strings (oder Mobjects) mit Bruchstrich."""
    parts = []
    for part in (numerator, denominator):
        if isinstance(part, str):
            part = MarkupText(part, font=FONT, font_size=size * 0.82, color=color)
        parts.append(part)
    top, bottom = parts
    bar = Line(LEFT, RIGHT, color=color, stroke_width=2)
    bar.set_width(max(top.width, bottom.width) + 0.12)
    fraction = VGroup(top, bar, bottom).arrange(DOWN, buff=0.07)
    fraction.anchor = bar
    return fraction


def _sum_symbol(upper: str, lower: str, size: float = 32, color=WHITE) -> VGroup:
    sigma = MarkupText("Σ", font=FONT, font_size=size * 1.35, color=color)
    group = VGroup(
        MarkupText(upper, font=FONT, font_size=size * 0.55, color=color),
        sigma,
        MarkupText(lower, font=FONT, font_size=size * 0.55, color=color),
    ).arrange(DOWN, buff=0.04)
    group.anchor = sigma
    return group


def _braced(term: Mobject, label: str, size: float = 32, color=WHITE) -> VGroup:
    brace = Brace(term, DOWN, buff=0.06, color=color)
    text = MarkupText(label, font=FONT, font_size=size * 0.6, color=color).next_to(
        brace, DOWN, buff=0.04
    )
    group = VGroup(term, brace, text)
    group.anchor = getattr(term, "anchor", term)
    return group


def _math(*parts, size: float = 32, color=WHITE, buff: float = 0.1) -> VGroup:
    """Formel aus Markup-Strings und fertigen Bausteinen, auf einer Mittellinie ausgerichtet."""
    group = VGroup()
    for part in parts:
        if isinstance(part, str):
            part = MarkupText(part, font=FONT, font_size=size, color=color)
        group.add(part)
    group.arrange(RIGHT, buff=buff)
    reference_y = group[0].get_center()[1] if not hasattr(group[0], "anchor") else group[0].anchor.get_center()[1]
    for part in group:
        anchor = getattr(part, "anchor", part)
        part.shift(UP * (reference_y - anchor.get_center()[1]))
    return group


class Chapter9(ThreeDScene):
    """Kapitel 9: Von den Gasgesetzen zur Zustandsgleichung des idealen Gases."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("VON DEN GASGESETZEN ZU EINER FORMEL", 31, BLUE_A).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.8)

        formula = _math("pV", "=", "nRT", size=47)
        formula[0].set_color(BLUE_A)
        formula[2].set_color(YELLOW)
        formula.to_edge(UP, buff=0.85)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(FadeIn(formula, scale=0.75), run_time=0.7)
        glossary_title = _text("Was bedeuten die Symbole?", 24, WHITE).move_to(
            UP * 1.55
        )
        self.add_fixed_in_frame_mobjects(glossary_title)
        self.play(FadeIn(glossary_title), run_time=0.5)

        definitions = [
            ("p", "Druck", "Pa"),
            ("V", "Volumen", "m³"),
            ("n", "Stoffmenge", "mol"),
            ("R", "Universelle Gaskonstante", "J/(mol·K)"),
            ("T", "Absolute Temperatur", "K"),
        ]
        definition_groups = VGroup()
        for symbol, meaning, unit in definitions:
            row = VGroup(
                _math(symbol, size=31, color=TEAL_A),
                _text(f": {meaning}  [{unit}]", 20, WHITE),
            ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
            definition_groups.add(row)
        definition_groups.arrange_in_grid(
            rows=3,
            cols=2,
            buff=(0.4, 0.65),
            cell_alignment=LEFT,
        ).move_to(DOWN * 0.55)
        self.add_fixed_in_frame_mobjects(definition_groups)
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=UP * 0.08) for row in definition_groups],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )
        self.wait(3)

        micro_title = _text(
            "1. Wie entsteht der Druck aus Molekülstößen?",
            25,
            BLUE_A,
        ).move_to(UP * 2.45)
        self.add_fixed_in_frame_mobjects(micro_title)
        self.remove_fixed_in_frame_mobjects(formula, glossary_title, definition_groups)
        self.play(
            FadeOut(formula),
            FadeOut(glossary_title),
            FadeOut(definition_groups),
            FadeIn(micro_title),
            run_time=0.7,
        )

        box = Rectangle(
            width=2.6,
            height=2.15,
            color=BLUE_A,
            stroke_width=2,
        ).move_to(LEFT * 4.45 + DOWN * 0.25)
        wall_left = Line(box.get_left(), box.get_left() + UP * 0.7, color=YELLOW, stroke_width=5)
        wall_right = Line(box.get_right(), box.get_right() + DOWN * 0.7, color=YELLOW, stroke_width=5)
        molecule = Dot(LEFT * 5.2 + DOWN * 0.25, radius=0.13, color=ORANGE)
        vx_arrow = Arrow(
            molecule.get_center(),
            molecule.get_center() + RIGHT * 0.65,
            color=ORANGE,
            buff=0.12,
            max_tip_length_to_length_ratio=0.2,
        )
        box_label = _text("Würfel mit Kantenlänge L", 17, GREY_A).next_to(box, DOWN, buff=0.18)
        self.add_fixed_in_frame_mobjects(box, wall_left, wall_right, molecule, vx_arrow, box_label)
        self.play(Create(box), FadeIn(wall_left), FadeIn(wall_right), FadeIn(molecule), GrowArrow(vx_arrow), FadeIn(box_label), run_time=1)
        self.play(molecule.animate.move_to(box.get_right() + LEFT * 0.18), run_time=0.7, rate_func=linear)
        self.play(
            molecule.animate.move_to(box.get_left() + RIGHT * 0.18),
            vx_arrow.animate.rotate(PI).move_to(box.get_left() + RIGHT * 0.65),
            run_time=0.8,
            rate_func=linear,
        )
        # Impuls als m·v geschrieben, damit er nicht mit dem Druck p verwechselt wird.
        collision_math = VGroup(
            _math("Δ(m v<sub>x</sub>) = 2m |v<sub>x</sub>|", size=32, color=YELLOW),
            _math("Δt =", _frac("2L", "|v<sub>x</sub>|", 32, TEAL_A), size=32, color=TEAL_A),
            _math(
                "F<sub>x</sub> =",
                _frac("Δ(m v<sub>x</sub>)", "Δt", 32, WHITE),
                "=",
                _frac("m v<sub>x</sub><sup>2</sup>", "L", 32, WHITE),
                size=32,
                color=WHITE,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.45 + UP * 0.15)
        collision_note = _text(
            "Beim Abprallen kehrt sich der Impuls um.\n"
            "Kraft = Impulsänderung / vergangene Zeit.\n"
            "m: Masse des Moleküls • L: Kantenlänge • v_x: Geschwindigkeit in x-Richtung",
            17,
            GREY_A,
        ).move_to(RIGHT * 2.45 + DOWN * 1.6)
        self.add_fixed_in_frame_mobjects(collision_math, collision_note)
        self.play(
            LaggedStart(*[FadeIn(line, shift=RIGHT * 0.12) for line in collision_math], lag_ratio=0.2),
            FadeIn(collision_note),
            run_time=1.1,
        )
        self.wait(3)

        pressure_title = _text(
            "2. Die Bewegung in alle drei Richtungen berücksichtigen",
            25,
            BLUE_A,
        ).move_to(UP * 2.45)
        pressure_steps = VGroup(
            _math("p =", _frac("F", "A", 36, WHITE), size=36, color=WHITE),
            _math("pV = N m &lt;v<sub>x</sub><sup>2</sup>&gt;", size=36, color=TEAL_A),
            _math(
                "&lt;v<sub>x</sub><sup>2</sup>&gt; =",
                _frac("&lt;v<sup>2</sup>&gt;", "3", 34, YELLOW),
                size=34,
                color=YELLOW,
            ),
            _math(
                "pV =",
                _frac("1", "3", 39, WHITE),
                "N m &lt;v<sup>2</sup>&gt;",
                size=39,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.32).move_to(DOWN * 0.1)
        isotropy_note = _text(
            "p: Druck  •  A: Wandfläche  •  V = A·L",
            18,
            GREY_A,
        ).to_edge(DOWN, buff=0.42)
        self.remove_fixed_in_frame_mobjects(
            box, wall_left, wall_right, molecule, vx_arrow,
            box_label, collision_math, collision_note,
        )
        self.play(
            FadeOut(box),
            FadeOut(wall_left),
            FadeOut(wall_right),
            FadeOut(molecule),
            FadeOut(vx_arrow),
            FadeOut(box_label),
            FadeOut(collision_math),
            FadeOut(collision_note),
            Transform(micro_title, pressure_title),
            run_time=0.7,
        )
        for line in pressure_steps:
            self.add_fixed_in_frame_mobjects(line)
            self.play(FadeIn(line, shift=UP * 0.08), run_time=0.5)
            self.wait(0.8)
        self.add_fixed_in_frame_mobjects(isotropy_note)
        self.play(FadeIn(isotropy_note), run_time=0.5)
        self.wait(2)

        energy_title = _text(
            "3. Gesamte kinetische Energie der Translation",
            25,
            BLUE_A,
        ).move_to(UP * 2.45)
        kinetic_definition = _math(
            "U<sub>kin</sub> =",
            _sum_symbol("N", "i=1", 32, YELLOW),
            _frac("1", "2", 32, YELLOW),
            "m v<sub>i</sub><sup>2</sup> =",
            _frac("1", "2", 32, YELLOW),
            "N m &lt;v<sup>2</sup>&gt;",
            size=32,
            color=YELLOW,
        ).move_to(UP * 0.75)
        kinetic_explanation = _text(
            "Ein Teilchen hat die Translationsenergie ½mv².\n"
            "Wir addieren diese Energien über alle Teilchen.",
            20,
            WHITE,
        ).move_to(DOWN * 0.3)
        two_thirds = _math(
            "pV =",
            _frac("2", "3", 43, TEAL_A),
            "U<sub>kin</sub>",
            size=43,
            color=TEAL_A,
        ).move_to(DOWN * 1.45)
        coefficient_note = _text(
            "2/3 = (1/3) : (1/2): 1/3 kommt von den drei Richtungen, 1/2 aus der Definition der Energie.",
            17,
            GREY_A,
        ).to_edge(DOWN, buff=0.3)
        self.remove_fixed_in_frame_mobjects(pressure_steps, isotropy_note)
        self.add_fixed_in_frame_mobjects(kinetic_definition)
        self.play(
            FadeOut(pressure_steps),
            FadeOut(isotropy_note),
            Transform(micro_title, energy_title),
            FadeIn(kinetic_definition),
            run_time=0.8,
        )
        self.add_fixed_in_frame_mobjects(kinetic_explanation)
        self.play(FadeIn(kinetic_explanation), run_time=0.5)
        self.wait(2)
        self.add_fixed_in_frame_mobjects(two_thirds, coefficient_note)
        self.play(FadeIn(two_thirds), FadeIn(coefficient_note), run_time=0.8)
        self.wait(3)

        thermal_title = _text(
            "4. Die Temperatur hängt mit der mittleren kinetischen Energie zusammen",
            24,
            BLUE_A,
        ).move_to(UP * 2.45)

        def half_kt() -> VGroup:
            return _math(_frac("1", "2", 32, YELLOW), "k<sub>B</sub>T", size=32, color=YELLOW, buff=0.06)

        equipartition = _math(
            "&lt;E<sub>kin</sub>&gt; =",
            _braced(half_kt(), "x", 32, YELLOW),
            "+",
            _braced(half_kt(), "y", 32, YELLOW),
            "+",
            _braced(half_kt(), "z", 32, YELLOW),
            "=",
            _frac("3", "2", 32, YELLOW),
            "k<sub>B</sub>T",
            size=32,
            color=YELLOW,
        ).move_to(UP * 0.75)
        equipartition_note = _text(
            "Gleichverteilungssatz: Im Gleichgewicht trägt jede unabhängige\n"
            "Bewegungsrichtung im Mittel gleich viel Energie.",
            20,
            WHITE,
        ).move_to(DOWN * 0.35)
        total_kinetic = _math(
            "U<sub>kin</sub> = N &lt;E<sub>kin</sub>&gt; =",
            _frac("3", "2", 35, TEAL_A),
            "N k<sub>B</sub>T",
            size=35,
            color=TEAL_A,
        ).move_to(DOWN * 1.35)
        boltzmann = VGroup(
            _math("k<sub>B</sub> = 1,380649 × 10<sup>−23</sup> J/K", size=27, color=GREEN_A),
            _text(
                "Die Boltzmann-Konstante verknüpft die Temperatur mit der Energie pro Teilchen.",
                17,
                GREY_A,
            ),
            _text(
                "Sie wurde experimentell bestimmt; heute ist ihr Wert im SI exakt festgelegt.",
                16,
                GREY_A,
            ),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.22)
        self.remove_fixed_in_frame_mobjects(
            kinetic_definition, kinetic_explanation, two_thirds, coefficient_note
        )
        self.add_fixed_in_frame_mobjects(equipartition, equipartition_note)
        self.play(
            FadeOut(kinetic_definition),
            FadeOut(kinetic_explanation),
            FadeOut(two_thirds),
            FadeOut(coefficient_note),
            Transform(micro_title, thermal_title),
            FadeIn(equipartition),
            FadeIn(equipartition_note),
            run_time=0.8,
        )
        self.add_fixed_in_frame_mobjects(total_kinetic, boltzmann)
        self.play(FadeIn(total_kinetic), FadeIn(boltzmann), run_time=0.7)
        self.wait(4)

        assemble_title = _text(
            "5. Zusammensetzen: von der Teilchenzahl zur Stoffmenge",
            24,
            BLUE_A,
        ).move_to(UP * 2.45)
        assembly_equation = _math(
            "pV =",
            _frac("2", "3", 31, WHITE),
            "U<sub>kin</sub> =",
            _frac("2", "3", 31, WHITE),
            "(",
            _frac("3", "2", 31, WHITE),
            "N k<sub>B</sub>T )",
            size=31,
            color=WHITE,
        ).move_to(UP * 0.9)
        molecule_definitions = VGroup(
            VGroup(
                _math("N", size=25, color=TEAL_A),
                _text(": Gesamtzahl der Teilchen", 17, WHITE),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                _math("N<sub>A</sub>", size=25, color=TEAL_A),
                _math(": ≈ 6,022 × 10<sup>23</sup> mol<sup>−1</sup>", size=17, color=WHITE),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                _math("n", size=25, color=TEAL_A),
                _text(": Stoffmenge (mol)", 17, WHITE),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                _math("k<sub>B</sub>", size=25, color=TEAL_A),
                _math(": 1,380649 × 10<sup>−23</sup> J/K", size=17, color=WHITE),
            ).arrange(RIGHT, buff=0.08),
        ).arrange_in_grid(
            rows=2,
            cols=2,
            buff=(0.16, 0.65),
            cell_alignment=LEFT,
        ).move_to(DOWN * 1.45)
        cancellation_explanation = _text(
            "2/3 mal 3/2 ergibt 1; die Faktoren kürzen sich weg.",
            19,
            YELLOW,
        ).move_to(DOWN * 0.05)
        r_equation = _math(
            "R = N<sub>A</sub> k<sub>B</sub> = 8,314 J mol<sup>−1</sup> K<sup>−1</sup>",
            size=34,
            color=GREEN_A,
        ).move_to(UP * 0.9)
        r_units = _math(
            "mol<sup>−1</sup> × J/K = J mol<sup>−1</sup> K<sup>−1</sup>",
            size=28,
            color=TEAL_A,
        ).move_to(DOWN * 0.05)
        final_assembly = _math("pV = nRT", size=51, color=YELLOW).move_to(UP * 0.65)
        r_explanation = _text(
            "R ist die Boltzmann-Konstante, hochgerechnet auf ein Mol Teilchen.",
            18,
            WHITE,
        ).move_to(DOWN * 0.8)
        self.remove_fixed_in_frame_mobjects(
            equipartition, equipartition_note, total_kinetic, boltzmann
        )
        self.add_fixed_in_frame_mobjects(assembly_equation, cancellation_explanation)
        self.play(
            FadeOut(equipartition),
            FadeOut(equipartition_note),
            FadeOut(total_kinetic),
            FadeOut(boltzmann),
            Transform(micro_title, assemble_title),
            FadeIn(assembly_equation),
            FadeIn(cancellation_explanation),
            run_time=0.8,
        )
        self.wait(2)
        gas_particle_equation = _math("pV = N k<sub>B</sub>T", size=43, color=YELLOW).move_to(UP * 0.9)
        self.play(
            Transform(assembly_equation, gas_particle_equation),
            FadeOut(cancellation_explanation),
            run_time=0.7,
        )
        self.wait(1.5)
        amount_equation = _math("N = n N<sub>A</sub>", size=43, color=TEAL_A).move_to(UP * 1.0)
        self.add_fixed_in_frame_mobjects(molecule_definitions)
        self.play(
            Transform(assembly_equation, amount_equation),
            FadeIn(molecule_definitions),
            run_time=0.7,
        )
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(molecule_definitions)
        self.add_fixed_in_frame_mobjects(r_units)
        self.play(
            Transform(assembly_equation, r_equation),
            FadeOut(molecule_definitions),
            FadeIn(r_units),
            run_time=0.8,
        )
        self.add_fixed_in_frame_mobjects(r_explanation)
        self.play(FadeIn(r_explanation), run_time=0.5)
        self.wait(2)
        self.play(
            Transform(assembly_equation, final_assembly),
            FadeOut(r_units),
            FadeOut(r_explanation),
            run_time=0.8,
        )
        self.wait(3)

        kelvin_title = _text(
            "T: absolute Temperatur in Kelvin",
            24,
            ORANGE,
        ).move_to(UP * 2.45)
        kelvin_formula = _math("T [K] = t [°C] + 273,15", size=39, color=ORANGE).move_to(UP * 0.65)
        absolute_zero = _text(
            "Der Nullpunkt der Kelvin-Skala ist der absolute Nullpunkt:\n"
            "0 K = −273,15 °C. Deshalb setzt man K ein, nicht °C.",
            20,
            WHITE,
        ).move_to(DOWN * 0.55)
        self.remove_fixed_in_frame_mobjects(
            assembly_equation, molecule_definitions, r_units, r_explanation
        )
        self.add_fixed_in_frame_mobjects(kelvin_formula, absolute_zero)
        self.play(
            FadeOut(assembly_equation),
            Transform(micro_title, kelvin_title),
            FadeIn(kelvin_formula),
            FadeIn(absolute_zero),
            run_time=0.9,
        )
        self.wait(4)

        law_title = _text("Drei Spezialfälle: dieselbe Gleichung, andere Konstanten", 23, WHITE).move_to(
            UP * 2.85
        )
        final_formula = _math("pV", "=", "nRT", size=43)
        final_formula[0].set_color(BLUE_A)
        final_formula[2].set_color(YELLOW)
        final_formula.move_to(UP * 2.0)
        self.remove_fixed_in_frame_mobjects(kelvin_formula, absolute_zero)
        self.add_fixed_in_frame_mobjects(final_formula)
        self.play(
            FadeOut(kelvin_formula),
            FadeOut(absolute_zero),
            Transform(micro_title, law_title),
            FadeIn(final_formula),
            run_time=0.8,
        )

        # Deutsche Namen: p/T = konst. heißt Amontons, V/T = konst. heißt Gay-Lussac.
        law_specs = [
            ("BOYLE-MARIOTTE", lambda: _math("pV = konstant", size=29), "T und n konstant", BLUE_A),
            ("AMONTONS", lambda: _math(_frac("p", "T", 29, WHITE), "= konstant", size=29), "V und n konstant", ORANGE),
            ("GAY-LUSSAC", lambda: _math(_frac("V", "T", 29, WHITE), "= konstant", size=29), "p und n konstant", GREEN_A),
        ]
        law_cards = []
        targets = [LEFT * 4.45 + DOWN * 0.1, DOWN * 0.1, RIGHT * 4.45 + DOWN * 0.1]
        for (name, make_equation, condition, color), target in zip(law_specs, targets):
            card_background = RoundedRectangle(
                width=3.8,
                height=1.75,
                corner_radius=0.14,
                stroke_color=color,
                stroke_width=2,
                fill_color=BLACK,
                fill_opacity=0.9,
            )
            card_name = _text(name, 19, color).move_to(UP * 0.5)
            card_formula = make_equation().move_to(DOWN * 0.02)
            card_condition = _text(condition, 15, GREY_A).move_to(DOWN * 0.58)
            card = VGroup(card_background, card_name, card_formula, card_condition)
            card.move_to(DOWN * 1.2)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card, scale=0.88), run_time=0.4)
            self.play(card.animate.move_to(target), run_time=0.85, rate_func=smooth)
            law_cards.append(card)
            self.wait(0.45)

        amount_relation = VGroup(
            _text("Stoffmenge (eigener Zusammenhang):", 17, YELLOW),
            _math(_frac("p", "n", 25, YELLOW), "= konstant", size=25, color=YELLOW),
            _text("T und V konstant", 15, GREY_A),
        ).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.32)
        assumptions = _text(
            "Ideales Gas: Eigenvolumen vernachlässigt • elastische Stöße • keine Wechselwirkung außer Stößen",
            15,
            GREY_A,
        ).next_to(amount_relation, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(amount_relation, assumptions)
        self.play(FadeIn(amount_relation), FadeIn(assumptions), run_time=0.7)
        self.wait(5)


class Chapter10a(ThreeDScene):
    """Kapitel 10a: Wärmeleitung (Konduktion)."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("WÄRMELEITUNG  •  KONDUKTION", 31, BLUE_A).to_edge(UP, buff=0.28)
        subtitle = _text(
            "Metalllöffel im türkischen Tee: Energie fließt vom heißen Ende zum kalten Stiel",
            18,
            GREY_A,
        ).next_to(title, DOWN, buff=0.1)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        glass_center = np.array([-2.45, -0.15, 0.0])
        glass_bottom, glass_top = -1.55, 1.25
        profile_v = np.array([0, 0.035, 0.12, 0.25, 0.4, 0.52, 0.62, 0.75, 0.9, 0.975, 1.0])
        profile_r = np.array([0.38, 0.42, 0.54, 0.67, 0.65, 0.51, 0.49, 0.59, 0.76, 0.81, 0.82])

        def glass_radius(v):
            return float(np.interp(np.clip(v, 0, 1), profile_v, profile_r))

        def glass_profile_point(side, v, inner_offset=0.0):
            y = glass_bottom + v * (glass_top - glass_bottom)
            radius = glass_radius(v) - inner_offset
            return glass_center + np.array([side * radius, y, 0])

        glass_profile_samples = np.linspace(0, 1, 34)
        glass_shell = Polygon(
            *[
                glass_profile_point(-1, v)
                for v in glass_profile_samples
            ],
            *[
                glass_profile_point(1, v)
                for v in glass_profile_samples[::-1]
            ],
            color=BLUE_A,
            stroke_width=1.3,
            fill_color=BLUE_C,
            fill_opacity=0.09,
        )
        inner_glint = VMobject(color=BLUE_A, stroke_width=2.0)
        inner_glint.set_points_smoothly(
            [glass_profile_point(-1, v, 0.035) for v in glass_profile_samples[2:-2]]
        )
        outer_glint = VMobject(color=WHITE, stroke_opacity=0.6, stroke_width=1.1)
        outer_glint.set_points_smoothly(
            [glass_profile_point(1, v) for v in glass_profile_samples[3:-3]]
        )
        rim = Ellipse(
            width=1.64,
            height=0.3,
            color=BLUE_A,
            stroke_width=2.2,
            fill_color=BLUE_E,
            fill_opacity=0.12,
        ).move_to(glass_center + UP * (glass_top - 0.02))
        base_ring = Ellipse(
            width=0.78,
            height=0.16,
            color=BLUE_A,
            stroke_width=1.0,
        ).move_to(glass_center + UP * (glass_bottom + 0.02))

        tea_top = 0.94
        tea_fraction = (tea_top - glass_bottom) / (glass_top - glass_bottom)
        tea_profile_samples = np.linspace(0.04, tea_fraction, 26)
        tea_surface_wall = Polygon(
            *[
                glass_profile_point(-1, v, inner_offset=0.045)
                for v in tea_profile_samples
            ],
            *[
                glass_profile_point(1, v, inner_offset=0.045)
                for v in tea_profile_samples[::-1]
            ],
            color=MAROON,
            stroke_width=0.35,
            fill_color=RED_E,
            fill_opacity=0.88,
        )
        tea_radius = glass_radius(tea_fraction) - 0.05
        tea_surface = Ellipse(
            width=2 * tea_radius,
            height=0.19,
            color=ORANGE,
            stroke_width=0.8,
            fill_color=MAROON,
            fill_opacity=0.88,
        ).move_to(glass_center + UP * tea_top)

        tea_bubbles = VGroup()
        bubble_rng = np.random.default_rng(1010)
        for _ in range(24):
            bx = bubble_rng.uniform(-0.75, 0.75)
            bz = bubble_rng.uniform(-0.75, 0.75)
            if bx * bx + bz * bz < 0.72**2:
                bubble = Dot(
                    point=glass_center + np.array([bx, tea_top + 0.02 + bz * 0.1, 0]),
                    radius=float(bubble_rng.uniform(0.012, 0.026)),
                    color=GOLD_A,
                    fill_opacity=0.55,
                    stroke_width=0,
                )
                tea_bubbles.add(bubble)

        coaster = Ellipse(
            width=1.96,
            height=0.3,
            color=GOLD_E,
            stroke_width=1.0,
            fill_color=MAROON_E,
            fill_opacity=0.95,
        ).move_to(glass_center + DOWN * 1.62)
        coaster_rim = Ellipse(
            width=1.82,
            height=0.23,
            color=GOLD_E,
            stroke_width=0.8,
        ).move_to(glass_center + DOWN * 1.6)

        spoon_bowl_center = glass_center + np.array([-0.15, 0.72, 0.0])
        spoon_bowl = Ellipse(
            width=0.98,
            height=0.54,
            color=GREY_B,
            stroke_width=1.5,
            fill_color=GREY_D,
            fill_opacity=0.96,
        ).move_to(spoon_bowl_center)
        spoon_bowl.rotate(15 * DEGREES)
        spoon_bowl_glint = Arc(
            radius=0.32,
            start_angle=205 * DEGREES,
            angle=115 * DEGREES,
            color=WHITE,
            stroke_width=1.3,
        ).move_to(spoon_bowl_center + UP * 0.015)
        spoon_start = glass_center + np.array([0.34, 0.86, 0.0])
        spoon_end = np.array([3.0, 2.75, 0.15])
        spoon_shaft = Line(
            spoon_start,
            spoon_end,
            color=GREY_B,
            stroke_width=9,
        )
        spoon_highlight = Line(
            spoon_start + np.array([0.035, 0.055, 0.02]),
            spoon_end + np.array([0.035, 0.055, 0.02]),
            color=WHITE,
            stroke_width=1.3,
        )

        steam = VGroup(
            ParametricFunction(
                lambda t: glass_center
                + np.array(
                    [
                        0.1 + 0.08 * np.sin(2 * PI * t),
                        0.78 + 0.52 * t,
                        0.32,
                    ]
                ),
                t_range=[0, 1],
                color=GREY_A,
                stroke_width=1.6,
            ),
            ParametricFunction(
                lambda t: glass_center
                + np.array(
                    [
                        0.42 + 0.08 * np.sin(2 * PI * t + 1.4),
                        0.74 + 0.48 * t,
                        0.28,
                    ]
                ),
                t_range=[0, 1],
                color=GREY_A,
                stroke_width=1.2,
            ),
        )
        mola = Dot3D(
            point=spoon_end + np.array([-0.12, 0.12, 0]),
            radius=0.14,
            color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        )
        mola_label = _text("Mola • kalter Stiel", 17, ORANGE).move_to([4.1, 1.45, 0])
        hot_label = _text("Heißes Ende im Tee", 17, ORANGE).move_to(
            [-4.6, -1.9, 0]
        )
        heat_flow = Arrow(
            [-1.8, 0.55, 0],
            [2.4, 1.65, 0],
            color=ORANGE,
            stroke_width=4,
            buff=0.08,
            max_tip_length_to_length_ratio=0.055,
        )
        flow_label = _text("Wärmefluss", 17, YELLOW).move_to([0.2, 1.95, 0])
        macro_note = _text(
            "Heißer Tee  →  Metalllöffel  →  kälterer Stiel",
            19,
            WHITE,
        ).to_edge(DOWN, buff=0.35)
        macro_objects = VGroup(
            coaster,
            coaster_rim,
            glass_shell,
            tea_surface_wall,
            tea_surface,
            tea_bubbles,
            inner_glint,
            outer_glint,
            rim,
            base_ring,
            spoon_bowl,
            spoon_bowl_glint,
            spoon_shaft,
            spoon_highlight,
            steam,
            mola,
        )
        self.play(
            FadeIn(coaster),
            Create(glass_shell),
            FadeIn(tea_surface_wall),
            FadeIn(tea_surface),
            Create(rim),
            Create(base_ring),
            run_time=2.0,
        )
        self.play(
            FadeIn(coaster_rim),
            FadeIn(tea_bubbles),
            Create(inner_glint),
            Create(outer_glint),
            FadeIn(spoon_bowl),
            Create(spoon_shaft),
            Create(spoon_highlight),
            Create(steam),
            FadeIn(mola),
            run_time=1.6,
        )
        self.add_fixed_in_frame_mobjects(
            mola_label, hot_label, flow_label, macro_note
        )
        self.play(
            FadeIn(mola_label),
            FadeIn(hot_label),
            GrowArrow(heat_flow),
            FadeIn(flow_label),
            FadeIn(macro_note),
            run_time=1.0,
        )
        self.wait(4)
        self.play(
            Indicate(spoon_bowl, color=ORANGE),
            Indicate(mola, color=ORANGE),
            run_time=0.8,
        )
        self.wait(2)

        zoom_caption = _text(
            "Jetzt zoomen wir in das Metallgitter des Löffels",
            21,
            YELLOW,
        ).to_edge(DOWN, buff=0.35)
        # Überblenden statt Transform: Bei Transform entstehen neue Buchstaben, die nicht
        # im Bild fixiert sind; beim anschließenden Zoom fliegen sie dann auseinander.
        self.add_fixed_in_frame_mobjects(zoom_caption)
        self.play(
            FadeOut(macro_note),
            FadeIn(zoom_caption),
            run_time=0.6,
        )
        self.move_camera(
            zoom=1.8,
            frame_center=[0.65, 0.93, 0],
            run_time=1.6,
        )
        micro_title = _text("KRISTALLGITTER DES METALLLÖFFELS", 25, BLUE_A).to_edge(
            UP, buff=0.38
        )
        micro_subtitle = _text(
            "Etwa 1.500 Atome • vergrößertes Modell, nicht maßstabsgetreu",
            17,
            GREY_A,
        ).next_to(micro_title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(micro_title)
        self.play(
            *[FadeOut(mobject) for mobject in macro_objects],
            FadeOut(heat_flow),
            FadeOut(mola_label),
            FadeOut(hot_label),
            FadeOut(flow_label),
            FadeOut(subtitle),
            FadeOut(zoom_caption),
            FadeOut(title),
            FadeIn(micro_title),
            run_time=1.7,
        )
        # Erst nach dem Ausblenden aus der Fixierung lösen (sonst springen sie beim Zoom).
        self.remove_fixed_in_frame_mobjects(
            subtitle, mola_label, hot_label, flow_label, macro_note, zoom_caption, title
        )
        title = micro_title
        self.add_fixed_in_frame_mobjects(micro_subtitle)
        self.remove(
            *macro_objects,
            heat_flow,
            mola_label,
            hot_label,
            flow_label,
            macro_note,
        )
        self.move_camera(zoom=1.0, frame_center=ORIGIN, run_time=1.6)

        columns, rows, layers = 30, 17, 3
        x_values = np.linspace(-5.1, 5.1, columns)
        y_values = np.linspace(-2.2, 2.2, rows)
        layer_x_offsets = [-0.12, 0.0, 0.12]
        layer_y_offsets = [-0.1, 0.0, 0.1]
        atom_points = []
        atom_columns = []
        atom_rows = []
        atom_layers = []
        bond_rows = VGroup()
        for layer in range(layers):
            z = (layer - 1) * 0.18
            for row, y in enumerate(y_values):
                points = [
                    np.array(
                        [
                            x + layer_x_offsets[layer],
                            y + layer_y_offsets[layer],
                            z,
                        ]
                    )
                    for x in x_values
                ]
                bond = VMobject(
                    stroke_color=TEAL_C,
                    stroke_opacity=0.38,
                    stroke_width=0.9,
                )
                bond.set_points_as_corners(points)
                bond_rows.add(bond)
                for column, point in enumerate(points):
                    atom_points.append(point)
                    atom_columns.append(column)
                    atom_rows.append(row)
                    atom_layers.append(layer)
            for column, x in enumerate(x_values):
                points = [
                    np.array(
                        [
                            x + layer_x_offsets[layer],
                            y + layer_y_offsets[layer],
                            z,
                        ]
                    )
                    for y in y_values
                ]
                bond = VMobject(
                    stroke_color=TEAL_C,
                    stroke_opacity=0.38,
                    stroke_width=0.9,
                )
                bond.set_points_as_corners(points)
                bond_rows.add(bond)

        atom_count = columns * rows * layers
        base_positions = np.asarray(atom_points)
        column_indices = np.asarray(atom_columns)
        layer_indices = np.asarray(atom_layers)
        base_colors = np.asarray(
            [
                color_to_rgb(interpolate_color(BLUE_C, GREY_B, layer / 2))
                for layer in layer_indices
            ]
        )
        hot_color = color_to_rgb(ORANGE)
        atom_cloud = PMobject(stroke_width=5)
        atom_cloud.add_points(
            base_positions.copy(),
            rgbas=np.column_stack(
                (base_colors, np.full(atom_count, 0.98))
            ),
        )

        # Wärmeleitung als Temperaturprofil: Das Ende im Tee bleibt heiß, die
        # "Wärmefront" wandert zum Stiel. Jedes Atom schwingt ungeordnet um seine
        # Ruhelage; die Amplitude wächst mit der örtlichen Temperatur.
        # (Vorher lief ein einzelner Wellenpuls durch, und das heiße Ende kühlte
        # danach wieder ab, obwohl es noch im Tee steckt.)
        heat_front = ValueTracker(2.0)
        phase_rng = np.random.default_rng(1011)
        phase_x = phase_rng.uniform(0, TAU, atom_count)
        phase_y = phase_rng.uniform(0, TAU, atom_count)
        vibration = {"time": 0.0}

        def animate_lattice_heat(mob, dt):
            vibration["time"] += dt
            heat = 1 / (1 + np.exp((column_indices - heat_front.get_value()) / 2.5))
            amplitude = 0.02 + 0.13 * heat
            angle = 2 * PI * 3.0 * vibration["time"]
            mob.points[:] = base_positions
            mob.points[:, 0] += 0.45 * amplitude * np.sin(angle + phase_x)
            mob.points[:, 1] += amplitude * np.sin(angle * 1.13 + phase_y)
            color_mix = np.clip(heat * 0.95, 0, 0.95)[:, np.newaxis]
            mob.rgbas[:, :3] = base_colors * (1 - color_mix) + hot_color * color_mix

        atom_cloud.add_updater(animate_lattice_heat)
        energy_direction = Arrow(
            LEFT * 4.7 + UP * 2.55,
            RIGHT * 4.7 + UP * 2.55,
            color=ORANGE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.055,
        )
        hot_end = _text("HEISSES ENDE", 15, ORANGE).move_to(LEFT * 5.0 + UP * 2.8)
        cold_end = _text("KALTER STIEL", 15, BLUE_A).move_to(RIGHT * 5.0 + UP * 2.8)
        structure_note = _text(
            "Die Atome schwingen an ihrem Platz; weitergegeben wird nur die Energie.",
            18,
            WHITE,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(
            energy_direction, hot_end, cold_end, structure_note
        )
        self.play(
            Create(bond_rows),
            FadeIn(atom_cloud),
            GrowArrow(energy_direction),
            FadeIn(hot_end),
            FadeIn(cold_end),
            FadeIn(structure_note),
            run_time=2.4,
        )
        count_note = _text(
            f"{atom_count} Atome dargestellt: Jeder Punkt ist ein Metallatom.",
            16,
            GREY_A,
        ).next_to(structure_note, UP, buff=0.16)
        self.add_fixed_in_frame_mobjects(count_note)
        self.play(FadeIn(count_note), run_time=0.5)
        self.wait(4)

        vibration_note = _text(
            "Nahaufnahme: Am heißen Ende schwingen die Atome stärker.",
            18,
            ORANGE,
        ).to_edge(DOWN, buff=0.35)
        self.play(Transform(structure_note, vibration_note), run_time=0.6)
        self.wait(2)
        self.play(
            heat_front.animate.set_value(columns * 0.5),
            run_time=8.5,
            rate_func=linear,
        )
        self.wait(2)

        electron_note = _text(
            "In echten Metallen transportieren freie Elektronen sogar den größten Teil der Wärme.\n"
            "Diese Darstellung zeigt nur den Beitrag der Gitterschwingungen.",
            18,
            GREY_A,
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(electron_note)
        self.play(
            FadeOut(structure_note),
            FadeOut(count_note),
            FadeIn(electron_note),
            run_time=0.6,
        )
        self.remove_fixed_in_frame_mobjects(structure_note, count_note)
        self.wait(4)

        # Am Ende bleibt ein Temperaturgefälle: Der Stiel ist warm, aber kühler als das Ende im Tee.
        self.play(
            heat_front.animate.set_value(columns - 3),
            run_time=7.5,
            rate_func=linear,
        )
        self.wait(2)

        final_note = _text(
            "Heißer Tee → Atomgitter des Löffels → kälterer Stiel",
            21,
            YELLOW,
        ).to_edge(DOWN, buff=0.35)
        self.play(Transform(electron_note, final_note), run_time=0.6)
        self.wait(6)


class Chapter10b(ThreeDScene):
    """Kapitel 10b: Wärmeströmung (Konvektion)."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("WÄRMESTRÖMUNG  •  KONVEKTION", 32, BLUE_A).to_edge(
            UP, buff=0.3
        )
        subtitle = _text(
            "In Flüssigkeiten und Gasen wird Energie mit der strömenden Materie transportiert",
            19,
            GREY_A,
        ).next_to(title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        vessel = Cylinder(
            radius=1.28,
            height=2.8,
            direction=UP,
            resolution=(24, 16),
            fill_color=BLUE_E,
            fill_opacity=0.12,
            stroke_color=BLUE_A,
            stroke_width=1.5,
        ).move_to([-2.1, -0.05, 0])
        water = Cylinder(
            radius=1.12,
            height=2.35,
            direction=UP,
            resolution=(24, 16),
            fill_color=BLUE_D,
            fill_opacity=0.24,
            stroke_color=BLUE_C,
            stroke_width=0.5,
        ).move_to([-2.1, -0.12, 0])
        # Heizer unter der linken Seite: dort steigt das warme Wasser auf,
        # rechts sinkt das kühlere ab (vorher lag der Heizer unter beiden Seiten).
        heater = RoundedRectangle(
            width=0.95,
            height=0.22,
            corner_radius=0.08,
            color=ORANGE,
            fill_color=RED_E,
            fill_opacity=0.95,
        ).move_to([-2.7, -1.65, 0])
        heater_label = _text("Heizer", 17, ORANGE).next_to(
            heater, DOWN, buff=0.1
        )
        self.play(Create(vessel), FadeIn(water), FadeIn(heater), run_time=1.4)
        self.add_fixed_in_frame_mobjects(heater_label)
        self.play(FadeIn(heater_label), run_time=0.4)

        loop_points = [
            [-2.85, -0.9, 0],
            [-2.85, -0.25, 0],
            [-2.72, 0.45, 0],
            [-2.3, 0.93, 0],
            [-1.65, 0.92, 0],
            [-1.32, 0.35, 0],
            [-1.3, -0.35, 0],
            [-1.58, -0.95, 0],
            [-2.12, -1.05, 0],
        ]
        hot_up = Arrow(
            [-2.85, -0.75, 0],
            [-2.78, 0.55, 0],
            color=ORANGE,
            stroke_width=5,
            buff=0.05,
        )
        warm_top = Arrow(
            [-2.55, 0.95, 0],
            [-1.65, 0.95, 0],
            color=RED_C,
            stroke_width=5,
            buff=0.05,
        )
        cool_down = Arrow(
            [-1.3, 0.58, 0],
            [-1.35, -0.72, 0],
            color=BLUE_A,
            stroke_width=5,
            buff=0.05,
        )
        cool_bottom = Arrow(
            [-1.65, -1.05, 0],
            [-2.55, -1.05, 0],
            color=BLUE_C,
            stroke_width=5,
            buff=0.05,
        )
        arrows = VGroup(hot_up, warm_top, cool_down, cool_bottom)
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15),
            run_time=1.8,
        )

        warm_note = _text(
            "Erwärmtes Wasser dehnt sich aus,\nseine Dichte sinkt, es steigt auf.",
            19,
            ORANGE,
        ).move_to([2.85, 0.85, 0])
        cool_note = _text(
            "Abgekühltes, dichteres Wasser\nsinkt nach unten.",
            19,
            BLUE_A,
        ).move_to([2.85, -0.25, 0])
        self.add_fixed_in_frame_mobjects(warm_note, cool_note)
        self.play(FadeIn(warm_note), FadeIn(cool_note), run_time=0.6)
        self.wait(3)
        self.wait(4)

        # Alle drei Teilchen strömen im geschlossenen Kreislauf mit.
        loop_count = len(loop_points)
        offsets = [0, 4, 6]
        molecules = VGroup(
            Dot(loop_points[0], radius=0.12, color=ORANGE),
            Dot(loop_points[4], radius=0.09, color=RED_C),
            Dot(loop_points[6], radius=0.09, color=BLUE_A),
        )
        mola_label = _text("Mola", 17, ORANGE).next_to(
            molecules[0], LEFT, buff=0.12
        )
        mola_label.add_updater(lambda mob: mob.next_to(molecules[0], LEFT, buff=0.12))
        self.add_fixed_in_frame_mobjects(mola_label)
        self.play(FadeIn(molecules), FadeIn(mola_label), run_time=0.5)
        for loop in range(4):
            for step in range(1, loop_count + 1):
                animations = []
                for index, (molecule, offset) in enumerate(zip(molecules, offsets)):
                    point_index = (step + offset) % loop_count
                    animation = molecule.animate.move_to(loop_points[point_index])
                    if index > 0:
                        # Aufsteigende Seite und oben warm, absteigende Seite kühl.
                        animation = animation.set_color(RED_C if point_index <= 4 else BLUE_A)
                    animations.append(animation)
                self.play(*animations, run_time=0.32, rate_func=linear)
            if loop == 0:
                self.wait(1)
        mola_label.clear_updaters()

        density_note = _text(
            "Temperaturunterschied → Dichteunterschied → Strömungskreislauf",
            21,
            YELLOW,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(density_note)
        self.play(FadeIn(density_note), run_time=0.7)
        self.wait(12)
        self.wait(4)


class Chapter10c(ThreeDScene):
    """Kapitel 10c: Wärmestrahlung."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("WÄRMESTRAHLUNG", 32, BLUE_A).to_edge(
            UP, buff=0.3
        )
        subtitle = _text(
            "Energieübertragung durch elektromagnetische Wellen",
            19,
            GREY_A,
        ).next_to(title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        sun = Sphere(
            radius=0.72,
            resolution=(12, 12),
            color=YELLOW,
            checkerboard_colors=[YELLOW, YELLOW],
            fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.25, 0.15, 0])
        sun_glow = VGroup(
            Circle(radius=0.92, color=ORANGE, stroke_opacity=0.7),
            Circle(radius=1.08, color=RED_C, stroke_opacity=0.35),
        ).move_to(sun.get_center())
        sun_label = _text("Sonne", 19, YELLOW).next_to(sun, DOWN, buff=0.2)
        target = Cube(
            side_length=1.25,
            fill_color=GREY_D,
            fill_opacity=0.95,
            stroke_color=WHITE,
        ).move_to([2.55, -0.05, 0])
        target_label = _text("Oberfläche", 18, WHITE).next_to(target, DOWN, buff=0.2)
        self.play(
            FadeIn(sun_glow),
            FadeIn(sun),
            FadeIn(sun_label),
            FadeIn(target),
            FadeIn(target_label),
            run_time=1.3,
        )

        ray_levels = [-0.55, 0.05, 0.65]
        rays = VGroup(
            *[
                Arrow(
                    [-2.35, level, 0],
                    [1.85, level, 0],
                    color=YELLOW if index != 1 else ORANGE,
                    stroke_width=3.5,
                    buff=0.04,
                    max_tip_length_to_length_ratio=0.06,
                )
                for index, level in enumerate(ray_levels)
            ]
        )
        vacuum = _text("Leerer Weltraum", 17, GREY_A).move_to([-0.25, 1.05, 0])
        no_medium = _text(
            "Kein Stoff nötig",
            18,
            TEAL_A,
        ).move_to([-0.25, -1.05, 0])
        self.add_fixed_in_frame_mobjects(vacuum, no_medium)
        self.play(
            LaggedStart(*[GrowArrow(ray) for ray in rays], lag_ratio=0.2),
            FadeIn(vacuum),
            FadeIn(no_medium),
            run_time=1.8,
        )
        self.wait(3)

        energy_packets = VGroup(
            *[
                Dot([-2.2, level, 0], radius=0.1, color=ORANGE)
                for level in ray_levels
            ]
        )
        self.play(FadeIn(energy_packets), run_time=0.35)
        self.play(
            *[
                packet.animate.move_to([1.82, level, 0])
                for packet, level in zip(energy_packets, ray_levels)
            ],
            run_time=2.4,
            rate_func=linear,
        )
        self.play(FadeOut(energy_packets), run_time=0.25)
        self.wait(2)
        repeat_packets = VGroup(
            *[
                Dot([-2.2, level, 0], radius=0.1, color=ORANGE)
                for level in ray_levels
            ]
        )
        self.play(FadeIn(repeat_packets), run_time=0.3)
        self.play(
            *[
                packet.animate.move_to([1.82, level, 0])
                for packet, level in zip(repeat_packets, ray_levels)
            ],
            run_time=2.4,
            rate_func=linear,
        )
        self.play(FadeOut(repeat_packets), run_time=0.25)

        wave_subtitle = _text(
            "Nahaufnahme: elektrisches und magnetisches Feld stehen senkrecht aufeinander",
            19,
            GREY_A,
        ).next_to(title, DOWN, buff=0.12)
        wave_heading = _text(
            "ELEKTROMAGNETISCHE WELLE",
            18,
            WHITE,
        ).to_edge(DOWN, buff=0.72)
        wave_legend = _text(
            "Blau: elektrisches Feld E     Rot: magnetisches Feld B     Ausbreitungsrichtung: →",
            16,
            GREY_A,
        ).to_edge(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(wave_heading, wave_legend, wave_subtitle)
        # Überblenden statt Transform, damit der Untertitel beim Drehen der Kamera fixiert bleibt.
        self.play(
            FadeOut(sun_glow),
            FadeOut(sun),
            FadeOut(sun_label),
            FadeOut(target),
            FadeOut(target_label),
            FadeOut(rays),
            FadeOut(vacuum),
            FadeOut(no_medium),
            FadeOut(subtitle),
            FadeIn(wave_subtitle),
            run_time=0.8,
        )
        self.remove_fixed_in_frame_mobjects(vacuum, no_medium, subtitle)
        subtitle = wave_subtitle
        self.move_camera(
            phi=50 * DEGREES,
            theta=-45 * DEGREES,
            zoom=1.0,
            frame_center=ORIGIN,
            run_time=1.4,
        )

        wave_x = np.linspace(-3.65, 3.65, 56)

        def field_points(field):
            wave = np.sin(2 * PI * wave_x / 3.8)
            if field == "electric":
                return np.column_stack((wave_x, 1.05 * wave, np.zeros_like(wave_x)))
            return np.column_stack((wave_x, np.zeros_like(wave_x), 1.05 * wave))

        electric_wave = VMobject(color=BLUE_B, stroke_width=4)
        electric_wave.set_points_smoothly(field_points("electric"))
        magnetic_wave = VMobject(color=RED_C, stroke_width=4)
        magnetic_wave.set_points_smoothly(field_points("magnetic"))
        propagation_arrow = Arrow(
            [-3.5, -1.35, -1.0],
            [3.5, -1.35, -1.0],
            color=WHITE,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.05,
        )
        electric_vector = Arrow(
            [2.95, 0, 0],
            [2.95, 1.25, 0],
            color=BLUE_B,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        magnetic_vector = Arrow(
            [2.95, 0, 0],
            [2.95, 0, 1.25],
            color=RED_C,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        wave_progress = ValueTracker(-3.5)
        wave_marker = Dot(radius=0.09, color=YELLOW)
        wave_marker.move_to([-3.5, 1.05 * np.sin(2 * PI * -3.5 / 3.8), 0])
        wave_marker.add_updater(
            lambda mob: mob.move_to(
                [
                    wave_progress.get_value(),
                    1.05
                    * np.sin(2 * PI * wave_progress.get_value() / 3.8),
                    0,
                ]
            )
        )
        wave_group = VGroup(
            electric_wave,
            magnetic_wave,
            propagation_arrow,
            electric_vector,
            magnetic_vector,
            wave_marker,
        )
        self.play(
            Create(electric_wave),
            Create(magnetic_wave),
            FadeIn(propagation_arrow),
            FadeIn(electric_vector),
            FadeIn(magnetic_vector),
            FadeIn(wave_marker),
            FadeIn(wave_heading),
            FadeIn(wave_legend),
            run_time=1.5,
        )
        self.wait(1)
        self.play(
            wave_progress.animate.set_value(3.5),
            run_time=2.5,
            rate_func=linear,
        )
        self.wait(1)

        absorption_subtitle = _text(
            "Nahaufnahme: Die Oberfläche absorbiert die Strahlung und erwärmt sich",
            19,
            GREY_A,
        ).next_to(title, DOWN, buff=0.12)
        self.play(
            FadeOut(wave_heading),
            FadeOut(wave_legend),
            run_time=0.8,
        )
        self.remove_fixed_in_frame_mobjects(wave_heading, wave_legend)
        self.add_fixed_in_frame_mobjects(absorption_subtitle)
        self.play(FadeOut(subtitle), FadeIn(absorption_subtitle), run_time=0.5)
        self.remove_fixed_in_frame_mobjects(subtitle)
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=0.75,
            frame_center=ORIGIN,
            run_time=1.2,
        )

        absorption_title = _text(
            "ABSORPTION: DIE ENERGIE DER WELLE GEHT AUF DIE OBERFLÄCHE ÜBER",
            19,
            ORANGE,
        ).to_edge(DOWN, buff=0.4)
        surface_atoms = VGroup(
            *[
                Dot3D(
                    point=[
                        2.55 + (column - 1.5) * 0.28,
                        -0.05 + (row - 1.5) * 0.28,
                        0.66,
                    ],
                    radius=0.075,
                    color=BLUE_C,
                )
                for row in range(4)
                for column in range(4)
            ]
        )
        absorbed_mola = Dot3D(
            point=[2.55, -0.05, 0.72],
            radius=0.13,
            color=ORANGE,
        )
        absorption_note = _text(
            "Die Energie geht auf die Teilchen über; sie schwingen stärker, die Temperatur steigt.",
            16,
            GREY_A,
        ).to_edge(DOWN, buff=0.08)
        self.add_fixed_in_frame_mobjects(absorption_title, absorption_note)
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=2.1,
            frame_center=[2.55, -0.05, 0],
            added_anims=[
                FadeOut(wave_group),
                FadeIn(target),
                FadeIn(target_label),
                FadeIn(surface_atoms),
                FadeIn(absorbed_mola),
                FadeIn(absorption_title),
                FadeIn(absorption_note),
            ],
            run_time=1.5,
        )
        incoming_energy = Dot3D(
            point=[-1.6, -0.05, 0.68],
            radius=0.12,
            color=YELLOW,
        )
        self.play(FadeIn(incoming_energy), run_time=0.25)
        self.play(
            incoming_energy.animate.move_to([1.93, -0.05, 0.68]),
            run_time=1.8,
            rate_func=linear,
        )
        self.play(
            FadeOut(incoming_energy),
            target.animate.set_fill(ORANGE, opacity=0.72),
            *[
                atom.animate.set_color(ORANGE).scale(1.3).shift(UP * 0.035)
                for atom in surface_atoms
            ],
            absorbed_mola.animate.set_color(RED).scale(1.25),
            run_time=0.8,
        )
        self.play(
            *[atom.animate.shift(DOWN * 0.07) for atom in surface_atoms],
            run_time=0.25,
        )
        self.play(
            *[atom.animate.shift(UP * 0.07) for atom in surface_atoms],
            run_time=0.25,
        )
        self.wait(3)

        comparison = _text(
            "Leitung: von Atom zu Atom     Strömung: mit dem Fluid     Strahlung: mit der Welle",
            18,
            WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(comparison)
        self.play(
            FadeOut(absorption_title),
            FadeOut(absorption_note),
            FadeIn(comparison),
            run_time=0.7,
        )
        self.remove_fixed_in_frame_mobjects(absorption_title, absorption_note)
        self.wait(12)
        self.wait(6)


class Chapter11(ThreeDScene):
    """Kapitel 11: Zusammenfassung der Reise durch die Thermodynamik."""

    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

        title = _text("VOM MOLEKÜL ZUM GANZEN SYSTEM", 31, BLUE_A).to_edge(
            UP, buff=0.35
        )
        subtitle = _text(
            "Begriffslandkarte der Reise durch die Thermodynamik",
            19,
            GREY_A,
        ).next_to(title, DOWN, buff=0.12)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        card_specs = [
            ("p  •  DRUCK", "Kraft der Wandstöße\npro Fläche", ORANGE, [-4.55, 1.2, 0]),
            ("V  •  VOLUMEN", "Raum, den das Gas\neinnimmt", BLUE_B, [4.55, 1.2, 0]),
            ("n  •  STOFFMENGE", "Gasmenge,\nin Mol", TEAL_A, [-4.55, -1.2, 0]),
            ("T  •  ABSOLUTE TEMPERATUR", "Hängt mit der mittleren Translationsenergie\nzusammen, in Kelvin", YELLOW, [4.55, -1.2, 0]),
        ]

        def make_card(heading, detail, color, center, width=3.25, height=1.45):
            background = RoundedRectangle(
                corner_radius=0.14,
                width=width,
                height=height,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.12,
            ).move_to(center)
            heading_text = _text(heading, 17, color)
            if heading_text.width > width - 0.2:
                heading_text.scale_to_fit_width(width - 0.2)
            heading_text.move_to(background.get_center() + UP * 0.34)
            detail_text = _text(detail, 14, WHITE)
            if detail_text.width > width - 0.2:
                detail_text.scale_to_fit_width(width - 0.2)
            detail_text.move_to(background.get_center() + DOWN * 0.22)
            return VGroup(background, heading_text, detail_text)

        map_cards = VGroup(
            *[
                make_card(heading, detail, color, center)
                for heading, detail, color, center in card_specs
            ]
        )
        formula = _text("pV = nRT", 48, WHITE).move_to(ORIGIN)
        connectors = VGroup(
            Line([-2.92, 0.78, 0], [-1.75, 0.35, 0], color=ORANGE, stroke_width=2),
            Line([2.92, 0.78, 0], [1.75, 0.35, 0], color=BLUE_B, stroke_width=2),
            Line([-2.92, -0.78, 0], [-1.75, -0.35, 0], color=TEAL_A, stroke_width=2),
            Line([2.92, -0.78, 0], [1.75, -0.35, 0], color=YELLOW, stroke_width=2),
        )
        self.add_fixed_in_frame_mobjects(connectors, formula, map_cards)
        self.play(
            Create(connectors),
            LaggedStart(*[FadeIn(card) for card in map_cards], lag_ratio=0.16),
            FadeIn(formula, scale=0.8),
            run_time=2.2,
        )
        kelvin_note = _text(
            "T [K] = t [°C] + 273,15",
            17,
            YELLOW,
        ).next_to(formula, DOWN, buff=0.45)
        self.add_fixed_in_frame_mobjects(kelvin_note)
        self.play(FadeIn(kelvin_note), run_time=0.5)
        self.wait(4)

        law_title = _text(
            "DIE GASGESETZE ENTSTEHEN, WENN MAN EINIGE GRÖSSEN KONSTANT HÄLT",
            20,
            BLUE_A,
        ).move_to([0, 2.45, 0])
        law_specs = [
            ("BOYLE-MARIOTTE", "T und n konstant", "p · V = konstant", BLUE_B),
            ("AMONTONS", "V und n konstant", "p / T = konstant", ORANGE),
            ("GAY-LUSSAC", "p und n konstant", "V / T = konstant", TEAL_A),
        ]
        law_cards = VGroup(
            *[
                make_card(
                    f"GESETZ VON {name}",
                    f"{condition}\n{relation}",
                    color,
                    [x, 0.25, 0],
                    width=3.9,
                    height=1.65,
                )
                for (name, condition, relation, color), x in zip(
                    law_specs, [-4.55, 0, 4.55]
                )
            ]
        )
        law_takeaway = _text(
            "Achte bei jedem Versuch darauf, welche Größen konstant bleiben.",
            18,
            WHITE,
        ).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(law_title, law_cards, law_takeaway)
        self.play(
            FadeOut(VGroup(connectors, formula, kelvin_note, map_cards, subtitle)),
            FadeIn(law_title),
            LaggedStart(*[FadeIn(card) for card in law_cards], lag_ratio=0.2),
            FadeIn(law_takeaway),
            run_time=1.6,
        )
        self.remove_fixed_in_frame_mobjects(
            connectors, formula, kelvin_note, map_cards, subtitle
        )
        self.wait(5)

        transfer_title = _text(
            "ENERGIE KANN AUF DREI WEGEN ÜBERTRAGEN WERDEN",
            23,
            BLUE_A,
        ).move_to([0, 2.5, 0])
        transfer_specs = [
            ("WÄRMELEITUNG", "Von Atom zu Atom", ORANGE),
            ("WÄRMESTRÖMUNG", "Mit dem strömenden Fluid", TEAL_A),
            ("WÄRMESTRAHLUNG", "Mit elektromagnetischen Wellen", YELLOW),
        ]
        transfer_cards = VGroup(
            *[
                make_card(
                    name,
                    explanation,
                    color,
                    [x, 1.05, 0],
                    width=4.0,
                    height=1.7,
                )
                for (name, explanation, color), x in zip(
                    transfer_specs, [-4.55, 0, 4.55]
                )
            ]
        )
        conduction_icon = VGroup(
            *[
                Dot([-5.55 + index * 0.48, -0.45, 0], radius=0.065, color=ORANGE)
                for index in range(5)
            ],
            *[
                Line(
                    [-5.48 + index * 0.48, -0.45, 0],
                    [-5.14 + index * 0.48, -0.45, 0],
                    color=ORANGE,
                    stroke_width=2,
                )
                for index in range(4)
            ],
        )
        convection_icon = VGroup(
            *[
                Dot([x, y, 0], radius=0.07, color=TEAL_A)
                for x, y in [(-0.3, -0.52), (0.25, -0.52), (-0.3, 0.03), (0.25, 0.03)]
            ],
            Arc(
                radius=0.28,
                start_angle=20 * DEGREES,
                angle=290 * DEGREES,
                color=TEAL_A,
                stroke_width=2,
            ).move_to([0, -0.25, 0]),
        )
        wave_points = [
            np.array([3.72 + index * 0.11, -0.45 + 0.14 * np.sin(index * PI / 3), 0])
            for index in range(25)
        ]
        radiation_icon = VMobject(color=YELLOW, stroke_width=2.5)
        radiation_icon.set_points_smoothly(wave_points)
        self.add_fixed_in_frame_mobjects(
            transfer_title,
            transfer_cards,
            conduction_icon,
            convection_icon,
            radiation_icon,
        )
        self.play(
            FadeOut(VGroup(law_title, law_cards, law_takeaway)),
            FadeIn(transfer_title),
            LaggedStart(*[FadeIn(card) for card in transfer_cards], lag_ratio=0.2),
            FadeIn(conduction_icon),
            FadeIn(convection_icon),
            Create(radiation_icon),
            run_time=1.6,
        )
        self.remove_fixed_in_frame_mobjects(law_title, law_cards, law_takeaway)
        self.wait(4)

        takeaway = _text(
            "Temperatur: mittlere Energie     •     Innere Energie: gesamte Energie",
            22,
            YELLOW,
        ).move_to([0, -1.4, 0])
        heat_note = _text(
            "Wärme wird nicht gespeichert; sie ist Energieübertragung wegen eines Temperaturunterschieds.",
            17,
            WHITE,
        ).move_to([0, -2.0, 0])
        final_line = _text(
            "Jetzt kennst du nicht nur die Formel, sondern auch ihren Grund, vom Molekül aus gedacht.",
            17,
            BLUE_A,
        ).to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(takeaway, heat_note, final_line)
        self.play(
            FadeIn(takeaway),
            FadeIn(heat_note),
            FadeIn(final_line),
            run_time=0.9,
        )
        self.wait(7)
