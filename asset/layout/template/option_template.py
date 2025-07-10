

import flet as ft

#top app bar
#TODO: clear all magic value
class top_app_bar(ft.Row):
    def __init__(self,width,height,function_btn=None):
        super().__init__()
        self.height = height
        self.width = width

        self.function_btn = function_btn

        self.text_view = ft.Text(width=self.width-self.height*(2 if self.function_btn else 1)-20,
                                 height=self.height-10,text_align=ft.TextAlign.START,
                                 color= "WHITE",value="ABSCSDdfdfdsf")
        self.return_btn = ft.IconButton(icon=ft.Icons.ARROW_BACK,width=self.height,
                                        height=self.height,icon_color="WHITE",icon_size=self.height-10,
                                        hover_color="",
                                        focus_color="TRANSPARENT",
                                        highlight_color="TRANSPARENT",

                                        padding=ft.padding.all(0))
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.return_btn.on_click = self.__call_button_click
        self.spacing = 10
        self.button_onclick = None
        self.controls = [self.return_btn,self.text_view]
        if self.function_btn:
            self.controls.append(function_btn)

    def __call_button_click(self,e):
        if self.button_onclick:
            self.button_onclick()
        else:
            print("function haven't assigned")

class content_display(ft.Container):
    def __init__(self,width,height,content=None):
        super().__init__()
        self.width = width
        self.height = height

        if self.content:
            self.content = content
        else:
            self.content = ft.Text(value="No content here")
            self.alignment = ft.alignment.center

class Option_Template(ft.Column):
    def __init__(self,width,height,Content=None,func_btn = None):
        super().__init__()
        self.width = width
        self.height = height
        self.top_app_bar = top_app_bar(width=self.width,height=50,function_btn=func_btn)
        self.content_display = content_display(self.width,self.height-50,content=Content)

        self.controls = [self.top_app_bar,self.content_display]
        self.spacing = 0

    def init_content(self,content):
        self.content_display.content = content

    def init_return_page(self,function):
        self.top_app_bar.button_onclick = function

if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width = 300
        page.window.height = 450
        page.padding = ft.padding.all(0)
        f = ft.Container(bgcolor="")
        t = content_display(height=400,width=280)
        f.content = t
        page.add(f)

        page.update()


    ft.app(target=main)


