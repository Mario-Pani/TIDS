def _iter_key_value_pairs(file_content):
    for raw_line in file_content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        clean_key = key.strip()
        if clean_key:
            yield clean_key, value.strip()


def _subtract_offset(value, offset):
    try:
        adjusted = float(value) - offset
    except (TypeError, ValueError):
        return value

    return ("{0:.12f}".format(adjusted)).rstrip("0").rstrip(".")


def _apply_main_unit_adjustments(final_parameters):
    key_lookup = {key.upper(): key for key in final_parameters.keys()}

    for logical_key in ("CORE_WINDOW_HT", "HV_BOT_ELCT_CLR", "HV_BOT_ELECT_CLR"):
        actual_key = key_lookup.get(logical_key)
        if actual_key:
            final_parameters[actual_key] = _subtract_offset(final_parameters[actual_key], 0.31)


def identify_unit_type(file_content, file_name):
    """Identifies if the unit is Main, Series, or Reactor."""
    parameters = dict(_iter_key_value_pairs(file_content))
    parameters_upper = {key.upper(): value for key, value in parameters.items()}

    if "REACTOR_GEN" in parameters_upper:
        return "Reactor"
    gm_value = parameters_upper.get("GM$", "").strip().upper()
    if "SERIES" in file_name.upper() or gm_value.endswith("S"):
        return "Series"
    return "Main Unit"


def process_files(base_content, base_name, extra_content, apply_main_adjustments=True):
    """Merges base parameters with extra parameters."""
    unit_type = identify_unit_type(base_content, base_name)

    final_parameters = {}
    keys_order = []

    for clean_key, clean_value in _iter_key_value_pairs(base_content):
        final_parameters[clean_key] = clean_value
        if clean_key not in keys_order:
            keys_order.append(clean_key)

    for clean_key, clean_value in _iter_key_value_pairs(extra_content):
        final_parameters[clean_key] = clean_value
        if clean_key not in keys_order:
            keys_order.append(clean_key)

    if apply_main_adjustments and unit_type == "Main Unit":
        _apply_main_unit_adjustments(final_parameters)

    output_lines = []
    for key in keys_order:
        output_lines.append(f"{key:<20}={final_parameters[key]}")

    return unit_type, "\n".join(output_lines)
