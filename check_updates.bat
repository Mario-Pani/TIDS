@echo off
REM TIDS Update Script - Descarga e instala la ultima version desde GitHub

setlocal enabledelayedexpansion

set TIDS_DIR=%~dp0
set TIDS_DIR=%TIDS_DIR:~0,-1%

echo.
echo ========================================
echo TIDS - Verificador de Actualizaciones
echo ========================================
echo.

REM Verificar que Git está disponible
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no encontrado en PATH
    echo Por favor instala Git desde https://git-scm.com
    pause
    exit /b 1
)

echo [OK] Git encontrado

REM Fetch latest changes sin descargarlos
echo.
echo Verificando actualizaciones desde GitHub...
cd /d "%TIDS_DIR%"
git fetch origin main >nul 2>&1

REM Comparar local vs remote
for /f %%A in ('git rev-parse HEAD') do set LOCAL_COMMIT=%%A
for /f %%A in ('git rev-parse origin/main') do set REMOTE_COMMIT=%%A

if "%LOCAL_COMMIT%"=="%REMOTE_COMMIT%" (
    echo.
    echo [OK] Ya tienes la ultima version!
    echo.
    echo Tu version: %LOCAL_COMMIT:~0,8%
    echo.
) else (
    echo.
    echo [!] Hay una nueva version disponible
    echo.
    echo Tu version:  %LOCAL_COMMIT:~0,8%
    echo Version nueva: %REMOTE_COMMIT:~0,8%
    echo.
    
    set /p CONFIRM="Deseas actualizar? (S/N): "
    if /i not "!CONFIRM!"=="S" (
        echo Actualizacion cancelada.
        pause
        exit /b 0
    )
    
    echo.
    echo Descargando cambios...
    git pull origin main
    
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo descargar los cambios
        echo Verifica tu conexion de internet
        pause
        exit /b 1
    )
    
    echo.
    echo Reinstalando dependencias...
    pip install -r "%TIDS_DIR%\requirements.txt" >nul 2>&1
    
    if errorlevel 1 (
        echo [ADVERTENCIA] Error al instalar dependencias
        echo Intenta manualmente: pip install -r requirements.txt
    ) else (
        echo [OK] Dependencias actualizadas
    )
    
    echo.
    echo ========================================
    echo Actualizacion completada exitosamente!
    echo ========================================
    echo.
    echo Nueva version: %REMOTE_COMMIT:~0,8%
    echo.
)

echo Presiona cualquier tecla para salir...
pause >nul
