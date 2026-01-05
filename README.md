# Generative AI Projects

A collection of AI-powered automation and information retrieval projects leveraging LLMs, RAG, and multi-agent systems.

## Projects

### 1. [unit_tests_generator](./unit_tests_generator/)

**Type**: Multi-Agent Flow-Based Automation

**Description**: Complete workflow automation for unit test generation using CrewAI Flows. Clones repositories, generates unit tests, and commits to a new branch. Features a flow-based architecture.

![Flow Diagram](https://github.com/ramandeep11/Generative-AI-Applications/blob/main/unit_tests_generator/Screenshot%202026-01-05%20at%209.28.01%E2%80%AFPM.png)

**Key Features**:
- Complete end-to-end workflow from clone to commit
- Three specialized crews: GitClone, GenerateUnitTest, GitCheckoutAndCommit
- Hierarchical process with manager agent for test generation
- Custom tools: GitCloneTool, FileWriterTool, ProjectBuildTool
- Build validation

**Tech Stack**: CrewAI Flows 1.7.2, OpenAI GPT-4o-mini, Python 3.10+, GitPython

**[→ View Full Documentation](./unit_tests_generator/README.md)**

---

### 2. [unit_tests_generator_with_feedback_loop](./unit_tests_generator_with_feedback_loop/)

**Type**: Iterative AI System with Feedback Loop

**Description**: AI-powered unit test generator with iterative feedback loop to refine tests until they compile successfully. Starts from pre-cloned repositories and focuses on the generate-build-refine cycle with separate crews for each step.

![Flow Diagram](https://github.com/ramandeep11/Generative-AI-Applications/blob/main/unit_tests_generator_with_feedback_loop/Screenshot%202026-01-05%20at%209.26.58%E2%80%AFPM.png)

**Key Features**:
- Dedicated feedback loop architecture (no git clone step)
- Separate BuildProjectCrew for validation
- Router-based retry logic with build feedback
- Maximum 3 retry attempts with error analysis
- Pydantic output models for structured results
- Sequential process for predictable flow

**Tech Stack**: CrewAI Flows 1.7.2, OpenAI GPT-4o-mini, Python 3.10+, GitPython

**[→ View Full Documentation](./unit_tests_generator_with_feedback_loop/README.md)**

---

### 3. [RAG](./RAG/)

**Type**: Retrieval-Augmented Generation System

**Description**: A Flask-based RAG system with OCR capabilities that processes text and images from webpages and PDFs to answer user queries. The system combines document processing, image text extraction using Tesseract OCR, vector storage with Chroma, and LLM-powered question answering using local models via Ollama.

**Key Features**:
- PDF document processing and querying
- Webpage content extraction with image OCR support
- Advanced image preprocessing for accurate text extraction
- Vector storage with Chroma and FastEmbed embeddings
- Interactive Gradio UI with conversation history
- Multiple API endpoints for different use cases
- Source attribution in responses

**Tech Stack**: Flask, LangChain, Ollama (Qwen 2.5 Coder), Tesseract OCR, Chroma, Gradio, BeautifulSoup

**[→ View Full Documentation](./RAG/README.md)**

---

### 4. [LLM_with_Web](./LLM_with_Web/)

**Type**: LLM-Powered Web Search & Analysis

**Description**: An intelligent campaign information retrieval system that combines LLM capabilities with web search and scraping to extract current marketing campaign details for companies across different regions. The system searches the web using DuckDuckGo, scrapes relevant content, and uses AI to generate concise campaign summaries.

**Key Features**:
- DuckDuckGo web search integration
- Automated web scraping with BeautifulSoup
- LLM-powered content analysis and summarization
- Multi-region support (Japan, US, UK)
- Simple Gradio UI for easy interaction
- Single-line campaign summaries
- Local LLM execution (no API keys required)

**Tech Stack**: DuckDuckGo Search API, BeautifulSoup, LangChain, Ollama (Deepseek-R1), Gradio

**[→ View Full Documentation](./LLM_with_Web/README.md)**

---

## Common Prerequisites

All projects require:

### Ollama
```bash
# Install Ollama for local LLM inference
# Visit https://ollama.ai for installation

# Pull required models
ollama pull qwen2.5-coder:7b    # For RAG project
ollama pull deepseek-r1         # For LLM_with_Web project
```

### Python
- Python 3.10+ (Unit-test-generator requires <3.14)
- Virtual environment recommended

### Environment Setup
```bash
# For all unit test generator projects
export OPENAI_API_KEY="your-api-key"

# For RAG (install Tesseract)
brew install tesseract  # macOS
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
```

---

## Quick Start

### unit_tests_generator
```bash
cd unit_tests_generator
crewai install
crewai flow kickoff
```

### unit_tests_generator_with_feedback_loop
```bash
cd unit_tests_generator_with_feedback_loop
crewai install
crewai flow kickoff
```

### RAG
```bash
cd RAG
pip install flask langchain chromadb gradio pytesseract beautifulsoup4
python rag.py  # Start API server
python ChatUI.py  # Launch UI (in separate terminal)
```

### LLM_with_Web
```bash
cd LLM_with_Web
pip install gradio duckduckgo-search beautifulsoup4 langchain
python ScrapeUI.py
```

---

## Project Comparison

| Feature | unit_tests_generator | unit_tests_generator_with_feedback_loop | RAG | LLM_with_Web |
|---------|---------------------|----------------------------------------|-----|--------------|
| **Primary Use** | Complete test workflow | Test refinement loop | Document Q&A | Web research |
| **LLM Provider** | OpenAI API | OpenAI API | Ollama (Local) | Ollama (Local) |
| **Framework** | CrewAI Flows | CrewAI Flows | Flask + LangChain | LangChain |
| **UI** | CLI | CLI | Gradio | Gradio |
| **Crews** | 3 crews | 3 crews | Single pipeline | Single agent |
| **Process** | Hierarchical + Sequential | Sequential | Pipeline | Single step |
| **Git Operations** | Clone + Commit | Commit only | None | None |
| **Data Source** | Git repositories | Pre-cloned repos | PDFs, Webpages | Web search |
| **Output** | Generated + committed tests | Generated + committed tests | Answers + sources | Campaign summaries |
| **Retry Logic** | Router-based (3 max) | Router-based (3 max) | None | None |

---

## Architecture Patterns

### unit_tests_generator: Complete Workflow
```
Start → Git Clone → Generate/Build/Validate → Checkout & Commit → End
```

### unit_tests_generator_with_feedback_loop: Feedback Loop
```
Start → Generate → Build → Checkout & Commit → End
            ↑         ↓
            └─(retry)─┘
        (with feedback, max 3 times)
```

### RAG: Pipeline Pattern
```
Document → Split → Embed → VectorDB → Retrieve → LLM → Answer
```

### LLM_with_Web: Search-Analyze Pattern
```
Query → Search → Scrape → LLM Analysis → Summary
```

---

## License

See individual project directories for license information.

---

## Contributing

Each project is independent. Please refer to individual project READMEs for specific contribution guidelines.

---

## Support

For issues or questions:
1. Check the individual project README
2. Review troubleshooting sections
3. Ensure all prerequisites are installed
4. Verify Ollama is running (for RAG and LLM_with_Web)
5. Check API key configuration (for Unit-test-generator)