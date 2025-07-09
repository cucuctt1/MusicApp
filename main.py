import flet as ft
from asset.window import main_page
from asset.layout import playback_main




if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width=300
        page.title = "abc"
        page.bgcolor = ft.Colors.TRANSPARENT
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.window.title_bar_hidden = True
        page.window.frameless = True
        page.window.height = 450

        main_w = main_page.Dragable_holder(page=page)
        pl = playback_main.Main_layout(width=290,height=400,player=None,controller=None)
        main_w.content.content.controls[-1].content = pl
        
        
        page.add(main_w)
        page.padding = 0
        page.update()
        

    ft.app(target=main)
