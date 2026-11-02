"""
GeneraExe.py — Script di compilazione eseguibile Windows (.exe) per DNS Change
Genera il file eseguibile standalone nella cartella "dist/DNS Change.exe"
e archivia tutti i file temporanei di build nella cartella "Codex_Work/".

Created by Alex Lignola - © 2026 DNS Change - All rights reserved.
"""
import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
WORK_DIR = os.path.join(BASE_DIR, "Codex_Work", "pyinstaller_build")
SPEC_DIR = os.path.join(BASE_DIR, "Codex_Work")
ICON_PATH = os.path.join(BASE_DIR, "Icona", "icon.ico")
WEB_DIR = os.path.join(BASE_DIR, "web")
MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")


def build_executable():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(SPEC_DIR, exist_ok=True)

    # Sincronizza e autoincrementa il numero di versione direttamente tramite main.py (incluso nei sorgenti GitHub)
    try:
        from main import check_and_auto_increment_version
        active_ver = check_and_auto_increment_version()
        print(f"Versione WebApp rilevata/aggiornata: v{active_ver}")
    except Exception as e:
        print(f"Nota versionamento: {e}")

    if not os.path.exists(ICON_PATH):
        gen_icon = os.path.join(BASE_DIR, "Codex_Work", "generate_icon.py")
        if os.path.exists(gen_icon):
            subprocess.run([sys.executable, gen_icon], check=True)

    add_data_sep = ";" if os.name == "nt" else ":"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        "DNS Change",
        "--icon",
        ICON_PATH,
        "--distpath",
        DIST_DIR,
        "--workpath",
        WORK_DIR,
        "--specpath",
        SPEC_DIR,
        "--add-data",
        f"{WEB_DIR}{add_data_sep}web",
        "--add-data",
        f"{os.path.join(BASE_DIR, 'Icona')}{add_data_sep}Icona",
        "--add-data",
        f"{os.path.join(BASE_DIR, 'version.json')}{add_data_sep}.",
        MAIN_SCRIPT,
    ]

    print("=" * 72)
    print("Avvio generazione eseguibile Windows: DNS Change.exe")
    print(f"Cartella di output: {DIST_DIR}")
    print("=" * 72)

    result = subprocess.run(cmd, cwd=BASE_DIR)
    if result.returncode != 0:
        print("Errore durante la generazione dell'eseguibile.")
        sys.exit(result.returncode)

    exe_path = os.path.join(DIST_DIR, "DNS Change.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("=" * 72)
        print(f"COMPILAZIONE COMPLETATA CON SUCCESSO!")
        print(f"File generato: {exe_path} ({size_mb:.2f} MB)")
        print("=" * 72)
    else:
        print("Attenzione: file .exe non trovato nel percorso previsto.")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()

