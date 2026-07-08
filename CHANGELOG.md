# Changelog - TIDS

## Version History

### v1.1.0 (2026-07-08) - Bilingual UI & Modularization & CAD Optional
- ✨ Added EN/ES bilingual interface with language selector
- 🔧 Refactored app.py into modular components (tab_*.py, ui_*.py)
- 🎯 Separated concerns: UI, services, domain logic
- 🐛 Fixed VPN latency issues with path caching (30s TTL)
- 🔧 Made AutoCAD (pyautocad) optional dependency
- 🎯 App works without CAD installed (Draw button disabled)
- ✅ All 9 tests passing

**Breaking Changes:** None

**Files:** app.py, ui_text.py, tab_dups.py, tab_new_job.py, tab_schedule.py, ui_settings.py, cad_check.py

---

### v1.0.0 (2026-07-01) - Initial Release
- Core TIDS functionality
- File merge and CAD drawing
- AutoCAD integration
- Basic configuration system

---

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

For CAD support:
```bash
pip install pyautocad
```

---

## Support

For issues or feature requests, visit:
https://github.com/Mario-Pani/TIDS/issues
