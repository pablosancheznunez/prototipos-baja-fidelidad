"""Genera las figuras del libro (SVG) en figuras/ y las plantillas para dibujar
esquemas en papel (plantillas/plantillas_esquemas.pdf).

Uso, desde la raíz del libro:   python3 herramientas/figuras.py
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
Los datos de las figuras 4 y 9 se calculan con las mismas fórmulas que UxLearn.
"""
import math, pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": GRIS, "axes.labelcolor": TINTA2, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc, linespacing=1.15, fontweight=peso)


def flecha(ax, a, b, texto=None, desp=(0, 0), color=TINTA2, rad=0.0, fs=8.5):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=color, lw=1.1,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if texto:
        mx, my = (a[0] + b[0]) / 2 + desp[0], (a[1] + b[1]) / 2 + desp[1]
        ax.text(mx, my, texto, ha="center", va="center", fontsize=fs, color=TINTA2,
                bbox=dict(fc=SUP, ec="none", pad=1))


def wald_ajustado(x, n, z=1.959964):
    na = n + z ** 2; pa = (x + z ** 2 / 2) / na; m = z * math.sqrt(pa * (1 - pa) / na)
    return x / n, max(0, pa - m), min(1, pa + m)


# ------------------------------------------------------------------ Tema 1
def tema1():
    dims = ["Apariencia", "Datos", "Funcionalidad", "Interactividad", "Estructura espacial"]
    arts = ["Boceto en papel", "Esquema digital\ncon textos reales", "Prototipo de\nalta fidelidad"]
    nivel = [[1, 1, 1, 1, 2], [1, 3, 1, 2, 3], [3, 2, 2, 3, 3]]
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    for j, a in enumerate(arts):
        ax.text(1.9 + j * 1.6, 5.55, a, ha="center", va="center", fontsize=10, color=TINTA, linespacing=1.1)
    for i, d in enumerate(dims):
        y = 4.6 - i
        ax.text(0.0, y, d, ha="left", va="center", fontsize=10, color=TINTA2)
        ax.plot([0, 6.4], [y - 0.5, y - 0.5], color="#ecebe8", lw=0.8)
        for j in range(3):
            for k in range(3):
                lleno = k < nivel[j][i]
                ax.plot(1.65 + j * 1.6 + k * 0.25, y, 'o', ms=8, mfc=S[0] if lleno else SUP, mec=S[0], mew=1.2)
    ax.text(0, -0.25, "● alta fidelidad en esa dimensión   ○ baja", fontsize=8.5, color=TINTA2)
    ax.set_xlim(-0.05, 6.5); ax.set_ylim(-0.5, 6.0); ax.axis("off")
    guardar(fig, "tema1_fidelidad.svg")


# ------------------------------------------------------------------ Tema 2
def tema2():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.add_patch(Rectangle((0, 0), 10, 8, fc=SUP, ec=GRIS, lw=1))
    ax.plot([5, 5], [0, 8], color=GRIS, lw=1); ax.plot([0, 10], [4, 4], color=GRIS, lw=1)
    ax.text(5, 8.35, "Actitudinal (lo que dicen)", ha="center", fontsize=10, color=TINTA2)
    ax.text(5, -0.45, "Comportamental (lo que hacen)", ha="center", va="top", fontsize=10, color=TINTA2)
    ax.text(-0.25, 4, "Cualitativo\n(por qué, cómo)", ha="right", va="center", fontsize=10, color=TINTA2)
    ax.text(10.25, 4, "Cuantitativo\n(cuánto)", ha="left", va="center", fontsize=10, color=TINTA2)
    pts = [(1.4, 6.6, "Entrevistas", 0), (3.4, 5.4, "Grupos de discusión", 0), (7.6, 6.6, "Encuestas", 1),
           (1.6, 2.3, "Observación\ncontextual", 2), (3.4, 1.2, "Pruebas de\nusabilidad", 2),
           (7.2, 2.6, "Analítica web", 3), (8.6, 1.2, "Pruebas A/B", 3)]
    for x, y, t, c in pts:
        ax.add_patch(Circle((x, y), 0.17, fc=S[c], ec=SUP, lw=1.5))
        ax.text(x + 0.3, y, t, va="center", fontsize=9.5, color=TINTA, linespacing=1.1)
    caja(ax, 10.6, 5.6, 3.3, 1.9, "Inspección sin usuarios:\nrevisión heurística,\nanálisis de la competencia", fs=9)
    ax.set_xlim(-2.4, 14.1); ax.set_ylim(-1.1, 8.8); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema2_metodos.svg")


