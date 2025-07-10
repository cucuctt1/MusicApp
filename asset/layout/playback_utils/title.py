import flet as ft


class music_tile(ft.Container):

    def __init__(self,width,height,string=""):
        super().__init__()
        self.width = width
        self.height = height
        self.value = string

        #self.bgcolor = "BLACK"
        self.padding = ft.padding.only(left=10)
        self.text = ft.Text(value=self.value,width=self.width,height=self.height,size=self.height-5,color="WHITE")

        self.alignment = ft.alignment.top_left
        self.content = self.text


if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width = 300
        page.window.height = 450
        img = "abc abc"
        mc = music_tile(width=280,height=20,string=img)
        page.add(mc)
        page.update()
        

    ft.app(target=main)