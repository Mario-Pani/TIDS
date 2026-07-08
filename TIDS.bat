@echo off
REM TIDS - Transformer Insulation Design System
REM Launcher script

cd /d "%~dp0"

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado en PATH
    echo Por favor instala Python 3.11+ desde https://www.python.org
    pause
    exit /b 1
)

REM Verificar dependencias
echo Verificando dependencias...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Iniciar Streamlit
echo Iniciando TIDS...
streamlit run app.py
