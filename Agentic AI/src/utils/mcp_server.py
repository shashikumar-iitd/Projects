# src/utils/mcp_server.py
import sys
import os

# Add the src/ directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp.server.fastmcp import FastMCP
from agents.coordinator_agent import CoordinatorAgent
from agents.summarizer_agent import SummarizerAgent
from agents.transcriber_agent import TranscriberAgent
from agents.web_search_agent import WebSearchAgent
from services.pdf_service import PDFService
from services.audio_service import AudioService
from config.settings import Config

# Initialize services and agents
pdf_service = PDFService()
audio_service = AudioService()
summarizer = SummarizerAgent(pdf_service)
transcriber = TranscriberAgent(audio_service)
web_search_agent = WebSearchAgent(api_key=Config.API_KEY)
coordinator = CoordinatorAgent(summarizer, transcriber, web_search_agent)

# Initialize the MCP Server
mcp = FastMCP("document_processor", description="A server to process documents and perform web searches")

# Define MCP tools for each functionality
@mcp.tool()  # Fixed: Added parentheses
def summarize_pdf(pdf_path: str) -> str:
    """Summarize a PDF file given its path."""
    results = coordinator.full_pipeline(pdf_path, None, None)
    return results["pdf_summary"]

@mcp.tool()  # Fixed: Added parentheses
def transcribe_audio(audio_path: str) -> str:
    """Transcribe an audio file given its path."""
    results = coordinator.full_pipeline(None, audio_path, None)
    return results["audio_transcription"]

@mcp.tool()  # Fixed: Added parentheses
def search_web(query: str) -> list:
    """Perform a web search with the given query."""
    results = coordinator.full_pipeline(None, None, query)
    return results["web_results"]

# Start the MCP Server
if __name__ == "__main__":
    mcp.run()