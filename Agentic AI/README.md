# Offline Cloud AI

This project is designed to create an offline cloud solution utilizing Agentic AI for data processing. The application focuses on summarizing PDF documents and transcribing audio files, making it easier to manage and analyze various data formats.

## Project Structure

```
offline-cloud-ai
├── src
│   ├── main.py                # Entry point of the application
│   ├── agents
│   │   ├── summarizer_agent.py # Agent for summarizing PDF files
│   │   └── transcriber_agent.py # Agent for transcribing audio files
│   ├── services
│   │   ├── pdf_service.py      # Service for handling PDF files
│   │   ├── audio_service.py     # Service for handling audio files
│   │   └── data_loader.py       # Service for loading various data formats
│   ├── utils
│   │   └── helpers.py           # Utility functions
│   └── config
│       └── settings.py          # Configuration settings
├── requirements.txt             # List of dependencies
└── README.md                    # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd offline-cloud-ai
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

### Summarizing a PDF

To summarize a PDF file, you can use the `SummarizerAgent` class from the `summarizer_agent.py` file. Here is an example:

```python
from agents.summarizer_agent import SummarizerAgent

agent = SummarizerAgent()
summary = agent.summarize_pdf('path/to/your/file.pdf')
print(summary)
```

### Transcribing Audio

To transcribe an audio file, you can use the `TranscriberAgent` class from the `transcriber_agent.py` file. Here is an example:

```python
from agents.transcriber_agent import TranscriberAgent

agent = TranscriberAgent()
transcription = agent.transcribe_audio('path/to/your/file.mp3')
print(transcription)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.