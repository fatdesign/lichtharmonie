@echo off
echo ===================================================
echo   LICHTHARMONIE by Aksu - Website Server
echo ===================================================
echo.
echo Starte lokalen Server...
echo Bitte oeffne im Browser: http://localhost:8000
echo.
echo (Fenster offen lassen, solange die Seite laufen soll)
echo.
python -m http.server 8000
pause
