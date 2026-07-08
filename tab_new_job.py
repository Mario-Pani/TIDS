import os

import streamlit as st

from app_utils import (
    build_drawing_preview_svg,
    build_editor_rows,
    build_preview_html,
    decode_bytes,
    decode_uploaded_text,
    rows_to_text,
)
from cad_bridge import draw_smart_coils
from data_processor import process_files
from ui_text import t


@st.cache_data(ttl=30, show_spinner=False)
def _path_is_file(path):
    try:
        return os.path.isfile(path)
    except OSError:
        return False


def _render_editor_styles():
    st.markdown(
        """
        <style>
        div[data-testid="stDataEditor"] input[disabled],
        div[data-testid="stDataEditor"] textarea[disabled],
        div[data-testid="stDataEditor"] [aria-disabled="true"] {
            background: #dbe4f0 !important;
            color: #334155 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stDataEditor"] input:not([disabled]),
        div[data-testid="stDataEditor"] textarea:not([disabled]) {
            background: #eaf7ea !important;
            color: #0f172a !important;
        }

        div[data-testid="stDataEditor"] [role="gridcell"] {
            border-color: #cbd5e1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_new_job_tab(settings, lang):
    st.markdown(t(lang, "new_job_intro"))

    configured_extra_path = settings.get("paths", {}).get("supplementary_file", "")
    configured_extra_exists = bool(configured_extra_path) and _path_is_file(configured_extra_path)

    st.subheader(t(lang, "base_file"))
    base_file = st.file_uploader(t(lang, "upload_customer_file"), type=["ehv", "txt"], key="base")

    st.divider()

    st.subheader(t(lang, "extra_values_file"))
    if configured_extra_exists:
        extra_file = None
        st.success(t(lang, "using_default_supplementary", name=os.path.basename(configured_extra_path)))
    else:
        extra_file = st.file_uploader(t(lang, "upload_extra_values"), type=["ehv", "txt"], key="extra")

    st.divider()

    if not (base_file and (extra_file or configured_extra_exists)):
        if configured_extra_exists:
            st.info(t(lang, "upload_base_to_proceed"))
        else:
            st.info(t(lang, "upload_both_to_proceed"))
        return

    base_content = decode_uploaded_text(base_file)
    if extra_file:
        extra_content = decode_uploaded_text(extra_file)
        extra_name = extra_file.name
    else:
        with open(configured_extra_path, "rb") as handle:
            extra_content = decode_bytes(handle.read())
        extra_name = os.path.basename(configured_extra_path)

    if not base_content.strip() or not extra_content.strip():
        st.error(t(lang, "uploaded_files_empty"))
        st.stop()

    try:
        unit_type, original_merged_data = process_files(
            base_content,
            base_file.name,
            extra_content,
            apply_main_adjustments=False,
        )
        _, merged_data = process_files(
            base_content,
            base_file.name,
            extra_content,
            apply_main_adjustments=True,
        )
    except Exception as exc:
        st.error(t(lang, "processing_failed", exc=exc))
        st.stop()

    st.success(t(lang, "processing_complete", unit_type=unit_type))
    st.caption(t(lang, "supplementary_source", name=extra_name))

    st.subheader(t(lang, "review_edit_merged"))
    _render_editor_styles()

    merged_signature = (
        f"{base_file.name}:{len(original_merged_data)}:{hash(original_merged_data)}:"
        f"{len(merged_data)}:{hash(merged_data)}"
    )
    if st.session_state.get("merged_signature") != merged_signature:
        st.session_state["merged_signature"] = merged_signature
        st.session_state["edited_rows"] = build_editor_rows(
            original_merged_data.splitlines(),
            merged_data.splitlines(),
        )

    original_lines = original_merged_data.splitlines()
    upload_lines = merged_data.splitlines()
    rows = st.session_state.get("edited_rows")
    if not rows:
        rows = build_editor_rows(original_lines, upload_lines)

    editor_data = st.data_editor(
        rows,
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        height=420,
        disabled=["EHV Original Field", "EHV Original Value", "EHV Uploaded Field"],
        key="merged_editor_grid",
    )

    if hasattr(editor_data, "to_dict"):
        records = editor_data.to_dict("records")
    elif isinstance(editor_data, list):
        records = editor_data
    else:
        records = rows

    for row in records:
        uploaded_value = str(row.get("EHV Uploaded Value", "")).strip()
        if not uploaded_value:
            row["EHV Uploaded Value"] = "0"

    st.session_state["edited_rows"] = records
    edited_merged_data = rows_to_text(records)

    col_action1, col_action2 = st.columns(2)

    with col_action1:
        base_name, ext = os.path.splitext(base_file.name)
        new_file_name = f"{base_name}_Upload{ext}"

        st.download_button(
            label=t(lang, "download"),
            icon=":material/download:",
            data=edited_merged_data,
            file_name=new_file_name,
            mime="text/plain",
            use_container_width=True,
            help=t(lang, "download_help", name=new_file_name),
        )

    with col_action2:
        if st.button(
            t(lang, "draw"),
            type="primary",
            icon=":material/architecture:",
            use_container_width=True,
            help=t(lang, "draw_help"),
        ):
            with st.spinner(t(lang, "connecting_cad")):
                success, message = draw_smart_coils(edited_merged_data)

                if success:
                    st.success(message)
                else:
                    st.error(message)

    preview_tab_1, preview_tab_2 = st.tabs([t(lang, "preview_tab"), t(lang, "drawing_preview_tab")])

    with preview_tab_1:
        st.markdown(build_preview_html(records), unsafe_allow_html=True)

    with preview_tab_2:
        drawing_svg, drawing_error = build_drawing_preview_svg(edited_merged_data)
        if drawing_error:
            st.info(drawing_error)
        else:
            st.markdown(drawing_svg, unsafe_allow_html=True)
