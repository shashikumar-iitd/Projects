import os
import PyPDF2
import pandas as pd
import json

def load_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        return text.strip()
    except Exception as e:
        return f"Error loading PDF: {e}"

def load_csv(file_path):
    """Loads a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        return f"Error loading CSV: {e}"

def load_json(file_path):
    """Loads a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return f"Error loading JSON: {e}"

def load_txt(file_path):
    """Loads a text file."""
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text.strip()
    except Exception as e:
        return f"Error loading TXT: {e}"

def load_audio(file_path):
    """Placeholder for audio loading."""
    return f"Audio file loaded from {file_path}"

def load_data(file_path):
    """
    Loads data based on file extension.
    Supports: .pdf, .csv, .json, .txt, .wav, .mp3, .m4a
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    if file_extension == '.pdf':
        return load_pdf(file_path)
    elif file_extension == '.csv':
        return load_csv(file_path)
    elif file_extension == '.json':
        return load_json(file_path)
    elif file_extension == '.txt':
        return load_txt(file_path)
    elif file_extension in ['.wav', '.mp3', '.m4a']:
        return load_audio(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")