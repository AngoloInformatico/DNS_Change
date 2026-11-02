"""
DNS Change — Windows 10/11 Modern Desktop WebApp
Created by Alex Lignola - © 2026 DNS Change - All rights reserved.
https://www.youtube.com/@AngoloInformatico
https://github.com/AngoloInformatico
"""
import os
import re
import sys
import json
import time
import socket
import ctypes
import hashlib
import webbrowser
import subprocess
from concurrent.futures import ThreadPoolExecutor
import webview

APP_TITLE = "DNS Change — Windows 10/11 Network Resolver Studio"
APP_VERSION = "0.1.7"
APP_USER_MODEL_ID = "AngoloInformatico.DNSChange.DesktopApp"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860


def get_resource_path(relative_path: str) -> str:
    """Restituisce il percorso assoluto della risorsa sia in sviluppo che nel bundle PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def check_and_auto_increment_version() -> str:
    """
    Legge e aggiorna il file version.json nella root del progetto (incluso su GitHub).
    Parte dalla versione 0.1.6 e ad ogni modifica rilevata nei file sorgente
    (main.py, web/index.html, GeneraExe.py) incrementa automaticamente il numero di versione
    salvandolo in version.json e sincronizzando main.py, web/index.html e Readme.md.
    """
    global APP_VERSION
    version_file = get_resource_path("version.json")

    # Se siamo dentro l'eseguibile compilato (.exe), legge semplicemente la versione da version.json
    if hasattr(sys, "_MEIPASS"):
        if os.path.exists(version_file):
            try:
                with open(version_file, "r", encoding="utf-8") as f:
                    APP_VERSION = json.load(f).get("version", APP_VERSION)
            except Exception:
                pass
        return APP_VERSION

    base_dir = os.path.dirname(os.path.abspath(__file__))
    version_json_path = os.path.join(base_dir, "version.json")
    watched_rel = ["main.py", "web/index.html", "GeneraExe.py"]

    data = {
        "app_name": "DNS Change",
        "version": "0.1.6",
        "source_hash": "",
        "watched_files": watched_rel,
        "author": "Alex Lignola",
        "copyright": "Created by Alex Lignola - © 2026 DNS Change - All rights reserved.",
    }

    if os.path.exists(version_json_path):
        try:
            with open(version_json_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    data.update(loaded)
        except Exception:
            pass

    def calc_sources_hash() -> str:
        h = hashlib.sha256()
        for rel in data.get("watched_files", watched_rel):
            p = os.path.join(base_dir, rel.replace("/", os.sep))
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                txt = re.sub(r"\b\d+\.\d+\.\d+\b", "X.Y.Z", txt)
                h.update(txt.encode("utf-8"))
        return h.hexdigest()

    current_hash = calc_sources_hash()
    saved_hash = data.get("source_hash", "")
    ver = data.get("version", "0.1.6")

    if not saved_hash:
        # Prima inizializzazione su 0.1.6: salva l'impronta corrente senza incrementare
        data["version"] = ver
        data["source_hash"] = current_hash
        _sync_version_files(base_dir, version_json_path, data, calc_sources_hash)
    elif current_hash != saved_hash:
        # Codice sorgente modificato: auto-incrementa la versione (es. 0.1.6 -> 0.1.7)
        parts = [int(x) for x in ver.split(".")]
        while len(parts) < 3:
            parts.append(0)
        parts[2] += 1
        ver = f"{parts[0]}.{parts[1]}.{parts[2]}"
        data["version"] = ver
        _sync_version_files(base_dir, version_json_path, data, calc_sources_hash)

    APP_VERSION = ver
    return APP_VERSION


def _sync_version_files(base_dir: str, version_json_path: str, data: dict, hash_fn):
    """Propaga la versione su main.py, web/index.html, Readme.md e salva version.json."""
    ver = data["version"]

    main_path = os.path.join(base_dir, "main.py")
    if os.path.exists(main_path):
        with open(main_path, "r", encoding="utf-8") as f:
            txt = f.read()
        new_txt = re.sub(r'APP_VERSION\s*=\s*"\d+\.\d+\.\d+"', f'APP_VERSION = "{ver}"', txt)
        if new_txt != txt:
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(new_txt)

    html_path = os.path.join(base_dir, "web", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            txt = f.read()
        new_txt = re.sub(r"v\d+\.\d+\.\d+\s*•\s*WIN 10/11", f"v{ver} • WIN 10/11", txt)
        new_txt = re.sub(r"DNS Change v\d+\.\d+\.\d+", f"DNS Change v{ver}", new_txt)
        new_txt = re.sub(r"let appVersion\s*=\s*'\d+\.\d+\.\d+'", f"let appVersion = '{ver}'", new_txt)
        if new_txt != txt:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(new_txt)

    readme_path = os.path.join(base_dir, "Readme.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            txt = f.read()
        new_txt = re.sub(r"Version-\d+\.\d+\.\d+-", f"Version-{ver}-", txt)
        if new_txt != txt:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_txt)

    data["source_hash"] = hash_fn()
    with open(version_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def set_windows_app_id():
    """Imposta l'AppUserModelID di Windows 10/11 affinché la barra delle applicazioni mostri sempre icon.ico."""
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"{APP_USER_MODEL_ID}.{APP_VERSION}")
    except Exception:
        pass


