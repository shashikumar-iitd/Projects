class CoordinatorAgent:
    def __init__(self, summarizer, transcriber, web_search):
        self.summarizer = summarizer
        self.transcriber = transcriber
        self.web_search = web_search

    def process_pdf_and_search(self, pdf_path, search_query=None):
        summary = self.summarizer.summarize_pdf(pdf_path)
        web_results = None
        if search_query:
            web_results = self.web_search.search(search_query)
        return summary, web_results

    def process_audio_and_search(self, audio_path, search_query=None):
        transcription = self.transcriber.transcribe_audio(audio_path)
        web_results = None
        if search_query:
            web_results = self.web_search.search(search_query)
        return transcription, web_results

    def full_pipeline(self, pdf_path, audio_path, search_query=None):
        summary = self.summarizer.summarize_pdf(pdf_path)
        transcription = self.transcriber.transcribe_audio(audio_path)
        web_results = None
        if search_query:
            web_results = self.web_search.search(search_query)
        return {
            "pdf_summary": summary,
            "audio_transcription": transcription,
            "web_results": web_results
        }