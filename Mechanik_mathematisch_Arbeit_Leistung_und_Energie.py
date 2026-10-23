"""
Arbeit, Leistung und Energie – Manim-Video (Deutsch, ohne Untertitelleiste)

Gesamtvideo:
    manim -pql arbeit_leistung_energie.py Gesamt       # schnelle Vorschau (480p15)
    manim -pqm arbeit_leistung_energie.py Gesamt       # 720p30
    manim -p -r 854,480 --fps 30 arbeit_leistung_energie.py Gesamt   # 480p30

Einzelne Szenen (zum schnellen Testen):
    Szene0_Titel, Szene1_Arbeit, Szene2_Integral3D, Szene3_Zeit,
    Szene4_Herleitungen, Szene5_Leistung, Szene6_Energie, Zusammenfassung

Voraussetzungen: manim, LaTeX (MiKTeX / TeX Live), ffmpeg.
"""
import numpy as np
from manim import *

BG = "#14213D"
C_F = "#E9A23B"   # Kraft
C_S = "#5BC0BE"   # Weg
C_W = "#7FD1AE"   # Arbeit
C_P = "#F28482"   # Leistung
C_E = "#9D8DF1"   # Energie
FONT = "Calibri"  # Mac/Linux: ggf. "Arial" oder "DejaVu Sans"


def de(text, size=30, color=WHITE, **kw):
    """Deutscher Text (Pango) – Umlaute funktionieren."""
    return Text(text, font=FONT, font_size=size, color=color, **kw)


