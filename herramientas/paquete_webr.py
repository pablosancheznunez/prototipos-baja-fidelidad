"""Genera datos/<paquete>.R: las funciones y los datos de un paquete de R en un
solo fichero que los capítulos cargan con source() dentro de webR (el paquete
no está compilado para WebAssembly).

Uso:   python3 herramientas/paquete_webr.py RUTA_DEL_PAQUETE
"""
import pathlib, re, subprocess, sys
sys.path.insert(0, pathlib.Path(__file__).resolve().parent.as_posix())
from comun import RAIZ, config

cfg = config()
pkg = pathlib.Path(sys.argv[1]).resolve()
nombre = cfg["paquete"]
partes = [f"# {nombre} para webR: generado por herramientas/paquete_webr.py.",
          f"# No editar: el código fuente está en https://github.com/{cfg['paquete_github']}.",
          f"# En tu ordenador, instala el paquete y usa library({nombre}).", ""]
for f in sorted((pkg / "R").glob("*.R")):
    if f.name == "datos.R":
        continue
    codigo = [l for l in f.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#'")]
    texto = re.sub(r"\n{3,}", "\n\n", "\n".join(codigo)).strip()
    partes += [f"# ---- {f.name} ----", texto, ""]
datos = subprocess.run(
    ["Rscript", "-e", f'for (f in list.files("{pkg}/data", full.names = TRUE)) load(f);'
     'for (o in sort(setdiff(ls(), "f"))) { cat(o, "<- "); dput(get(o)); cat("\\n") }'],
    capture_output=True, text=True, env={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"})
if datos.returncode:
    sys.exit(datos.stderr)
partes += ["# ---- datos ----", datos.stdout.strip(), ""]
destino = RAIZ / "datos" / f"{nombre.lower()}.R"
destino.parent.mkdir(exist_ok=True)
destino.write_text("\n".join(partes), encoding="utf-8")
print(destino.relative_to(RAIZ), len("\n".join(partes)), "caracteres")
