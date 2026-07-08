# TIDS - Instalación y Distribución

## Opción 1: Instalación Simple (Recomendado)

### Pasos:
1. **Descarga el proyecto:**
   - Descarga esta carpeta o clónala desde GitHub: https://github.com/Mario-Pani/TIDS

2. **Ejecuta el instalador:**
   - Abre la carpeta del proyecto
   - Haz doble clic en `install.bat`
   - Espera a que instale las dependencias
   - Se creará un acceso directo "TIDS" en tu escritorio

3. **Usa la app:**
   - Haz doble clic en "TIDS" en el escritorio
   - O ejecuta `TIDS.bat` desde la carpeta del proyecto

### Requisitos previos:
- **Python 3.11+** instalado y en PATH
  - Descarga desde: https://www.python.org/downloads/
  - ✓ Marca la opción "Add Python to PATH" durante la instalación

- **Conexión VPN activada** (para acceder a F:\)

- **AutoCAD instalado** (opcional, solo si usas la función "Draw")

---

## Opción 2: Ejecución Manual

Si el instalador no funciona, ejecuta manualmente:

```bash
# En la carpeta del proyecto:
pip install -r requirements.txt
streamlit run app.py
```

---

## Archivos incluidos

- `app.py` - Aplicación principal (Streamlit)
- `requirements.txt` - Dependencias Python
- `config.local.json` - Configuración (rutas F:\)
- `TIDS.bat` - Launcher de la app
- `install.bat` - Instalador de dependencias

---

## Solución de problemas

### Error: "Python no encontrado"
→ Instala Python 3.11+ desde https://www.python.org

### Error: "No se puede acceder a F:\"
→ Activa la conexión VPN primero, luego reinicia la app

### Error: "streamlit: command not found"
→ Abre una nueva ventana de PowerShell y reinicia el instalador

### La app es lenta
→ Normal en VPN. Los archivos están en red (F:\). El cacheo optimiza esto.

---

## Actualizaciones

### Verificar si hay nuevas versiones:
```bash
check_updates.bat
```

Este script:
1. Conecta con GitHub
2. Verifica si hay cambios nuevos
3. Si los hay, pregunta si deseas actualizar
4. Descarga e instala automáticamente

### Actualización Manual:
```bash
cd C:\ruta\a\TIDS
git pull origin main
pip install -r requirements.txt
```

---

## Historial de Cambios

Ver [CHANGELOG.md](CHANGELOG.md) para lista completa de versiones.

---

## Contacto

Para reportar problemas o sugerencias: 
[Tu email o GitHub issues]
