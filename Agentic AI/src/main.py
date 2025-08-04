from agents.summarizer_agent import SummarizerAgent
from agents.transcriber_agent import TranscriberAgent
from agents.web_search_agent import WebSearchAgent
from agents.coordinator_agent import CoordinatorAgent
from services.pdf_service import PDFService
from services.audio_service import AudioService
from config.settings import CONFIG, Config

def main():
    print("Initializing MCP server...")

    pdf_service = PDFService()
    audio_service = AudioService()
    summarizer = SummarizerAgent(pdf_service)
    transcriber = TranscriberAgent(audio_service)
    web_search_agent = WebSearchAgent(api_key=Config.API_KEY)

    coordinator = CoordinatorAgent(summarizer, transcriber, web_search_agent)

    pdf_file_path = CONFIG['pdf_file_path']
    audio_file_path = CONFIG['audio_file_path']

    user_query = input("Enter a web search query (or leave blank to skip): ").strip()
    results = coordinator.full_pipeline(pdf_file_path, audio_file_path, user_query if user_query else None)

    print("\nPDF Summary:", results["pdf_summary"])
    print("\nAudio Transcription:", results["audio_transcription"])
    if results["web_results"]:
        print("\nWeb Search Results:")
        for idx, result in enumerate(results["web_results"], 1):
            print(f"{idx}. {result['title']}\n   {result['link']}")

if __name__ == "__main__":
    main()


# from mcp.client import McpClient as MCPClient  # Correct import for version 1.9.3
# from config.settings import CONFIG

# def main():
#     print("Connecting to MCP server...")

#     mcp_client = MCPClient("document_processor")

#     pdf_file_path = CONFIG['pdf_file_path']
#     audio_file_path = CONFIG['audio_file_path']

#     user_query = input("Enter a web search query (or leave blank to skip): ").strip()

#     pdf_summary = mcp_client.call("summarize_pdf", pdf_path=pdf_file_path) if pdf_file_path else None
#     audio_transcription = mcp_client.call("transcribe_audio", audio_path=audio_file_path) if audio_file_path else None
#     web_results = mcp_client.call("search_web", query=user_query) if user_query else None

#     print("\nPDF Summary:", pdf_summary)
#     print("\nAudio Transcription:", audio_transcription)
#     if web_results:
#         print("\nWeb Search Results:")
#         for idx, result in enumerate(web_results, 1):
#             print(f"{idx}. {result['title']}\n   {result['link']}")

# if __name__ == "__main__":
#     main()