
import flet as ft



class top_border_bar(ft.Row):

    def __init__ (self,height,width,owner):
        super().__init__()
        self.height = height
        self.width = width
        self.owner = owner

        self.minize_btn = ft.IconButton(
                    icon=ft.Icons.MINIMIZE_ROUNDED,
                    icon_color="#E1E1E1",
                    height=self.height-2,
                    icon_size=10,
                    width=20,
                    padding=ft.padding.only(bottom=5),
                    on_click= lambda e: self.minimize()
                )
        
        self.close_btn = ft.IconButton(
                    icon=ft.Icons.CLOSE_OUTLINED,
                    icon_color="#E1E1E1",
                    height=self.height-2,
                    icon_size=10,
                    width=20,
                    on_click= lambda e: self.close(),
                    padding=0,
                    hover_color="#00000000"
                )
        self.spacing=5
        self.controls = [self.minize_btn,self.close_btn]
        self.alignment = ft.MainAxisAlignment.END
    def minimize(self):
        self.owner.page.window.minimized = True
        self.owner.page.update()

    def close(self):
        self.owner.page.window.close()


class display(ft.Column):

    def __init__(self,width,height,owner):
        super().__init__()
        self.width = width
        self.height = height
        self.owner = owner
        self.status_bar = top_border_bar(width=self.width-10,height=20,owner=owner)
        self.main_display = ft.Container(width=width,height=self.height-40,alignment=ft.alignment.center)
        self.spacing=0
        self.controls = [self.status_bar,self.main_display]
        self.alignment = ft.MainAxisAlignment.CENTER

    