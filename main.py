import os
import json
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()

# ----------------------------
# CONFIGURATION
# ----------------------------
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
SOURCE_DIR = "SakilaProject"
OUTPUT_FILE = "outputs/extracted_knowledge.json"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ----------------------------
# INIT LLM
# ----------------------------
llm = ChatOpenAI(
     model_name=os.getenv("MODEL_NAME", "anthropic/claude-3-haiku"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0
)

system_prompt = """
You are a code analysis assistant. For each code snippet, extract:
1. File summary
2. All method names, signatures, and descriptions
3. Estimated complexity (low/medium/high) with different lines of analysis
4. Any bugs or code quality suggestions

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

# ----------------------------
# UTILITIES
# ----------------------------

def load_files(directory, extensions=(".java",)):
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extensions):
                path = os.path.join(root, filename)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    files[path] = f.read()
    return files

def chunk_code(content, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(content)

def analyze_with_llm(file_path, code_chunk):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze this code from {file_path}:\n{code_chunk}")
    ]
    response = llm(messages)
    return response.content

def write_json(data, path=OUTPUT_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ----------------------------
# MAIN LOGIC
# ----------------------------

def main():
    print(f" Loading files from: {SOURCE_DIR}")
    files = load_files(SOURCE_DIR)
    extracted = {}

    for file_path, content in tqdm(files.items(), desc="🔎 Analyzing files"):
        chunks = chunk_code(content)
        file_summary = []

        for i, chunk in enumerate(chunks):
            try:
                print(f" Analyzing chunk {i+1}/{len(chunks)} of {file_path}...")
                result = analyze_with_llm(file_path, chunk)
                file_summary.append(result)
            except Exception as e:
                print(f" Error in {file_path} chunk {i+1}: {e}")
        
        extracted[file_path] = file_summary

    write_json(extracted)
    print(f"\n Analysis complete. Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
