import os

import streamlit as st

from dups_service import duplicate_design_folder
from ui_text import t


@st.cache_data(ttl=30, show_spinner=False)
def _path_is_dir(path):
    try:
        return os.path.isdir(path)
    except OSError:
        return False


@st.cache_data(ttl=30, show_spinner=False)
def _path_is_file(path):
    try:
        return os.path.isfile(path)
    except OSError:
        return False


def render_dups_tab(settings, lang):
    st.subheader(t(lang, "dups_subheader"))
    designs_root = settings.get("paths", {}).get("disenos", "")
    dups_template_file = settings.get("paths", {}).get("dups_template_file", "")

    if "dups_open_visible" not in st.session_state:
        st.session_state["dups_open_visible"] = False
        st.session_state["dups_last_target_path"] = None

    if not designs_root:
        st.warning(t(lang, "designs_path_empty"))
        return

    if not _path_is_dir(designs_root):
        st.error(t(lang, "designs_path_missing", path=designs_root))
        return

    if not dups_template_file:
        st.warning(t(lang, "dups_template_path_empty"))
        return

    if not _path_is_file(dups_template_file):
        st.error(t(lang, "dups_template_missing", path=dups_template_file))
        return

    st.caption(t(lang, "designs_root_caption", path=designs_root))
    st.caption(t(lang, "using_template_caption", path=dups_template_file))
    source_folder_name = st.text_input(
        t(lang, "source_design_folder"),
        value="",
        placeholder=t(lang, "source_design_folder_placeholder"),
        key="dups_source_folder",
    )

    new_folder_name = st.text_input(
        t(lang, "new_folder_name"),
        value="",
        placeholder=t(lang, "new_folder_name_placeholder"),
        key="dups_new_folder_name",
    )

    if st.button(t(lang, "duplicate_folder"), type="primary", use_container_width=True, key="dups_duplicate_btn"):
        progress = st.progress(0, text=t(lang, "progress_starting"))

        def _update_progress(value, text):
            bounded = max(0, min(100, int(value)))
            progress.progress(bounded, text=text)

        try:
            with open(dups_template_file, "rb") as tpl_handle:
                template_bytes = tpl_handle.read()
        except OSError as exc:
            st.error(t(lang, "could_not_read_template", exc=exc))
            template_bytes = None

        ok, message = duplicate_design_folder(
            designs_root,
            source_folder_name,
            new_folder_name,
            progress_callback=_update_progress,
            template_bytes=template_bytes,
        )

        if ok:
            st.session_state["dups_last_target_path"] = os.path.join(designs_root, new_folder_name.strip())
            st.session_state["dups_open_visible"] = True
            st.success(message)
        else:
            st.session_state["dups_open_visible"] = False
            st.session_state["dups_last_target_path"] = None
            st.error(message)

    open_target_path = st.session_state.get("dups_last_target_path")
    if st.session_state.get("dups_open_visible") and open_target_path and _path_is_dir(open_target_path):
        if st.button(t(lang, "open"), use_container_width=True, key="dups_open_btn"):
            try:
                os.startfile(open_target_path)
                st.info(t(lang, "opened_path", path=open_target_path))
            except OSError as exc:
                st.error(t(lang, "could_not_open_path", exc=exc))
