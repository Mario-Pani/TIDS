# TIDS - Estrategias de Actualización

## 📋 Resumen

Hay 3 formas de manejar actualizaciones según tu caso de uso:

---

## Estrategia 1: Instalación Independiente (Recomendado para usuarios)

Para usuarios finales que no clonan el repositorio.

### Primera instalación:
```bash
1. Descarga TIDS_distribution.zip desde GitHub Releases
2. Descomprime en una carpeta
3. Double-click: install.bat
```

### Para actualizar:
```bash
1. Descarga la nueva TIDS_distribution.zip
2. Descomprime en una NUEVA carpeta
3. Ejecuta install.bat en la nueva carpeta
```

**Ventaja:** Cada versión es independiente, sin riesgos de conflictos  
**Desventaja:** Ocupa más espacio en disco  

---

## Estrategia 2: Git Pull (Para desarrolladores)

Si clonaste el repositorio directamente.

### Primera instalación:
```bash
git clone https://github.com/Mario-Pani/TIDS.git
cd TIDS
install.bat
```

### Para actualizar:
```bash
check_updates.bat
```

O manualmente:
```bash
git pull origin main
pip install -r requirements.txt
```

**Ventaja:** Una sola carpeta, actualizaciones automáticas  
**Desventaja:** Requiere Git instalado  

---

## Estrategia 3: GitHub Desktop / VS Code (Interfaz gráfica)

Si prefieres no usar terminal.

### GitHub Desktop:
1. File → Clone repository
2. Pega: `https://github.com/Mario-Pani/TIDS`
3. Luego: Current Branch → Fetch → Pull
4. Ejecuta: `install.bat` desde la carpeta

### VS Code:
1. Command Palette (Ctrl+Shift+P)
2. "Git: Clone"
3. Pega: `https://github.com/Mario-Pani/TIDS`
4. Luego: Source Control → Fetch → Pull
5. Ejecuta: `install.bat`

**Ventaja:** No necesitas terminal ni comandos  
**Desventaja:** Una herramienta más instalada  

---

## 🔄 Flujo de Actualización Recomendado

### Para el Developer (tú):
```
1. Haces cambios en el código
2. git add .
3. git commit -m "descripcion"
4. Actualizar version.json + CHANGELOG.md
5. git push origin main
6. Crear GitHub Release (opcional)
7. Comunicar a usuarios: "Nueva version disponible"
```

### Para los usuarios:
```
Si usan Estrategia 1 (ZIP):
→ Descargar nuevo ZIP de Releases

Si usan Estrategia 2 (Git):
→ Ejecutar check_updates.bat

Si usan Estrategia 3 (GUI):
→ Pull desde GitHub Desktop / VS Code
```

---

## 📦 Cómo Hacer GitHub Releases

Cada que haces push importante:

1. Ve a: https://github.com/Mario-Pani/TIDS/releases
2. Click "Create a new release"
3. Tag: `v1.2.0` (ej)
4. Title: "TIDS v1.2.0 - Description"
5. Description: Copia del CHANGELOG.md
6. Sube: TIDS_distribution.zip
7. Publish Release

Usuarios verán el botón "Download" para obtener la versión.

---

## 🧹 Limpieza Después de Actualizar

### Si actualizaste y hay problemas:

```bash
# Limpiar cache de Python
del /s __pycache__
del /s *.pyc

# Reinstalar dependencias desde cero
pip uninstall -y streamlit pyautocad pywin32
pip install -r requirements.txt

# O simplemente ejecuta de nuevo:
install.bat
```

---

## 🔒 Versionamiento Semántico

TIDS sigue [SemVer](https://semver.org/):

- **v1.0.0** → MAJOR.MINOR.PATCH
- **v1.1.0** → Nueva feature (compatible con v1.0.0)
- **v1.1.1** → Bug fix
- **v2.0.0** → Breaking change (incompatible)

---

## 📣 Notificar a Usuarios

Opciones para comunicar actualizaciones:

1. **Email** - Envía noticia de nueva versión
2. **GitHub Releases** - Usuarios reciben notificación en GitHub
3. **In-app Banner** - Modificar `ui_text.py` para mostrar aviso
4. **Changelog** - Archivo CHANGELOG.md siempre accesible

---

## Preguntas Frecuentes

**¿Puedo actualizar sin perder mis configuraciones?**
→ Sí, `config.local.json` no se sobrescribe en pull/zip

**¿Qué pasa si no actualizo?**
→ La app sigue funcionando, pero sin nuevas features/fixes

**¿Cómo rollback a versión anterior?**
→ `git checkout v1.1.0` o descarga ZIP de release anterior

**¿Puedo tener dos versiones simultáneamente?**
→ Sí, en carpetas diferentes (Estrategia 1)

---

## Resumen de Comandos

| Tarea | Comando |
|-------|---------|
| Verificar actualizaciones | `check_updates.bat` |
| Descargar cambios | `git pull origin main` |
| Ver historial | `git log --oneline` |
| Ver versión actual | `type version.json` |
| Volver a versión anterior | `git checkout v1.1.0` |

