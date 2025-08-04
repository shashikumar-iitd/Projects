from flask import Flask, render_template, request
from agents.summarizer_agent import SummarizerAgent
from agents.transcriber_agent import TranscriberAgent
from agents.web_search_agent import WebSearchAgent
from agents.coordinator_agent import CoordinatorAgent
from services.pdf_service import PDFService
from services.audio_service import AudioService
from config.settings import Config
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pdf_service = PDFService()
audio_service = AudioService()
summarizer = SummarizerAgent(pdf_service)
transcriber = TranscriberAgent(audio_service)
web_search_agent = WebSearchAgent(api_key=Config.API_KEY)
coordinator = CoordinatorAgent(summarizer, transcriber, web_search_agent)

@app.route('/', methods=['GET', 'POST'])
def index():
    pdf_summary = None
    audio_transcription = None
    web_results = None

    if request.method == 'POST':
        pdf_file = request.files.get('pdf_file')
        audio_file = request.files.get('audio_file')
        web_query = request.form.get('web_query')

        pdf_path = None
        audio_path = None

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(pdf_path)
        if audio_file and (audio_file.filename.endswith('.mp3') or audio_file.filename.endswith('.wav')):
            audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(audio_path)

        # Use the coordinator to process everything together
        results = coordinator.full_pipeline(pdf_path, audio_path, web_query if web_query else None)
        pdf_summary = results["pdf_summary"]
        audio_transcription = results["audio_transcription"]
        web_results = results["web_results"]

    return render_template(
        'index.html',
        pdf_summary=pdf_summary,
        audio_transcription=audio_transcription,
        web_results=web_results
    )

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request
# from mcp.client import McpClient as MCPClient  # Correct import for version 1.9.3
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# mcp_client = MCPClient("document_processor")

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     pdf_summary = None
#     audio_transcription = None
#     web_results = None

#     if request.method == 'POST':
#         pdf_file = request.files.get('pdf_file')
#         audio_file = request.files.get('audio_file')
#         web_query = request.form.get('web_query')

#         pdf_path = None
#         audio_path = None

#         if pdf_file and pdf_file.filename.endswith('.pdf'):
#             pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
#             pdf_file.save(pdf_path)
#         if audio_file and (audio_file.filename.endswith('.mp3') or audio_file.filename.endswith('.wav')):
#             audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
#             audio_file.save(audio_path)

#         if pdf_path:
#             pdf_summary = mcp_client.call("summarize_pdf", pdf_path=pdf_path)
#         if audio_path:
#             audio_transcription = mcp_client.call("transcribe_audio", audio_path=audio_path)
#         if web_query:
#             web_results = mcp_client.call("search_web", query=web_query)

#     return render_template(
#         'index.html',
#         pdf_summary=pdf_summary,
#         audio_transcription=audio_transcription,
#         web_results=web_results
#     )

# if __name__ == '__main__':
#     app.run(debug=True)