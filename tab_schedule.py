import streamlit as st

from ui_text import t


def render_schedule_tab(settings, lang):
    st.subheader(t(lang, "schedule_subheader"))
    schedule_url = settings.get("paths", {}).get("schedule_url", "")

    if not schedule_url:
        st.warning(t(lang, "schedule_url_empty"))
        return

    st.link_button(
        t(lang, "open_schedule_file"),
        schedule_url,
        use_container_width=True,
        type="primary",
    )
