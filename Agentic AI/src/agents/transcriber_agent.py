class TranscriberAgent:
    """
    Agent for transcribing audio files using the provided audio service.
    """
    def __init__(self, audio_service):
        self.audio_service = audio_service

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes the audio file at the given path and returns the transcribed text.
        """
        try:
            transcribed_text = self.audio_service.convert_audio_to_text(audio_file_path)
            return transcribed_text
        except Exception as e:
            return f"Error during transcription: {str(e)}"