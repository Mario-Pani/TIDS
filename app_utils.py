import html


def decode_uploaded_text(uploaded_file):
    raw_bytes = uploaded_file.getvalue()
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def decode_bytes(raw_bytes):
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def split_parameter_line(line):
    if "=" not in line:
        return line.strip(), ""
    variable, value = line.split("=", 1)
    return variable.strip(), value.strip()


def build_editor_rows(input_lines, upload_lines, seed_rows=None):
    rows = []
    seed_rows = seed_rows or []
    max_rows = max(len(input_lines), len(upload_lines), len(seed_rows))

    for index in range(max_rows):
        input_line = input_lines[index] if index < len(input_lines) else ""
        upload_line = upload_lines[index] if index < len(upload_lines) else ""
        seed_row = seed_rows[index] if index < len(seed_rows) else None
        input_variable, input_value = split_parameter_line(input_line)
        upload_variable, upload_value = split_parameter_line(upload_line)

        if isinstance(seed_row, dict):
            output_variable = str(seed_row.get("Output Variable", upload_variable))
            output_value = str(seed_row.get("Output Value", upload_value))
        else:
            output_variable, output_value = upload_variable, upload_value

        if not str(output_value).strip():
            output_value = "0"

        rows.append(
            {
                "EHV Original Field": input_variable,
                "EHV Original Value": input_value,
                "EHV Uploaded Field": output_variable,
                "EHV Uploaded Value": output_value,
            }
        )

    return rows


def rows_to_text(rows):
    output_lines = []
    for row in rows:
        output_variable = str(row.get("EHV Uploaded Field", "")).strip()
        output_value = str(row.get("EHV Uploaded Value", "")).strip()

        if not output_variable and not output_value:
            output_lines.append("")
            continue

        output_lines.append(f"{output_variable:<20}={output_value}")

    return "\n".join(output_lines)


def build_preview_html(rows):
    line_blocks = []
    for row in rows:
        output_variable = str(row.get("EHV Uploaded Field", "")).strip()
        output_value = str(row.get("EHV Uploaded Value", "")).strip()
        original_value = str(row.get("EHV Original Value", "")).strip()

        if not output_variable and not output_value:
            line_blocks.append('<div class="ehv-line">&nbsp;</div>')
            continue

        variable_text = html.escape(f"{output_variable:<20}")
        escaped_value = html.escape(output_value)
        changed = output_value != original_value

        if changed:
            value_html = f'<span class="changed-value">{escaped_value}</span>'
        else:
            value_html = escaped_value

        line_blocks.append(
            f'<div class="ehv-line"><span class="ehv-var">{variable_text}</span>=<span class="ehv-val">{value_html}</span></div>'
        )

    body = "".join(line_blocks)
    return f"""
    <style>
    .ehv-preview {{
        background: #0b1220;
        color: #dbe5f1;
        border-radius: 8px;
        padding: 12px;
        font-family: Consolas, 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.55;
        overflow-x: auto;
    }}
    .ehv-line {{
        white-space: pre;
    }}
    .changed-value {{
        background: #fef08a;
        color: #111827;
        padding: 0 2px;
        border-radius: 3px;
        font-weight: 700;
    }}
    </style>
    <div class="ehv-preview">{body}</div>
    """


def parse_merged_parameters(merged_text):
    params = {}
    for raw_line in merged_text.splitlines():
        if "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        clean_key = key.strip()
        if clean_key:
            params[clean_key.upper()] = value.strip()
    return params


def safe_float_any(params, *keys):
    for key in keys:
        value = params.get(key.upper())
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def build_drawing_preview_svg(merged_text):
    params = parse_merged_parameters(merged_text)

    window_width = safe_float_any(params, "WINDOW_WIDTH", "CORE_CL_CL_DIST")
    core_window_ht = safe_float_any(params, "CORE_WINDOW_HT")

    if window_width is None or core_window_ht is None or window_width <= 0 or core_window_ht <= 0:
        return "", "Missing or invalid WINDOW_WIDTH/CORE_WINDOW_HT for drawing preview."

    hv_bot = safe_float_any(params, "HV_BOT_ELCT_CLR", "HV_BOT_ELECT_CLR")
    if hv_bot is None:
        hv_bot = 0.0

    coils = []
    for name in ("LV", "HV", "RV", "TV"):
        coil_id = safe_float_any(params, f"{name}_COIL_ID")
        coil_od = safe_float_any(params, f"{name}_COIL_OD")
        coil_ht = safe_float_any(params, f"{name}_MECH_HT")
        if coil_id is None or coil_od is None or coil_ht is None:
            continue
        if coil_id <= 0 or coil_od <= coil_id or coil_ht <= 0:
            continue
        coils.append(
            {
                "name": name,
                "id": coil_id,
                "od": coil_od,
                "ht": coil_ht,
            }
        )

    hv = next((item for item in coils if item["name"] == "HV"), None)
    hv_height = hv["ht"] if hv else 0.0
    hv_center_y = hv_bot + (hv_height / 2.0)

    for coil in coils:
        coil["thickness"] = (coil["od"] - coil["id"]) / 2.0
        coil["x"] = coil["id"] / 2.0
        if coil["name"] == "HV":
            coil["y"] = hv_bot
        else:
            coil["y"] = hv_center_y - (coil["ht"] / 2.0)

    min_x = 0.0
    max_x = window_width
    min_y = 0.0
    max_y = core_window_ht
    for coil in coils:
        min_x = min(min_x, coil["x"])
        max_x = max(max_x, coil["x"] + coil["thickness"])
        min_y = min(min_y, coil["y"])
        max_y = max(max_y, coil["y"] + coil["ht"])

    viewport_w = 900.0
    viewport_h = 380.0
    margin = 24.0
    geo_w = max(max_x - min_x, 1.0)
    geo_h = max(max_y - min_y, 1.0)
    scale = min((viewport_w - 2 * margin) / geo_w, (viewport_h - 2 * margin) / geo_h)

    draw_w = geo_w * scale
    draw_h = geo_h * scale
    offset_x = (viewport_w - draw_w) / 2.0
    offset_y = (viewport_h - draw_h) / 2.0

    def sx(value):
        return offset_x + ((value - min_x) * scale)

    def sy(value):
        return offset_y + draw_h - ((value - min_y) * scale)

    core_x = sx(0.0)
    core_y = sy(core_window_ht)
    core_w = window_width * scale
    core_h = core_window_ht * scale

    coil_color = "#ef4444"
    coil_stroke = "#7f1d1d"
    coil_svg_parts = []
    for coil in coils:
        x = sx(coil["x"])
        y = sy(coil["y"] + coil["ht"])
        w = coil["thickness"] * scale
        h = coil["ht"] * scale
        coil_svg_parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{coil_color}" fill-opacity="0.28" stroke="{coil_stroke}" stroke-width="2"/>'
        )
        coil_svg_parts.append(
            f'<text x="{(x + w + 4):.2f}" y="{(y + 14):.2f}" font-size="12" fill="#0f172a">{coil["name"]}</text>'
        )

    svg = f"""
    <svg width="100%" viewBox="0 0 {viewport_w:.0f} {viewport_h:.0f}" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="{viewport_w:.0f}" height="{viewport_h:.0f}" fill="#f8fafc"/>
      <rect x="{core_x:.2f}" y="{core_y:.2f}" width="{core_w:.2f}" height="{core_h:.2f}" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
      {''.join(coil_svg_parts)}
      <text x="16" y="22" font-size="14" fill="#0f172a">900 Drawing Preview (Core Window + Coil Geometry)</text>
    </svg>
    """
    return svg, ""