# ------------------------------------------------------------------ Tema 4
def tema4():
    ns = [5, 10, 20, 40, 80]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    for i, n in enumerate(ns):
        p, lo, hi = wald_ajustado(0.8 * n, n)
        ax.plot([i, i], [lo * 100, hi * 100], color=S[0], lw=2, solid_capstyle="round")
        ax.plot(i, p * 100, 'o', ms=8, mfc=S[0], mec=SUP, mew=1.5, zorder=3)
        ax.text(i + 0.14, hi * 100, f"{hi * 100:.0f} %", fontsize=8.5, color=TINTA2, va="center")
        ax.text(i + 0.14, lo * 100, f"{lo * 100:.0f} %", fontsize=8.5, color=TINTA2, va="center")
    ax.axhline(80, color=GRIS, lw=0.8, ls="--", zorder=0)
    ax.set_xticks(range(len(ns))); ax.set_xticklabels([f"{n}" for n in ns])
    ax.set_xlabel("Participantes en la prueba"); ax.set_ylabel("Tasa de éxito (%)")
    ax.set_ylim(25, 105); ax.set_xlim(-0.4, 4.7)
    ax.grid(axis="y", color="#ecebe8", lw=0.8); ax.set_axisbelow(True)
    guardar(fig, "tema4_intervalos.svg")


# ------------------------------------------------------------------ Tema 5
def rombo(ax, cx, cy, w, h, texto):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], fc="#fff4e5", ec=S[3], lw=1.2))
    ax.text(cx, cy, texto, ha="center", va="center", fontsize=8.8, color=TINTA, linespacing=1.1)


def tema5():
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    def ovalo(x, y, t):
        ax.add_patch(FancyBboxPatch((x - 0.6, y - 0.3), 1.2, 0.6, boxstyle="round,pad=0,rounding_size=0.3", fc=TINTA, ec=TINTA))
        ax.text(x, y, t, ha="center", va="center", color=SUP, fontsize=9)
    W, H = 1.9, 0.75
    ovalo(0.7, 3.6, "Inicio")
    caja(ax, 1.8, 3.6 - H / 2, W, H, "Elegir fecha\ny franja", fs=9)
    caja(ax, 4.3, 3.6 - H / 2, W, H, "Lista de salas\nlibres", fs=9)
    caja(ax, 6.8, 3.6 - H / 2, W, H, "Elegir sala", fs=9)
    rombo(ax, 9.9, 3.6, 2.0, 1.15, "¿Sesión\niniciada?")
    caja(ax, 9.0, 1.65, W, H, "Iniciar sesión", fs=9, fc="#eaf5ef", ec="#9fd8bf")
    caja(ax, 11.6, 3.6 - H / 2, W, H, "Confirmar\nreserva", fs=9)
    rombo(ax, 12.55, 1.9, 2.0, 1.15, "¿Sigue\nlibre?")
    caja(ax, 6.6, 0.05, 3.0, 1.05, "Error: «La sala se ha\nocupado». Se conserva\nla fecha elegida", fs=8.5, fc="#fdece6", ec="#f3b39b")
    caja(ax, 13.9, 0.2, W, H, "Reserva\nconfirmada", fs=9)
    ovalo(15.1, 1.9, "Fin")
    flecha(ax, (1.3, 3.6), (1.8, 3.6)); flecha(ax, (3.7, 3.6), (4.3, 3.6)); flecha(ax, (6.2, 3.6), (6.8, 3.6))
    flecha(ax, (8.7, 3.6), (8.9, 3.6))
    flecha(ax, (10.9, 3.6), (11.6, 3.6), "sí", (0, 0.2))
    flecha(ax, (9.9, 3.02), (9.9, 2.4), "no", (0.22, 0))
    flecha(ax, (10.9, 2.0), (11.6, 3.25), None, rad=-0.3)
    flecha(ax, (12.55, 3.22), (12.55, 2.48))
    flecha(ax, (11.55, 1.9), (9.6, 0.75), "no", (0.15, 0.25))
    flecha(ax, (6.6, 0.6), (5.25, 3.22), None, rad=-0.25)
    flecha(ax, (13.55, 1.9), (14.4, 0.95), "sí", (0.2, 0.15))
    flecha(ax, (14.85, 0.95), (15.05, 1.6))
    ax.text(4.55, 1.45, "vuelve a la lista", fontsize=8.5, color=TINTA2, ha="center")
    ax.set_xlim(0, 15.9); ax.set_ylim(-0.2, 4.3); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema5_flujo.svg")