def definition_box(zeilen):
    label = de("DEFINITION", 20, C_W, weight=BOLD)
    body = VGroup(*[de(z, 28) for z in zeilen]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    inhalt = VGroup(label, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = SurroundingRectangle(inhalt, color=C_W, buff=0.3, corner_radius=0.15)
    box.set_fill(C_W, opacity=0.08)
    return VGroup(box, inhalt)


class Basis(ThreeDScene):
    """Gemeinsame Basis: Hintergrund, Hilfsfunktionen, 3D-fähig."""

    def setup(self):
        self.camera.background_color = BG

    # ---- Hilfsfunktionen ------------------------------------------------
    def flach(self):
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    def fix(self, *mobs):
        """Mobjects bildschirmfest machen (bleiben bei 3D-Kamerafahrt gerade),
        aber noch nicht anzeigen."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)

    def kapitel(self, text, fixed=False):
        t = de(text, 36, C_W, weight=BOLD).to_edge(UP, buff=0.45)   # immer waagerecht zentriert
        if fixed:
            self.fix(t)
        self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.5)
        return t

    def unter(self, m, ref, buff=0.5):
        """m unter ref platzieren und waagerecht in die Bildmitte setzen."""
        m.next_to(ref, DOWN, buff=buff)
        m.set_x(0)
        return m

    def balken(self, ax, n, D, xmax, tiefe=0.1):
        dx = xmax / n
        ux = ax.c2p(dx, 0, 0)[0] - ax.c2p(0, 0, 0)[0]
        uz = ax.c2p(0, 0, 1)[2] - ax.c2p(0, 0, 0)[2]
        farben = color_gradient([C_S, C_W], n)
        g = VGroup()
        for i in range(n):
            x0 = i * dx
            h = D * x0                       # linke Summe: F(s_i)
            if h < 1e-3:
                continue
            p = Prism(dimensions=[ux, tiefe, h * uz], fill_color=farben[i], fill_opacity=0.85, stroke_width=0)
            if n <= 40:
                p.set_stroke(WHITE, 0.6)
            p.move_to(ax.c2p(x0 + dx / 2, 0, h / 2))
            g.add(p)
        return g

    def aufraeumen(self):
        alle = list(self.mobjects)
        if alle:
            self.play(*[FadeOut(m) for m in alle], run_time=0.6)
        self.clear()
        self.flach()


# =====================================================================
# Szene 0: Titel
# =====================================================================
class Szene0_Titel(Basis):
    def construct(self):
        self.flach()
        t = de("Arbeit, Leistung und Energie", 56, WHITE, weight=BOLD)
        u = de("Mechanik – mathematisch erklärt", 32, GREY_B)
        f = MathTex(r"W = \int F \, \mathrm{d}s", font_size=90, color=C_W)
        n = de("Süleyman Kaya", 30, C_S)
        VGroup(t, u, f, n).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        self.play(Write(t), run_time=1.5)
        self.play(FadeIn(u), Write(f))
        self.play(FadeIn(n, shift=UP * 0.2))
        self.wait(2)
        self.aufraeumen()


# =====================================================================
# Szene 1: Arbeit – Definition, Fläche im F-s-Diagramm
# =====================================================================
class Szene1_Arbeit(Basis):
    def construct(self):
        self.flach()
        self.kapitel("1 · Arbeit")

        d = definition_box([
            "Die Arbeit W ist das Produkt aus der in Wegrichtung",
            "wirkenden Kraft F und dem zurückgelegten Weg s.",
        ])
        f = MathTex(r"W = F \cdot s", font_size=96, tex_to_color_map={"F": C_F, "s": C_S})
        e = MathTex(r"[W] = \mathrm{N \cdot m} = \mathrm{J} = \mathrm{W \cdot s}", font_size=42, color=GREY_B)
        grp = VGroup(d, f, e).arrange(DOWN, buff=0.55).move_to(DOWN * 0.4)
        self.play(FadeIn(d, shift=UP * 0.3))
        self.play(Write(f))
        self.play(FadeIn(e))
        self.wait(2.5)
        self.play(FadeOut(grp))

        # Beispiel: Fläche im F-s-Diagramm (alles erst bauen, dann als Block zentrieren)
        ax = Axes(
            x_range=[0, 120, 20], y_range=[0, 40, 10], x_length=7.5, y_length=3.8,
            tips=True, axis_config={"color": WHITE},
        )
        lx = MathTex(r"s\;[\mathrm{m}]", color=C_S, font_size=34).next_to(ax.x_axis.get_end(), DOWN, buff=0.2)
        ly = MathTex(r"F\;[\mathrm{N}]", color=C_F, font_size=34).next_to(ax.y_axis.get_end(), LEFT, buff=0.2)
        p0, p1, p2, p3 = ax.c2p(0, 0), ax.c2p(100, 0), ax.c2p(100, 20), ax.c2p(0, 20)
        rect = Polygon(p0, p1, p2, p3, color=C_W, fill_color=C_W, fill_opacity=0.6, stroke_width=3)
        fl = MathTex(r"F = 20\,\mathrm{N}", color=C_F, font_size=38).next_to(p3, LEFT, buff=0.15)
        sl = MathTex(r"s = 100\,\mathrm{m}", color=C_S, font_size=38).next_to(p1, DOWN, buff=0.15)
        flab = de("Fläche unter der Kurve = Arbeit", 26, C_W).next_to(ax, UP, buff=0.3)
        ergebnis = VGroup(
            MathTex(r"W = F \cdot s", font_size=50),
            MathTex(r"= 20\,\mathrm{N} \cdot 100\,\mathrm{m}", font_size=42),
            MathTex(r"= 2000\,\mathrm{J}", font_size=54, color=C_W),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.9)
        VGroup(ax, lx, ly, rect, fl, sl, flab, ergebnis).move_to(DOWN * 0.3)

        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        self.play(FadeIn(fl))
        self.play(GrowFromPoint(rect, p0), run_time=2)
        self.play(FadeIn(sl), Write(flab))
        self.play(Write(ergebnis))
        self.wait(2.5)
        self.aufraeumen()


# =====================================================================
# Szene 2: Summe -> Integral in 3D
# =====================================================================
class Szene2_Integral3D(Basis):
    """Veränderliche Kraft: F(s) und s(t), dritte Achse = Zeit t. Danach Summe -> Integral."""

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)
        self.kapitel("2 · Veränderliche Kraft", fixed=True)
        T, SMAX, D = 8.0, 24.0, 0.5
        s_f = lambda t: 3 * t + 2.5 * (1 - np.cos(0.8 * t))     # Ort zur Zeit t (wie in Szene 3)
        F_f = lambda x: D * x                                   # Beispiel: Feder
        tt = np.linspace(0, T, 2001)
        ss = s_f(tt)
        t_of_s = lambda x: float(np.interp(x, ss, tt))          # Umkehrfunktion t(s)

        # x = Weg s, y = Zeit t (dritte Achse), z = Kraft F
        ax = ThreeDAxes(
            x_range=[0, SMAX, 6], y_range=[0, T, 2], z_range=[0, 12, 4],
            x_length=6.0, y_length=4.0, z_length=3.2,
        ).shift(LEFT * 2.2 + DOWN * 0.2)
        lx = MathTex(r"s", color=C_S, font_size=40).move_to(ax.c2p(SMAX + 1.8, 0, 0))
        lt = MathTex(r"t", color=C_E, font_size=40).move_to(ax.c2p(0, T + 0.9, 0))
        lz = MathTex(r"F", color=C_F, font_size=40).move_to(ax.c2p(0, 0, 13.5))
        self.add_fixed_orientation_mobjects(lx, lt, lz)
        self.remove(lx, lt, lz)

        kF = ParametricFunction(lambda u: ax.c2p(u, 0, F_f(u)), t_range=[0, SMAX], color=C_F, stroke_width=7)
        kS = ParametricFunction(lambda u: ax.c2p(s_f(u), u, 0), t_range=[0, T], color=C_S, stroke_width=7)
        kFS = ParametricFunction(lambda u: ax.c2p(s_f(u), u, F_f(s_f(u))), t_range=[0, T], color=WHITE, stroke_width=6)

        # rechte Spalte (bildschirmfest): Formeln + kurze Erklärungen
        gl = MathTex(r"F(s) = D \cdot s", font_size=40, color=C_F)
        lab1 = de("Beispiel: Feder (D = 0,5 N/m)\nF hängt vom Ort s ab", 18, GREY_B)
        st = MathTex(r"s = s(t)", font_size=40, color=C_S)
        lab_st = de("Ort zur Zeit t –\nZeit ist die dritte Achse", 18, GREY_B)
        comp = MathTex(r"F = F\big(s(t)\big)", font_size=40)
        lab_c = de("Die Zeit verbindet\nF(s) und s(t)", 18, GREY_B)
        summe = MathTex(r"W \approx \sum_i F_i \cdot \Delta s_i", font_size=38)
        lab_sum = de("Weg in Streifen Δs\nzerlegen und addieren", 18, GREY_B)
        zaehler = MathTex(r"n = 4", font_size=40, color=C_P)
        col = VGroup(gl, lab1, st, lab_st, comp, lab_c, summe, lab_sum, zaehler).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        col.to_edge(RIGHT, buff=0.4).set_y(-0.35)
        lab_dt = de("Gleiche Δs ergeben\nungleiche Δt", 18, C_E).move_to(lab_sum).align_to(lab_sum, LEFT)
        self.fix(gl, lab1, st, lab_st, comp, lab_c, summe, lab_sum, zaehler, lab_dt)

        # ---- Hilfen: Spiegelung der Arbeit auf die Zeitachse (P-t-Wand bei s = 0)
        v_f = lambda t: 3 + 2 * np.sin(0.8 * t)
        P_f = lambda t: F_f(s_f(t)) * v_f(t)
        zlen = ax.c2p(0, 0, 12)[2] - ax.c2p(0, 0, 0)[2]       # Szenenlänge für F = 12 N
        ud = ax.c2p(0, 1, 0)[1] - ax.c2p(0, 0, 0)[1]          # Szenenlänge pro Sekunde
        uP = zlen / 40.0                                      # Szenenlänge pro Watt (P-Achse 0..40 W)

        def spiegel(n):
            """Streifen Fi*Δsi -> Rechteck P̄i*Δti (gleiche Fläche in Joule) über der Zeitachse."""
            dx = SMAX / n
            farben = color_gradient([C_S, C_W], n)
            out = VGroup()
            for i in range(n):
                x0 = i * dx
                h = F_f(x0)
                if h < 1e-3:
                    continue                                   # gleiche Auslassung wie in balken()
                t0, t1 = t_of_s(x0), t_of_s(min(x0 + dx, SMAX))
                dt = max(t1 - t0, 1e-6)
                Pm = h * dx / dt                               # mittlere Leistung im Streifen
                r = Prism(dimensions=[0.06, dt * ud, Pm * uP], fill_color=farben[i], fill_opacity=0.85, stroke_width=0)
                if n <= 40:
                    r.set_stroke(WHITE, 0.6)
                r.move_to(ax.c2p(0, (t0 + t1) / 2, 0) + np.array([0, 0, Pm * uP / 2]))
                out.add(r)
            return out

        pfuss = ax.c2p(0, T, 0)
        p_achse = VGroup(Line(pfuss, pfuss + np.array([0, 0, 40 * uP]), color=C_P, stroke_width=4))
        for w in (20, 40):
            q = pfuss + np.array([0, 0, w * uP])
            p_achse.add(Line(q, q + np.array([0, 0.15, 0]), color=C_P, stroke_width=3))
        p_lbl = VGroup(
            MathTex(r"P\;[\mathrm{W}]", color=C_P, font_size=34).move_to(pfuss + np.array([0, 0.2, 40 * uP + 0.55])),
            MathTex(r"20", color=C_P, font_size=26).move_to(pfuss + np.array([0, 0.55, 20 * uP])),
            MathTex(r"40", color=C_P, font_size=26).move_to(pfuss + np.array([0, 0.55, 40 * uP])),
        )
        self.add_fixed_orientation_mobjects(*p_lbl)
        self.remove(*p_lbl)
        p_kurve = ParametricFunction(lambda u: ax.c2p(0, u, 0) + np.array([0, 0, P_f(u) * uP]),
                                     t_range=[0, T], color=C_P, stroke_width=6)

        # Texte rechts (bildschirmfest) für die Spiegelung
        m1 = MathTex(r"F_i\,\Delta s_i = \bar P_i\,\Delta t_i", font_size=40)
        m1l = de("Gleiche Arbeit: der Streifen der F-s-Ebene\nwird zum Rechteck über der Zeitachse", 18, GREY_B)
        m2 = MathTex(r"\bar P_i = F_i \cdot \bar v_i", font_size=40, color=C_P)
        m2l = de("mit der mittleren Geschwindigkeit\n im Streifen: Δs / Δt", 18, GREY_B)
        mir = VGroup(m1, m1l, m2, m2l).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        mir.align_to(gl, UP).align_to(gl, LEFT)
        ml = MathTex(r"\int F\,\mathrm{d}s = \int P\,\mathrm{d}t", font_size=44, color=C_W)
        mll = de("n → ∞: dieselbe Arbeit, einmal über den Weg\nund einmal über die Zeit", 18, GREY_B)
        mlim = VGroup(ml, mll).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        mlim.align_to(gl, UP).align_to(gl, LEFT)
        self.fix(m1, m1l, m2, m2l, ml, mll)

        # ---- 1) Achsen, F(s) in der F-s-Ebene, s(t) in der s-t-Ebene
        self.play(Create(ax), FadeIn(lx), FadeIn(lt), FadeIn(lz))
        self.play(Create(kF), Write(gl), FadeIn(lab1))
        self.wait(1)
        self.play(Create(kS), Write(st), FadeIn(lab_st))
        self.wait(1)

        # ---- 2) Raumkurve (s(t), t, F(s(t))) mit Projektionen
        self.play(Create(kFS), Write(comp), FadeIn(lab_c), run_time=3)
        tr = ValueTracker(0.05)

        def werte():
            t = tr.get_value()
            return t, s_f(t), F_f(s_f(t))

        dot = always_redraw(lambda: Dot3D(ax.c2p(werte()[1], werte()[0], werte()[2]), color=WHITE, radius=0.09))
        auf_st = always_redraw(lambda: DashedLine(ax.c2p(werte()[1], werte()[0], werte()[2]),
                                                  ax.c2p(werte()[1], werte()[0], 0), color=C_S, stroke_width=3))
        auf_fs = always_redraw(lambda: DashedLine(ax.c2p(werte()[1], werte()[0], werte()[2]),
                                                  ax.c2p(werte()[1], 0, werte()[2]), color=C_F, stroke_width=3))
        self.add(dot, auf_st, auf_fs)
        self.play(tr.animate.set_value(T), run_time=6, rate_func=linear)
        self.wait(1)
        for m in (dot, auf_st, auf_fs):
            m.clear_updaters()
        self.play(FadeOut(dot), FadeOut(auf_st), FadeOut(auf_fs), FadeOut(kFS))

        # ---- 3) Summe: Streifen in der F-s-Ebene, Δs <-> Δt über die Zeitachse
        bars = self.balken(ax, 4, D, SMAX)
        self.play(Write(summe), FadeIn(lab_sum), FadeIn(zaehler),
                  LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), run_time=2)
        self.wait(1)

        n10 = self.balken(ax, 10, D, SMAX)
        z10 = MathTex(r"n = 10", font_size=40, color=C_P).move_to(zaehler).align_to(zaehler, LEFT)
        self.fix(z10)
        self.play(FadeOut(bars), FadeIn(n10), FadeOut(zaehler), FadeIn(z10), run_time=1.2)
        bars, zaehler = n10, z10

        conn = VGroup()
        for i in range(1, 11):
            si = i * SMAX / 10
            ti = t_of_s(si)
            conn.add(DashedLine(ax.c2p(si, 0, 0), ax.c2p(si, ti, 0), color=C_S, stroke_width=3))
            conn.add(DashedLine(ax.c2p(si, ti, 0), ax.c2p(0, ti, 0), color=C_E, stroke_width=3))
        self.play(FadeOut(lab_sum), FadeIn(lab_dt))
        self.play(LaggedStart(*[Create(c) for c in conn], lag_ratio=0.08), run_time=3.5)
        self.wait(2)

        # ---- 3b) Spiegelung auf die Zeitachse: Fi·Δsi = P̄i·Δti
        self.play(*[FadeOut(m) for m in (gl, lab1, st, lab_st, comp, lab_c, lab_dt, conn)], FadeIn(lab_sum))
        self.move_camera(phi=65 * DEGREES, theta=-40 * DEGREES, run_time=2)
        self.play(Create(p_achse), FadeIn(p_lbl))
        rects = spiegel(10)
        kopien = [b.copy() for b in bars]
        self.add(*kopien)
        self.play(LaggedStart(*[ReplacementTransform(c, r) for c, r in zip(kopien, rects)], lag_ratio=0.3),
                  FadeIn(mir), run_time=5)
        self.wait(3)
        self.play(FadeOut(rects), FadeOut(mir))

        for n in (25, 60):
            neu = self.balken(ax, n, D, SMAX)
            z2 = MathTex(rf"n = {n}", font_size=40, color=C_P).move_to(zaehler).align_to(zaehler, LEFT)
            self.fix(z2)
            self.play(FadeOut(bars), FadeIn(neu), FadeOut(zaehler), FadeIn(z2), run_time=1.2)
            bars, zaehler = neu, z2
            self.wait(0.4)

        rects60 = spiegel(60)
        self.play(LaggedStart(*[FadeIn(r) for r in rects60], lag_ratio=0.03), Create(p_kurve),
                  FadeIn(mlim), run_time=4)
        self.wait(2.5)

        # ---- 4) Kamerafahrt: alle drei Achsen sichtbar
        self.move_camera(phi=70 * DEGREES, theta=-25 * DEGREES, run_time=3)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()

        # ---- 5) Grenzwert: Integral
        i1 = MathTex(r"W = \int_0^{s} F\,\mathrm{d}x", font_size=46)
        i2 = MathTex(r"= \int_0^{s} D\,x\,\mathrm{d}x", font_size=46)
        i3 = MathTex(r"= \tfrac{1}{2}\, D\, s^2 = \tfrac{1}{2}\, F\, s", font_size=44, color=C_W)
        lab_i = de("Δs → 0: aus der Summe\nwird ein Integral", 18, GREY_B)
        res = VGroup(i1, i2, i3, lab_i).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        res.to_edge(RIGHT, buff=0.4).set_y(0.3)
        self.fix(i1, i2, i3, lab_i)
        self.play(FadeOut(summe), FadeOut(lab_sum), FadeOut(zaehler), FadeOut(mlim))
        self.play(Write(i1), FadeIn(lab_i))
        self.play(Write(i2))
        self.play(Write(i3))
        self.wait(3)
        self.aufraeumen()


# =====================================================================
# Szene 3: Arbeit über die Zeit (allgemeine Geschwindigkeit v(t))
# =====================================================================
class Szene3_Zeit(Basis):
    def construct(self):
        self.flach()
        T = 8.0
        v = lambda t: 3 + 2 * np.sin(0.8 * t)                 # immer > 0
        s = lambda t: 3 * t + 2.5 * (1 - np.cos(0.8 * t))     # Stammfunktion von v
        F = lambda x: 0.5 * x                                 # Beispiel: Feder, D = 0,5 N/m
        P = lambda t: F(s(t)) * v(t)

        def W_num(t):                                         # ∫ P dt numerisch
            t = max(t, 1e-3)
            ts = np.linspace(0, t, 300)
            mid = (ts[:-1] + ts[1:]) / 2
            return float(np.sum(P(mid)) * (t / 299))

        self.kapitel("3 · Arbeit über die Zeit")

        # ---- Phase A: v(t) -> Weg als Fläche
        axv = Axes(x_range=[0, 8, 2], y_range=[0, 6, 2], x_length=8.0, y_length=3.4,
                   tips=True, axis_config={"color": WHITE}).move_to(DOWN * 0.7)
        cv = axv.plot(v, x_range=[0, T], color=C_S, stroke_width=6)
        lx = MathTex(r"t\;[\mathrm{s}]", color=C_S, font_size=32).next_to(axv.x_axis.get_end(), DOWN, buff=0.2)
        ly = MathTex(r"v\;[\mathrm{m/s}]", color=C_F, font_size=32).next_to(axv.y_axis.get_end(), LEFT, buff=0.2)
        info = de("Beliebige Geschwindigkeit v(t) – hier immer vorwärts", 26, GREY_B)
        info.next_to(axv, UP, buff=0.25)
        tr = ValueTracker(0.02)
        flaeche = always_redraw(lambda: axv.get_area(
            cv, x_range=(0, max(tr.get_value(), 0.02)), color=C_S, opacity=0.5))
        punkt = always_redraw(lambda: Dot(axv.c2p(tr.get_value(), v(tr.get_value())), color=C_F, radius=0.1))
        lab = MathTex(r"s(t) = \int_0^{t} v\,\mathrm{d}\tau =", font_size=40)
        zahl = DecimalNumber(0, num_decimal_places=1, font_size=40, color=C_S)
        einheit = MathTex(r"\mathrm{m}", font_size=40)
        zahl.add_updater(lambda m: m.set_value(s(tr.get_value())).next_to(lab, RIGHT, buff=0.2))
        einheit.add_updater(lambda m: m.next_to(zahl, RIGHT, buff=0.15))
        lab.move_to(UP * 2.3 + LEFT * 0.5)

        self.play(Create(axv), FadeIn(lx), FadeIn(ly), FadeIn(info))
        self.play(Create(cv), Write(lab), FadeIn(zahl), FadeIn(einheit))
        self.add(flaeche, punkt)
        self.play(tr.animate.set_value(T), run_time=5, rate_func=linear)
        flab = de("Fläche unter v(t) = zurückgelegter Weg", 26, C_S).next_to(axv, DOWN, buff=0.5)
        self.play(Write(flab))
        self.wait(2)
        zahl.clear_updaters(); einheit.clear_updaters()
        flaeche.clear_updaters(); punkt.clear_updaters()
        self.play(*[FadeOut(m) for m in (axv, cv, lx, ly, info, flaeche, punkt, lab, zahl, einheit, flab)])

        # ---- Phase B: gleiche Arbeit, zwei Sichtweisen
        e1 = MathTex(r"\mathrm{d}s = v\,\mathrm{d}t", font_size=80, tex_to_color_map={"v": C_S})
        l1 = de("Wegelement = Geschwindigkeit · Zeitelement", 28, GREY_B)
        VGroup(e1, l1).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(e1)); self.play(FadeIn(l1)); self.wait(1.5)
        e2 = MathTex(r"W = \int F\,\mathrm{d}s = \int F \cdot v\,\mathrm{d}t = \int P\,\mathrm{d}t", font_size=52)
        e2.move_to(UP * 2.35)
        self.play(FadeOut(l1), ReplacementTransform(e1, e2))
        self.wait(1)

        axL = Axes(x_range=[0, 30, 10], y_range=[0, 16, 4], x_length=5.2, y_length=3.0,
                   tips=True, axis_config={"color": WHITE}).move_to(LEFT * 3.4 + DOWN * 0.45)
        axR = Axes(x_range=[0, 8, 2], y_range=[0, 45, 15], x_length=5.2, y_length=3.0,
                   tips=True, axis_config={"color": WHITE}).move_to(RIGHT * 3.4 + DOWN * 0.45)
        cL = axL.plot(F, x_range=[0, 30], color=C_F, stroke_width=6)
        cR = axR.plot(P, x_range=[0, T], color=C_P, stroke_width=6)
        tL = de("Sicht 1: nach dem Weg s", 24, C_F).next_to(axL, UP, buff=0.2)
        tR = de("Sicht 2: nach der Zeit t", 24, C_P).next_to(axR, UP, buff=0.2)
        lLx = MathTex(r"s\;[\mathrm{m}]", font_size=28).next_to(axL.x_axis.get_end(), DOWN, buff=0.15)
        lLy = MathTex(r"F\;[\mathrm{N}]", font_size=28).next_to(axL.y_axis.get_end(), LEFT, buff=0.15)
        lRx = MathTex(r"t\;[\mathrm{s}]", font_size=28).next_to(axR.x_axis.get_end(), DOWN, buff=0.15)
        lRy = MathTex(r"P\;[\mathrm{W}]", font_size=28).next_to(axR.y_axis.get_end(), LEFT, buff=0.15)
        bsp = de("Beispiel: F = 0,5 · s  (Feder)", 22, GREY_B).next_to(axL, DOWN, buff=0.75)

        self.play(Create(axL), Create(axR), FadeIn(tL), FadeIn(tR),
                  FadeIn(lLx), FadeIn(lLy), FadeIn(lRx), FadeIn(lRy))
        self.play(Create(cL), Create(cR), FadeIn(bsp))

        tr2 = ValueTracker(0.02)
        areaL = always_redraw(lambda: axL.get_area(
            cL, x_range=(0, max(s(tr2.get_value()), 0.05)), color=C_F, opacity=0.5))
        areaR = always_redraw(lambda: axR.get_area(
            cR, x_range=(0, max(tr2.get_value(), 0.02)), color=C_P, opacity=0.5))
        dotL = always_redraw(lambda: Dot(axL.c2p(s(tr2.get_value()), F(s(tr2.get_value()))), color=WHITE, radius=0.09))
        dotR = always_redraw(lambda: Dot(axR.c2p(tr2.get_value(), P(tr2.get_value())), color=WHITE, radius=0.09))

        def zaehler(fn, farbe, ax):
            a = MathTex(r"W =", font_size=38)
            z = DecimalNumber(0, num_decimal_places=1, font_size=38, color=farbe)
            u = MathTex(r"\mathrm{J}", font_size=38)
            z.add_updater(lambda m: m.set_value(fn(tr2.get_value())).next_to(a, RIGHT, buff=0.15))
            u.add_updater(lambda m: m.next_to(z, RIGHT, buff=0.12))
            a.move_to(ax.get_bottom() + DOWN * 0.45 + LEFT * 0.4)
            return a, z, u

        aL, zL, uL = zaehler(lambda t: 0.25 * s(t) ** 2, C_F, axL)
        aR, zR, uR = zaehler(W_num, C_P, axR)
        self.add(areaL, areaR, dotL, dotR)
        self.play(FadeIn(aL), FadeIn(zL), FadeIn(uL), FadeIn(aR), FadeIn(zR), FadeIn(uR))
        self.play(tr2.animate.set_value(T), run_time=8, rate_func=linear)
        self.wait(1)
        schluss = de("Gleiche Arbeit – einmal über den Weg, einmal über die Zeit", 28, C_W)
        schluss.to_edge(DOWN, buff=0.35)
        self.play(Write(schluss), Indicate(zL), Indicate(zR))
        self.wait(3)
        self.aufraeumen()


# =====================================================================
# Szene 4: Herleitung Beschleunigungsarbeit
# =====================================================================
class Szene4_Herleitungen(Basis):
    def construct(self):
        self.flach()
        self.kapitel("4 · Beschleunigungsarbeit")

        s1 = MathTex(r"W = F \cdot s", font_size=72)
        s2 = MathTex(r"W = m \cdot a \cdot s", font_size=72)
        s3 = MathTex(r"W = m \cdot a \cdot \tfrac{1}{2}\, a\, t^2", font_size=72)
        s4 = MathTex(r"W = \tfrac{1}{2}\, m\, (a\,t)^2", font_size=72)
        s5 = MathTex(r"W = \tfrac{1}{2}\, m\, v^2", font_size=84, color=C_W)
        gl = VGroup(MathTex(r"v = a \cdot t", font_size=46, color=C_S),
                    MathTex(r"s = \tfrac{1}{2}\, a\, t^2", font_size=46, color=C_S)).arrange(RIGHT, buff=1.2)
        gl.move_to(UP * 2.0)

        def hinweis(txt):
            return de(txt, 28, GREY_B).to_edge(DOWN, buff=1.0)

        self.play(Write(s1))
        h = hinweis("Ansatz: Arbeit = Kraft · Weg")
        self.play(FadeIn(h)); self.wait(1.5)
        self.play(TransformMatchingTex(s1, s2), Transform(h, hinweis("Newton: F = m · a")))
        self.wait(1.2)
        self.play(FadeIn(gl), Transform(h, hinweis("Gleichmäßig beschleunigt: v = a·t und s = ½·a·t²")))
        self.wait(1.5)
        self.play(TransformMatchingTex(s2, s3), Transform(h, hinweis("Weg s einsetzen")))
        self.wait(1.2)
        self.play(TransformMatchingTex(s3, s4), Transform(h, hinweis("Zusammenfassen")))
        self.wait(1.2)
        self.play(TransformMatchingTex(s4, s5), Transform(h, hinweis("Mit a · t = v")))
        box = SurroundingRectangle(s5, color=C_W, buff=0.3)
        self.play(Create(box), Transform(h, hinweis("Beschleunigungsarbeit = kinetische Energie")))
        self.wait(3)
        self.aufraeumen()


# =====================================================================
# Szene 5: Leistung
# =====================================================================
class Szene5_Leistung(Basis):
    def construct(self):
        self.flach()
        k = self.kapitel("5 · Leistung")
        d = definition_box([
            "Die Leistung P ist der Quotient aus der verrichteten",
            "Arbeit W und der dafür benötigten Zeit t.",
        ])
        f = MathTex(r"P = \frac{W}{t}", font_size=90, tex_to_color_map={"W": C_W, "P": C_P})
        e = MathTex(r"1\,\mathrm{W} = \frac{1\,\mathrm{J}}{1\,\mathrm{s}}", font_size=46, color=GREY_B)
        zeile = VGroup(f, e).arrange(RIGHT, buff=1.3)
        grp = VGroup(d, zeile).arrange(DOWN, buff=0.6).move_to(DOWN * 0.3)
        self.play(FadeIn(d, shift=UP * 0.3))
        self.play(Write(f), FadeIn(e))
        self.wait(2.5)
        self.play(FadeOut(grp))

        # Wettlauf (kurz): gleiche Arbeit, unterschiedliche Zeit
        bahnA = Line(LEFT * 3, RIGHT * 3)
        bahnB = Line(LEFT * 3, RIGHT * 3)
        la = VGroup(de("A", 30, C_P), MathTex(r"t = 10\,\mathrm{s}", font_size=36)).arrange(RIGHT, buff=0.3)
        lb = VGroup(de("B", 30, C_S), MathTex(r"t = 20\,\mathrm{s}", font_size=36)).arrange(RIGHT, buff=0.3)
        zA = VGroup(la, bahnA).arrange(RIGHT, buff=0.5)
        zB = VGroup(lb, bahnB).arrange(RIGHT, buff=0.5)
        gr = VGroup(zA, zB).arrange(DOWN, buff=1.5, aligned_edge=RIGHT).move_to(DOWN * 0.3)
        w = MathTex(r"W = 2000\,\mathrm{J}\ \text{für beide}", font_size=44, color=C_W).next_to(gr, UP, buff=0.5)
        a = Dot(bahnA.get_start(), color=C_P, radius=0.2)
        b = Dot(bahnB.get_start(), color=C_S, radius=0.2)
        pa = MathTex(r"P_A = \frac{2000\,\mathrm{J}}{10\,\mathrm{s}} = 200\,\mathrm{W}", font_size=38, color=C_P).next_to(bahnA, DOWN, buff=0.15)
        pb = MathTex(r"P_B = \frac{2000\,\mathrm{J}}{20\,\mathrm{s}} = 100\,\mathrm{W}", font_size=38, color=C_S).next_to(bahnB, DOWN, buff=0.15)
        self.play(Write(w), FadeIn(gr), FadeIn(a), FadeIn(b))
        self.play(MoveAlongPath(a, bahnA, rate_func=linear, run_time=1.5),
                  MoveAlongPath(b, bahnB, rate_func=linear, run_time=3.0))
        self.play(Write(pa), Write(pb))
        merke = de("Gleiche Arbeit in kürzerer Zeit → größere Leistung", 28, WHITE).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(merke))
        self.wait(2)
        self.play(*[FadeOut(m) for m in (w, gr, a, b, pa, pb, merke)])

        # P = F·v
        g1 = MathTex(r"P = \frac{W}{t}", font_size=72)
        g2 = MathTex(r"P = \frac{F \cdot s}{t}", font_size=72)
        g3 = MathTex(r"P = F \cdot \frac{s}{t}", font_size=72)
        g4 = MathTex(r"P = F \cdot v", font_size=90, color=C_P)
        rot = MathTex(r"P = M \cdot \omega", font_size=70, color=C_P)
        VGroup(g4, rot).arrange(DOWN, buff=0.9).move_to(DOWN * 0.2)
        for g in (g1, g2, g3):
            g.move_to(g4)

        def hinweis(txt):
            return de(txt, 28, GREY_B).to_edge(DOWN, buff=1.0)

        self.play(Write(g1))
        h = hinweis("Ausgangspunkt: Leistung = Arbeit pro Zeit")
        self.play(FadeIn(h)); self.wait(1)
        self.play(TransformMatchingTex(g1, g2), Transform(h, hinweis("Mit W = F · s"))); self.wait(1)
        self.play(TransformMatchingTex(g2, g3), Transform(h, hinweis("s durch t ist die Geschwindigkeit v"))); self.wait(1)
        self.play(TransformMatchingTex(g3, g4)); self.wait(0.5)
        self.play(Write(rot), Transform(h, hinweis("Bei Drehungen: Drehmoment M mal Winkelgeschwindigkeit ω")))
        self.wait(3)
        self.aufraeumen()


# =====================================================================
# Szene 6: Energie, Wirkungsgrad, Goldene Regel
# =====================================================================
class Szene6_Energie(Basis):
    def construct(self):
        self.flach()
        k = self.kapitel("6 · Energie und Wirkungsgrad")
        d = definition_box([
            "Energie ist die Fähigkeit eines Körpers, Arbeit zu",
            "verrichten – sie ist gespeicherte Arbeit.   [E] = J",
        ])
        self.unter(d, k, 0.45)
        self.play(FadeIn(d, shift=UP * 0.3))
        self.wait(1.5)

        paare = [
            ("Hubarbeit", r"E_{\mathrm{pot}} = m\,g\,h"),
            ("Beschleunigungsarbeit", r"E_{\mathrm{kin}} = \tfrac{1}{2}\,m\,v^2"),
            ("Spannarbeit", r"E_{\mathrm{Spann}} = \tfrac{1}{2}\,D\,s^2"),
            ("Rotationsarbeit", r"E_{\mathrm{rot}} = \tfrac{1}{2}\,J\,\omega^2"),
        ]
        zellen = VGroup()
        for name, fm in paare:
            zellen.add(VGroup(de(name, 24, C_W), MathTex(fm, font_size=38, color=C_E)).arrange(DOWN, buff=0.15))
        zellen.arrange_in_grid(rows=2, cols=2, buff=(1.6, 0.6))
        self.unter(zellen, d, 0.6)
        self.play(LaggedStart(*[FadeIn(z, shift=RIGHT * 0.3) for z in zellen], lag_ratio=0.35))
        gesamt = MathTex(r"E_{\mathrm{kin,ges}} = \tfrac{1}{2}\,m\,v^2 + \tfrac{1}{2}\,J\,\omega^2", font_size=44)
        gesamt.to_edge(DOWN, buff=0.5)
        self.play(Write(gesamt))
        self.wait(3)
        self.play(FadeOut(VGroup(d, zellen, gesamt)))

        # Wirkungsgrad
        d2 = definition_box([
            "Der Wirkungsgrad η ist das Verhältnis aus abgegebener",
            "Arbeit W_out und aufgenommener Arbeit W_in.",
        ])
        self.unter(d2, k, 0.4)
        self.play(FadeIn(d2))
        self.wait(1.5)

        eta = ValueTracker(0.6)
        breite = 6.0
        w_in = Rectangle(width=breite, height=0.7, color=WHITE, fill_color=C_E, fill_opacity=0.85).shift(DOWN * 0.5 + LEFT * 0.8)
        out = always_redraw(lambda: Rectangle(width=max(breite * eta.get_value(), 0.001), height=0.7, color=WHITE,
                                              fill_color=C_W, fill_opacity=0.9).align_to(w_in, LEFT).shift(DOWN * 1.8))
        verlust = always_redraw(lambda: Rectangle(width=max(breite * (1 - eta.get_value()), 0.001), height=0.7, color=WHITE,
                                                  fill_color=C_P, fill_opacity=0.9).next_to(out, RIGHT, buff=0))
        lab_in = MathTex(r"W_{\mathrm{in}}", font_size=40).next_to(w_in, LEFT, buff=0.4)
        lab_out = MathTex(r"W_{\mathrm{out}}", font_size=40, color=C_W).next_to(lab_in, DOWN, buff=1.05)
        lab_v = MathTex(r"W_{\mathrm{Reib}}", font_size=36, color=C_P)
        lab_v.add_updater(lambda m: m.next_to(verlust, DOWN, buff=0.2))
        formel = MathTex(r"\eta = \frac{W_{\mathrm{out}}}{W_{\mathrm{in}}}", font_size=60).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.5)
        wert = DecimalNumber(0.6, num_decimal_places=2, font_size=54, color=C_W)
        wert.add_updater(lambda m: m.set_value(eta.get_value()).next_to(formel, DOWN, buff=0.4))
        self.play(FadeIn(w_in), FadeIn(out), FadeIn(verlust), FadeIn(lab_in), FadeIn(lab_out), FadeIn(lab_v),
                  Write(formel), FadeIn(wert))
        self.play(eta.animate.set_value(0.9), run_time=1.8)
        self.play(eta.animate.set_value(0.4), run_time=1.8)
        self.play(eta.animate.set_value(1.0), run_time=1.8)
        gr = MathTex(r"W_{\mathrm{in}} = W_{\mathrm{out}} + W_{\mathrm{Reib}},\qquad 0 < \eta \leq 1",
                     font_size=40, color=GREY_B).to_edge(DOWN, buff=0.5)
        self.play(Write(gr))
        self.wait(3)
        self.play(*[FadeOut(m) for m in (d2, w_in, out, verlust, lab_in, lab_out, lab_v, formel, wert, gr)])

        # Goldene Regel + Hebelgesetz
        gr1 = MathTex(r"F_1 \cdot \Delta s_1 = F_2 \cdot \Delta s_2", font_size=70)
        gr2 = MathTex(r"W_1 = W_2", font_size=70, color=C_W)
        VGroup(gr1, gr2).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        txt = de("Goldene Regel: Kraftwandler ändern Kraft und Weg – nicht die Arbeit (ohne Reibung).", 26, GREY_B)
        txt.to_edge(DOWN, buff=1.0)
        self.play(Write(gr1)); self.play(Write(gr2)); self.play(FadeIn(txt))
        self.wait(2.5)
        self.play(FadeOut(VGroup(gr1, gr2, txt)))

        hebel = Line(LEFT * 4, RIGHT * 4, color=WHITE, stroke_width=8).shift(DOWN * 0.3)
        dp = hebel.point_from_proportion(0.17)
        drehpunkt = Triangle(color=C_F, fill_opacity=1).scale(0.3).move_to(dp + DOWN * 0.3)
        last = Square(0.8, color=C_P, fill_opacity=0.9).next_to(hebel.get_start(), UP, buff=0)
        pfeil = Arrow(hebel.get_end() + UP * 1.4, hebel.get_end(), color=C_F, buff=0, stroke_width=8)
        l1 = BraceBetweenPoints(hebel.get_start() + DOWN * 0.7, dp + DOWN * 0.7, direction=DOWN, color=C_P)
        l2 = BraceBetweenPoints(dp + DOWN * 0.7, hebel.get_end() + DOWN * 0.7, direction=DOWN, color=C_F)
        l1t = MathTex(r"l_1", color=C_P).next_to(l1, DOWN, buff=0.1)
        l2t = MathTex(r"l_2", color=C_F).next_to(l2, DOWN, buff=0.1)
        f1t = MathTex(r"F_1", color=C_P).next_to(last, UP, buff=0.1)
        f2t = MathTex(r"F_2", color=C_F).next_to(pfeil, UP, buff=0.1)
        hg = MathTex(r"F_1 \cdot l_1 = F_2 \cdot l_2", font_size=64).to_edge(UP, buff=1.5)
        hg_t = de("Hebelgesetz: Last · Lastarm = Kraft · Kraftarm", 28, GREY_B).next_to(hg, DOWN, buff=0.3)
        self.play(Create(hebel), FadeIn(drehpunkt), FadeIn(last), GrowArrow(pfeil))
        self.play(Write(l1t), Write(l2t), Create(l1), Create(l2), Write(f1t), Write(f2t))
        self.play(Write(hg), FadeIn(hg_t))
        self.wait(3)
        self.aufraeumen()


# =====================================================================
# Zusammenfassung
# =====================================================================
class Zusammenfassung(Basis):
    def construct(self):
        self.flach()
        t = de("Das Wichtigste", 44, WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(t))
        daten = [
            ("ARBEIT", r"W = F \cdot s = \int F\,\mathrm{d}s", C_W),
            ("LEISTUNG", r"P = \frac{W}{t} = F \cdot v", C_P),
            ("ENERGIE", r"E = \text{gespeicherte Arbeit}", C_E),
            ("WIRKUNGSGRAD", r"\eta = \frac{W_{\mathrm{out}}}{W_{\mathrm{in}}}", C_F),
        ]
        karten = []
        for name, f, col in daten:
            inhalt = VGroup(de(name, 22, col, weight=BOLD), MathTex(f, font_size=42)).arrange(DOWN, buff=0.3)
            box = SurroundingRectangle(inhalt, color=col, buff=0.35, corner_radius=0.15)
            box.set_fill(col, opacity=0.08)
            karten.append(VGroup(box, inhalt))
        gruppe = VGroup(*karten).arrange_in_grid(rows=2, cols=2, buff=0.6)
        self.unter(gruppe, t, 0.7)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.3) for k in karten], lag_ratio=0.3))
        merke = de("Merke: Bei gleicher Arbeit gilt – je kürzer die Zeit, desto größer die Leistung.", 28)
        merke.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(merke))
        self.wait(4)
        self.aufraeumen()


# =====================================================================
# Gesamtvideo
# =====================================================================
class Gesamt(Basis):
    """Spielt alle Szenen nacheinander ab (ein einziges Video)."""

    def construct(self):
        for S in (Szene0_Titel, Szene1_Arbeit, Szene2_Integral3D, Szene3_Zeit,
                  Szene4_Herleitungen, Szene5_Leistung, Szene6_Energie, Zusammenfassung):
            S.construct(self)
            self.flach()
