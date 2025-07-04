import flet as ft
import ctypes
import time
from ctypes import wintypes
import system_func
import os
import window_func





class Dragable_holder(ft.GestureDetector):

    def __init__(self,width = 300,height = 450,page=None,hwnd=None):
        super().__init__()
        self.page = page
        self.x = self.page.window.left
        self.y = self.page.window.top
        self.hwnd = hwnd
        self.width = width
        self.height = height
        self.on_pan_update = self.drag
        self.on_pan_start = self.start
        self.count = True
        self.ox,self.oy = 0,0
        
        self.main_display = window_func.display(self.width,self.height,owner=self)
        self.content = ft.Container(border_radius=20,width=self.width,height=self.height,image=ft.DecorationImage(src="./asset/window/background.png"),
                                    content=self.main_display,alignment=ft.alignment.center)
        
    
    def start(self, e):
        self.start_mouse_x, self.start_mouse_y = system_func.get_mouse_position()
        #self.start_win_x, self.start_win_y, _, _ = system_func.get_window_position(self.hwnd)
        self.start_win_x = self.page.window.left
        self.start_win_y = self.page.window.top

    def drag(self, e):
        mouse_x, mouse_y = system_func.get_mouse_position()
        dx = mouse_x - self.start_mouse_x
        dy = mouse_y - self.start_mouse_y

        new_x = self.start_win_x + dx
        new_y = self.start_win_y + dy

        #self.x, self.y = system_func.move_window(new_x, new_y, self.hwnd)
        self.page.window.left = new_x
        self.page.window.top = new_y
        self.x = new_x
        self.y = new_y
        self.page.update()

        

        
        
        
        




if __name__ == "__main__":
    def main(page: ft.Page):
        page.window.width=300
        page.title = "abc"
        page.bgcolor = ft.Colors.TRANSPARENT
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.window.title_bar_hidden = True
        page.window.frameless = True
        page.window.height = 450

        main_w = Dragable_holder(page=page)
        t = ft.Container(width=30,height=450,bgcolor="RED", opacity=1)
        
        
        page.add(main_w)
        page.padding = 0
        page.update()
        with open("flet_pid.txt", "w") as f:
            f.write(str(os.getpid()))
        

    ft.app(target=main)