# ------------------------------------------------------------------ Tema 6
def persona(ax, x, y, s=1.0, cara="neutral"):
    ax.add_patch(Circle((x, y + 1.25 * s), 0.28 * s, fc=SUP, ec=TINTA, lw=1.3))
    ax.plot([x, x], [y + 0.97 * s, y + 0.35 * s], color=TINTA, lw=1.3)
    ax.plot([x - 0.35 * s, x, x + 0.35 * s], [y + 0.55 * s, y + 0.8 * s, y + 0.55 * s], color=TINTA, lw=1.3)
    ax.plot([x - 0.25 * s, x, x + 0.25 * s], [y, y + 0.35 * s, y], color=TINTA, lw=1.3)
    if cara == "feliz":
        t = [i / 10 for i in range(11)]
        ax.plot([x - 0.12 * s + 0.24 * s * u for u in t], [y + 1.18 * s - 0.06 * s * math.sin(math.pi * u) for u in t], color=TINTA, lw=1)
    elif cara == "preocupada":
        t = [i / 10 for i in range(11)]
        ax.plot([x - 0.12 * s + 0.24 * s * u for u in t], [y + 1.12 * s + 0.05 * s * math.sin(math.pi * u) for u in t], color=TINTA, lw=1)
    else:
        ax.plot([x - 0.1 * s, x + 0.1 * s], [y + 1.15 * s, y + 1.15 * s], color=TINTA, lw=1)


