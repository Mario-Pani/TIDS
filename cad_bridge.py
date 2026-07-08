import array


def _parse_parameters(merged_text):
    params = {}
    for raw_line in merged_text.splitlines():
        if "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        clean_key = key.strip()
        if clean_key:
            params[clean_key] = value.strip()
    return params


def _safe_float(params, key):
    value = params.get(key)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_float_any(params_upper, *keys):
    for key in keys:
        value = params_upper.get(key.upper())
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def _ensure_layer(acad, layer_name):
    layer_name_upper = layer_name.upper()
    layer_colors = {
        "CORE_WINDOW": 2,  # Yellow
        "HV_COIL": 1,      # Red
        "LV_COIL": 1,      # Red
        "RV_COIL": 1,      # Red
        "TV_COIL": 1,      # Red
        "HV_INSUL": 3,     # Green
        "LV_INSUL": 3,     # Green
        "RV_INSUL": 3,     # Green
        "TV_INSUL": 3,     # Green
    }
    color_index = layer_colors.get(layer_name_upper)

    try:
        layer_obj = acad.doc.Layers.Item(layer_name)
    except Exception:
        layer_obj = acad.doc.Layers.Add(layer_name)

    color_applied = False
    if color_index is not None:
        try:
            layer_obj.Color = color_index
            color_applied = True
        except Exception:
            color_applied = False

    return color_index, color_applied


def _draw_closed_polyline(acad, layer_name, points):
    pts_array = array.array("d", points)
    color_index, color_applied = _ensure_layer(acad, layer_name)
    pline = acad.model.AddPolyline(pts_array)
    pline.Closed = True
    pline.Layer = layer_name
    if color_index is not None:
        try:
            # Prefer ByLayer when layer color assignment succeeded.
            pline.Color = 256 if color_applied else color_index
        except Exception:
            pass


def _draw_rectangle(acad, layer_name, left, bottom, width, height):
    right = left + width
    top = bottom + height
    points = [
        left, bottom, 0.0,
        right, bottom, 0.0,
        right, top, 0.0,
        left, top, 0.0,
        left, bottom, 0.0,
    ]
    _draw_closed_polyline(acad, layer_name, points)


def draw_smart_coils(merged_text):
    try:
        import pythoncom
        from pyautocad import Autocad
    except ImportError as exc:
        return False, f"Missing CAD dependency: {exc}"

    pythoncom.CoInitialize()
    try:
        try:
            acad = Autocad(create_if_not_exists=True)
        except Exception as exc:
            return False, f"AutoCAD connection error: {exc}"

        params = _parse_parameters(merged_text)
        if not params:
            return False, "No key/value parameters were found in merged data."

        params_upper = {k.upper(): v for k, v in params.items()}

        # Engineering fallback: if WINDOW_WIDTH is missing, use CORE_CL_CL_DIST.
        window_width = _safe_float_any(params_upper, "WINDOW_WIDTH")
        if window_width is None:
            window_width = _safe_float_any(params_upper, "CORE_CL_CL_DIST")
            if window_width is not None:
                params["WINDOW_WIDTH"] = str(window_width)
                params_upper["WINDOW_WIDTH"] = str(window_width)

        core_window_ht = _safe_float_any(params_upper, "CORE_WINDOW_HT")
        hv_bot_elect_clr = _safe_float_any(params_upper, "HV_BOT_ELCT_CLR", "HV_BOT_ELECT_CLR")
        # Geometry values should come from the merged data as-is.
        # Main Unit offsets are applied in data_processor to avoid double adjustment.
        adjusted_core_window_ht = core_window_ht
        adjusted_hv_bot_elect_clr = hv_bot_elect_clr

        items_drawn = 0
        draw_errors = []

        if window_width is not None and adjusted_core_window_ht is not None:
            if window_width > 0 and adjusted_core_window_ht > 0:
                try:
                    _draw_rectangle(acad, "CORE_WINDOW", 0.0, 0.0, window_width, adjusted_core_window_ht)
                    items_drawn += 1
                except Exception as exc:
                    draw_errors.append(f"CORE_WINDOW: {exc}")

        coils = [
            ("LV_COIL", "LV_COIL_ID", "LV_COIL_OD", "LV_MECH_HT"),
            ("HV_COIL", "HV_COIL_ID", "HV_COIL_OD", "HV_MECH_HT"),
            ("RV_COIL", "RV_COIL_ID", "RV_COIL_OD", "RV_MECH_HT"),
            ("TV_COIL", "TV_COIL_ID", "TV_COIL_OD", "TV_MECH_HT"),
        ]

        hv_height = _safe_float(params, "HV_MECH_HT") or 0.0
        hv_reference_y = adjusted_hv_bot_elect_clr if adjusted_hv_bot_elect_clr is not None else 0.0
        hv_center_y = hv_reference_y + (hv_height / 2.0)

        for layer, id_key, od_key, ht_key in coils:
            id_val = _safe_float(params, id_key)
            od_val = _safe_float(params, od_key)
            ht_val = _safe_float(params, ht_key)

            if id_val is None or od_val is None or ht_val is None:
                continue

            # Logical geometry guard: OD must be larger than ID and height must be positive.
            if not (id_val > 0 and od_val > id_val and ht_val > 0):
                continue

            try:
                radial_thickness = (od_val - id_val) / 2.0
                x = id_val / 2.0
                if layer == "HV_COIL":
                    y_bottom = hv_reference_y
                else:
                    y_bottom = hv_center_y - (ht_val / 2.0)

                points = [
                    x, y_bottom, 0.0,
                    x + radial_thickness, y_bottom, 0.0,
                    x + radial_thickness, y_bottom + ht_val, 0.0,
                    x, y_bottom + ht_val, 0.0,
                    x, y_bottom, 0.0,
                ]

                _draw_closed_polyline(acad, layer, points)
                items_drawn += 1
            except Exception as exc:
                draw_errors.append(f"{layer}: {exc}")

        if items_drawn > 0:
            if draw_errors:
                return True, f"Cross-section drawn. Some layers failed: {'; '.join(draw_errors)}"
            return True, f"Cross-section drawn"

        if draw_errors:
            return False, f"Nothing drawn. Drawing errors: {'; '.join(draw_errors)}"
        return False, "No valid geometry found on data."
    finally:
        pythoncom.CoUninitialize()