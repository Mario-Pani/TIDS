import os
import shutil
import subprocess
import time
from urllib.parse import quote


def list_design_subfolders(designs_root):
    if not designs_root or not os.path.isdir(designs_root):
        return []

    folder_names = []
    for name in os.listdir(designs_root):
        candidate = os.path.join(designs_root, name)
        if os.path.isdir(candidate):
            folder_names.append(name)
    folder_names.sort(key=str.lower)
    return folder_names


def _emit_progress(progress_callback, value, text):
    if callable(progress_callback):
        progress_callback(value, text)


def _create_source_folder_link(target_path, source_path):
    source_uri = "file:///" + quote(source_path.replace("\\", "/"), safe=":/")
    link_path = os.path.join(target_path, "Source Design Folder.url")
    content = f"[InternetShortcut]\nURL={source_uri}\n"
    with open(link_path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _create_renamed_template_docx(target_path, new_folder_name, template_bytes):
    output_name = f"{new_folder_name}.docx"
    output_path = os.path.join(target_path, output_name)
    with open(output_path, "wb") as handle:
        handle.write(template_bytes)


def duplicate_design_folder(
    designs_root,
    source_folder_name,
    new_folder_name,
    progress_callback=None,
    template_bytes=None,
):
    clean_source_name = str(source_folder_name or "").strip()
    clean_new_name = str(new_folder_name or "").strip()

    _emit_progress(progress_callback, 5, "Validating inputs...")

    if not clean_source_name:
        return False, "Source design folder is required."
    if not clean_new_name:
        return False, "New folder name is required."
    if not template_bytes:
        return False, "Template file is required in configured path before duplicating."

    invalid_chars = set('\\/:*?"<>|')
    if any(char in invalid_chars for char in clean_new_name):
        return False, "New folder name contains invalid characters."

    if clean_new_name in (".", ".."):
        return False, "Invalid folder name."

    source_path = os.path.join(designs_root, clean_source_name)
    target_path = os.path.join(designs_root, clean_new_name)

    _emit_progress(progress_callback, 10, "Checking source and target folders...")

    if not os.path.isdir(source_path):
        return False, "The design to duplicate has not been created yet."
    if os.path.exists(target_path):
        return False, f"Target folder already exists: {clean_new_name}"

    # Fast path on Windows/network shares: multithreaded robocopy.
    try:
        _emit_progress(progress_callback, 15, "Starting fast copy (Robocopy)...")
        robocopy_cmd = [
            "robocopy",
            source_path,
            target_path,
            "/E",
            "/R:2",
            "/W:1",
            "/MT:32",
            "/NFL",
            "/NDL",
            "/NJH",
            "/NJS",
            "/NP",
        ]
        process = subprocess.Popen(
            robocopy_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        start_time = time.time()
        while process.poll() is None:
            elapsed = max(0.0, time.time() - start_time)
            # Robocopy does not expose deterministic progress in this mode,
            # so we move a capped activity progress bar while it runs.
            rolling_progress = min(90, 15 + int(elapsed * 2))
            _emit_progress(progress_callback, rolling_progress, "Copying files...")
            time.sleep(0.5)

        stdout, stderr = process.communicate()
        return_code = process.returncode

        _emit_progress(progress_callback, 95, "Finalizing copy...")

        # Robocopy success codes are 0-7.
        if return_code <= 7:
            try:
                _create_source_folder_link(target_path, source_path)
                _create_renamed_template_docx(target_path, clean_new_name, template_bytes)
            except Exception as exc:
                return False, f"Copy completed, but post-copy setup failed: {exc}"
            _emit_progress(progress_callback, 100, "Copy complete")
            return True, f"Folder copied to: {target_path}"
        error_tail = (stderr or stdout or "").strip().splitlines()
        error_hint = error_tail[-1] if error_tail else "No details available."
        return False, f"Copy failed (robocopy code {return_code}). {error_hint}"
    except FileNotFoundError:
        # Fallback if robocopy is unavailable.
        pass
    except Exception as exc:
        return False, f"Copy failed: {exc}"

    try:
        _emit_progress(progress_callback, 20, "Robocopy not available. Using standard copy...")
        file_count = 0
        for root, _, files in os.walk(source_path):
            file_count += len(files)

        os.makedirs(target_path, exist_ok=False)
        copied_files = 0
        for child_name in os.listdir(source_path):
            source_child = os.path.join(source_path, child_name)
            target_child = os.path.join(target_path, child_name)
            if os.path.isdir(source_child):
                shutil.copytree(source_child, target_child)
                for _, _, files in os.walk(source_child):
                    copied_files += len(files)
            else:
                shutil.copy2(source_child, target_child)
                copied_files += 1

            if file_count > 0:
                pct = 20 + int((copied_files / file_count) * 75)
                _emit_progress(progress_callback, min(95, pct), "Copying files...")

        _create_source_folder_link(target_path, source_path)
        _create_renamed_template_docx(target_path, clean_new_name, template_bytes)
    except Exception as exc:
        return False, f"Copy failed: {exc}"

    _emit_progress(progress_callback, 100, "Copy complete")
    return True, f"Folder copied to: {target_path}"
