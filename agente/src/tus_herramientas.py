"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import json
import subprocess
import urllib.parse
import urllib.request
import re
import os
import tempfile
import html

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))




DOMINIO_RE = re.compile(r"^[a-z0-9]([a-z0-9.-]{0,251}[a-z0-9])?$", re.I)


@protegida(objetivo="dominio")
def tecnologias_whatweb(dominio: str, esquema: str = "https") -> str:
    """Identifica las tecnologías de un sitio web (servidor, CMS, frameworks, cabeceras,
    versiones) con WhatWeb. ACTIVA: hace una petición al objetivo, aunque en modo
    sigiloso (agresividad 1). esquema: https o http."""
    esquema = esquema.lower()
    if esquema not in ("http", "https"):
        return "ERROR: esquema no válido. Usa http o https."
    if not DOMINIO_RE.match(dominio):
        return f"ERROR: dominio no válido ({dominio!r})."
    cmd = ["whatweb", "--color=never", "--no-errors", "-a", "1",
           "--max-redirects=0", f"{esquema}://{dominio}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return "ERROR: whatweb no respondió en 60 segundos."
    except FileNotFoundError:
        return "ERROR: whatweb no está instalado (apt install whatweb)."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar whatweb: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: whatweb falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"whatweb no devolvió resultados para {dominio}."

# ====================================================
#    Nmap
# ====================================================

def _puertos_validos(spec: str) -> bool:
    if not PUERTOS_RE.match(spec):
        return False
    for tramo in spec.split(","):
        for p in tramo.split("-"):
            if not 1 <= int(p) <= 65535:
                return False
        if "-" in tramo:
            a, b = map(int, tramo.split("-"))
            if a > b:
                return False
    return True


@protegida(objetivo="dominio")
def escaneo_nmap(dominio: str, puertos: str = "", servicios: bool = False) -> str:
    """Escanea puertos TCP de un dominio con nmap (solo puertos abiertos).
    ACTIVA: envía tráfico al objetivo. puertos: vacío = los 100 más comunes, o una lista
    como '22,80,443' o '1-1024' (máx. 50 tramos). servicios: si True, detecta servicio y
    versión (-sV, más lento y más ruidoso)."""
    if not DOMINIO_RE.match(dominio):
        return f"ERROR: dominio no válido ({dominio!r})."
    puertos = puertos.replace(" ", "")
    if puertos and not _puertos_validos(puertos):
        return "ERROR: lista de puertos no válida. Ejemplos: '22,80,443' o '1-1024'."

    cmd = ["nmap", "-sT", "-n", "-Pn", "--open", "-T3",
           "--max-retries", "1", "--host-timeout", "240s"]
    cmd += ["-p", puertos] if puertos else ["--top-ports", "100"]
    if servicios:
        cmd += ["-sV", "--version-light"]
    cmd += ["--", dominio]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return "ERROR: nmap no terminó en 300 segundos. Prueba con menos puertos."
    except FileNotFoundError:
        return "ERROR: nmap no está instalado (apt install nmap)."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar nmap: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: nmap falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"nmap no devolvió resultados para {dominio}."


# =================================================
#    subfinduer
# =================================================

@protegida(objetivo="dominio")
def subdominios_subfinder(dominio: str, todas_las_fuentes: bool = False) -> str:
    """Enumera subdominios de un dominio con subfinder usando fuentes públicas.
    Pasivo: no toca el objetivo. todas_las_fuentes: si True usa todas las fuentes
    (más resultados, más lento). Devuelve solo los subdominios dentro del alcance."""
    if not DOMINIO_RE.match(dominio):
        return f"ERROR: dominio no válido ({dominio!r})."

    cmd = ["subfinder", "-d", dominio, "-silent", "-nc",
           "-timeout", "20", "-max-time", "3"]
    if todas_las_fuentes:
        cmd.append("-all")

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return "ERROR: subfinder no terminó en 240 segundos."
    except FileNotFoundError:
        return ("ERROR: subfinder no está instalado "
                "(go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest).")
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar subfinder: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: subfinder falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")

    nombres = {n.strip().lstrip("*.").lower() for n in r.stdout.splitlines() if n.strip()}
    if not nombres:
        return f"subfinder no encontró subdominios para {dominio}."
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))

# =================================================
#    TheHarvester
# =================================================

FUENTES_HARVESTER = {"crtsh", "hackertarget", "rapiddns", "otx", "urlscan",
                     "anubis", "threatminer", "duckduckgo", "bing", "yahoo"}
FUENTES_POR_DEFECTO = "crtsh,hackertarget,rapiddns,otx,urlscan,anubis"

