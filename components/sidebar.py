import flet as ft
import os
import sys
from assets.colors.custom_colors import CustomColor

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CustomSidebar(ft.Container):
    def __init__(self, items, on_item_click):
        super().__init__()
        self.items = items
        self.on_item_click = on_item_click
        self.sidebar_controls = []

        # Create sidebar items
        for idx, (label, emoji) in enumerate(self.items):
            container = ft.Container(
                border_radius=20,
                padding=ft.Padding(8, 8, 20, 8),
                bgcolor=CustomColor.SECONDARY if idx == 0 else CustomColor.BACKGROUND,
                content=ft.Row(
                    spacing=15,
                    controls=[
                        # Larger, perfectly square background for emoji
                        ft.Container(
                            width=48,
                            height=48,
                            bgcolor=CustomColor.CARD,
                            border_radius=16,
                            alignment=ft.alignment.center,
                            content=ft.Text(emoji, size=24, weight=ft.FontWeight.BOLD)
                        ),
                        ft.Text(label, size=18, color=CustomColor.TEXT, weight=ft.FontWeight.BOLD)
                    ]
                ),
                # Use `idx=idx` to properly bind the correct index value
                on_click=lambda e, idx=idx: [self.update_selection(idx), self.on_item_click(idx)],
            )
            self.sidebar_controls.append(container)

        self.content = ft.Container(
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor=CustomColor.CARD,
                        border_radius=30,
                        padding=8,
                        content=ft.Image(
                            # Use resource_path to find the logo correctly
                            src=resource_path("assets/logo/logo.png"),
                            width=100,
                            height=100,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=20
                        )
                    )
                ] + self.sidebar_controls,
                spacing=30  # More spacing for better layout
            )
        )

    def update_selection(self, index):
        for i, item in enumerate(self.sidebar_controls):
            item.bgcolor = CustomColor.SECONDARY if i == index else CustomColor.BACKGROUND
            item.content.controls[1].color = CustomColor.TEXT
            # We need to call update on the item to see the change
            item.update()
