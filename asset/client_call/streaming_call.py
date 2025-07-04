import requests
import os
  # no extension
url = "http://127.0.0.1:5000"


current_sesion = requests.Session()
def get_header_data(filename):
    
    r = current_sesion.post(f"{url}/req_header/{filename}", data="OK")
    
    r = r.json()
    
    if r!= {'error': 'file not found'}:
        duration,fil,num_chunks,chunk_duras = r["duration"],r['filename'],r['num_chunks'],r['chunk_durations']
        return duration,fil,num_chunks,chunk_duras
    else:
        return

import time
def data_call(filename, chunks):
    start_time = time.time()
    try:
        
        #r = current_sesion.post(f"{url}/req_chunk/{filename}", data=str(chunks))
        r = current_sesion.get(f"{url}/req_chunk/{filename}?id={chunks}")
        
        if r.ok and r.headers.get("Content-Type", "") == "audio/mpeg":
            
            return r.content
        else:
            
            return None
    except requests.exceptions.Timeout:
        
        return None



if __name__ == "__main__":
    from asset.player.playback import *

    def simulate():
        player = StreamingAudioPlayer()

        # Start player thread
        
        dura,file,num_chunks = get_header_data(filename=filename)
        #request new chunks
        os.makedirs(f"./asset/cache/{file}/",exist_ok=True)
        for i in range(num_chunks):
            data_call(file,chunks=i)
            player.add_to_buffer(f"./asset/cache/{file}/chunk_{i}.mp3")
            if i == 0:
                player.play()
            if player.current_time>50:
                player.seek(70)
            print("recived chunk",i)


    simulate()

        