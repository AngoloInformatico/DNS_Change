<div align="center">

<img src="Icona/icon.ico" alt="DNS Change Logo" width="96" height="96" />

# DNS Change

**Modern Desktop WebApp per la gestione rapida, l'analisi telemetrica e la combinazione libera dei Server DNS (Primario e Secondario) su PC Windows 10 e Windows 11.**

[![Version](https://img.shields.io/badge/Version-0.1.7-10B981?style=for-the-badge&logo=semanticrelease&logoColor=white)](https://github.com/AngoloInformatico)
[![OS](https://img.shields.io/badge/OS-Windows%2010%20%2F%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white)](https://learn.microsoft.com/powershell/)
[![License](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge)](LICENSE)

</div>

---

## Panoramica

**DNS Change** è una WebApp desktop di ultima generazione sviluppata per **Windows 10 e Windows 11** che consente di cambiare con un clic i server **DNS Primario e Secondario** sulle schede di rete attive (`Ethernet`, `Wi-Fi`, ecc.).

Progettata con un'interfaccia professionale multi-stile (**Windows 11 Mica Tactile**, **Swiss Precision Telemetry** e **Industrial Hardware Rack**) e doppia modalità **Dark / Light** (con avvio predefinito in **Mica Light**), offre sia la selezione rapida della **coppia certificata di uno stesso provider**, sia la modalità **Mix Ibrido Multi-Provider** (impostando il **DNS Primario** di un provider e il **DNS Secondario** di un altro provider per massimizzare ridondanza e sicurezza).

---

## Anteprime (Temi Windows 11 Mica Light & Dark)

### Tema Predefinito: Mica Light (`Light Mode`)
![DNS Change - Tema Mica Light](SreenShot/DNS_Change_Light_Theme.png)

### Tema Mica Dark (`Dark Mode`)
![DNS Change - Tema Mica Dark](SreenShot/DNS_Change_Dark_Theme.png)

---

## Caratteristiche Principali

- **Selezione Flessibile (Coppia o Mix Ibrido):**
  - **Usa Coppia:** Applica contemporaneamente il DNS Primario e Secondario dello stesso provider.
  - **1° Primario + 2° Secondario Indipendenti:** Scegli il DNS Primario da un provider (es. *Cloudflare `1.1.1.1`*) e il DNS Secondario da un altro provider (es. *Quad9 `149.112.112.112`* o *Google `8.8.8.8`*).
- **Catalogo Completo dei Provider DNS più Conosciuti:**
  Include descrizioni tecniche dettagliate, indirizzi IPv4 Primario/Secondario, barre telemetriche di **Velocità (ms)** e **Affidabilità (%)**, e pulsante diretto al **Sito Ufficiale** per ogni provider:
  1. **Cloudflare DNS** (`1.1.1.1` / `1.0.0.1`) — *Velocità estrema & Privacy*
  2. **Google Public DNS** (`8.8.8.8` / `8.8.4.4`) — *Massima compatibilità globale*
  3. **Quad9 Security DNS** (`9.9.9.9` / `149.112.112.112`) — *Scudo Anti-Malware & Phishing Svizzero*
  4. **Cisco OpenDNS Home** (`208.67.222.222` / `208.67.220.220`) — *Protezione Anti-Phishing Enterprise*
  5. **AdGuard DNS Public** (`94.140.14.14` / `94.140.15.15`) — *Ad-Block & Anti-Tracking nativo*
  6. **CleanBrowsing Security** (`185.228.168.9` / `185.228.169.9`) — *Filtro Malware & Family Shield*
  7. **NextDNS Public Anycast** (`45.90.28.190` / `45.90.30.190`) — *Firewall DNS Ultra-Veloce*
  8. **Control D Unfiltered** (`76.76.2.0` / `76.76.10.0`) — *Routing Anycast di nuova generazione*
  9. **Verisign Public DNS** (`64.6.64.6` / `64.6.65.6`) — *Stabilità Root Server pura*
- **Layout a Card in Righe Verticali:** Le card dei provider sono impilate in righe a tutta larghezza una sotto l'altra, per una consultazione chiara e immediata con valori di latenza e affidabilità al fianco di ciascun resolver.
- **3 Varianti di Stile Grafico + Temi Dark e Light:**
  - `2. Win11 Mica (Predefinito)`: Barra laterale del profilo attivo e card morbide in stile Windows 11 (avvio predefinito in modalità Mica Light).
  - `1. Swiss Telemetry`: Griglia tecnica da `1px`, contrasto tipografico netto e indicatori telemetrici.
  - `3. Hardware Rack`: Display digitale centrale a doppio canale (`CH-01` / `CH-02`) e pulsanti meccanici.
- **📖 Wiki & Guida Interattiva per Neofiti Integrata:** Include un manuale pratico suddiviso in capitoli accessibile dalla barra superiore:
  - *1. Cos'è il DNS (spiegato semplice con la metafora della rubrica telefonica)*
  - *2. Come usare DNS Change in 4 semplici passi*
  - *3. Differenza tra DNS Primario e Secondario e perché fare il Mix Ibrido*
  - *4. Quale DNS scegliere per le proprie esigenze (con preset rapidi)*
  - *5. Glossario pratico (DHCP, Flush DNS, Ping e Uptime)*
- **🏆 Pulsante Preset 1-Click:** Pulsante dedicato nella barra superiore della dashboard che porta direttamente al Capitolo 4 della Wiki per caricare configurazioni ottimali in un clic (*Gaming & Fibra*, *Protezione Malware Famiglia*, *Ad-Block*, *Mix Privacy + Sicurezza*).
- **🔄 Auto-Incremento Versione (`version.json`):** Tracciamento automatico basato su hash SHA-256 dei file sorgente, per garantire un versionamento trasparente e autonomo a chiunque cloni la repository da GitHub.
- **Strumenti di Rete Windows 10/11 Integrati:**
  - Pulsante **⚡ Utilizza DNS Selezionati** con elevazione automatica UAC di Windows.
  - Pulsante **🔄 DHCP Auto** per ripristinare i DNS automatici dell'operatore.
  - Pulsante **🧹 Flush DNS** per svuotare istantaneamente la cache DNS (`ipconfig /flushdns`).
  - Pulsante **📡 Test Ping** per misurare in tempo reale la latenza effettiva verso tutti i server DNS.
- **Centraggio Automatico sullo Schermo:** All'avvio la finestra si posiziona sempre esattamente al centro del monitor principale di Windows.
- **Integrazione Icona Completa:** L'icona `Icona/icon.ico` è associata al file `.exe`, alla finestra nativa e alla barra delle applicazioni (Taskbar) anche quando l'applicazione è minimizzata.

---

## Struttura del Progetto

```text
DNS Change/
├── Icona/
│   └── icon.ico                        # Icona ufficiale multi-risoluzione della WebApp
├── SreenShot/
│   ├── DNS_Change_Light_Theme.png      # Screenshot ufficiale Tema Predefinito (Mica Light)
│   └── DNS_Change_Dark_Theme.png       # Screenshot ufficiale Tema Mica Dark
├── web/
│   └── index.html                      # Frontend WebApp (3 stili, Dark/Light, Wiki e Preset)
├── dist/
│   └── DNS Change.exe                  # Eseguibile standalone per Windows 10/11
├── main.py                             # Avvio WebApp centrata e API nativa Windows 10/11
├── GeneraExe.py                        # Script per compilare l'eseguibile in dist/
├── requirements.txt                    # Dipendenze Python
├── version.json                        # Registro di versione con auto-incremento SHA-256
├── LICENSE                             # Licenza ufficiale del progetto
└── Readme.md                           # Documentazione ufficiale GitHub
```

*(Tutti i file e gli script ausiliari di lavoro e compilazione sono isolati nella cartella `Codex_Work/`, esclusa dal caricamento su GitHub tramite `.gitignore`).*

---

## Installazione e Avvio

### 1. Avvio diretto dell'Eseguibile (`.exe`)
Puoi avviare direttamente l'applicazione compilata per Windows 10/11 presente in:
```text
dist/DNS Change.exe
```

### 2. Avvio da Codice Sorgente Python
Assicurati di avere **Python 3.10+** installato su Windows 10/11:
```powershell
pip install -r requirements.txt
python main.py
```

### 3. Generazione dell'Eseguibile (`GeneraExe.py`)
Per rigenerare autonomamente il file `.exe` all'interno della cartella `dist/`:
```powershell
python GeneraExe.py
```

---

## Licenza

Questo progetto è distribuito sotto i termini specificati nel file [LICENSE](LICENSE) incluso nella repository.

---

## Autore & Copyright

**Created by Alex Lignola - © 2026 DNS Change - All rights reserved.**

- 📺 **YouTube:** [https://www.youtube.com/@AngoloInformatico](https://www.youtube.com/@AngoloInformatico)
- 💻 **GitHub Profile:** [https://github.com/AngoloInformatico](https://github.com/AngoloInformatico)
- 📦 **GitHub Repositories:** [https://github.com/AngoloInformatico?tab=repositories](https://github.com/AngoloInformatico?tab=repositories)
