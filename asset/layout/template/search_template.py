
import flet as ft


class TwoStateBtn(ft.Container):
    def __init__(self,width,height,icon1,icon2,func1,func2):
        super().__init__()
        self.state = True
        self.width = width
        self.height = height
        self.icon1 = ft.Icon(name=icon1,size=self.height-10,color="WHITE")
        self.icon2 = ft.Icon(name=icon2,size=self.height-10,color="WHITE")

        self.func1 = func1
        self.func2 = func2

        self.content = self.icon1 if self.state else self.icon2
        self.alignment = ft.alignment.center
        self.on_click = self.func1 if self.state else self.func2


    def update_state(self,state:bool=None):
        if state is None:
            self.state = not self.state

        else:
            self.state = state

        self.content = self.icon1 if self.state else self.icon2
        self.on_click = self.func1 if self.state else self.func2

class Btn(ft.Container):

    def __init__(self,width,height,icons,func):
        super().__init__()
        self.width = width
        self.height = height
        self.icons = ft.Icon(name=icons,size=self.height-10,color="WHITE")
        self.padding = ft.padding.all(0)
        self.func = func
        self.content = self.icons
        self.on_click = self.__call_func

    def __call_func(self,e):
        if self.func:

            self.func(e)
        else:
            print("no function")

class search(ft.TextField):
    def __init__(self,width,height,controller):
        super().__init__()
        self.main_width = width
        self.width = width
        self.height = height
        self.text_style=ft.TextStyle(color="WHITE")
        self.text_vertical_align = ft.VerticalAlignment.START
        self.border = ft.InputBorder.NONE
        self.content_padding = ft.padding.only(top=-20,left=10)
        self.cursor_height = 5
        self.controller = controller
        #call when in focus

        self.on_focus = self.__in_focus
        self.on_blur = self.__in_blur

    def __in_focus(self,e):
        self.width = self.main_width - self.height
        self.controller.SearchBarInFocus()

    def __in_blur(self,e):
        self.width = self.main_width
        #self.page_controller.SearchBarInBlur()

    def cancel(self,e):

        self.value = ""
        self.controller.SearchBarInBlur()
        self.update()





class Search_bar(ft.Row):

    def __init__(self,width,height,controller=None):
        super().__init__()
        self.width = width
        self.height = height
        self.controller = controller
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 0
        #switch state button like 2 state button but 2rd state no function

        self.ToStateBtn = TwoStateBtn(self.height,self.height,
                                      ft.Icons.ARROW_BACK,ft.Icons.SEARCH,
                                      None,None)
        self.text_search = search(width=self.width - 1 * self.height, height=self.height, controller=self)
        self.cancel_btn = Btn(width=self.height,height=self.height,icons = ft.Icons.CLOSE,func=self.text_search.cancel)


        self.controls = [self.ToStateBtn,self.text_search]
    def SearchBarInFocus(self):
        #add cancel btn
        print("added button to control")
        if self.cancel_btn not in self.controls:
            self.controls.append(self.cancel_btn)
            self.ToStateBtn.update_state(False)
        self.update()
        pass


    def SearchBarInBlur(self):
        #remove btn
        print("remove button in control")
        if self.cancel_btn in self.controls:
            self.controls.remove(self.cancel_btn)
            self.ToStateBtn.update_state(True)
        self.update()
        pass


if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width = 300
        page.window.height = 450
        page.padding = ft.padding.all(0)
        f = ft.Container(bgcolor="GREEN")
        bar = Search_bar(width=280,height=30,controller=None)
        f.content = bar
        page.add(f)

        page.update()


    ft.app(target=main)
