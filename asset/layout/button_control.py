import flet as ft
from asset.layout import functional_btn as fb

class btn_control(ft.Row):
    def __init__(self,width,height,controller=None):
        super().__init__()

        self.width = width
        self.height = height
        self.controller = controller
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.btn_size1 = self.height
        self.btn_size2 = self.height-15
        self.btn_size3 = self.height-20

        self.like_icon1 = ft.Icon(name=ft.Icons.FAVORITE,size=self.btn_size3-15)
        self.like_icon2 = ft.Icon(name=ft.Icons.FAVORITE_BORDER,size=self.btn_size3-15)

        self.previous_icon = ft.Icon(name=ft.Icons.SKIP_PREVIOUS)

        self.play_icon = ft.Icon(name=ft.Icons.PLAY_ARROW)
        self.pause_icon = ft.Icon(name=ft.Icons.PAUSE)

        self.next_icon = ft.Icon(name=ft.Icons.SKIP_NEXT)

        self.list_icon = ft.Icon(name=ft.Icons.FORMAT_LIST_BULLETED,size=self.btn_size3-10)

        self.like_btn = fb.tostate_btn(width=self.btn_size3,height=self.btn_size3,icon1=self.like_icon1,icon2=self.like_icon2)

        self.previous_btn = fb.func_btn(width=self.btn_size2,height=self.btn_size2,icon=self.previous_icon)

        self.play_btn = fb.tostate_btn(width=self.btn_size1,height=self.btn_size1,icon1=self.play_icon,icon2=self.pause_icon)

        self.next_btn = fb.func_btn(width=self.btn_size2,height=self.btn_size2,icon=self.next_icon)

        self.list_btn = fb.func_btn(width=self.btn_size3,height=self.btn_size3,icon=self.list_icon)

        self.controls = [self.like_btn,self.previous_btn,self.play_btn,self.next_btn,self.list_btn]
        
    

if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width = 300
        page.window.height = 450

        btn_c = btn_control(width=280,height=50,controller=None)
        page.add(btn_c)
        
        page.update()
        

    ft.app(target=main)