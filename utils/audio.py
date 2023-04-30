import sounddevice as sd
import wave
import whisper
import soundfile as sf
import numpy as np

class AudioRecorder:
    def __init__(self):
        self.transcription = None
        self.is_recording = False

    def transcribe(self, audio_file_path: str) -> str:
        # Read the audio data and sample rate from the file
        audio_data, sample_rate = sf.read(audio_file_path, dtype='int16')
        # Convert the audio data to a NumPy array
        audio_data = np.array(audio_data, dtype=np.float32) / 32768.0
        model = whisper.load_model("base")
        result = model.transcribe(audio_data)
        return result["text"]

    def record(self, temp_audio_file, duration=3):
        self.is_recording = True
        fs = 16000  # Sample rate
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        wav_data = (myrecording * np.iinfo(np.int16).max).astype(np.int16).tobytes()

        with wave.open(temp_audio_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(wav_data)

        self.transcription = self.transcribe(temp_audio_file.name)
        temp_audio_file.close()
        print(f"User asks: {self.transcription}")
        self.is_recording = False
