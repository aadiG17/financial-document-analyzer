## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("Read Financial Document")
def read_data_tool(file_path: str = 'data/sample.pdf') -> str:
    """Tool to read data from a PDF file and return its text content.

    Args:
        file_path (str, optional): Path of the PDF file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full text content of the financial document.
    """
    from pypdf import PdfReader

    reader = PdfReader(file_path)
    full_report = ""
    for page in reader.pages:
        content = page.extract_text() or ""

        # Remove extra whitespace and format properly
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")

        full_report += content + "\n"

    return full_report