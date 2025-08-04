import PyPDF2

class PDFService:
    def extract_text(self, pdf_path):
        """
        Extracts text from a PDF file.
        """
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        return text.strip()

    @staticmethod
    def save_summary_to_file(summary, output_path):
        """
        Saves the summary to a text file.
        """
        with open(output_path, "w") as file:
            file.write(summary)