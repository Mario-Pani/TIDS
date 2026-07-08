# Changelog - TIDS

## Version History

### v1.2.0 (2026-07-08) - Installation & Packaging
- ✨ Added automatic installer (`install.bat`)
- ✨ Added update checker (`check_updates.bat`)
- ✨ Added distribution packager (`make_distribution.bat`)
- 🐛 Fixed VPN latency issues with path caching (30s TTL)
- 📦 Corrected schedule_url format in config

**Breaking Changes:** None

**Migration:** For existing users: run `check_updates.bat` to update

---

### v1.1.0 (2026-07-07) - Bilingual UI & Modularization
- ✨ Added EN/ES bilingual interface with language selector
- 🔧 Refactored app.py into modular components (tab_*.py, ui_*.py)
- 🎯 Separated concerns: UI, services, domain logic
- ✅ All 9 tests passing

**Breaking Changes:** None

**Files Changed:** app.py, ui_text.py, tab_dups.py, tab_new_job.py, tab_schedule.py, ui_settings.py

---

### v1.0.0 (2026-07-01) - Initial Release
- Core TIDS functionality
- File merge and CAD drawing
- AutoCAD integration
- Basic configuration system

---

## Installation & Updates

### First Time Setup
```bash
# Run installer
install.bat
```

### Check for Updates
```bash
# Check if new version available
check_updates.bat
```

### Manual Update (Git)
```bash
cd C:\path\to\TIDS
git pull origin main
pip install -r requirements.txt
```

---

## Version Format

Follows [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH**
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

---

## Upcoming Features (Roadmap)

- [ ] Dark mode support
- [ ] Export to PDF
- [ ] Batch file processing
- [ ] Web deployment (Streamlit Cloud)
- [ ] Unit type AI detection

---

## Support

For issues or feature requests, visit:
https://github.com/Mario-Pani/TIDS/issues
