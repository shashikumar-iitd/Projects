class SummarizerAgent:
    def __init__(self, pdf_service, summary_length=150):
        """
        Initializes the SummarizerAgent with a PDF service and summary length.
        """
        self.pdf_service = pdf_service
        self.summary_length = summary_length

    def summarize_pdf(self, pdf_file_path):
        """
        Extracts text from a PDF and returns a summary.
        """
        try:
            text = self.pdf_service.extract_text(pdf_file_path)
            summary = self._generate_summary(text)
            return summary
        except Exception as e:
            return f"Error during summarization: {str(e)}"

    def _generate_summary(self, text):
        """
        Generates a simple summary from the extracted text.
        """
        return text[:self.summary_length] + '...' if len(text) > self.summary_length else text