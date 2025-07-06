from asset.player import playback as pb
from asset.client_call import streaming_call as sc
from asset.layout.playback_layout import *
import time
import threading
import os


current_time = 0

bt = 0
chunks_duration = []
def wait_for_file(path, timeout=10):
    start = time.time()
    while not os.path.exists(path):
        time.sleep(0.01)
        if time.time() - start > timeout:
            raise FileNotFoundError(f"Timed out waiting for {path}")

def stream(chunk,player,file):
    global bt,chunks_duration
    for i in range(chunk):
        st = time.time()
        data = sc.data_call(filename=file,chunks=i)
        bt += chunks_duration[i]
        #wait_for_file(f"./asset/cache/{file}/chunk_{i}.mp3")
        
        player.add_to_ram(data)
        #player.add_to_buffer(f"./asset/cache/{file}/chunk_{i}.mp3")
        
        if i==0:
            player.play()
        



def main(page: ft.Page):
    global chunks_duration
    page.window.width = 300
    page.window.height = 450
    #DuraController(280,10)
    player = pb.StreamingAudioPlayer()
    
    duration,file,chunks,chunks_duration = sc.get_header_data("sample3")
    dura = dura_bar(width=280,height=15,duration=duration,dura_width=200,dura_height=10,text_width=30,player=player)
    
    os.makedirs(f"./asset/cache/{file}/",exist_ok=True)
    dura.duration = duration

    dura.player = player
    isplay = True
    threading.Thread(target=stream,args=(chunks,player,file,),daemon=True).start()
    #update loop
    page.add(dura)
    while isplay:
        buffduration = bt
        current_time = player.current_time
        if not dura.DURA.in_seek:
            dura.update_progress(current_time)
        dura.update()
        time.sleep(0.1)
    
    dura.update()
    page.update()
        

ft.app(target=main)