1. Rezept-Repo holen & Dev-Container aktivieren (auf dem Host)
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp -R devcontainer-example .devcontainer
Dann in .devcontainer/docker-compose.yml das Bench-Image pinnen: image: frappe/bench:v5.27.0.

2. Dieses Repo daneben klonen & Zutaten hineinkopieren
cd ..
git clone git@github.com:Brass53/erpnext-demo.git erpnext-demo
cp erpnext-demo/apps.json  frappe_docker/development/apps.json
cp -R erpnext-demo/backup  frappe_docker/development/backup

3. In VS Code Ordner frappe_docker öffnen → unten rechts „Reopen in Container". Ab jetzt alle Befehle im Container-Terminal.

4. Python 3.14 + Node 24 bereitstellen (ERPNext v16 braucht das)
pyenv install -s 3.14.2
nvm install 24 && nvm alias default 24 && npm install -g yarn

5. Installer laufen lassen (baut Bench + lädt Apps + legt Site an)
cd /workspace/development
python installer.py -j apps.json -s development.localhost \
  -r https://github.com/frappe/frappe -t version-16 -p 3.14.2 -n 24 -v

6. Testdaten einspielen (das eigentliche „Demo-Daten"-Stück)
cd frappe-bench
BK=/workspace/development/backup
bench --site development.localhost restore \
  $BK/20260712_144126-development_localhost-database.sql.gz \
  --with-public-files  $BK/20260712_144126-development_localhost-files.tar \
  --with-private-files $BK/20260712_144126-development_localhost-private-files.tar
bench --site development.localhost migrate

7. Starten
bench use development.localhost
bench start
→ Browser: http://development.localhost:8000 — Administrator / admin.

---
Der Kern in einem Satz: frappe_docker liefert die Container-Umgebung, apps.json die Software, das backup/ die Daten — Schritt 6 macht aus einem leeren ERPNext eure fertige Demo. Auf deinem Rechner ist das alles schon erledigt; da genügen die zwei Start-Befehle von vorhin.
*diese Anleitung ist KI generiert und dient nur zur übersicht
*auch der Prototyp ist KI generiert das aufsetzen und die python scripte sind KI geschrieben und erstellt.
