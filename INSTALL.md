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

### Dependencias Opcionales:

#### AutoCAD Drawing Support
Si quieres usar la función "Draw" en AutoCAD:
```bash
pip install -r requirements-optional.txt
```

**Requisitos:**
- AutoCAD instalado en Windows
- Python en la misma máquina que AutoCAD

**Si NO instalas esto:** La app funciona normalmente, pero el botón "Draw" estará deshabilitado (aparecerá con ⚠️)

---

## Opción 2: Ejecución Manual

Si el instalador no funciona, ejecuta manualmente:

```bash
# Dependencias core:
pip install -r requirements.txt

# Dependencias opcionales (si quieres AutoCAD):
pip install -r requirements-optional.txt

# Iniciar app:
streamlit run app.py
```

---

## Archivos incluidos

- `app.py` - Aplicación principal (Streamlit)
- `requirements.txt` - Dependencias obligatorias
- `requirements-optional.txt` - Dependencias opcionales (CAD)
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

### Error: "No module named 'pyautocad'"
→ Normal si no quieres usar AutoCAD. La app funciona sin él.
→ Si quieres dibujar en CAD, instala:
```bash
pip install -r requirements-optional.txt
```
→ Si `pip install pyautocad` falla, puede ser porque:
  - No tienes VC++ Build Tools instalado
  - AutoCAD no está en la máquina
  - En ese caso, la app sigue funcionando sin la función Draw

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
