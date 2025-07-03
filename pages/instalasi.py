import flet as ft
import subprocess
import sys
import os
import time
import json
from threading import Thread
import importlib.util
from assets.colors.custom_colors import CustomColor

APP_NAME = "BisindoApp"
if sys.platform == "win32":
    APP_DATA_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
else:
    APP_DATA_DIR = os.path.join(os.path.expanduser('~'), '.config', APP_NAME)

os.makedirs(APP_DATA_DIR, exist_ok=True)
USER_INSTALLATION_STATUS_FILE = os.path.join(APP_DATA_DIR, "installation_status.json")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def InstalasiPage(page: ft.Page):
    progress_bar = ft.ProgressBar(
        width=600,
        height=14,
        border_radius=30,
        color=CustomColor.PRIMARY,
        bgcolor=CustomColor.SECONDARY,
        value=0.0
    )

    status_text = ft.Text(
        "Menunggu proses pemeriksaan...",
        size=18,
        color=CustomColor.TEXT,
        weight=ft.FontWeight.BOLD
    )
    
    obs_status_label = ft.Text(
        "Status OBS Studio akan muncul di sini.",
        color="#AAAAAA"
    )

    requirements_path = resource_path("requirements.txt")
    dependencies = []
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as file:
            dependencies = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    dependency_status = [
        {"name": dep, "checkbox": ft.Checkbox(value=False, disabled=True), "label": ft.Text(dep, color=CustomColor.TEXT)}
        for dep in dependencies
    ]

    is_running = [False]

    def save_installation_status():
        status_to_save = {
            "dependencies": {item["name"]: item["checkbox"].value for item in dependency_status},
            "obs_status": obs_status_label.value,
            "obs_color": obs_status_label.color,
        }
        try:
            with open(USER_INSTALLATION_STATUS_FILE, "w") as f:
                json.dump(status_to_save, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan status instalasi: {e}")

    def load_installation_status():
        try:
            if os.path.exists(USER_INSTALLATION_STATUS_FILE):
                with open(USER_INSTALLATION_STATUS_FILE, "r") as f:
                    saved_status = json.load(f)
                
                for item in dependency_status:
                    is_installed = saved_status.get("dependencies", {}).get(item["name"], False)
                    item["checkbox"].value = is_installed
                    if not is_installed:
                        item["label"].color = "#FF6B6B"

                obs_status_label.value = saved_status.get("obs_status", "Status OBS Studio akan muncul di sini.")
                obs_status_label.color = saved_status.get("obs_color", "#AAAAAA")
                
                status_text.value = "Status tersimpan. Klik untuk memeriksa ulang."
                
                all_deps_installed = all(item["checkbox"].value for item in dependency_status)
                obs_ok = "Terdeteksi" in obs_status_label.value
                progress_bar.value = 1.0 if all_deps_installed and obs_ok else 0.0

                page.update()
        except Exception as e:
            print(f"Gagal memuat status instalasi: {e}")

    def get_module_name(library_name):
        name = library_name.split('==')[0].split('>')[0].split('<')[0].strip()
        if 'opencv-python' in name:
            return 'cv2'
        if 'scikit-learn' in name:
            return 'sklearn'
        return name

    def check_library_installed(library_name):
        module_name = get_module_name(library_name)
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except Exception:
            return False

    def check_obs_installed():
        try:
            if sys.platform == "win32":
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\OBS Studio")
                    winreg.CloseKey(key)
                    return True
                except FileNotFoundError:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\OBS Studio")
                        winreg.CloseKey(key)
                        return True
                    except FileNotFoundError:
                        return False
            else:
                possible_paths = ["/Applications/OBS.app", "/Applications/OBS Studio.app"]
                return any(os.path.exists(path) for path in possible_paths)
        except Exception as e:
            print(f"Error checking OBS installation: {e}")
            return False

    def check_dependencies_thread():
        status_text.value = "🔍 Memeriksa instalasi..."
        progress_bar.value = 0
        page.update()
        time.sleep(0.5)

        total_steps = len(dependencies) + 1
        current_step = 0

        status_text.value = "🔍 Memeriksa pustaka Python..."
        page.update()
        for dependency in dependency_status:
            is_installed = check_library_installed(dependency["name"])
            dependency["checkbox"].value = is_installed
            dependency["label"].color = CustomColor.TEXT if is_installed else "#FF6B6B"
            current_step += 1
            progress_bar.value = current_step / total_steps
            page.update()
            time.sleep(0.1)
        
        status_text.value = "🔍 Memeriksa instalasi OBS Studio..."
        page.update()
        time.sleep(0.5)

        obs_installed = check_obs_installed()
        if obs_installed:
            obs_status_label.value = "📡 OBS Studio Terdeteksi! 🚀 Siap digunakan!"
            obs_status_label.color = CustomColor.TEXT
        else:
            obs_status_label.value = "🚨 OBS Studio Tidak Ditemukan! 😢"
            obs_status_label.color = "#FF6B6B"

        current_step += 1
        progress_bar.value = current_step / total_steps
        
        status_text.value = "✅ Pemeriksaan instalasi selesai."
        save_installation_status()

        is_running[0] = False
        start_button.disabled = False
        start_button.text = "🔍 Periksa Ulang"
        page.update()


    def run_installation(e):
        if is_running[0]:
            return

        is_running[0] = True
        start_button.disabled = True
        start_button.text = "Berhenti"
        page.update()

        Thread(target=check_dependencies_thread).start()

    start_button = ft.ElevatedButton(
        text="🔍 Periksa instalasi",
        bgcolor=CustomColor.PRIMARY,
        color=CustomColor.CARD,
        height=65,
        width=230,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=ft.Padding(18, 25, 18, 25)
        ),
        on_click=run_installation
    )

    def step_item(emoji, label):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Container(
                    width=110,
                    height=110,
                    bgcolor=CustomColor.CARD,
                    border_radius=25,
                    alignment=ft.alignment.center,
                    content=ft.Text(emoji, size=50)
                ),
                ft.Text(label, size=18, color=CustomColor.TEXT, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
            ]
        )
    
    load_installation_status()

    return ft.Container(
        expand=True,
        width=float("inf"),
        bgcolor=CustomColor.BACKGROUND,
        border_radius=30,
        padding=40,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=28,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=100,
                    controls=[
                        step_item("🐍", "Environment"),
                        step_item("📚", "Library"),
                        step_item("🎥", "OBS"),
                    ]
                ),
                status_text,
                progress_bar,
                obs_status_label,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Row(
                            spacing=5,
                            controls=[status["checkbox"], status["label"]]
                        ) for status in dependency_status
                    ]
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=20,
                    content=start_button
                )
            ]
        )
    )