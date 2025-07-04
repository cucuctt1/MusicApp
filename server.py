from flask import Flask, request, redirect, jsonify, send_file,Response
from pydub import AudioSegment
from io import BytesIO
import os, json
import threading
app = Flask(__name__)

CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

# Define custom chunk durations (in milliseconds)
PROGRESSIVE_CHUNK_MS = [500,500,500,500,1000,1000,2000,2000,3000, 3000, 5000, 7000]  # Then repeat 10s hardcoded
DEFAULT_CHUNK_MS = 10000

@app.route('/')
def index():
    return redirect('/upload')





@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = os.path.splitext(file.filename)[0]
        folder = os.path.join(CACHE_DIR, filename)
        os.makedirs(folder, exist_ok=True)

        # Process audio
        audio = AudioSegment.from_file(file)
        duration_sec = len(audio) / 1000
        pointer = 0
        chunks = []
        chunk_durations = []

        # Apply progressive chunking
        while pointer < len(audio):
            if len(chunk_durations) < len(PROGRESSIVE_CHUNK_MS):
                chunk_len = PROGRESSIVE_CHUNK_MS[len(chunk_durations)]
            else:
                chunk_len = DEFAULT_CHUNK_MS

            chunk = audio[pointer: pointer + chunk_len]
            chunks.append(chunk)
            chunk_durations.append(len(chunk) / 1000.0)  # save in seconds
            pointer += chunk_len

        # Save chunks
        for idx, chunk in enumerate(chunks):
            chunk_path = os.path.join(folder, f"chunk_{idx}.mp3")
            chunk.export(chunk_path, format="mp3")

        # Save metadata
        header = {
            'filename': filename,
            'num_chunks': len(chunks),
            'duration': duration_sec,
            'chunk_durations': chunk_durations
        }
        with open(os.path.join(folder, "header.json"), 'w') as f:
            json.dump(header, f)

        return f'Saved {len(chunks)} chunks to {folder}'

    return '''
    <h1>Upload Audio</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept="audio/*">
        <input type="submit" value="Upload">
    </form>
    '''

preload_dict = {}
max_preload = 10 #10 chunk ahead
def preload(filename,n=1):
    global max_preload,preload_dict
    print("start preload")
    # check if song not ever loaded
    if not filename in preload_dict:
        preload_dict[filename] = [] #chunk data
    
    #find the file 
    for i in range(n):
        preloaded_idx = len(preload_dict[filename])
        if os.path.exists(f".\cache\{filename}\chunk_{preloaded_idx}.mp3"):
            with open(f".\cache\{filename}\chunk_{preloaded_idx}.mp3","rb") as f:
                preload_dict[filename].append(f.read())
        else:
            break
    print(len(preload_dict[filename]))
    

    


    
@app.route('/req_header/<filename>', methods=['POST'])
def req_header(filename):
    folder = os.path.join(CACHE_DIR, filename)
    header_path = os.path.join(folder, "header.json")

    if not os.path.exists(header_path):
        return jsonify({'error': 'file not found'}), 404

    ok = request.data.decode().strip()
    if ok != 'OK':
        return jsonify({'error': 'must send OK first'}), 400

    with open(header_path, 'r') as f:
        header = json.load(f)
    #add to preloadict
    if not filename in preload_dict:
        preload_dict[filename] = [] #chunk data
    threading.Thread(target=preload,args=(filename,5,),daemon=True).start()
    return jsonify(header)

@app.route('/req_chunk/<filename>', methods=['GET'])
def req_chunk(filename):
    global preload_dict
    chunk_index = int(request.args.get("id", "0"))




    


    # chunk_path = os.path.join(folder, f"chunk_{chunk_index}.mp3")
    # if not os.path.exists(chunk_path):
    #     return jsonify({'error': 'chunk not found'}), 404
    threading.Thread(target=preload,args=(filename,2,),daemon=True).start()
    return Response(preload_dict[filename][chunk_index],mimetype="audio/mpeg")

    return send_file(chunk_path, mimetype='audio/mpeg',as_attachment=False,
        conditional=True,)

if __name__ == '__main__':
    app.run(debug=True)
