import flet as ft
from assets.colors.custom_colors import CustomColor
from core.detection import settings
import json
import os
import sys

APP_NAME = "BisindoApp"
if sys.platform == "win32":
    APP_DATA_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
else:
    APP_DATA_DIR = os.path.join(os.path.expanduser('~'), '.config', APP_NAME)

os.makedirs(APP_DATA_DIR, exist_ok=True)
USER_SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")

def load_user_settings():
    try:
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, 'r') as f:
                saved_settings = json.load(f)
                settings.update(saved_settings)
    except Exception as e:
        print(f"Gagal memuat pengaturan pengguna: {e}")

def PengaturanPage(page: ft.Page):
    load_user_settings()
    
    settings_changed = False

    def on_setting_change(e):
        nonlocal settings_changed
        if not settings_changed:
            settings_changed = True
            save_button.disabled = False
            page.update()

    def save_settings(e):
        nonlocal settings_changed
        try:
            with open(USER_SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
            print("✅ Pengaturan berhasil disimpan!")
            settings_changed = False
            save_button.disabled = True
            page.update()
        except Exception as ex:
            print(f"❌ Gagal menyimpan pengaturan: {ex}")


    def on_landmark_switch_change(e):
        settings["show_landmarks"] = e.control.value
        print(f"Show Landmarks set to: {settings['show_landmarks']}")
        on_setting_change(e)

    def on_delay_slider_change(e):
        delay_value = int(e.control.value)
        settings["word_delay"] = delay_value
        
        if delay_value <= 10:
            speed = "Sangat Cepat"
        elif delay_value <= 17:
            speed = "Cepat"
        elif delay_value <= 25:
            speed = "Normal"
        else:
            speed = "Lambat"
            
        delay_label.value = f"Jeda Kata: {delay_value} frame ({speed})"
        delay_label.update()
        print(f"Word Delay set to: {settings['word_delay']}")
        on_setting_change(e)

    landmark_switch = ft.Switch(
        value=settings["show_landmarks"],
        on_change=on_landmark_switch_change,
        active_color=CustomColor.PRIMARY,
    )
    
    initial_delay = settings["word_delay"]
    if initial_delay <= 10:
        initial_speed = "Sangat Cepat"
    elif initial_delay <= 17:
        initial_speed = "Cepat"
    elif initial_delay <= 25:
        initial_speed = "Normal"
    else:
        initial_speed = "Lambat"
        
    delay_label = ft.Text(f"Jeda Kata: {initial_delay} frame ({initial_speed})", color=CustomColor.BORDER)

    delay_slider = ft.Slider(
        min=5,
        max=35,
        value=initial_delay,
        on_change=on_delay_slider_change,
        active_color=CustomColor.PRIMARY,
        inactive_color=CustomColor.BORDER,
    )
    
    save_button = ft.ElevatedButton(
        text="Simpan Pengaturan",
        on_click=save_settings,
        height=55,
        width=250,
        disabled=True,
        style=ft.ButtonStyle(
            color={
                "disabled": "#A6A6A6",
                "default": CustomColor.CARD
            },
            bgcolor={
                "disabled": "#E0E0E0",
                "default": CustomColor.PRIMARY
            }
        )
    )

    def create_setting_card(icon, title, description, control):
        return ft.Container(
            bgcolor=CustomColor.CARD,
            border_radius=15,
            padding=ft.padding.symmetric(horizontal=25, vertical=20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=20,
                        controls=[
                            ft.Text(icon, size=24),
                            ft.Column(
                                spacing=3,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Text(title, weight=ft.FontWeight.BOLD, size=16, color=CustomColor.TEXT),
                                    ft.Text(description, size=12, color="#B3333333"),
                                ]
                            )
                        ]
                    ),
                    control
                ]
            )
        )

    return ft.Container(
        expand=True,
        bgcolor=CustomColor.BACKGROUND,
        border_radius=30,
        padding=40,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text("Pengaturan Deteksi", size=24, weight=ft.FontWeight.BOLD, color=CustomColor.TEXT),
                ft.Container(
                    width=700,
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            create_setting_card(
                                "🖐️",
                                "Tampilkan Landmark Tangan",
                                "Menampilkan kerangka titik pada tangan.",
                                landmark_switch
                            ),
                             create_setting_card(
                                "⏱️",
                                "Kecepatan Pembentukan Kata",
                                "Atur jeda sebelum huruf ditambahkan.",
                                ft.Column(
                                    [delay_label, delay_slider], 
                                    spacing=0, 
                                    width=250, 
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            )
                        ]
                    )
                ),
                save_button
            ]
        )
    )
