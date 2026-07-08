@echo off
REM TIDS Installer - Crea acceso directo en el escritorio
setlocal enabledelayedexpansion

set TIDS_DIR=%~dp0
set TIDS_DIR=%TIDS_DIR:~0,-1%
set DESKTOP=%USERPROFILE%\Desktop

echo.
echo ========================================
echo TIDS - Transformer Insulation Design System
echo ========================================
echo.
echo Directorio de instalacion: %TIDS_DIR%
echo Escritorio: %DESKTOP%
echo.

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado.
    echo Por favor instala Python 3.11+ desde https://www.python.org
    echo y añadelo al PATH.
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r "%TIDS_DIR%\requirements.txt" >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Verifica tu conexion de internet
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas

REM Crear acceso directo en el escritorio
echo.
echo Creando acceso directo en el escritorio...

set SHORTCUT=%DESKTOP%\TIDS.lnk
set BATCH_FILE=%TIDS_DIR%\TIDS.bat
set ICON_PATH=%TIDS_DIR%\app.py

REM Crear acceso directo usando PowerShell
powershell -NoProfile -Command "^
    $WshShell = New-Object -ComObject WScript.Shell; ^
    $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); ^
    $Shortcut.TargetPath = '%BATCH_FILE%'; ^
    $Shortcut.WorkingDirectory = '%TIDS_DIR%'; ^
    $Shortcut.Description = 'Transformer Insulation Design System'; ^
    $Shortcut.IconLocation = 'C:\Windows\System32\wscript.exe'; ^
    $Shortcut.Save()
" >nul 2>&1

if exist "%SHORTCUT%" (
    echo [OK] Acceso directo creado: %SHORTCUT%
) else (
    echo [ADVERTENCIA] No se pudo crear el acceso directo automaticamente
    echo Puedes ejecutar TIDS.bat manualmente desde: %TIDS_DIR%
)

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para iniciar TIDS:
echo - Haz doble clic en "TIDS" en el escritorio
echo - O ejecuta: %BATCH_FILE%
echo.
echo Presiona cualquier tecla para salir...
pause >nul
