import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

llm = ChatOpenAI(model_name=os.getenv("MODEL_NAME", "gpt-4o-mini"))

system_prompt = """
You are a code analysis assistant. For each code snippet, extract:
1. File summary
2. All method names, signatures, and descriptions
3. Estimated complexity (low/medium/high)

Respond as:
{
  "file": "<filename>",
  "summary": "<summary>",
  "methods": [
    {
      "name": "<method name>",
      "signature": "<signature>",
      "description": "<description>",
      "complexity": "<low/medium/high>"
    }
  ]
}
"""

def analyze_with_llm(file_path, code_chunk):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze this code from {file_path}:\n{code_chunk}")
    ]
    response = llm(messages)
    return response.content