def tema6():
    fig, axs = plt.subplots(1, 4, figsize=(10, 3.2))
    textos = ["1. Mañana tiene examen.\n¿Habrá sitio en la biblioteca?", "2. Lo consulta en el móvil\ndesde casa",
              "3. Momento clave:\n«12 puestos libres»", "4. Llega y encuentra sitio"]
    for i, ax in enumerate(axs):
        ax.add_patch(Rectangle((0, 0), 4, 3, fc=SUP, ec=TINTA2, lw=1.2))
        ax.text(2, -0.35, textos[i], ha="center", va="top", fontsize=8.8, color=TINTA, linespacing=1.15)
        ax.set_xlim(-0.1, 4.1); ax.set_ylim(-1.2, 3.1); ax.set_aspect("equal"); ax.axis("off")
    a = axs[0]; persona(a, 1.3, 0.4, 1.0, "preocupada")
    a.add_patch(FancyBboxPatch((2.2, 1.9), 1.5, 0.7, boxstyle="round,pad=0.05,rounding_size=0.2", fc=SUP, ec=TINTA2, lw=1))
    a.text(2.95, 2.25, "¿sitio?", ha="center", va="center", fontsize=9, color=TINTA)
    a.add_patch(Circle((2.05, 1.75), 0.06, fc=SUP, ec=TINTA2)); a.add_patch(Circle((1.85, 1.6), 0.04, fc=SUP, ec=TINTA2))
    a = axs[1]; persona(a, 1.2, 0.4, 1.0)
    a.add_patch(Rectangle((1.9, 0.9), 0.55, 0.95, fc=SUP, ec=TINTA, lw=1.2))
    a.plot([1.55, 1.9], [1.2, 1.3], color=TINTA, lw=1.3)
    a = axs[2]
    a.add_patch(FancyBboxPatch((1.2, 0.25), 1.6, 2.5, boxstyle="round,pad=0,rounding_size=0.15", fc=SUP, ec=TINTA, lw=1.4))
    a.add_patch(Rectangle((1.4, 1.95), 1.2, 0.18, fc=CAJA2, ec="none"))
    a.text(2.0, 1.4, "12", ha="center", va="center", fontsize=22, color=S[0], fontweight="bold")
    a.text(2.0, 0.85, "puestos libres", ha="center", va="center", fontsize=8, color=TINTA2)
    a = axs[3]; persona(a, 1.0, 0.5, 1.0, "feliz")
    a.add_patch(Rectangle((1.6, 0.9), 1.9, 0.12, fc=TINTA2, ec="none"))
    a.plot([1.8, 1.8], [0.2, 0.9], color=TINTA2, lw=1.3); a.plot([3.3, 3.3], [0.2, 0.9], color=TINTA2, lw=1.3)
    for k in range(4):
        a.add_patch(Rectangle((2.7 + k * 0.18, 1.02), 0.13, 0.45 + 0.08 * (k % 2), fc=[S[0], S[1], S[2], S[3]][k], ec="none"))
    fig.subplots_adjust(wspace=0.08)
    guardar(fig, "tema6_storyboard.svg")


# ------------------------------------------------------------------ Tema 7
def tema7():
    ancho, cols, med, marg = 1440, 12, 24, 80
    col = (ancho - 2 * marg - (cols - 1) * med) / cols
    x0 = lambda i: marg + i * (col + med)
    fig, ax = plt.subplots(figsize=(9.2, 6.0))
    ax.add_patch(Rectangle((0, 0), ancho, 940, fc=SUP, ec=TINTA2, lw=1.5))
    for i in range(cols):
        ax.add_patch(Rectangle((x0(i), 0), col, 940, fc="#e9f1fb", ec="none", alpha=0.7))
    # cabecera
    ax.add_patch(Rectangle((x0(0), 860), x0(2) + col - x0(0), 50, fc=CAJA2, ec=TINTA2))
    ax.text(x0(0) + 10, 885, "Logotipo", va="center", fontsize=9, color=TINTA)
    for k, t in enumerate(["Catálogo", "Salas", "Actividades", "Mi cuenta", "Ayuda"]):
        ax.text(x0(4) + k * 1.6 * (col + med) + col / 2, 885, t, va="center", ha="center", fontsize=8, color=TINTA)
    # buscador
    ax.add_patch(Rectangle((x0(1), 750), x0(9) + col - x0(1), 60, fc=SUP, ec=TINTA2, lw=1.3))
    ax.text(x0(1) + 15, 780, "Buscar en el catálogo…", va="center", fontsize=9.5, color=TINTA2)
    ax.add_patch(Rectangle((x0(10), 750), x0(10) + col - x0(10) + col + med, 60, fc=TINTA, ec=TINTA))
    ax.text(x0(10) + (2 * col + med) / 2, 780, "Buscar", ha="center", va="center", fontsize=10, color=SUP, fontweight="bold")
    # contenido 8 columnas
    xc, wc = x0(0), x0(7) + col - x0(0)
    ax.add_patch(Rectangle((xc, 640), wc * 0.6, 34, fc=TINTA2, ec="none"))
    for k in range(5):
        ax.add_patch(Rectangle((xc, 590 - k * 26), wc * (0.95 if k < 4 else 0.6), 8, fc=GRIS, ec="none"))
    ax.add_patch(Rectangle((xc, 150), wc, 280, fc=SUP, ec=TINTA2))
    ax.plot([xc, xc + wc], [150, 430], color=TINTA2, lw=0.8); ax.plot([xc, xc + wc], [430, 150], color=TINTA2, lw=0.8)
    # lateral 4 columnas
    xl, wl = x0(8), x0(11) + col - x0(8)
    for k in range(3):
        ax.add_patch(Rectangle((xl, 520 - k * 170), wl, 140, fc=CAJA, ec=CAJA2))
        ax.add_patch(Rectangle((xl + 15, 620 - k * 170), wl * 0.5, 14, fc=TINTA2, ec="none"))
        for j in range(3):
            ax.add_patch(Rectangle((xl + 15, 590 - k * 170 - j * 22), wl * 0.8, 7, fc=GRIS, ec="none"))
    # pie
    ax.add_patch(Rectangle((x0(0), 30), x0(11) + col - x0(0), 70, fc=CAJA, ec=CAJA2))
    ax.text(x0(0) + 10, 65, "Pie: dirección, horario, accesibilidad, aviso legal", va="center", fontsize=9, color=TINTA)
    # rótulos
    def rotulo(x, y, t):
        ax.annotate(t, xy=(x, y), xytext=(ancho + 60, y), fontsize=9.5, color=TINTA, va="center",
                    arrowprops=dict(arrowstyle="-", color=TINTA2, lw=0.8))
    rotulo(ancho - 10, 885, "Cabecera y navegación")
    rotulo(ancho - 10, 780, "Acción principal")
    rotulo(xl + wl, 450, "Lateral: 4 columnas")
    rotulo(ancho - 10, 65, "Pie")
    ax.annotate("Contenido: 8 columnas", xy=(xc + wc / 2, 140), xytext=(xc + wc / 2, -60), ha="center", fontsize=9.5,
                color=TINTA, arrowprops=dict(arrowstyle="-", color=TINTA2, lw=0.8))
    ax.text(0, 965, "Rejilla de 12 columnas · medianil 24 px · margen 80 px · columna 84,7 px", fontsize=9, color=TINTA2)
    ax.set_xlim(-10, ancho + 420); ax.set_ylim(-110, 990); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema7_anatomia.svg")


