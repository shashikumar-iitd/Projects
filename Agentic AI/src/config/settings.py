# Configuration settings for the offline cloud AI application

class Config:
    PDF_DIRECTORY = "path/to/pdf/files"
    AUDIO_DIRECTORY = "path/to/audio/files"
    OUTPUT_DIRECTORY = "path/to/output/files"
    LOGGING_LEVEL = "INFO"
    API_KEY = "e93a2ff8baac5675f44d83135a2cbf00daa5c64547acf72373f9140d85bd25b1"  # Replace with your actual API key

    # Actual file paths for testing
    PDF_FILE = r"C:\Users\shash\OneDrive\Desktop\AAI\testpdf.pdf"
    AUDIO_FILE = r"C:\Users\shash\Downloads\4_Clap_Your_Hands.mp3"

    @staticmethod
    def init_app(app):
        pass

CONFIG = {
    "pdf_file_path": Config.PDF_FILE,
    "audio_file_path": Config.AUDIO_FILE
}