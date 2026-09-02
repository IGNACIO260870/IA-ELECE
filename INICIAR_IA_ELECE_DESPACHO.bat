@echo off
REM ============================================================
REM   IA ELECE  -  MODO DESPACHO
REM
REM   Igual que INICIAR_IA_ELECE.bat, pero escuchando en toda la
REM   red en vez de solo en este ordenador, para que Mamen entre
REM   desde su navegador.
REM
REM   AL ESCUCHAR EN RED SE ENCIENDE LA PUERTA: pide usuario y
REM   clave. Las claves se ponen con
REM       python webapp\crear_usuario.py mamen
REM   desde la carpeta de Colibri. Sin clave puesta, no entra
REM   nadie.
REM
REM   Direccion para Mamen:   http://192.168.0.31:8100
REM   (esa es la IP de este equipo; si cambia, cambia la direccion)
REM
REM   Este ordenador tiene que estar encendido y con esta ventana
REM   abierta. El dia que IA ELECE viva en el servidor del
REM   despacho, esto se lanza alli y da igual quien apague su PC.
REM ============================================================
cd /d "%~dp0"
set IA_ELECE_HOST=0.0.0.0
set IA_ELECE_PUERTO=8100
set PY=C:\Users\Ignacio\Desktop\colibri-servidor\.venv\Scripts\python.exe
if not exist "%PY%" set PY=python
echo.
echo   IA ELECE en modo despacho.
echo   Mamen entra en:  http://192.168.0.31:8100
echo.
"%PY%" servidor.py
pause
