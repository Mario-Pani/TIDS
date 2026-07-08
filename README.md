# Insulation Design Automation Tool (TIDS)

## Overview
TIDS is an engineering utility to merge insulation design parameters and optionally draw coil cross-sections in AutoCAD.

## Quick Start

### Windows Installer (Recommended)
1. Download this repository
2. Double-click `install.bat`
3. Follow the on-screen instructions
4. Click "TIDS" on your desktop to launch

### Manual Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Project Structure
- app.py: Thin Streamlit entrypoint that wires settings and main tabs.
- ui_settings.py: Settings popover UI (path edit, validate, open path/URL).
- tab_dups.py: DUPS tab UI and folder duplication flow.
- tab_new_job.py: NEW JOB tab UI and merge/edit/draw workflow.
- tab_schedule.py: SCHEDULE tab UI and schedule link launcher.
- ui_text.py: central EN/ES UI text dictionary and translation helpers.
- app_utils.py: UI-side helpers for decoding, editable-grid row mapping, text rebuild, and drawing preview SVG.
- dups_service.py: DUPS service logic for folder duplication, progress reporting, and post-copy artifacts.
- data_processor.py: parsing, unit type detection (Main, Series, Reactor), and deterministic merge logic.
- cad_bridge.py: AutoCAD COM bridge with guarded drawing and layer handling.
- config.py: central configuration loader/validator with defaults, file config, and env overrides.
- config.local.json: editable runtime configuration for managed paths.
- config.example.json: template configuration file.
- tests/test_data_processor.py: unit tests for parser and merge behavior.

## Requirements
- Windows with AutoCAD installed and available through COM.
- Python 3.11+ recommended.
- Python packages:

```bash
pip install streamlit pyautocad pywin32
```

## Run
```bash
streamlit run app.py
```

## Workflow
1. Upload base template file (.ehv or .txt).
2. Upload supplementary values file (.ehv or .txt), or let the app use configured path automatically.
3. Review detected topology and merged preview.
4. Download generated _Upload file.
5. Optionally click Draw Coils in AutoCAD.

## Hardening Notes
- File decoding now attempts utf-8, cp1252, and latin-1 before fallback replacement.
- Empty/unreadable uploads are blocked with explicit UI feedback.
- CAD bridge now validates geometry with OD > ID and positive height.
- CAD dependencies are imported defensively with readable error messages.
- COM lifecycle is explicitly initialized and uninitialized.
- Parameter parser skips empty lines, comments, and malformed records.

## Central Configuration
- Default managed path key: paths.spx_goldsboro.
- Supplementary file key: paths.supplementary_file.
- Runtime configuration file: config.local.json.
- Environment variable override: TIDS_SPX_GOLDSBORO_PATH.
- Environment variable override for supplementary file: TIDS_SUPPLEMENTARY_FILE.
- Configuration is loaded at app startup and shown in a collapsible panel.

## Testing
Run the unit tests with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

If your system uses py launcher:

```bash
py -m unittest discover -s tests -p "test_*.py"
```
