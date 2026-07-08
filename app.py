import streamlit as st

from config import load_settings
from tab_dups import render_dups_tab
from tab_new_job import render_new_job_tab
from tab_schedule import render_schedule_tab
from ui_text import t
from ui_settings import render_settings_popover

st.set_page_config(page_title="TIDS", page_icon="⚡", layout="centered")

settings = load_settings()
if "path_validation_errors" not in st.session_state:
    st.session_state["path_validation_errors"] = []
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "en"

lang = st.session_state["ui_lang"]

st.title(t(lang, "app_title"))
st.subheader(f"⚡{t(lang, 'app_subtitle')}⚡")

_, settings_col_right = st.columns([11, 1])
with settings_col_right:
    render_settings_popover(settings, lang)
    lang = st.session_state.get("ui_lang", "en")

main_tab_dups, main_tab_new_job, main_tab_schedule = st.tabs(
    [t(lang, "tab_dups"), t(lang, "tab_new_job"), t(lang, "tab_schedule")]
)

with main_tab_dups:
    render_dups_tab(settings, lang)

with main_tab_new_job:
    render_new_job_tab(settings, lang)

with main_tab_schedule:
    render_schedule_tab(settings, lang)