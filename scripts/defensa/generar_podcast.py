"""Genera el audio del podcast de repaso de la defensa a partir de docs/defensa/podcast-guion.md.

Uso: python scripts/defensa/generar_podcast.py [--prueba] [salida.mp3]
Voces de Windows (WinRT, sin internet ni servicios externos): A = Laura, B = Pablo (es-ES). Necesita ffmpeg en el PATH.
Los audios intermedios van a una carpeta temporal y se reutilizan si se vuelve a ejecutar.
"""
import base64
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "docs" / "defensa" / "podcast-guion.md"
TMP = Path(tempfile.gettempdir()) / "podcast_cadus"
VOCES = {"A": "Laura", "B": "Pablo"}
TASA = 1.05  # velocidad de lectura
PAUSA_TURNO, PAUSA_RESPUESTA, PAUSA_SECCION = 0.45, 6.0, 1.2

# El sintetizador lee con reglas del español: lo que no lo es se escribe como suena.
PRONUNCIA = [
    (r"\bCMS\b", "ce eme ese"), (r"\bDMS\b", "de eme ese"), (r"\bUML\b", "u eme ele"), (r"\bRGPD\b", "erre ge pe de"),
    (r"\bSMTP\b", "ese eme te pe"), (r"\bAPI\b", "a pe i"), (r"\bPHP\b", "pe hache pe"), (r"\bNVDA\b", "ene uve de a"),
    (r"\bWCAG\b", "doble u ce a ge"), (r"\bSQL\b", "ese cu ele"), (r"\bDNI\b", "de ene i"), (r"\bPDF\b", "pe de efe"),
    (r"\bRN\b", "erre ene"), (r"\bRF\b", "erre efe"), (r"\bIR\b", "i erre"), (r"\bREM\b", "rem"), (r"\bSEO\b", "seo"),
    (r"\bIP\b", "i pe"), (r"\bAA\b", "a a"), (r"\bP cinco\b", "pe cinco"), (r"\bT uno a T tres\b", "te uno a te tres"),
    (r"\bGmail\b", "yimeil"), (r"\bSupportCandy\b", "Sopórt Candi"), (r"\bYoast\b", "Youst"), (r"\bWP\b", "doble u pe"),
    (r"\bSCRUM\b", "escrum"), (r"\bsprints\b", "esprints"), (r"\bsprint\b", "esprint"), (r"\bbacklog\b", "báklog"),
    (r"\bburndown\b", "bérndaun"), (r"\bProduct Owner\b", "Próduct Óuner"), (r"\bScrum Master\b", "Escrum Máster"),
    (r"\breview\b", "reviú"), (r"\bcommits\b", "comits"), (r"\bpull requests\b", "pul requests"), (r"\bplugins\b", "plaguins"),
    (r"\bplugin\b", "plaguin"), (r"\bnonce\b", "nons"), (r"\bfeeds\b", "fids"), (r"\bscript\b", "escript"),
    (r"\bzip\b", "sip"), (r"\bkilobytes\b", "kilobaits"), (r"\bRole\b", "Róul"), (r"\bGroup\b", "Grup"),
    (r"\bSubgroups\b", "Sabgrups"), (r"\bTool\b", "Tul"), (r"\bPermission\b", "Permishon"), (r"\bREMUS\b", "Rémus"),
    (r"\bGitHub\b", "Guit-jab"), (r"\bTeams\b", "Tims"), (r"\bSMS\b", "ese eme ese"),
]


def leer_guion():
    """Devuelve [("A"|"B", texto) | ("pausa", segundos) | ("seccion", 0)]."""
    items = []
    for l in GUION.read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if l.startswith("## "):
            items.append(("seccion", 0))
        elif l == "[pausa]":
            items.append(("pausa", PAUSA_RESPUESTA))
        elif re.match(r"^[AB]: ", l):
            items.append((l[0], l[3:]))
    return items


def hablar(texto):
    for a, b in PRONUNCIA:
        texto = re.sub(a, b, texto)
    return texto.replace("/", " barra ").replace("%", " por ciento")


CODIGO_PS = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[void][Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Wait-Op($op, $t) { $task = $asTask.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result }
$items = Get-Content $env:PODCAST_JSON -Raw -Encoding UTF8 | ConvertFrom-Json
$voices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
$s = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$s.Options.SpeakingRate = [double]$env:PODCAST_TASA
foreach ($it in $items) {
  if (Test-Path $it.file) { continue }
  $s.Voice = ($voices | Where-Object { $_.DisplayName -like "*$($it.voice)*" } | Select-Object -First 1)
  $st = Wait-Op ($s.SynthesizeTextToStreamAsync($it.text)) ([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
  $in = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($st)
  $fs = [IO.File]::Create($it.file); $in.CopyTo($fs); $fs.Close(); $in.Close()
}
"""


def sintetizar(turnos):
    TMP.mkdir(exist_ok=True)
    lista = [{"file": str(TMP / f"{i:03d}.wav"), "voice": VOCES[v], "text": hablar(t)} for i, (v, t) in turnos]
    (TMP / "items.json").write_text(json.dumps(lista, ensure_ascii=False), encoding="utf-8")
    cod = base64.b64encode(CODIGO_PS.encode("utf-16-le")).decode()
    env = {**__import__("os").environ, "PODCAST_JSON": str(TMP / "items.json"), "PODCAST_TASA": str(TASA)}
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", cod], env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit("Fallo al sintetizar: " + r.stderr[-800:])


def unir(items, salida):
    # todos los trozos a 24 kHz, mono, 16 bits, para poder concatenarlos con el módulo wave
    pcm = bytearray()
    sil = lambda s: bytes(int(24000 * s) * 2)
    for i, (v, dato) in enumerate(items):
        if v in ("A", "B"):
            origen, destino = TMP / f"{i:03d}.wav", TMP / f"{i:03d}_n.wav"
            if not destino.exists():
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(origen), "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(destino)], check=True)
            with wave.open(str(destino)) as w:
                pcm += w.readframes(w.getnframes())
            pcm += sil(PAUSA_TURNO)
        elif v == "pausa":
            pcm += sil(dato)
        else:
            pcm += sil(PAUSA_SECCION)
    crudo = TMP / "todo.wav"
    with wave.open(str(crudo), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(bytes(pcm))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(crudo), "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "96k",
                    "-metadata", "title=Repaso de la defensa del proyecto CADUS", "-metadata", "artist=GSI", str(salida)], check=True)
    return len(pcm) / 2 / 24000


def main():
    prueba = "--prueba" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    salida = Path(args[0]) if args else RAIZ / "docs" / "defensa" / "podcast-repaso-defensa.mp3"
    items = leer_guion()
    if prueba:
        items = items[:8]
    sintetizar([(i, x) for i, x in enumerate(items) if x[0] in ("A", "B")])
    seg = unir(items, salida)
    print(f"{salida} ({seg / 60:.1f} min, {salida.stat().st_size / 1e6:.1f} MB)")


main()
