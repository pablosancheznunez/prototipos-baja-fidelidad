"""Plantillas imprimibles (PDF A4) y kit de componentes (SVG) para bocetar esquemas."""
import pathlib
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "plantillas"; OUT.mkdir(exist_ok=True)
GRIS, OSC, PIE = HexColor("#a3a29e"), HexColor("#0b0b0b"), "Pablo Sánchez-Núñez · Esquemas de página y prototipos de baja fidelidad · CC BY 4.0"
W, H = landscape(A4)

def cabecera(c, titulo, ayuda):
    c.setFillColor(OSC); c.setFont("Helvetica-Bold", 14); c.drawString(36, H - 40, titulo)
    c.setFont("Helvetica", 9); c.drawString(36, H - 56, ayuda)
    c.drawString(W - 260, H - 40, "Proyecto: ______________________"); c.drawString(W - 260, H - 56, "Fecha: ____________  Versión: _____")
    c.setFillColor(GRIS); c.setFont("Helvetica", 7); c.drawString(36, 18, PIE)

def movil(c, x, y, w, h, n):
    c.setStrokeColor(OSC); c.setLineWidth(1.2); c.roundRect(x, y, w, h, 14)
    c.setStrokeColor(GRIS); c.setLineWidth(0.6); c.roundRect(x + w / 2 - 18, y + h - 10, 36, 4, 2)
    c.setFillColor(OSC); c.setFont("Helvetica", 8); c.drawString(x, y - 12, f"{n}. Pantalla: _____________")
    c.setFillColor(GRIS)
    for k in range(3): c.line(x, y - 24 - k * 11, x + w, y - 24 - k * 11)