# ------------------------------------------------------------------ Tema 8
def tema8():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    est = {"Reposo": (2.6, 2.6), "Cargando": (6.0, 2.6), "Confirmado": (9.6, 3.6), "Error": (9.6, 1.4), "Desactivado": (2.6, 0.5)}
    W, H = 2.0, 0.8
    for k, (x, y) in est.items():
        fc = {"Error": "#fdece6", "Confirmado": "#eaf5ef", "Desactivado": "#f2f2f0"}.get(k, CAJA)
        ec = {"Error": "#f3b39b", "Confirmado": "#9fd8bf", "Desactivado": GRIS}.get(k, CAJA2)
        caja(ax, x - W / 2, y - H / 2, W, H, k, fc=fc, ec=ec, fs=10, peso="bold")
    ax.add_patch(Circle((0.6, 2.6), 0.12, fc=TINTA)); flecha(ax, (0.72, 2.6), (1.6, 2.6))
    flecha(ax, (3.6, 2.6), (5.0, 2.6), "pulsar", (0, 0.2))
    flecha(ax, (7.0, 2.8), (8.6, 3.5), "reserva correcta", (-0.3, 0.32))
    flecha(ax, (7.0, 2.4), (8.6, 1.5), "sala ocupada", (-0.25, -0.3))
    flecha(ax, (8.6, 1.2), (3.2, 2.2), "elegir otra sala", (0, -0.5), rad=-0.15)
    flecha(ax, (2.3, 2.2), (2.3, 0.9), "sin sala elegida", (-0.95, 0))
    flecha(ax, (2.9, 0.9), (2.9, 2.2), "elegir sala", (0.62, 0))
    ax.add_patch(FancyArrowPatch((5.6, 3.0), (6.4, 3.0), connectionstyle="arc3,rad=-1.6", arrowstyle="-|>",
                                 mutation_scale=10, color=TINTA2, lw=1))
    ax.text(6.0, 3.85, "pulsar otra vez: se ignora", ha="center", fontsize=8.5, color=TINTA2)
    ax.set_xlim(0.3, 10.8); ax.set_ylim(-0.1, 4.3); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema8_estados.svg")


