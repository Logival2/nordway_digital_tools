@echo off
rem NORDWAY Tools : ouvre les outils dans le navigateur, servis par un petit serveur local.
rem (Ouverts en double-clic sur index.html, certains outils ne peuvent pas charger leurs fichiers :
rem  relief du Mont Blanc, Brand images, export d'images.)  Fermer cette fenêtre arrête le serveur.
cd /d "%~dp0"
title NORDWAY Tools - http://localhost:8000
start "" cmd /c "timeout /t 1 >nul & start http://localhost:8000/"
where python >nul 2>nul && (python -m http.server 8000 --bind 127.0.0.1) || (py -m http.server 8000 --bind 127.0.0.1)
pause
