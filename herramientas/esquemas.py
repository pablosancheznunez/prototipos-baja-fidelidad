"""Genera esquemas de baja fidelidad en SVG para la galería (figuras/g_*.svg)."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "figuras"
T, T2, G1, G2, G3, A = "#0b0b0b", "#52514e", "#eceae5", "#d9d8d4", "#a3a29e", "#2a78d6"

def svg(nombre, cuerpo, alto=640):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 {alto}" width="360" height="{alto}" font-family="Source Sans 3, Helvetica, Arial, sans-serif">
<rect x="1" y="1" width="358" height="{alto-2}" rx="28" fill="#fff" stroke="{T}" stroke-width="2"/>
<rect x="140" y="12" width="80" height="8" rx="4" fill="{G2}"/>{cuerpo}</svg>'''
    (OUT / f"{nombre}.svg").write_text(s, encoding="utf-8")

def r(x, y, w, h, f=G1, rx=6, st=None): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}"' + (f' stroke="{st}" stroke-width="1.5"' if st else "") + "/>"
def t(x, y, s, size=13, c=T, w="400", a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{w}" text-anchor="{a}">{s}</text>'
def lin(x, y, w, n=2, gap=9, c=G2): return "".join(f'<rect x="{x}" y="{y+i*gap}" width="{w - (30 if i==n-1 else 0)}" height="5" rx="2.5" fill="{c}"/>' for i in range(n))
def boton(x, y, w, s, prim=True): return r(x, y, w, 40, A if prim else "#fff", 8, None if prim else T) + t(x + w/2, y + 25, s, 14, "#fff" if prim else T, "600", "middle")
def cab(s, atras=False): return r(16, 36, 328, 44, "#fff", 0) + (t(24, 64, "‹", 22, T) if atras else t(24, 64, "≡", 20, T)) + t(180, 64, s, 15, T, "600", "middle") + f'<line x1="16" y1="84" x2="344" y2="84" stroke="{G2}"/>'
def nav(): return f'<line x1="16" y1="580" x2="344" y2="580" stroke="{G2}"/>' + "".join(r(46 + i*92, 592, 24, 20, G2, 4) + t(58 + i*92, 626, n, 10, T2, "400", "middle") for i, n in enumerate(["Inicio", "Reservas", "Mapa", "Perfil"]))

# 1 Inicio
c = cab("ReservaSala") + t(24, 112, "Hola, Lucía", 18, T, "600") + r(24, 124, 312, 74, "#fff", 10, G3) + t(36, 146, "Tu próxima reserva", 11, T2) + t(36, 168, "Sala 2.14 · Hoy 16:00–18:00", 14, T, "600") + t(36, 188, "Cancelar · Cómo llegar", 11, A)
c += t(24, 230, "¿Cuándo quieres estudiar?", 15, T, "600") + "".join(r(24 + i*80, 242, 72, 34, "#fff", 17, T if i else A) + t(60 + i*80, 264, s, 12, T, "400", "middle") for i, s in enumerate(["Ahora", "Esta tarde", "Mañana", "Elegir"]))
c += r(24, 242, 72, 34, A, 17) + t(60, 264, "Ahora", 12, "#fff", "600", "middle")
c += t(24, 310, "Salas libres ahora", 15, T, "600") + "".join(r(24, 322 + i*58, 312, 50, G1, 8) + t(36, 342 + i*58, f"Sala {s}", 13, T, "600") + t(36, 360 + i*58, f"{p} personas · planta {s[0]}", 11, T2) + t(324, 352 + i*58, "Reservar ›", 12, A, "600", "end") for i, (s, p) in enumerate([("1.03", 4), ("2.14", 6), ("3.02", 2)]))
c += t(180, 520, "Ver todas las salas", 13, A, "600", "middle") + nav()
svg("g_inicio", c)
# 2 Lista con filtros
c = cab("Salas · Esta tarde", True) + "".join(r(24 + i*104, 96, 96, 30, "#fff", 15, T) + t(72 + i*104, 116, s, 12, T, "400", "middle") for i, s in enumerate(["16:00–18:00 ▾", "4 personas ▾", "Silencio ▾"]))
c += t(24, 150, "12 salas disponibles · ordenadas por cercanía", 11, T2)
for i in range(6):
    y = 162 + i*66
    c += r(24, y, 312, 58, "#fff", 8, G3) + t(36, y + 22, f"Sala {i+1}.0{i+2}", 14, T, "600") + t(36, y + 42, f"{4 + i % 3} personas · enchufes · planta {i+1}", 11, T2)
    c += "".join(r(200 + k*16, y + 34, 14, 10, A if (k + i) % 3 else G2, 2) for k in range(6)) + t(324, y + 26, "›", 18, T2, "400", "end")
c += nav()
svg("g_lista", c)
# 3 Detalle
c = cab("Sala 2.14", True) + r(16, 88, 328, 150, G1, 0) + f'<line x1="16" y1="88" x2="344" y2="238" stroke="{G2}"/><line x1="344" y1="88" x2="16" y2="238" stroke="{G2}"/>'
c += t(24, 268, "Sala de trabajo en grupo 2.14", 17, T, "600") + t(24, 290, "Biblioteca de Getafe · planta 2", 12, T2)
c += "".join(r(24 + i*104, 304, 96, 28, G1, 14) + t(72 + i*104, 323, s, 11, T, "400", "middle") for i, s in enumerate(["6 personas", "Pizarra", "Enchufes"]))
c += t(24, 364, "Disponibilidad hoy", 14, T, "600") + "".join(r(24 + k*26, 376, 24, 34, A if k not in (2, 3, 7) else G2, 3) for k in range(12))
c += t(24, 426, "9h", 10, T2) + t(330, 426, "21h", 10, T2, "400", "end") + r(24, 441, 10, 10, A, 2) + t(38, 450, "Libre", 11, T2) + r(80, 441, 10, 10, G2, 2) + t(94, 450, "Ocupada", 11, T2) + lin(24, 470, 300, 3)
c += boton(24, 528, 312, "Reservar 16:00–18:00")
svg("g_detalle", c)
# 4 Formulario
c = cab("Confirmar reserva", True) + t(24, 112, "Sala 2.14 · Hoy 16:00–18:00", 14, T, "600")
for i, (lab, ph) in enumerate([("Número de personas", "4"), ("Motivo (opcional)", "Preparar examen de Estadística"), ("Invitar a compañeros", "Correo de la UC3M")]):
    y = 136 + i*76
    c += t(24, y, lab, 12, T, "600") + r(24, y + 8, 312, 40, "#fff", 6, T2) + t(36, y + 33, ph, 13, T2)
c += r(24, 366, 18, 18, "#fff", 3, T) + t(52, 380, "Recordarme 30 minutos antes", 13, T)
c += r(24, 404, 312, 54, G1, 8) + t(36, 426, "Si no confirmas tu llegada en 15 minutos,", 11, T2) + t(36, 444, "la sala se libera para otras personas.", 11, T2)
c += boton(24, 484, 312, "Confirmar reserva") + boton(24, 534, 312, "Volver", False)
svg("g_formulario", c)
# 5 Confirmación
c = cab("Reserva confirmada") + f'<circle cx="180" cy="160" r="40" fill="{G1}" stroke="{T}" stroke-width="2"/>' + t(180, 172, "✓", 34, T, "600", "middle")
c += t(180, 240, "¡Sala reservada!", 20, T, "600", "middle") + t(180, 266, "Te hemos enviado la confirmación por correo.", 12, T2, "400", "middle")
c += r(24, 290, 312, 120, "#fff", 10, G3) + "".join(t(40, 320 + i*28, s, 13, T) for i, s in enumerate(["Sala 2.14 · planta 2", "Hoy, 16:00–18:00", "4 personas · código 7F3K"]))
c += boton(24, 440, 312, "Añadir al calendario") + boton(24, 490, 312, "Cancelar reserva", False) + t(180, 560, "Volver al inicio", 13, A, "600", "middle")
svg("g_confirmacion", c)
# 6 Estado vacío
c = cab("Salas · Mañana 10:00", True) + r(140, 150, 80, 80, G1, 40) + t(180, 202, "∅", 34, T2, "400", "middle")
c += t(180, 270, "No hay salas para 10 personas", 16, T, "600", "middle") + t(180, 294, "Las más grandes son para 8.", 12, T2, "400", "middle")
c += boton(40, 330, 280, "Ver salas para 8 personas") + boton(40, 380, 280, "Probar otra franja", False) + t(180, 450, "Avisarme si se libera una sala", 13, A, "600", "middle") + nav()
svg("g_vacio", c)
# 7 Esquema con problemas (para la actividad de zonas)
c = r(16, 36, 328, 44, "#fff", 0) + t(180, 64, "RESERVASALA v2.3 BETA", 13, T2, "400", "middle")
c += t(24, 108, "Bienvenido al sistema de gestión de espacios", 12, T2) + r(24, 120, 312, 120, G1, 4) + t(180, 186, "[ Banner de noticias ]", 13, T2, "400", "middle")
c += r(24, 256, 312, 36, "#fff", 4, G3) + t(36, 279, "AAAAMMDD-HHMM", 12, G3)
c += r(24, 302, 312, 36, "#fff", 4, G3) + t(36, 325, "Cód. espacio", 12, G3)
c += "".join(r(24 + i*58, 352, 52, 22, G2, 3) for i in range(5)) + t(24, 392, "Gris = no disponible, gris claro = disponible", 10, G3)
c += r(24, 410, 150, 36, G2, 4) + t(99, 433, "Ejecutar", 12, T, "400", "middle") + r(186, 410, 150, 36, G2, 4) + t(261, 433, "Borrar todo", 12, T, "400", "middle")
c += t(330, 600, "?", 10, G3, "400", "end")
svg("g_problemas", c)
print("ok")

# 8 Esquema anotado: el formulario con notas para desarrollo (pantalla + columna de notas)
import re as _re, textwrap as _tw
_base = (OUT / "g_formulario.svg").read_text(encoding="utf-8")
_cuerpo = _re.sub(r"^<svg[^>]*>|</svg>\s*$", "", _base.strip())
_notas = [
    (104, "Resumen fijo de la reserva: la persona no pierde el contexto al rellenar."),
    (164, "Número: teclado numérico en móvil; mínimo 1 y máximo la capacidad de la sala."),
    (240, "Campo opcional y marcado como tal; máximo 120 caracteres."),
    (316, "Autocompleta con el directorio UC3M y valida el dominio del correo."),
    (375, "Casilla desmarcada por defecto: decide la persona (sin patrones engañosos)."),
    (431, "Regla de negocio visible antes de confirmar, no después."),
    (507, "Acción principal: se desactiva y muestra «Reservando…» mientras se envía."),
    (557, "Secundaria: vuelve atrás conservando lo escrito."),
]
_c = f'<g>{_cuerpo}</g>'
for i, (y, nota) in enumerate(_notas, 1):
    yn = 70 + (i - 1) * 70
    _c += f'<path d="M336 {y} L368 {y} L392 {yn}" fill="none" stroke="#d6336c" stroke-width="1.5"/>'
    _c += f'<circle cx="404" cy="{yn}" r="12" fill="#d6336c"/><text x="404" y="{yn + 5}" font-size="13" fill="#fff" font-weight="700" text-anchor="middle">{i}</text>'
    for k, linea in enumerate(_tw.wrap(nota, 34)):
        _c += f'<text x="424" y="{yn + 5 + k * 17}" font-size="13" fill="#0b0b0b">{linea}</text>'
(OUT / "g_anotado.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 640" width="680" height="640" font-family="Source Sans 3, Helvetica, Arial, sans-serif"><rect width="680" height="640" fill="#fff"/>{_c}</svg>', encoding="utf-8")
print("anotado ok")
