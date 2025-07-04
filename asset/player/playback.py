import threading
import time
import queue
import pyaudio
from pydub import AudioSegment
from io import BytesIO
class StreamingAudioPlayer:
    def __init__(self, chunk_ms=100):
        self.buffer = []
        self.chunk_ms = chunk_ms
        self.playing = False
        self.paused = False
        self.lock = threading.Lock()

        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100

        self.play_thread = None
        self.current_time = 0  # Track playback time
        self.read_index = 0

    def _playback(self):
            p = pyaudio.PyAudio()
            stream = p.open(format=self.audio_format,
                            channels=self.channels,
                            rate=self.rate,
                            output=True)

            while self.playing:
                if self.paused:
                    time.sleep(0.05)
                    continue

                with self.lock:
                    if self.read_index >= len(self.buffer):
                        self.wait_for_buffer()
                        continue

                    data = self.buffer[self.read_index]
                    self.read_index += 1
                    self.current_time = self.read_index * self.chunk_ms / 1000

                stream.write(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

    def wait_for_buffer(self, min_wait=0.1, max_wait=5):
        """Block until buffer is filled again (simulate slow net)"""
        waited = 0
        while self.buffer.empty() and self.playing and not self.paused:
            time.sleep(min_wait)
            waited += min_wait
            if waited >= max_wait:
                print("⚠ Buffer underrun!")
                break

    def play(self, min_buffer_chunks=1):
        """Start playback (wait for initial buffer size)"""
        with self.lock:
            if self.playing:
                return
            self.playing = True
            self.paused = False

            # Wait until enough chunks are available after read_index
            while (len(self.buffer) - self.read_index) < min_buffer_chunks:
                time.sleep(0.01)

            self.play_thread = threading.Thread(target=self._playback, daemon=True)
            self.play_thread.start()

    def pause(self):
        with self.lock:
            self.paused = True

    def resume(self):
        with self.lock:
            if self.playing:
                self.paused = False

    def stop(self):
        with self.lock:
            self.playing = False
            self.paused = False
            while not self.buffer.empty():
                self.buffer.get_nowait()
            self.current_time = 0

    def seek(self, seconds):
        with self.lock:
            
            self.paused = True
            self.read_index = int((seconds * 1000) / self.chunk_ms)
            self.read_index = max(0, min(self.read_index, len(self.buffer)-1))
            self.current_time = self.read_index * self.chunk_ms / 1000
            self.paused = False


    def add_to_ram(self,bytess):
        sound = AudioSegment.from_file(BytesIO(bytess), format="mp3")
        sound = sound.set_channels(self.channels).set_frame_rate(self.rate)

        for i in range(0, len(sound), self.chunk_ms):
            chunk = sound[i:i+self.chunk_ms]
            self.buffer.append(chunk.raw_data)


    def get_current_time(self):
        return self.current_time