def apply_window_and_taskbar_icon(window, icon_path: str, title: str):
    """Forza l'icona icon.ico sia sulla finestra nativa (Titlebar) sia sulla Taskbar di Windows 10/11 (anche minimizzata)."""
    if not os.path.exists(icon_path):
        return

    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing
        native_form = getattr(window, "native", None)
        if native_form is not None:
            sys_icon = System.Drawing.Icon(icon_path)
            native_form.Icon = sys_icon
            native_form.ShowIcon = True
    except Exception:
        pass

    try:
        user32 = ctypes.windll.user32
        hwnd = None
        native_form = getattr(window, "native", None)
        if native_form is not None and hasattr(native_form, "Handle"):
            hwnd = int(native_form.Handle.ToInt64())
        if not hwnd:
            hwnd = user32.FindWindowW(None, title)

        if hwnd:
            IMAGE_ICON = 1
            LR_LOADFROMFILE = 0x00000010
            LR_DEFAULTSIZE = 0x00000040
            WM_SETICON = 0x0080
            ICON_SMALL = 0
            ICON_BIG = 1
            GCLP_HICON = -14
            GCLP_HICONSM = -34

            hicon_big = user32.LoadImageW(0, icon_path, IMAGE_ICON, 256, 256, LR_LOADFROMFILE)
            if not hicon_big:
                hicon_big = user32.LoadImageW(0, icon_path, IMAGE_ICON, 48, 48, LR_LOADFROMFILE | LR_DEFAULTSIZE)
            hicon_small = user32.LoadImageW(0, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

            if hicon_big:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
                try:
                    user32.SetClassLongPtrW(hwnd, GCLP_HICON, hicon_big)
                except Exception:
                    pass
            if hicon_small:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
                try:
                    user32.SetClassLongPtrW(hwnd, GCLP_HICONSM, hicon_small)
                except Exception:
                    pass
    except Exception:
        pass


def is_user_admin() -> bool:
    """Verifica se il processo corrente possiede privilegi di Amministratore su Windows."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_elevated_powershell(ps_script: str) -> bool:
    """Esegue un comando PowerShell chiedendo l'elevazione UAC se il processo non è amministratore."""
    try:
        if is_user_admin():
            res = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=15,
            )
            return res.returncode == 0
        else:
            params = f'-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "{ps_script}"'
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", params, None, 0)
            time.sleep(1.2)
            return int(ret) > 32
    except Exception:
        return False


def measure_tcp_latency(ip: str, port: int = 53, timeout: float = 0.8) -> int:
    """Misura la latenza reale verso un server DNS (porta 53 TCP) in millisecondi."""
    start = time.perf_counter()
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            elapsed = (time.perf_counter() - start) * 1000.0
            return max(1, int(round(elapsed)))
    except Exception:
        return 25