# 1. Seis pantallas de móvil con notas
c = canvas.Canvas(str(OUT / "plantilla-movil-6.pdf"), pagesize=landscape(A4)); c.setTitle("Plantilla: seis pantallas de móvil")
cabecera(c, "Seis pantallas de móvil", "Dibuja una pantalla por marco. Debajo: nombre, acción principal y a qué pantalla lleva.")
w, h = 118, 236
for i in range(6): movil(c, 46 + i * 128, 190, w, h, i + 1)
c.save()
# 2. Crazy 8s
c = canvas.Canvas(str(OUT / "crazy-8s.pdf"), pagesize=landscape(A4)); c.setTitle("Plantilla: Crazy 8s")
cabecera(c, "Crazy 8s · ocho ideas en ocho minutos", "Un minuto por recuadro. No borres: si una idea no sirve, pasa a la siguiente. Al final, marca con ★ las dos mejores.")
cw, ch = (W - 72 - 30) / 4, (H - 120 - 10) / 2
for i in range(8):
    x, y = 36 + (i % 4) * (cw + 10), H - 76 - ch - (i // 4) * (ch + 10)
    c.setStrokeColor(OSC); c.setLineWidth(1); c.rect(x, y, cw, ch); c.setFillColor(OSC); c.setFont("Helvetica-Bold", 11); c.drawString(x + 6, y + ch - 16, str(i + 1))
c.save()
# 3. Escritorio con rejilla de 12 columnas
c = canvas.Canvas(str(OUT / "plantilla-escritorio.pdf"), pagesize=landscape(A4)); c.setTitle("Plantilla: pantalla de escritorio con rejilla de 12 columnas")
cabecera(c, "Pantalla de escritorio · rejilla de 12 columnas", "Las columnas punteadas te ayudan a alinear. Deja márgenes y medianiles constantes.")
x0, y0, bw, bh = 36, 50, W - 72, H - 130
c.setStrokeColor(OSC); c.setLineWidth(1.2); c.roundRect(x0, y0, bw, bh, 8); c.line(x0, y0 + bh - 26, x0 + bw, y0 + bh - 26)
for k in range(3): c.circle(x0 + 14 + k * 14, y0 + bh - 13, 4)
c.roundRect(x0 + 70, y0 + bh - 20, bw - 140, 14, 7)
c.setStrokeColor(GRIS); c.setDash(2, 3); m, g = 24, 12; cw = (bw - 2 * m - 11 * g) / 12
for k in range(12):
    xx = x0 + m + k * (cw + g); c.rect(xx, y0 + 10, cw, bh - 46)
c.save()
# 4. Diagrama de flujo
c = canvas.Canvas(str(OUT / "hoja-flujo.pdf"), pagesize=landscape(A4)); c.setTitle("Plantilla: flujo de usuario")
cabecera(c, "Flujo de usuario", "Rectángulo = pantalla · rombo = decisión · óvalo = inicio o fin. Marca el camino principal con trazo grueso.")
c.setStrokeColor(OSC); c.setLineWidth(1); c.ellipse(46, H - 130, 136, H - 100); c.setFont("Helvetica", 8); c.setFillColor(OSC); c.drawString(70, H - 118, "Inicio")
c.rect(160, H - 132, 90, 34); c.drawString(170, H - 118, "Pantalla")
p = c.beginPath(); p.moveTo(320, H - 115); p.lineTo(350, H - 98); p.lineTo(380, H - 115); p.lineTo(350, H - 132); p.close(); c.drawPath(p); c.drawString(336, H - 118, "¿Sí?")
c.setFillColor(GRIS); c.setFont("Helvetica", 7)
for i in range(0, int(W), 18):
    for j in range(40, int(H) - 150, 18): c.circle(i + 6, j, 0.6, fill=1, stroke=0)
c.save()

# Kit de componentes en SVG
T, T2, G1, G2, G3, A = "#0b0b0b", "#52514e", "#eceae5", "#d9d8d4", "#a3a29e", "#2a78d6"
def r(x, y, w, h, f=G1, rx=6, st=None): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}"' + (f' stroke="{st}" stroke-width="1.5"' if st else "") + "/>"
def tx(x, y, s, size=13, c=T, w="400", a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{w}" text-anchor="{a}">{s}</text>'
def comp(id_, x, y, etiqueta, cuerpo): return f'<g id="{id_}" transform="translate({x} {y})">{tx(0, 0, etiqueta, 11, T2, "600")}<g transform="translate(0 10)">{cuerpo}</g></g>'
k = []
k.append(comp("boton-principal", 30, 70, "Botón principal", r(0, 0, 160, 40, A, 8) + tx(80, 25, "Acción", 14, "#fff", "600", "middle")))
k.append(comp("boton-secundario", 220, 70, "Botón secundario", r(0, 0, 160, 40, "#fff", 8, T) + tx(80, 25, "Acción", 14, T, "600", "middle")))
k.append(comp("enlace", 410, 70, "Enlace", tx(0, 25, "Texto del enlace ›", 14, A, "600")))
k.append(comp("campo", 30, 150, "Campo de texto", tx(0, 14, "Etiqueta", 12, T, "600") + r(0, 22, 250, 40, "#fff", 6, T2) + tx(12, 47, "Texto de ejemplo", 13, T2)))
k.append(comp("campo-error", 310, 150, "Campo con error", tx(0, 14, "Etiqueta", 12, T, "600") + r(0, 22, 250, 40, "#fff", 6, "#b3261e") + tx(0, 80, "⚠ Explica cómo corregirlo", 11, "#b3261e")))
k.append(comp("casilla", 30, 260, "Casilla", r(0, 0, 18, 18, "#fff", 3, T) + tx(28, 14, "Opción", 13)))
k.append(comp("radio", 150, 260, "Opción única", f'<circle cx="9" cy="9" r="9" fill="#fff" stroke="{T}" stroke-width="1.5"/><circle cx="9" cy="9" r="4" fill="{T}"/>' + tx(28, 14, "Opción", 13)))
k.append(comp("interruptor", 270, 260, "Interruptor", r(0, 0, 40, 22, A, 11) + '<circle cx="29" cy="11" r="8" fill="#fff"/>' + tx(52, 16, "Activado", 13)))
k.append(comp("chip", 420, 260, "Filtro (chip)", r(0, 0, 90, 28, "#fff", 14, T) + tx(45, 19, "Filtro ▾", 12, T, "400", "middle")))
k.append(comp("imagen", 30, 330, "Imagen", r(0, 0, 160, 100, G1, 6) + f'<line x1="0" y1="0" x2="160" y2="100" stroke="{G2}"/><line x1="160" y1="0" x2="0" y2="100" stroke="{G2}"/>'))
k.append(comp("texto", 220, 330, "Bloque de texto", "".join(r(0, i * 12, 200 - (40 if i == 3 else 0), 6, G2, 3) for i in range(4))))
k.append(comp("elemento-lista", 30, 470, "Elemento de lista", r(0, 0, 300, 56, "#fff", 8, G3) + tx(12, 24, "Título", 13, T, "600") + tx(12, 42, "Detalle secundario", 11, T2) + tx(288, 34, "›", 18, T2, "400", "end")))
k.append(comp("tarjeta", 360, 470, "Tarjeta", r(0, 0, 160, 150, "#fff", 8, G3) + r(8, 8, 144, 76, G1, 6) + tx(10, 108, "Título", 12, T, "600") + tx(10, 126, "Subtítulo", 10, T2)))
k.append(comp("cabecera", 30, 660, "Cabecera", r(0, 0, 328, 44, "#fff", 0) + tx(8, 28, "‹", 22) + tx(164, 28, "Título", 15, T, "600", "middle") + f'<line x1="0" y1="48" x2="328" y2="48" stroke="{G2}"/>'))
k.append(comp("pestanas", 30, 740, "Pestañas inferiores", f'<line x1="0" y1="0" x2="328" y2="0" stroke="{G2}"/>' + "".join(r(18 + i * 88, 10, 24, 20, A if i == 0 else G2, 4) + tx(30 + i * 88, 44, n, 10, A if i == 0 else T2, "400", "middle") for i, n in enumerate(["Inicio", "Buscar", "Listas", "Perfil"]))))
k.append(comp("aviso", 390, 660, "Aviso", r(0, 0, 220, 56, "#fdf1d8", 8, "#b35900") + tx(12, 24, "⚠ Título del aviso", 12, T, "600") + tx(12, 42, "Qué ha pasado y qué hacer.", 11, T2)))
k.append(comp("dialogo", 390, 740, "Diálogo", r(0, 0, 220, 130, "#fff", 12, T) + tx(14, 28, "¿Confirmar acción?", 13, T, "600") + "".join(r(14, 40 + i * 10, 180, 5, G2, 2) for i in range(2)) + r(14, 80, 92, 34, A, 8) + tx(60, 102, "Sí", 12, "#fff", "600", "middle") + r(114, 80, 92, 34, "#fff", 8, T) + tx(160, 102, "No", 12, T, "600", "middle")))
kit = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 900" width="640" height="900" font-family="Source Sans 3, Helvetica, Arial, sans-serif"><rect width="640" height="900" fill="#fff"/>{tx(30, 36, "Kit de componentes para esquemas de baja fidelidad", 18, T, "700")}{"".join(k)}{tx(30, 885, PIE, 10, T2)}</svg>'
(RAIZ / "figuras" / "kit-esquemas.svg").write_text(kit, encoding="utf-8")
(OUT / "kit-esquemas.svg").write_text(kit, encoding="utf-8")
print("ok", sorted(p.name for p in OUT.glob("*.pdf")))
