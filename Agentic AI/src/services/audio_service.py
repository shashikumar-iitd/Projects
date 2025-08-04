from pydub import AudioSegment
import speech_recognition as sr
import os

class AudioService:
    def convert_audio_to_text(self, audio_file_path):
        """
        Converts an audio file to text using speech recognition.
        """
        temp_wav_path = "temp_audio.wav"
        try:
            # Load and export audio to WAV
            audio = AudioSegment.from_file(audio_file_path)
            audio.export(temp_wav_path, format="wav")

            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    return "Audio could not be understood"
                except sr.RequestError as e:
                    return f"Could not request results from Google Speech Recognition service; {e}"
        finally:
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)