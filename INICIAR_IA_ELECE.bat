@echo off
REM ============================================================
REM   IA ELECE  -  la parte de abogacia del despacho.
REM
REM   Doble clic aqui: levanta el servidor y abre la pantalla.
REM   Colibri escucha en el 8000 y este en el 8100, asi que los
REM   dos pueden estar abiertos a la vez sin estorbarse.
REM
REM   De momento usa el Python de Colibri, que ya tiene todo
REM   instalado. Cuando IA ELECE se lleve al servidor del
REM   despacho tendra el suyo propio.
REM ============================================================
cd /d "%~dp0"
set PY=C:\Users\Ignacio\Desktop\colibri-servidor\.venv\Scripts\python.exe
if not exist "%PY%" set PY=python
start "" http://127.0.0.1:8100/
"%PY%" servidor.py
pause
