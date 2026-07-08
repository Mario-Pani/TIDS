import os

import streamlit as st

from config import load_settings, save_settings, validate_settings
from ui_text import LANG_OPTIONS, get_path_labels, t


def render_settings_popover(settings, lang):
    with st.popover(":material/settings:", use_container_width=True):
        st.markdown(f"**{t(lang, 'settings_title')}**")

        language_codes = list(LANG_OPTIONS.keys())
        current_lang = st.selectbox(
            t(lang, "language_label"),
            options=language_codes,
            format_func=lambda code: LANG_OPTIONS.get(code, code),
            index=language_codes.index(lang) if lang in language_codes else 0,
            key="ui_language_selector",
        )
        if current_lang != st.session_state.get("ui_lang"):
            st.session_state["ui_lang"] = current_lang
            st.rerun()
        st.session_state["ui_lang"] = current_lang
        lang = current_lang

        path_labels = get_path_labels(lang)

        available_keys = list(path_labels.keys())
        selected_path_key = st.selectbox(
            t(lang, "select_path_to_edit"),
            options=available_keys,
            format_func=lambda key: path_labels.get(key, key),
            key="selected_path_key",
        )

        current_value = settings.get("paths", {}).get(selected_path_key, "")
        edited_value = st.text_input(
            t(lang, "path"),
            value=current_value,
            key=f"path_editor_{selected_path_key}",
        )

        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            save_clicked = st.button(t(lang, "save_path"), key="save_configured_path", use_container_width=True)

        with btn_col2:
            open_clicked = st.button(
                t(lang, "open_folder"),
                key="open_configured_path_folder",
                use_container_width=True,
            )

        validate_clicked = st.button(t(lang, "validate_paths"), key="validate_paths_btn", use_container_width=True)

        if save_clicked:
            updated_settings = {
                "paths": dict(settings.get("paths", {})),
            }
            updated_settings["paths"][selected_path_key] = edited_value.strip()
            save_settings(updated_settings)
            st.success(t(lang, "path_updated_reloading"))
            st.rerun()

        if open_clicked:
            path_to_open = edited_value.strip() or current_value
            if not path_to_open:
                st.error(t(lang, "path_empty"))
            elif selected_path_key.endswith("_url") or path_to_open.lower().startswith(("http://", "https://")):
                try:
                    os.startfile(path_to_open)
                    st.info(t(lang, "opened_url"))
                except OSError as exc:
                    st.error(t(lang, "could_not_open_url", exc=exc))
            else:
                target_path = path_to_open
                if selected_path_key.endswith("_file"):
                    target_path = os.path.dirname(path_to_open)

                if not os.path.exists(target_path):
                    st.error(t(lang, "path_does_not_exist", path=target_path))
                else:
                    try:
                        os.startfile(target_path)
                        st.info(t(lang, "opened_path", path=target_path))
                    except OSError as exc:
                        st.error(t(lang, "could_not_open_path", exc=exc))

        if validate_clicked:
            st.session_state["path_validation_errors"] = validate_settings(load_settings())

        validation_errors = st.session_state.get("path_validation_errors", [])
        if validation_errors:
            st.warning(t(lang, "path_validation_issues"))
            for err in validation_errors:
                st.caption(err)
        elif validate_clicked:
            st.success(t(lang, "all_paths_valid"))

        with st.expander(t(lang, "current_paths"), expanded=False):
            st.write(settings.get("paths", {}))
