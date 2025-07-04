#bar test
import flet as ft


class Thumb(ft.GestureDetector):

    def __init__(self,width,height,thumb_color,thumb_size,x,y,controller,length):
        super().__init__()
        self.width = width
        self.height = height
        self.thumb_size = thumb_size
        self.thumb_color = thumb_color
        self.top = y
        self.left = x
        self.controller = controller
        self.length = length

        self.content = ft.Container(width=self.thumb_size,height=self.thumb_size,bgcolor=self.thumb_color,border_radius=self.width/2,alignment=ft.alignment.center)

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.end_drag

    def midpoint(self):
        return self.left + self.width/2,self.top+self.height/2
    
    def start_drag(self,e):
        self.controller.in_seek = True

    def drag(self,e):

        dx = e.delta_x
        self.left +=dx
        self.left = min(self.length,max(0,self.left))

        self.controller.update_in_seek(self.left/self.length)

    def end_drag(self,e):
        self.controller.in_seek = False
        percent = self.left/self.length

        self.controller.update_seek(percent)

    def update_thumb(self,percent):
        self.left = self.length*percent

class Bar(ft.Container):

    def __init__(self,
                 width,
                 height,
                 background_color,
                 buffer_color,
                 progress_color,
                 top,
                 left,
                 controller):
        super().__init__()
        self.width = width
        self.height = height
        self.background_color = background_color
        self.buffer_color = buffer_color
        self.progress_color = progress_color
        self.top = top
        self.left = left

        #controller
        self.controller = controller
        self.on_tap_down = self.click_handle

        #bar data
        self.buffered_lenght = 0
        self.progress_lenght = 0
        #display
        self.bgcolor = self.background_color

        self.buffer_bar = ft.Container(width=1,height=self.height,bgcolor=self.buffer_color,alignment=ft.alignment.center_left)

        self.progress_bar = ft.Container(width=1,height=self.height,bgcolor=self.progress_color,alignment=ft.alignment.center_left)

        self.buffer_bar.content = self.progress_bar

        self.content = self.buffer_bar
        self.alignment = ft.alignment.center_left

    
    def update_bar(self,buffered_percent = 0,progress_percent = 0):
        self.buffered_lenght = min(self.width,self.width*buffered_percent)
        self.progress_lenght = min(self.buffered_lenght,self.width*progress_percent)

        self.progress_bar.width = self.progress_lenght
        self.buffer_bar.width = self.buffered_lenght
        
    
    def click_handle(self,e):

        #callback to controller
        jump_percent = e.local_x/self.width
        self.controller.on_jump(jump_percent)

    

class Duration_bar(ft.Stack):

    def __init__(self,width,height):
        super().__init__()
        self.width = width
        self.height = height

        self.bar = Bar(self.width,5,
                       "#282828",
                       "#8D1919",
                       "#1CBAA2",
                       (self.height-5)/2,
                       0,
                       self)
        

        self.thumb = Thumb(width=height,height=height,thumb_color="WHITE",thumb_size=height,x=0,y=0,controller=self,length=self.width-height/2)
        
        self.controls = [self.bar,self.thumb]


        #controller
        self.progress_percent = 0
        self.buffer_percent = 0
    
    def on_jump(self,jump_percent):
        #tempo
        
        self.bar.update_bar(jump_percent,jump_percent)
        self.thumb.update_thumb(jump_percent)

        self.progress_percent = jump_percent
        
        self.buffer_percent = max(jump_percent,self.buffer_percent)

        self.update()
        

    def update_in_seek(self,percent):
        buffer_percent = self.bar.buffered_lenght/self.bar.width
        self.bar.update_bar(max(percent,buffer_percent),percent)
        self.update()

    def update_seek(self,percent):
        buffer_percent = self.bar.buffered_lenght/self.bar.width
        self.thumb.update_thumb(percent)
        self.bar.update_bar(max(percent,buffer_percent),percent)
        self.buffer_percent = max(percent,buffer_percent)
        self.progress_percent = percent
        self.update()
    
    def update_bar(self):
        self.bar.update_bar(self.buffer_percent,self.progress_percent)
        self.thumb.update_thumb(self.progress_percent)
        self.update()
    
#assosiate with player not steaming
class DuraController(Duration_bar):

    def __init__(self, width, height):
        super().__init__(width, height)
        #second
        self.duration = 0
        self.current_duration = 0
        self.current_buffer = 0
        self.player = None # assign player
        self.in_seek = False
    
    def update_duration(self,duration):
        # call interval 0.1 sec to update the duration calculte latency
        self.current_duration = duration
        #calculate percent progress
        progress = duration/self.duration
        self.progress_percent = progress
        self.update_bar()
    
    def update_buffer(self,time):
        # call interval 0.1 sec to update the duration calculte latency
        self.current_buffer = time
        self.current_buffer = min(self.duration,self.current_buffer)

        percent = self.current_buffer/self.duration
        self.buffer_percent = percent
        self.update_bar()

    def on_jump(self, jump_percent):
        super().on_jump(jump_percent)
        self.update()
        second = (jump_percent*self.duration)
        if self.player:
            self.player.seek(second)
        

    def update_seek(self, percent):
        super().update_seek(percent)
        second = (percent*self.duration)
        if self.player:
            self.player.seek(second)
        
        


    


    #add server logic
# from asset.player import playback as pb
# from asset.client_call import streaming_call as sc
# import time
# current_time = 0
# def main(page: ft.Page):
#     page.window.width = 300
#     page.window.height = 450
#     dura = DuraController(280,10)
#     player = pb.StreamingAudioPlayer()
#     duration,file,chunks = sc.get_header_data("sample")

#     page.add(dura)
#     dura.update()
#     page.update()
        

# ft.app(target=main)