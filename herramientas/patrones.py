"""Genera en SVG los patrones de navegación (p_*) y los casos del catálogo (c_*) y del museo (mu_*)."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "figuras"
T, T2, G1, G2, G3, A = "#0b0b0b", "#52514e", "#eceae5", "#d9d8d4", "#a3a29e", "#2a78d6"
F = 'font-family="Source Sans 3, Helvetica, Arial, sans-serif"'

def svg(nombre, cuerpo, alto=640):
    (OUT / f"{nombre}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 {alto}" width="360" height="{alto}" {F}><rect x="1" y="1" width="358" height="{alto-2}" rx="28" fill="#fff" stroke="{T}" stroke-width="2"/><rect x="140" y="12" width="80" height="8" rx="4" fill="{G2}"/>{cuerpo}</svg>', encoding="utf-8")
def r(x, y, w, h, f=G1, rx=6, st=None): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}"' + (f' stroke="{st}" stroke-width="1.5"' if st else "") + "/>"
def t(x, y, s, size=13, c=T, w="400", a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{w}" text-anchor="{a}">{s}</text>'
def lin(x, y, w, n=2, gap=9, c=G2): return "".join(f'<rect x="{x}" y="{y+i*gap}" width="{w - (30 if i==n-1 else 0)}" height="5" rx="2.5" fill="{c}"/>' for i in range(n))
def boton(x, y, w, s, prim=True): return r(x, y, w, 40, A if prim else "#fff", 8, None if prim else T) + t(x + w/2, y + 25, s, 14, "#fff" if prim else T, "600", "middle")
def cab(s, izq="≡"): return r(16, 36, 328, 44, "#fff", 0) + t(24, 64, izq, 20 if izq == "≡" else 22, T) + t(180, 64, s, 15, T, "600", "middle") + f'<line x1="16" y1="84" x2="344" y2="84" stroke="{G2}"/>'
def img(x, y, w, h): return r(x, y, w, h, G1, 6) + f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{G2}"/><line x1="{x+w}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{G2}"/>'
def tabbar(nombres, activo=0): return f'<line x1="16" y1="580" x2="344" y2="580" stroke="{G2}"/>' + "".join(r(46 + i*(268/(len(nombres)-1) if len(nombres) > 1 else 0) - 12 + 12, 592, 24, 20, A if i == activo else G2, 4) + t(58 + i*(268/(len(nombres)-1)), 626, n, 10, A if i == activo else T2, "600" if i == activo else "400", "middle") for i, n in enumerate(nombres))
def tarjeta(x, y, w, h, tit, sub=""): return r(x, y, w, h, "#fff", 8, G3) + img(x + 8, y + 8, w - 16, h * 0.5) + t(x + 10, y + h * 0.5 + 30, tit, 12, T, "600") + (t(x + 10, y + h * 0.5 + 47, sub, 10, T2) if sub else "")

# ---------- Patrones ----------
c = cab("Inicio") + t(24, 116, "Pestañas inferiores", 17, T, "600") + lin(24, 132, 300, 3) + "".join(r(24, 170 + i*70, 312, 60, G1, 8) + lin(36, 186 + i*70, 200, 2) for i in range(5)) + tabbar(["Inicio", "Buscar", "Reservas", "Perfil"])
svg("p_pestanas", c)
c = cab("Inicio") + "".join(r(24, 100 + i*70, 312, 60, G1, 8) for i in range(7)) + '<rect x="1" y="1" width="358" height="638" rx="28" fill="#0b0b0b" opacity="0.45"/>'
c += r(1, 1, 250, 638, "#fff", 0) + t(24, 70, "ReservaSala", 18, T, "600") + "".join(t(24, 120 + i*44, s, 15, A if i == 0 else T, "600" if i == 0 else "400") + f'<line x1="24" y1="{132 + i*44}" x2="226" y2="{132 + i*44}" stroke="{G2}"/>' for i, s in enumerate(["Inicio", "Buscar salas", "Mis reservas", "Mapa", "Normas", "Ayuda", "Cerrar sesión"]))
svg("p_cajon", c)
c = cab("Libro", "‹") + t(24, 108, "Catálogo  ›  Historia  ›  España contemporánea", 11, A) + img(24, 124, 110, 150) + t(146, 140, "Título del libro", 16, T, "600") + t(146, 160, "Autora, 2021", 12, T2) + lin(146, 176, 190, 4)
c += boton(24, 300, 312, "Reservar ejemplar") + t(24, 370, "Disponibilidad", 14, T, "600") + "".join(r(24, 382 + i*46, 312, 38, G1, 6) + t(36, 406 + i*46, s, 12, T) for i, s in enumerate(["Getafe · disponible", "Leganés · prestado hasta 12/12", "Colmenarejo · disponible"]))
svg("p_migas", c)
c = cab("Nueva reserva", "‹") + "".join(f'<circle cx="{60 + i*80}" cy="118" r="14" fill="{A if i < 2 else "#fff"}" stroke="{A if i < 3 else G3}" stroke-width="2"/>' + t(60 + i*80, 123, "✓" if i < 2 else str(i + 1), 12, "#fff" if i < 2 else (A if i == 2 else T2), "600", "middle") + t(60 + i*80, 152, s, 10, A if i == 2 else T2, "600" if i == 2 else "400", "middle") for i, s in enumerate(["Sala", "Fecha", "Datos", "Revisar"]))
c += "".join(f'<line x1="{74 + i*80}" y1="118" x2="{126 + i*80}" y2="118" stroke="{A if i < 2 else G3}" stroke-width="2"/>' for i in range(3))
c += t(24, 196, "Paso 3 de 4 · Tus datos", 16, T, "600") + "".join(t(24, 230 + i*76, s, 12, T, "600") + r(24, 238 + i*76, 312, 40, "#fff", 6, T2) for i, s in enumerate(["Número de personas", "Motivo (opcional)", "Invitar a compañeros"]))
c += boton(190, 520, 146, "Siguiente") + boton(24, 520, 146, "Anterior", False)
svg("p_pasos", c)
c = cab("Buscar", "‹") + r(24, 96, 312, 40, "#fff", 20, T) + t(44, 121, "⌕  estadística", 14, T) + "".join(r(24 + x, 148, w, 28, A if k == 0 else "#fff", 14, None if k == 0 else T) + t(24 + x + w/2, 167, s, 11, "#fff" if k == 0 else T, "400", "middle") for k, (x, w, s) in enumerate([(0, 76, "Libros ✕"), (82, 86, "Desde 2020"), (174, 80, "Disponible"), (260, 56, "+ Filtros")]))
c += t(24, 200, "128 resultados · más relevantes ▾", 11, T2) + "".join(r(24, 212 + i*76, 312, 68, "#fff", 8, G3) + img(32, 220 + i*76, 40, 52) + t(84, 236 + i*76, f"Resultado {i+1}", 13, T, "600") + lin(84, 246 + i*76, 230, 2) for i in range(4))
svg("p_busqueda", c)
c = cab("Exposiciones") + t(24, 112, "Destacadas", 15, T, "600") + "".join(tarjeta(24 + (i % 2)*160, 124 + (i // 2)*190, 152, 180, f"Exposición {i+1}", "Hasta marzo") for i in range(4)) + tabbar(["Inicio", "Mapa", "Visita", "Más"])
svg("p_tarjetas", c)
c = cab("Sala 2.14", "‹") + img(16, 88, 328, 150) + lin(24, 256, 300, 4) + '<rect x="1" y="1" width="358" height="638" rx="28" fill="#0b0b0b" opacity="0.45"/>'
c += r(1, 340, 358, 298, "#fff", 24) + r(150, 352, 60, 6, G2, 3) + t(24, 396, "¿Cancelar la reserva?", 18, T, "600") + t(24, 422, "Sala 2.14 · hoy 16:00–18:00. La sala quedará", 12, T2) + t(24, 440, "libre para otras personas.", 12, T2) + boton(24, 470, 312, "Sí, cancelar") + boton(24, 520, 312, "No, mantenerla", False)
svg("p_modal", c)
c = cab("Normas de uso", "‹") + "".join(r(24, 100 + i*56 + (150 if i > 1 else 0), 312, 48, "#fff", 8, G3) + t(36, 130 + i*56 + (150 if i > 1 else 0), s, 13, T, "600") + t(324, 130 + i*56 + (150 if i > 1 else 0), "−" if i == 1 else "+", 18, T, "400", "end") for i, s in enumerate(["¿Cuánto tiempo puedo reservar?", "¿Qué pasa si llego tarde?", "¿Puedo comer en la sala?", "¿Cómo invito a otras personas?", "¿Hay salas adaptadas?"]))
c += r(24, 206, 312, 140, G1, 8) + lin(36, 222, 280, 6, 14)
svg("p_acordeon", c)

# ---------- Caso: catálogo de biblioteca ----------
c = cab("Biblioteca UC3M") + t(24, 120, "¿Qué buscas?", 20, T, "600") + r(24, 136, 312, 44, "#fff", 22, T) + t(44, 164, "⌕  Título, autor, tema o ISBN", 13, T2)
c += t(24, 214, "Búsquedas recientes", 13, T, "600") + "".join(t(24, 242 + i*28, "↺  " + s, 13, T2) for i, s in enumerate(["metodología cualitativa", "Kahneman", "historia del cine"]))
c += t(24, 360, "Tus préstamos", 13, T, "600") + "".join(r(24, 372 + i*62, 312, 54, G1, 8) + t(36, 396 + i*62, f"Préstamo {i+1}", 13, T, "600") + t(36, 414 + i*62, "Vence en " + ("2 días" if i == 0 else "12 días"), 11, "#b3261e" if i == 0 else T2) for i in range(2)) + tabbar(["Buscar", "Préstamos", "Salas", "Perfil"])
svg("c_busqueda", c)
c = cab("«estadística»", "‹") + "".join(r(24 + x, 96, w, 28, A if k == 0 else "#fff", 14, None if k == 0 else T) + t(24 + x + w/2, 115, s, 11, "#fff" if k == 0 else T, "400", "middle") for k, (x, w, s) in enumerate([(0, 76, "Libro ✕"), (82, 88, "Disponible"), (176, 66, "Getafe"), (248, 64, "Filtros")]))
c += t(24, 148, "42 resultados", 11, T2) + "".join(r(24, 160 + i*96, 312, 86, "#fff", 8, G3) + img(32, 168 + i*96, 52, 70) + t(96, 184 + i*96, f"Título del libro {i+1}", 13, T, "600") + t(96, 202 + i*96, "Autoría · 2019", 11, T2) + r(96, 214 + i*96, 92 if i != 1 else 112, 20, "#e2f0e5" if i != 1 else G1, 10) + t(104, 228 + i*96, "● Disponible" if i != 1 else "○ Prestado · 3 reservas", 10, T) for i in range(4))
svg("c_resultados", c)
c = cab("Libro", "‹") + img(24, 96, 120, 165) + t(156, 116, "Título del libro 1", 16, T, "600") + t(156, 136, "Autoría · 2019 · 3.ª ed.", 11, T2) + t(156, 156, "Signatura: 519.2 GAR", 11, T2) + r(156, 172, 92, 22, "#e2f0e5", 11) + t(164, 187, "● Disponible", 10, T)
c += boton(24, 280, 312, "Reservar para recoger") + boton(24, 330, 152, "Guardar", False) + boton(184, 330, 152, "Citar", False)
c += t(24, 408, "Ejemplares", 14, T, "600") + "".join(r(24, 420 + i*44, 312, 38, G1, 6) + t(36, 444 + i*44, s, 12, T) for i, s in enumerate(["Getafe · planta 1 · disponible", "Leganés · prestado hasta 12/12", "Colmenarejo · disponible"]))
svg("c_registro", c)
c = cab("Reservar ejemplar", "‹") + t(24, 116, "¿Dónde quieres recogerlo?", 15, T, "600") + "".join(r(24, 128 + i*52, 312, 44, "#fff", 8, A if i == 0 else G3) + f'<circle cx="44" cy="{150 + i*52}" r="8" fill="{"#fff"}" stroke="{A if i == 0 else T2}" stroke-width="2"/>' + (f'<circle cx="44" cy="{150 + i*52}" r="4" fill="{A}"/>' if i == 0 else "") + t(62, 155 + i*52, s, 13, T) for i, s in enumerate(["Getafe · listo mañana", "Colmenarejo · listo en 3 días"]))
c += r(24, 250, 312, 64, G1, 8) + t(36, 274, "Tendrás 5 días para recogerlo.", 12, T2) + t(36, 294, "Te avisaremos por correo.", 12, T2) + boton(24, 340, 312, "Confirmar reserva")
svg("c_reserva", c)

# ---------- Caso: app de museo ----------
c = cab("Museo") + img(16, 88, 328, 150) + t(24, 268, "Planifica tu visita", 18, T, "600") + "".join(r(24 + i*106, 284, 98, 74, G1, 10) + t(73 + i*106, 316, s, 12, T, "600", "middle") + t(73 + i*106, 336, d, 10, T2, "400", "middle") for i, (s, d) in enumerate([("1 hora", "lo esencial"), ("2 horas", "recorrido"), ("A mi aire", "explorar")]))
c += t(24, 392, "Accesibilidad", 13, T, "600") + "".join(r(24 + i*104, 404, 96, 30, "#fff", 15, T) + t(72 + i*104, 424, s, 11, T, "400", "middle") for i, s in enumerate(["Sin escaleras", "Audiodescripción", "Lectura fácil"])) + tabbar(["Inicio", "Mapa", "Visita", "Más"])
svg("mu_inicio", c)
c = cab("Recorrido · 1 hora", "‹") + r(24, 96, 312, 300, G1, 10) + "".join(r(40 + (i % 3)*100, 112 + (i // 3)*130, 80, 110, "#fff", 4, G3) + t(80 + (i % 3)*100, 172 + (i // 3)*130, f"Sala {i+1}", 11, T2, "400", "middle") for i in range(6))
c += f'<path d="M80 200 L180 200 L180 330 L280 330" fill="none" stroke="{A}" stroke-width="4" stroke-dasharray="8 6"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{A}"/>' + t(x, y + 5, str(k + 1), 12, "#fff", "600", "middle") for k, (x, y) in enumerate([(80, 200), (180, 260), (280, 330)]))
c += t(24, 426, "Siguiente parada", 13, T2) + t(24, 448, "1 · Sala 1 · El retrato", 16, T, "600") + t(24, 468, "A 20 m · 12 minutos", 12, T2) + boton(24, 488, 312, "Empezar audioguía") + tabbar(["Inicio", "Mapa", "Visita", "Más"], 1)
svg("mu_mapa", c)
c = cab("Obra 1 de 6", "‹") + img(16, 88, 328, 220) + t(24, 338, "Título de la obra", 18, T, "600") + t(24, 360, "Autor · 1890 · óleo sobre lienzo", 12, T2)
c += r(24, 376, 312, 56, G1, 10) + f'<circle cx="52" cy="404" r="18" fill="{A}"/>' + t(52, 410, "▶", 14, "#fff", "600", "middle") + r(80, 400, 200, 6, G2, 3) + r(80, 400, 60, 6, A, 3) + t(324, 408, "3:20", 11, T2, "400", "end")
c += t(24, 462, "Transcripción · Lectura fácil · Ampliar", 12, A, "600") + lin(24, 478, 300, 3) + boton(24, 530, 146, "Anterior", False) + boton(190, 530, 146, "Siguiente")
svg("mu_obra", c)
c = cab("Tu visita") + f'<circle cx="180" cy="150" r="40" fill="{G1}" stroke="{T}" stroke-width="2"/>' + t(180, 162, "★", 30, T, "600", "middle") + t(180, 230, "Has visto 6 obras en 58 minutos", 16, T, "600", "middle")
c += t(24, 280, "Tus favoritas", 13, T, "600") + "".join(img(24 + i*106, 292, 98, 98) for i in range(3)) + boton(24, 420, 312, "Enviar el resumen a mi correo") + boton(24, 470, 312, "Valorar la visita", False) + tabbar(["Inicio", "Mapa", "Visita", "Más"], 2)
svg("mu_resumen", c)
print("ok")

# ---------- Estados de la lista (cargando, error, parcial) ----------
def chips(): return "".join(r(24 + i*104, 96, 96, 30, "#fff", 15, T) + t(72 + i*104, 116, s, 12, T, "400", "middle") for i, s in enumerate(["16:00–18:00 ▾", "4 personas ▾", "Silencio ▾"]))
def navr(): return f'<line x1="16" y1="580" x2="344" y2="580" stroke="{G2}"/>' + "".join(r(46 + i*92, 592, 24, 20, A if i == 1 else G2, 4) + t(58 + i*92, 626, n, 10, A if i == 1 else T2, "400", "middle") for i, n in enumerate(["Inicio", "Reservas", "Mapa", "Perfil"]))
c = cab("Salas · Esta tarde", "‹") + chips() + r(24, 140, 180, 10, G1, 5) + "".join(r(24, 162 + i*66, 312, 58, G1, 8) + r(36, 176 + i*66, 120, 10, G2, 5) + r(36, 196 + i*66, 200, 8, G2, 4) for i in range(6)) + navr()
svg("g_cargando", c)
c = cab("Salas · Esta tarde", "‹") + chips() + r(24, 150, 312, 150, "#fdf1d8", 10, "#b35900") + t(40, 182, "⚠ No hemos podido cargar las salas", 15, T, "600") + t(40, 208, "Parece que no hay conexión. Tus filtros", 12, T2) + t(40, 226, "se mantienen.", 12, T2) + boton(40, 244, 140, "Reintentar")
c += t(24, 340, "Última información guardada (hace 5 min)", 12, T2) + "".join(r(24, 352 + i*66, 312, 58, "#fff", 8, G3) + t(36, 376 + i*66, f"Sala {i+1}.0{i+2}", 14, T2, "600") + t(36, 396 + i*66, "Puede haber cambiado", 11, T2) for i in range(2)) + navr()
svg("g_error", c)
c = cab("Salas · Esta tarde", "‹") + chips() + t(24, 150, "1 sala disponible", 11, T2) + r(24, 162, 312, 58, "#fff", 8, G3) + t(36, 184, "Sala 3.02", 14, T, "600") + t(36, 204, "2 personas · planta 3", 11, T2) + t(324, 188, "›", 18, T2, "400", "end")
c += r(24, 240, 312, 150, G1, 10) + t(40, 270, "¿Quieres más opciones?", 15, T, "600") + "".join(t(40, 300 + i*26, "› " + s, 13, A, "600") for i, s in enumerate(["Ver salas de 18:00 a 20:00 (6 libres)", "Quitar el filtro «Silencio»", "Ver otras bibliotecas"])) + navr()
svg("g_parcial", c)

# ---------- Escritorio ----------
W, Hh = 1024, 640
c = f'<rect x="1" y="1" width="{W-2}" height="{Hh-2}" rx="10" fill="#fff" stroke="{T}" stroke-width="2"/><line x1="1" y1="36" x2="{W-1}" y2="36" stroke="{T}"/>' + "".join(f'<circle cx="{20 + k*16}" cy="18" r="5" fill="none" stroke="{T2}"/>' for k in range(3)) + r(80, 9, 600, 18, G1, 9)
c += t(40, 76, "ReservaSala", 18, T, "700") + "".join(t(560 + i*110, 76, s, 14, A if i == 0 else T, "600" if i == 0 else "400") for i, s in enumerate(["Buscar salas", "Mis reservas", "Mapa", "Ayuda"])) + f'<line x1="40" y1="96" x2="{W-40}" y2="96" stroke="{G2}"/>'
c += t(40, 132, "Filtros", 15, T, "600") + "".join(t(40, 168 + i*70, s, 12, T, "600") + r(40, 176 + i*70, 200, 34, "#fff", 6, T2) for i, s in enumerate(["Franja", "Personas", "Biblioteca", "Equipamiento"])) + boton(40, 470, 200, "Aplicar filtros")
c += t(280, 132, "12 salas disponibles esta tarde", 18, T, "600") + t(984, 132, "Ordenar: cercanía ▾", 12, T2, "400", "end")
for i in range(6):
    x, y = 280 + (i % 3)*240, 150 + (i // 3)*220
    c += r(x, y, 224, 204, "#fff", 10, G3) + r(x + 10, y + 10, 204, 90, G1, 6) + t(x + 14, y + 124, f"Sala {i+1}.0{i+2}", 14, T, "600") + t(x + 14, y + 144, f"{4 + i % 3} personas · planta {i+1}", 11, T2) + r(x + 14, y + 160, 196, 32, A, 8) + t(x + 112, y + 181, "Reservar", 13, "#fff", "600", "middle")
(OUT / "g_escritorio.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" {F}>{c}</svg>', encoding="utf-8")
print("estados y escritorio ok")
