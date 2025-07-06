import flet as ft


class music_cover(ft.Container):

    def __init__(self,width,height,img):

        super().__init__()
        self.width = width
        self.height = height
        self.img =img
        self.holder = None #for holder
        self.bgcolor = "BLACK"
        
        self.border_radius = 20

        self.image1 = ft.Image(src=self.img if self.img else self.holder,fit=ft.ImageFit.FILL)

        self.content = self.image1



if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width = 300
        page.window.height = 450
        img = "./asset/cache/ts.jpg"
        mc = music_cover(width=200,height=200,img=img)
        page.add(mc)
        page.update()
        

ft.app(target=main)