@protegida(objetivo="dominio")
def correos_theharvester(dominio: str, fuentes: str = FUENTES_POR_DEFECTO) -> str:
    """Recopila correos, hosts e IPs de un dominio con theHarvester usando fuentes públicas.
    Pasivo: no toca el objetivo. fuentes: lista separada por comas entre
    crtsh, hackertarget, rapiddns, otx, urlscan, anubis, threatminer, duckduckgo, bing, yahoo.
    Devuelve solo resultados dentro del alcance."""
    if not DOMINIO_RE.match(dominio):
        return f"ERROR: dominio no válido ({dominio!r})."
    lista = [f.strip().lower() for f in fuentes.split(",") if f.strip()]
    malas = [f for f in lista if f not in FUENTES_HARVESTER]
    if not lista or malas:
        return (f"ERROR: fuentes no válidas ({', '.join(malas) or 'vacío'}). "
                f"Usa: {', '.join(sorted(FUENTES_HARVESTER))}.")

    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "res")
        cmd = ["theHarvester", "-d", dominio, "-b", ",".join(lista),
               "-l", "200", "-f", base]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        except subprocess.TimeoutExpired:
            return "ERROR: theHarvester no terminó en 240 segundos. Prueba con menos fuentes."
        except FileNotFoundError:
            return "ERROR: theHarvester no está instalado (apt install theharvester)."
        except OSError as e:
            return recortar(f"ERROR: no se pudo ejecutar theHarvester: {e}")
        if r.returncode != 0:
            return recortar(f"ERROR: theHarvester falló ({r.returncode}): "
                            f"{r.stderr.strip() or 'sin detalles'}")
        try:
            with open(base + ".json", encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, ValueError) as e:
            return recortar(f"ERROR: no se pudo leer el resultado de theHarvester: {e}")

    if not isinstance(datos, dict):
        return "ERROR: theHarvester devolvió un formato inesperado."

    def _lista(clave):
        v = datos.get(clave, [])
        return [str(x).strip().lower() for x in v if isinstance(x, (str, int))] if isinstance(v, list) else []

    # Hosts: pueden venir como "sub.dominio.com:1.2.3.4"
    hosts = {h.split(":")[0].lstrip("*.") for h in _lista("hosts") if h}
    hosts_ok, hosts_fuera = filtrar(sorted(hosts))

    # Correos: se filtran por el dominio de la dirección
    correos = {c for c in _lista("emails") if "@" in c}
    doms_ok, _ = filtrar(sorted({c.split("@", 1)[1] for c in correos}))
    correos_ok = sorted(c for c in correos if c.split("@", 1)[1] in set(doms_ok))
    correos_fuera = len(correos) - len(correos_ok)

    ips = sorted(set(_lista("ips")))

    partes = [
        f"Fuentes: {', '.join(lista)}",
        f"\nCorreos en alcance ({len(correos_ok)}; {correos_fuera} filtrados):",
        *correos_ok,
        f"\nHosts en alcance ({len(hosts_ok)}; {hosts_fuera} filtrados):",
        *hosts_ok,
        f"\nIPs asociadas ({len(ips)}):",
        *ips,
    ]
    return recortar("\n".join(partes))


# =====================================================
#     Netcraft
# =====================================================

@protegida(objetivo="dominio")
def huella_netcraft(dominio: str) -> str:
    """Consulta el informe público de Netcraft (sitereport.netcraft.com) para obtener la
    huella tecnológica de un dominio: servidor, hosting, CMS, CDN, SPF, etc.
    Pasivo: consulta a Netcraft, no al objetivo. Es scraping de una web sin API oficial
    gratuita, así que puede fallar si Netcraft cambia la página o bloquea el acceso."""
    if not DOMINIO_RE.match(dominio):
        return f"ERROR: dominio no válido ({dominio!r})."
    url = "https://sitereport.netcraft.com/?url=" + urllib.parse.quote(dominio, safe="")
    try:
        crudo = _http(url, timeout=45)
    except Exception as e:
        return recortar(f"ERROR: Netcraft no respondió ({e}). Puede estar limitando el acceso "
                        "automatizado; reintenta más tarde o consulta el informe en el navegador.")

    texto = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", crudo)
    texto = re.sub(r"(?s)<[^>]+>", "\n", texto)
    lineas = [re.sub(r"\s+", " ", l).strip() for l in html.unescape(texto).splitlines()]
    lineas = [l for l in lineas if l]
    contenido = "\n".join(lineas)

    if len(contenido) < 300 or "enable javascript" in contenido.lower():
        return ("ERROR: Netcraft devolvió una página sin datos (probablemente se genera con "
                f"JavaScript o bloquea clientes automáticos). Informe manual: {url}")
    return recortar(f"Informe Netcraft de {dominio}\n{url}\n\n{contenido}")
