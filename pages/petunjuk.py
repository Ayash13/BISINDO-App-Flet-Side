import flet as ft
from assets.colors.custom_colors import CustomColor

def PetunjukPage():

    def create_instruction_card(emoji, title, description):
        return ft.Container(
            width=280,
            height=260,
            bgcolor=CustomColor.CARD,
            border_radius=30,
            padding=ft.padding.all(25),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=15,
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        border_radius=12,
                        bgcolor="#1A4A90E2",
                        alignment=ft.alignment.center,
                        content=ft.Text(emoji, size=28)
                    ),
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=CustomColor.TEXT),
                    ft.Text(description, size=14, color=CustomColor.TEXT, selectable=True),
                ]
            )
        )

    instructions = [
        create_instruction_card(
            "✅",
            "Periksa Instalasi",
            "Buka halaman 'Instalasi' dan klik 'Periksa Instalasi' untuk memastikan semua kebutuhan aplikasi terpenuhi."
        ),
        create_instruction_card(
            "🚀",
            "Mulai Deteksi",
            "Di halaman 'Mulai', tunggu model dimuat, lalu klik tombol '▶️ Mulai' untuk mengaktifkan kamera."
        ),
        create_instruction_card(
            "👋",
            "Peragakan Isyarat",
            "Posisikan tangan Anda di depan kamera. Aplikasi akan mendeteksi isyarat BISINDO dan menampilkannya."
        ),
        create_instruction_card(
            "⭐",
            "Pembentukan Kalimat",
            "Aplikasi akan secara otomatis menampilkan hasil deteksi ke dalam box seperti subtitle."
        ),
        create_instruction_card(
            "🛑",
            "Hentikan Deteksi",
            "Klik tombol '🛑 Stop' untuk menonaktifkan kamera dan menghentikan proses deteksi kapan saja."
        ),
        create_instruction_card(
            "🎥",
            "Kamera Virtual",
            "Aplikasi terintegrasi dengan kamera virtual supaya audiens dapat melihat translasi bahasa isyarat secara langsung pada pertemuan daring."
        ),
    ]

    instructions_grid = ft.GridView(
        runs_count=3,
        child_aspect_ratio=1.1,
        spacing=30,
        run_spacing=30,
        controls=instructions
    )

    return ft.Container(
        expand=True,
        bgcolor=CustomColor.BACKGROUND,
        border_radius=30,
        padding=40,
        alignment=ft.alignment.center,
        content=ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
            controls=[
                ft.Text(
                    "Selamat Datang di Aplikasi Deteksi BISINDO!",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=CustomColor.TEXT
                ),
                ft.Text(
                    "Panduan Cepat Penggunaan Aplikasi",
                    size=18,
                    text_align=ft.TextAlign.CENTER,
                    color=CustomColor.TEXT
                ),
                ft.Container(
                    width=1000,
                    content=instructions_grid
                ),
                ft.Container(
                    height=40
                )
            ]
        )
    )