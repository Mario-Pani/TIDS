import json
import os
from copy import deepcopy
from pathlib import Path


DEFAULT_SETTINGS = {
    "paths": {
        "spx_goldsboro": r"F:\\50_GlobalEngineering\\10_Tech_Services_AM\\Projects\\Projects-Customer\\SPX\\Goldsboro",
        "supplementary_file": r"F:\\50_GlobalEngineering\\10_Tech_Services_AM\\Projects\\Projects-Customer\\SPX\\Goldsboro\\TIDA A xtra values flat.ehv",
        "nuevo_diseno": r"F:\\50_GlobalEngineering\\10_Tech_Services_AM\\Projects\\Projects-Customer\\SPX\\Goldsboro",
        "manuales": r"F:\\50_GlobalEngineering\\10_Tech_Services_AM\\Projects\\Projects-Customer\\SPX\\Goldsboro",
        "disenos": r"F:\\50_GlobalEngineering\\10_Tech_Services_AM\\Projects\\Projects-Customer\\SPX\\Goldsboro",
        "dups_template_file": "DuplicatedDesign.docx",
        "schedule_url": "https://weidmanngroup.sharepoint.com/:x:/r/sites/w1006/_layouts/15/Doc.aspx?sourcedoc=%7BBF7479AC-3FAF-4850-B272-EDC6578152DD%7D&file=2026%20Goldsboro%20Schedule.xlsx&action=default&mobileredirect=true&DefaultItemOpen=1&wdOrigin=SHAREPOINT.SHELL%2CAPPHOME-WEB.UNAUTH%2CAPPHOME-WEB.SHELL.SIGNIN%2CAPPHOME-WEB.FILEBROWSER.RECENT&wdPreviousSession=da18e57d-7459-4132-80b8-a0170350dc3b&wdPreviousSessionSrc=AppHomeWeb&ct=1781636233823"
    }
}


def _deep_merge(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def _normalize_path(path_value):
    return str(Path(path_value).expanduser())


def _apply_env_overrides(settings):
    env_path = os.getenv("TIDS_SPX_GOLDSBORO_PATH")
    if env_path:
        settings["paths"]["spx_goldsboro"] = env_path
    env_supp_file = os.getenv("TIDS_SUPPLEMENTARY_FILE")
    if env_supp_file:
        settings["paths"]["supplementary_file"] = env_supp_file
    env_nuevo_diseno = os.getenv("TIDS_NUEVO_DISENO_PATH")
    if env_nuevo_diseno:
        settings["paths"]["nuevo_diseno"] = env_nuevo_diseno
    env_manuales = os.getenv("TIDS_MANUALES_PATH")
    if env_manuales:
        settings["paths"]["manuales"] = env_manuales
    env_disenos = os.getenv("TIDS_DISENOS_PATH")
    if env_disenos:
        settings["paths"]["disenos"] = env_disenos
    env_dups_template = os.getenv("TIDS_DUPS_TEMPLATE_FILE")
    if env_dups_template:
        settings["paths"]["dups_template_file"] = env_dups_template
    env_schedule_url = os.getenv("TIDS_SCHEDULE_URL")
    if env_schedule_url:
        settings["paths"]["schedule_url"] = env_schedule_url


def _validate_paths(settings):
    errors = []
    for name, value in settings.get("paths", {}).items():
        if not value:
            errors.append(f"Path '{name}' is empty.")
            continue
        if name.endswith("_url") or str(value).lower().startswith(("http://", "https://")):
            continue
        path_obj = Path(value)
        if not path_obj.exists():
            errors.append(f"Path '{name}' does not exist: {value}")
            continue
        if name.endswith("_file") and not path_obj.is_file():
            errors.append(f"Path '{name}' must be a file: {value}")
    return errors


def load_settings(config_file="config.local.json"):
    settings = deepcopy(DEFAULT_SETTINGS)
    config_path = Path(config_file)

    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
            if isinstance(loaded, dict):
                _deep_merge(settings, loaded)

    _apply_env_overrides(settings)

    for key, value in settings.get("paths", {}).items():
        settings["paths"][key] = _normalize_path(value)

    return settings


def validate_settings(settings):
    return _validate_paths(settings)


def save_settings(settings, config_file="config.local.json"):
    config_path = Path(config_file)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    serializable = deepcopy(settings)
    with config_path.open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=2, ensure_ascii=True)
        handle.write("\n")