# ------------------------------------------------------------------ Tema 9
def tema9():
    datos = {"Buscar un libro": (6, 8), "Renovar un préstamo": (5, 7), "Reservar una sala": (3, 5)}
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    for i, (t, (pap, dig)) in enumerate(datos.items()):
        for k, (x, nombre, c) in enumerate([(pap, "Papel", S[0]), (dig, "Digital", S[1])]):
            p, lo, hi = wald_ajustado(x, 8)
            y = i + (0.15 if k == 0 else -0.15)
            ax.plot([lo * 100, hi * 100], [y, y], color=c, lw=2, solid_capstyle="round")
            ax.plot(p * 100, y, "o", ms=7, mfc=c, mec=SUP, mew=1.3, zorder=4)
            ax.text(hi * 100 + 1.5, y, f"{x}/8", va="center", fontsize=8.5, color=TINTA2)
    ax.set_yticks(range(3)); ax.set_yticklabels(list(datos)); ax.invert_yaxis()
    ax.set_xlim(0, 108); ax.set_xlabel("Tasa de éxito (%) con intervalo al 95 %")
    ax.grid(axis="x", color="#ecebe8", lw=0.8); ax.set_axisbelow(True)
    ax.plot([], [], "o-", color=S[0], label="Prototipo en papel"); ax.plot([], [], "o-", color=S[1], label="Prototipo digital")
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=9)
    guardar(fig, "tema9_exito.svg")


