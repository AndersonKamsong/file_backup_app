import flet as ft

def main(page: ft.Page):
    page.title = "File Backup Application"
    page.scroll = "adaptive"  # Allow scrolling for long lists
    page.padding = 20

    # List to store file paths
    updated_paths = []

    # Callback to add new file paths
    def add_path(e):
        local_path = local_path_input.value.strip()
        remote_path = remote_path_input.value.strip()

        if local_path and remote_path:
            updated_paths.append((local_path, remote_path))
            paths_view.controls.append(
                ft.Row([
                    ft.Text(local_path, expand=True),
                    ft.Text(remote_path, expand=True),
                ])
            )
            # Clear the input fields after adding
            local_path_input.value = ""
            remote_path_input.value = ""
        page.update()

    # Top-right button callback
    def top_right_button_clicked(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Top-right button clicked!"),
            open=True
        )
        page.update()

    # Input fields
    local_path_input = ft.TextField(label="Local File Path", width=300)
    remote_path_input = ft.TextField(label="Remote File Path", width=300)
    add_path_button = ft.ElevatedButton("Add Path", on_click=add_path)

    # Container for the list of paths
    paths_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    # Main layout
    page.add(
        ft.Stack([
            # Top-right button
            ft.Container(
                ft.Row([
                    ft.Container(width=20),  # Spacer for alignment
                    ft.ElevatedButton("Top-Right Button", on_click=top_right_button_clicked)
                ], alignment="end"),
                alignment=ft.alignment.top_right,
                padding=10
            ),
            # Center container with two columns
            ft.Container(
                ft.Column([
                    ft.Text("Updated File Paths", size=20, weight="bold"),
                    ft.Row([
                        ft.Column([
                            local_path_input,
                            add_path_button,
                        ], expand=1),
                        ft.Column([
                            remote_path_input,
                        ], expand=1),
                    ]),
                    paths_view
                ]),
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_200,
                border_radius=10,
                padding=10
            )
        ])
    )

# Run the app
ft.app(target=main)
