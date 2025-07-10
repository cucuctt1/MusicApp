import flet as ft




class func_btn(ft.Container):
    def __init__(self,width,height,icon=None):
        super().__init__()

        self.width = width
        self.height = height
        self.icon = icon
        self.content = self.icon
        self.func = None

        self.bgcolor = "BLACK"
        self.opacity = 0.5

        self.border_radius = width/2
    
        self.on_click = self._call
    
    def _call(self,e):
        
        if self.func:
            self.func()


class tostate_btn(func_btn):

    def __init__(self, width, height, icon1,icon2):
        super().__init__(width, height, icon1)

        self.icon2 = icon2
        self.icon_State = True
        self.icon1 = icon1

        self.on_click = self._call

    def _call(self,e):
        self.icon_State = not self.icon_State
        super()._call(e)
        self.update()

    def reset_state(self):
        self.icon_State = True


    def update(self):
        self.icon = self.icon1 if self.icon_State else self.icon2
        self.content = self.icon
        return super().update()
    


    

