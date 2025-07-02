import flet as ft
import threading
import sklearn
from assets.colors.custom_colors import CustomColor
from core.detection import (
    load_heavy_dependencies,
    load_model,
    generate_placeholder_image,
    start_inference,
    stop_inference,
    model_loaded,
    ENABLE_VIRTUAL_CAM
)

def MulaiPage(page: ft.Page):
    stop_flag = [False]
    model_ready = [False]  
    virtual_cam = [None]  

    def start_detection_clicked(e):
        start_button.disabled = True
        stop_button.disabled = False
        start_inference(stop_flag, model_ready, virtual_cam, camera_placeholder, camera_frame, status_text, page)
        page.update()

    def stop_detection_clicked(e):
        start_button.disabled = False
        stop_button.disabled = True
        stop_inference(stop_flag, virtual_cam, camera_placeholder, status_text, page)
        page.update()

    def start_background_loading():
        def background_task():
            load_heavy_dependencies()  
            load_model()  
            model_ready[0] = True  
            camera_placeholder.content = ft.Text("📷", size=100)  
            status_text.value = "Klik tombol mulai untuk mulai mendeteksi."
            start_button.disabled = False
            page.update()

        threading.Thread(target=background_task, daemon=True).start()

    camera_frame = ft.Image(
        expand=True,
        fit=ft.ImageFit.CONTAIN,
        src_base64=generate_placeholder_image()
    )

    camera_placeholder = ft.Container(
        expand=True,
        aspect_ratio=16/9,
        border_radius=32,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        bgcolor=CustomColor.CARD,
        alignment=ft.alignment.center,
        content=ft.ProgressRing(width=60, height=60, stroke_width=5)  
    )

    start_button = ft.ElevatedButton(
        text="▶️ Mulai",
        color=CustomColor.CARD,
        height=60,
        width=200,
        on_click=start_detection_clicked,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={
                "default": CustomColor.PRIMARY,
                "disabled": "#E0E0E0",
            },
            color={
                "disabled": "#A6A6A6",
            }
        )
    )

    stop_button = ft.ElevatedButton(
        text="🛑 Stop",
        color=CustomColor.CARD,
        height=60,
        width=200,
        on_click=stop_detection_clicked,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={
                "default": "#FF6B6B",
                "disabled": "#E0E0E0",
            },
            color={
                "disabled": "#A6A6A6",
            }
        )
    )

    status_text = ft.Text(
        "⏳ Memuat model...",  
        size=18,
        color=CustomColor.TEXT,
        text_align=ft.TextAlign.CENTER
    )

    start_background_loading()

    return ft.Container(
        expand=True,
        width=float("inf"),
        bgcolor=CustomColor.BACKGROUND,
        border_radius=30,
        padding=32,
        alignment=ft.alignment.center,
        content=ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 7, "lg": 8},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[camera_placeholder, status_text]
                ),
                ft.Column(
                    col={"sm": 12, "md": 5, "lg": 4},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[start_button, stop_button]
                )
            ]
        )
    )
