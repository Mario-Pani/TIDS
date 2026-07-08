@echo off
REM Script para crear un paquete de distribucion de TIDS
REM Genera: TIDS_distribution.zip

setlocal enabledelayedexpansion

set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-1%
set DIST_NAME=TIDS_distribution
set DIST_DIR=%PROJECT_DIR%\%DIST_NAME%

echo.
echo ========================================
echo Empaquetador de TIDS
echo ========================================
echo.
echo Directorio del proyecto: %PROJECT_DIR%
echo Destino: %DIST_DIR%
echo.

REM Limpiar si existe
if exist "%DIST_DIR%" (
    echo Limpiando distribucion anterior...
    rmdir /s /q "%DIST_DIR%" >nul 2>&1
)

REM Crear directorio de distribucion
mkdir "%DIST_DIR%"

REM Copiar archivos esenciales
echo Copiando archivos...

copy "%PROJECT_DIR%\app.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\app_utils.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\cad_bridge.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\config.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\config.local.json" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\config.example.json" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\data_processor.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\dups_service.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\tab_dups.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\tab_new_job.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\tab_schedule.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\ui_settings.py" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\ui_text.py" "%DIST_DIR%\" >nul

copy "%PROJECT_DIR%\requirements.txt" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\README.md" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\INSTALL.md" "%DIST_DIR%\" >nul

copy "%PROJECT_DIR%\TIDS.bat" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%\install.bat" "%DIST_DIR%\" >nul

echo [OK] Archivos copiados

REM Crear ZIP (requiere 7-Zip o usar PowerShell)
echo.
echo Comprimiendo carpeta...

REM Intentar con PowerShell
powershell -NoProfile -Command "^
    if (Test-Path '%PROJECT_DIR%\%DIST_NAME%.zip') { Remove-Item '%PROJECT_DIR%\%DIST_NAME%.zip' }; ^
    Add-Type -AssemblyName System.IO.Compression.FileSystem; ^
    [System.IO.Compression.ZipFile]::CreateFromDirectory('%DIST_DIR%', '%PROJECT_DIR%\%DIST_NAME%.zip')
" >nul 2>&1

if exist "%PROJECT_DIR%\%DIST_NAME%.zip" (
    echo [OK] Distribucion creada: %DIST_NAME%.zip
    echo.
    echo Ubicacion: %PROJECT_DIR%\%DIST_NAME%.zip
) else (
    echo [ERROR] No se pudo crear el ZIP
    echo Verifica que PowerShell este disponible
)

echo.
echo ========================================
echo Contenido de la distribucion:
echo ========================================
dir /b "%DIST_DIR%"

echo.
echo Presiona cualquier tecla para salir...
pause >nul