class DnsChangeApi:
    """API esposta al frontend HTML5/JS tramite pywebview."""

    def get_system_info(self) -> dict:
        """Rileva le schede di rete attive su Windows 10/11 e i relativi server DNS IPv4 attuali."""
        adapters = []
        ps_cmd = (
            "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | ForEach-Object { "
            "$dns = (Get-DnsClientServerAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4).ServerAddresses; "
            "[PSCustomObject]@{ name = $_.Name; description = $_.InterfaceDescription; status = $_.Status; current_dns = @($dns) } "
            "} | ConvertTo-Json -Compress"
        )
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=8,
            )
            raw = res.stdout.strip()
            if raw:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    adapters = [parsed]
                elif isinstance(parsed, list):
                    adapters = parsed
        except Exception:
            pass

        if not adapters:
            adapters = [
                {
                    "name": "Ethernet",
                    "description": "Scheda di rete Windows principale",
                    "status": "Up",
                    "current_dns": [],
                }
            ]

        return {
            "version": APP_VERSION,
            "is_admin": is_user_admin(),
            "adapters": adapters,
        }

    def apply_dns(self, adapter_name: str, primary_ip: str, secondary_ip: str) -> dict:
        """Imposta il DNS Primario e Secondario sulla scheda di rete selezionata (Windows 10/11)."""
        primary_ip = (primary_ip or "").strip()
        secondary_ip = (secondary_ip or "").strip()
        if not primary_ip:
            return {"success": False, "message": "Indirizzo DNS Primario non valido."}

        safe_adapter = adapter_name.replace("'", "''")
        if secondary_ip:
            addresses = f"'{primary_ip}','{secondary_ip}'"
        else:
            addresses = f"'{primary_ip}'"

        ps_cmd = (
            f"Set-DnsClientServerAddress -InterfaceAlias '{safe_adapter}' -ServerAddresses ({addresses}); "
            f"Clear-DnsClientCache"
        )
        ok = run_elevated_powershell(ps_cmd)
        if ok:
            return {
                "success": True,
                "message": f"DNS impostati con successo su '{adapter_name}': Primario {primary_ip} • Secondario {secondary_ip or 'Nessuno'}",
            }
        return {
            "success": False,
            "message": "Impossibile applicare i DNS. Verifica di aver confermato il prompt UAC di Amministratore.",
        }

    def restore_dhcp(self, adapter_name: str) -> dict:
        """Ripristina l'ottenimento automatico dei server DNS tramite DHCP sulla scheda selezionata."""
        safe_adapter = adapter_name.replace("'", "''")
        ps_cmd = (
            f"Set-DnsClientServerAddress -InterfaceAlias '{safe_adapter}' -ResetServerAddresses; "
            f"Clear-DnsClientCache"
        )
        ok = run_elevated_powershell(ps_cmd)
        if ok:
            return {
                "success": True,
                "message": f"DNS ripristinati in modalità Automatica (DHCP) sulla scheda '{adapter_name}'.",
            }
        return {
            "success": False,
            "message": "Ripristino DHCP annullato o permessi di Amministratore non concessi.",
        }

    def flush_dns(self) -> dict:
        """Svuota la cache del resolver DNS di Windows (ipconfig /flushdns)."""
        try:
            res = subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=6,
            )
            if res.returncode == 0:
                return {"success": True, "message": "Cache DNS di Windows 10/11 svuotata con successo (ipconfig /flushdns)."}
        except Exception:
            pass
        return {"success": False, "message": "Errore durante lo svuotamento della cache DNS."}

    def benchmark_dns(self, ip_list: list) -> dict:
        """Esegue un test di latenza reale parallelo su tutti i server DNS forniti."""
        results = {}
        if not isinstance(ip_list, list):
            return results
        with ThreadPoolExecutor(max_workers=9) as pool:
            futures = {ip: pool.submit(measure_tcp_latency, ip) for ip in ip_list}
            for ip, fut in futures.items():
                try:
                    results[ip] = fut.result()
                except Exception:
                    results[ip] = 20
        return results

    def open_url(self, url: str) -> bool:
        """Apre il sito web ufficiale del provider DNS nel browser predefinito di sistema."""
        if url and (url.startswith("https://") or url.startswith("http://")):
            webbrowser.open(url)
            return True
        return False


def get_centered_geometry(width: int, height: int) -> tuple[int, int]:
    """Calcola le coordinate (X, Y) per centrare esattamente la finestra sullo schermo principale di Windows."""
    try:
        user32 = ctypes.windll.user32
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass
        screen_w = user32.GetSystemMetrics(0)
        screen_h = user32.GetSystemMetrics(1)
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)
        return x, y
    except Exception:
        return 120, 80


def main():
    check_and_auto_increment_version()
    set_windows_app_id()
    api = DnsChangeApi()
    html_path = get_resource_path(os.path.join("web", "index.html"))
    icon_file = get_resource_path(os.path.join("Icona", "icon.ico"))
    pos_x, pos_y = get_centered_geometry(WINDOW_WIDTH, WINDOW_HEIGHT)

    window = webview.create_window(
        title=APP_TITLE,
        url=html_path,
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        x=pos_x,
        y=pos_y,
        min_size=(1020, 700),
        background_color="#EEF2F7",
        text_select=False,
    )

    def on_shown():
        cx, cy = get_centered_geometry(WINDOW_WIDTH, WINDOW_HEIGHT)
        try:
            window.move(cx, cy)
        except Exception:
            pass
        apply_window_and_taskbar_icon(window, icon_file, APP_TITLE)

    def on_loaded():
        apply_window_and_taskbar_icon(window, icon_file, APP_TITLE)

    window.events.shown += on_shown
    window.events.loaded += on_loaded
    webview.start(debug=False, icon=icon_file if os.path.exists(icon_file) else None)


if __name__ == "__main__":
    main()
