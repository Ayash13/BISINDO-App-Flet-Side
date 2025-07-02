import flet as ft
import sys
import os

from assets.colors.custom_colors import CustomColor
from components.main_content import CustomMainContent
from components.sidebar import CustomSidebar
from pages.instalasi import InstalasiPage
from pages.petunjuk import PetunjukPage
from pages.pengaturan import PengaturanPage
from pages.mulai import MulaiPage

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main(page: ft.Page):
    page.title = "Aplikasi Translasi Bahasa Isyarat Indonesia"
    page.bgcolor = CustomColor.BACKGROUND
    page.padding = 0

    def get_page_content(route):
        if route == "/petunjuk":
            return "Petunjuk", PetunjukPage()
        elif route == "/instalasi":
            return "Instalasi", InstalasiPage(page=page)
        elif route == "/mulai":
            return "Mulai", MulaiPage(page=page)
        elif route == "/pengaturan":
            return "Pengaturan", PengaturanPage(page=page)
        else:
            return "Page Not Found", ft.Text("Page not found", size=20, color=CustomColor.TEXT)

    def route_change(e):
        route_to_index = {
            "/petunjuk": 0,
            "/instalasi": 1,
            "/mulai": 2,
            "/pengaturan": 3
        }
        route_index = route_to_index.get(page.route, 0)
        title, content = get_page_content(page.route)
        main_content.update_content(title, content)
        sidebar.update_selection(route_index)
        page.update()

    sidebar_items = [
        ("Petunjuk", "📄"),
        ("Instalasi", "🚀"),
        ("Mulai", "😆"),
        ("Pengaturan", "⚙️")
    ]

    def on_item_click(index):
        routes = ["/petunjuk", "/instalasi", "/mulai", "/pengaturan"]
        page.go(routes[index])

    sidebar = CustomSidebar(sidebar_items, on_item_click=on_item_click)
    main_content = CustomMainContent()

    page.add(ft.Row([sidebar, main_content], expand=True))
    page.on_route_change = route_change
    page.go("/petunjuk")

ft.app(target=main, assets_dir="assets")