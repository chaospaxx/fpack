# fpack
fpack – Find Packages Across APT, Flatpak, Snap &amp; AppImages Ein Linux-Diagnose- und Such-Tool, das Programm­installationen über alle relevanten Paketquellen findet – inklusive Versionen, Speicherorten, Config-Verzeichnissen, Desktop-Einträgen und Deinstallations­hinweisen. Unterstützt  alle Distributionen, die Python3 nutzen.

# fpack – Unified Linux Package & Application Finder

`fpack` ist ein leistungsfähiges Diagnosetool für Linux.  
Es durchsucht **alle wichtigen Paketquellen** nach Programmen:

- **APT / dpkg**
- **Flatpak**
- **Snap**
- **AppImage-Dateien**
- **Executables im $PATH**

Es zeigt Installationsorte, Versionen, Config-Files, Desktop-Dateien und Deinstallationsbefehle an.  
Ideal für Entwickler, Admins und alle, die Ordnung in ihre Linux-Systeme bringen möchten.

---

## 🚀 Features

✔ Suche eines Programms anhand eines **Stichworts oder Namens**  
✔ Erkennung von Installationen über **mehrere Paketquellen gleichzeitig**  
✔ Ausgabe von **Version**, Installationsort, Executable & Config-Files  
✔ **Deinstallations-Hinweise** mit `-d`  
✔ **JSON-Output** für Skripte & automatisierte Tools (`-j`)  
✔ **Unit-Tests** integrierbar mit `-u`  
✔ robust – funktioniert auch ohne Snap/Flatpak/AppImage  
✔ keine externen Abhängigkeiten außer Python 3

---

## 📦 Installation

Klonen des Repositories:

git clone https://github.com/<DEIN-NAME>/fpack.git
Script ausführbar machen:
chmod +x fpack.py
(Optional: Systemweit verfügbar machen)
sudo cp fpack.py /usr/local/bin/fpack

## 🧠 Verwendung
🔍 Basis-Suche
./fpack.py cura

📄 JSON-Ausgabe
./fpack.py -j firefox

🧹 Deinstallationshinweise anzeigen
./fpack.py -d vlc

🧪 Unit-Tests ausführen
./fpack.py -u

Flags können kombiniert werden
./fpack.py -j -d obs

🛠 Anforderungen

Python 3.8 oder höher
Optional:
apt (Debian/Ubuntu)
flatpak
snap
AppImage-Dateien im Home-Verzeichnis

Alle Komponenten sind optional – fpack läuft auch ohne sie.

🤝 Beiträge

Pull Requests sind willkommen!
Ideen oder Bugs? → GitHub Issues.

📜 Lizenz

Dieses Projekt wird unter der MIT License veröffentlicht.

⭐ Wenn dir das Projekt gefällt …

Bitte ⭐ auf GitHub setzen!
Das hilft, das Projekt sichtbar zu machen.
cd fpack