# ------------------------------------------------------------------ Tema 12
def simular(hexc, tipo):
    M = {"protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
         "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]}[tipo]
    rgb = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    sim = [min(max(sum(M[r][k] * lin[k] for k in range(3)), 0), 1) for r in range(3)]
    srgb = [12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055 for c in sim]
    return "#" + "".join(f"{round(c * 255):02x}" for c in srgb)


def tema12():
    pal = [("Primario", "#1a73e8"), ("Acento", "#f29900"), ("Éxito", "#188038"), ("Error", "#d93025")]
    filas = [("Visión típica", None), ("Protanopía", "protan"), ("Deuteranopía", "deutan")]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    for i, (nombre, tipo) in enumerate(filas):
        y = 2 - i
        ax.text(-0.15, y + 0.35, nombre, ha="right", va="center", fontsize=10, color=TINTA)
        for j, (et, c) in enumerate(pal):
            col = c if tipo is None else simular(c, tipo)
            ax.add_patch(FancyBboxPatch((j * 1.25, y), 1.05, 0.7, boxstyle="round,pad=0,rounding_size=0.08", fc=col, ec=SUP, lw=2))
            if i == 0:
                ax.text(j * 1.25 + 0.525, 2.95, et, ha="center", fontsize=9.5, color=TINTA2)
    ax.plot([2.5, 4.8], [-0.12, -0.12], color=TINTA2, lw=0.8)
    ax.text(3.65, -0.3, "éxito y error, casi iguales", ha="center", va="top", fontsize=9, color=TINTA)
    ax.set_xlim(-1.9, 5.0); ax.set_ylim(-0.7, 3.2); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema12_daltonismo.svg")


# ------------------------------------------------------------------ Plantillas en papel
def plantillas_pdf():
    destino = RAIZ / "plantillas" / "plantillas_esquemas.pdf"
    A4 = (8.27, 11.69)
    with PdfPages(destino) as pdf:
        def puntos(ax, x0, y0, w, h, paso):
            xs = [x0 + paso * i for i in range(int(w / paso) + 1)]
            ys = [y0 + paso * j for j in range(int(h / paso) + 1)]
            ax.scatter([x for x in xs for _ in ys], [y for _ in xs for y in ys], s=0.6, c="#b9b9b9", linewidths=0)

        def pie(fig, t):
            fig.text(0.5, 0.025, t + " · Esquemas de página y prototipos de baja fidelidad · CC BY 4.0", ha="center", fontsize=7, color=TINTA2)

        # 1. Tres móviles
        fig = plt.figure(figsize=A4); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 210); ax.set_ylim(0, 297); ax.axis("off")
        ax.text(15, 282, "Pantallas de móvil", fontsize=13, color=TINTA, fontweight="bold")
        ax.text(15, 275, "Proyecto: ____________________   Flujo: ____________________   Versión: ____", fontsize=8.5, color=TINTA2)
        for i in range(3):
            x = 12 + i * 64; w, h = 58, 118
            for fila in range(2):
                y = 140 - fila * 128
                ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=6", fc=SUP, ec=TINTA, lw=1.2))
                puntos(ax, x + 3, y + 6, w - 6, h - 12, 4)
                ax.text(x, y + h + 2.5, f"Pantalla {fila * 3 + i + 1}: ________________", fontsize=7, color=TINTA2)
        pie(fig, "Rejilla de puntos de 4 mm"); pdf.savefig(fig); plt.close(fig)

        # 2. Escritorio
        fig = plt.figure(figsize=(A4[1], A4[0])); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 297); ax.set_ylim(0, 210); ax.axis("off")
        ax.text(15, 196, "Pantalla de escritorio (12 columnas)", fontsize=13, color=TINTA, fontweight="bold")
        ax.text(15, 189, "Proyecto: ____________________   Pantalla: ____________________   Versión: ____", fontsize=8.5, color=TINTA2)
        x0, y0, w, h = 15, 22, 267, 160
        ax.add_patch(Rectangle((x0, y0), w, h, fc=SUP, ec=TINTA, lw=1.2))
        ax.add_patch(Rectangle((x0, y0 + h - 8), w, 8, fc="#f2f2f0", ec=TINTA, lw=1))
        for k in range(3):
            ax.add_patch(Circle((x0 + 5 + k * 5, y0 + h - 4), 1.2, fc=SUP, ec=TINTA2, lw=0.8))
        marg, med = 12, 4; col = (w - 2 * marg - 11 * med) / 12
        for i in range(12):
            ax.add_patch(Rectangle((x0 + marg + i * (col + med), y0 + 2), col, h - 12, fc="#eef3fb", ec="none"))
        puntos(ax, x0 + 2, y0 + 2, w - 4, h - 12, 5)
        pie(fig, "Columnas tenues como guía"); pdf.savefig(fig); plt.close(fig)

        # 3. Storyboard de seis viñetas
        fig = plt.figure(figsize=(A4[1], A4[0])); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 297); ax.set_ylim(0, 210); ax.axis("off")
        ax.text(15, 196, "Storyboard", fontsize=13, color=TINTA, fontweight="bold")
        ax.text(15, 189, "Escenario: ____________________________________________   Persona: ______________", fontsize=8.5, color=TINTA2)
        for i in range(6):
            fx = 15 + (i % 3) * 91; fy = 105 - (i // 3) * 85
            ax.add_patch(Rectangle((fx, fy + 18), 85, 55, fc=SUP, ec=TINTA, lw=1.1))
            ax.text(fx, fy + 75, f"{i + 1}", fontsize=9, color=TINTA, fontweight="bold")
            for k in range(3):
                ax.plot([fx, fx + 85], [fy + 12 - k * 5.5, fy + 12 - k * 5.5], color="#cfcfcf", lw=0.6)
        pie(fig, "Texto breve bajo cada viñeta"); pdf.savefig(fig); plt.close(fig)
    print("ok", destino.name)


if __name__ == "__main__":
    for f in (tema1, tema2, tema4, tema5, tema6, tema7, tema8, tema9, tema12, plantillas_pdf):
        f()
