# Baatchit - AI Chatbot

A sophisticated, multi-threaded AI chatbot application built with LangGraph, OpenAI's GPT-4o-mini, and Streamlit. Baatchit provides an intuitive conversational interface with advanced features including document understanding, web search, stock price tracking, and extensible tool integration through Model Context Protocol (MCP).

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## ✨ Features

### Core Chat Features

- **Interactive Conversational Interface**: Real-time chat interface powered by Streamlit with a clean, user-friendly design
- **Multi-Threaded Conversations**: Maintain multiple independent conversations with separate session states and context
- **Persistent Conversation History**: All conversations are automatically saved and can be restored at any time
- **Real-Time Streaming Responses**: Stream AI responses character-by-character for a seamless user experience
- **Context-Aware Replies**: AI maintains context across multiple turns within a conversation thread

### Document Understanding (RAG)

- **PDF Upload and Indexing**: Upload PDF documents directly in the chat interface
- **Automatic PDF Processing**: PDFs are automatically chunked, embedded, and indexed into a vector store
- **Semantic Search**: Query relevant information from uploaded PDFs using similarity-based retrieval
- **Multi-Document Support**: Upload multiple PDFs per conversation thread
- **Document Metadata Tracking**: Track filename, number of pages, and number of chunks for each indexed PDF
- **Smart Chunking**: Recursive document splitting with configurable chunk size (1000 chars) and overlap (200 chars)
- **FAISS Vector Store**: High-performance similarity search using FAISS (Facebook AI Similarity Search)
- **OpenAI Embeddings**: State-of-the-art embedding model (text-embedding-3-small) for semantic understanding

### Tool Integration

#### Built-in Tools

1. **Web Search Tool**
   - Powered by DuckDuckGo API
   - Regional search support (US-EN)
   - Real-time internet search capabilities
   - Returns relevant search results for user queries

2. **Stock Price Fetcher**
   - Fetch real-time stock prices using Alpha Vantage API
   - Support for major stock symbols (AAPL, TSLA, etc.)
   - Latest quote data and market information
   - Seamless integration with conversation flow

3. **RAG Tool (Retrieval-Augmented Generation)**
   - Retrieve relevant information from uploaded PDFs
   - Thread-aware document retrieval
   - Returns query results with context and metadata
   - Source file attribution for transparenc
   - Similarity-based document retrieval with top-4 results

#### MCP (Model Context Protocol) Tools

The application supports extensible tool integration through Model Context Protocol:

**Arithmetic Operations Server** (`mcp_server/arith`):
- `add(a, b)`: Addition operation
- `sub(a, b)`: Subtraction operation
- `mul(a, b)`: Multiplication operation
- `div(a, b)`: Division operation with zero-division protection
- `pow(a, b)`: Exponentiation operation
- `modulus(a, b)`: Modulo operation with zero-division protection

**Expense Tracking Service**:
- External HTTP-based MCP service for expense tracking
- Seamless integration with FastMCP adapter

### Session & Persistence Features

- **SQLite Checkpointing**: All conversation states are persisted to SQLite database
- **Thread Management**: Create, manage, and switch between conversation threads
- **Session State Management**: Automatic session initialization and state restoration
- **Async Runtime Management**: Efficient async task handling with proper queue management
- **Conversation Recovery**: Restore previous conversations from database

### User Interface Features

- **Sidebar Navigation**
  - "New Chat" button to start fresh conversations
  - Recent conversations list with truncated previews
  - PDF status indicator showing current indexed document
  - PDF upload widget for document ingestion
  - Document indexing progress indicator

- **Main Chat Area**
  - Full conversation history display
  - User and assistant message differentiation
  - Real-time streaming response visualization
  - Document metadata display after each response
  - Clean, readable message formatting

- **Status Indicators**
  - Active PDF document display in sidebar
  - Chunk and page count for indexed PDFs
  - Tool usage indicators (e.g., "🔧 Using `search_tool`")
  - Indexing progress with status updates

### Advanced Features

- **Intelligent Tool Selection**: LLM automatically selects appropriate tools based on user queries
- **Conditional Tool Execution**: Tools are only executed when the LLM determines they're needed
- **Tool Result Streaming**: Tool outputs are streamed back to the user in real-time
- **Error Handling**: Graceful error handling for missing documents, tool failures, and invalid inputs
- **Typestack Messages**: Messages are filtered to show only user and assistant content

## System Architecture

- **State Management**: LangGraph-based state machine for conversation flow
- **Async Queue Processing**: Efficient async task queuing for non-blocking operations
- **Multi-Server MCP Client**: Unified client for connecting to multiple MCP servers
- **Configuration-Based Threading**: Thread IDs passed through configuration for proper context isolation

### Security Features

- **API Key Management**: Environment variable-based API key storage
- **Error Suppression**: MCP tool loading gracefully degrades if servers are unavailable
- **Query Validation**: Input validation for stock symbols and numeric operations
- **Division by Zero Protection**: Safe arithmetic operations with proper error handling

## 🏗️ Project Structure

```
Baatchit - Chatbot/
├── backend/                      # Backend services and core logic
│   ├── __init__.py              # Exports main API
│   ├── app.py                   # Core application setup
│   ├── async_runtime.py         # Async task execution and management
│   ├── checkpoint.py            # SQLite persistence layer
│   ├── graph.py                 # LangGraph conversation state machine
│   ├── llm_setup.py             # OpenAI LLM and embeddings configuration
│   ├── pdf_index.py             # PDF ingestion and vector store management
│   └── tools.py                 # Tool definitions and MCP client setup
├── frontend/                     # Streamlit UI application
│   ├── __init__.py
│   ├── app.py                   # Main Streamlit application
│   ├── conversation.py          # Conversation loading and history management
│   ├── state.py                 # Session state initialization and management
│   └── streaming.py             # Real-time response streaming logic
├── mcp_server/                  # Model Context Protocol server
│   ├── main.py                  # Arithmetic operations MCP server
│   ├── pyproject.toml           # Python project configuration
│   └── README.md                # MCP server documentation
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key for GPT-4o-mini access
- Alpha Vantage API key for stock price data (optional)
- 2GB+ RAM recommended
- 500MB+ disk space for vector stores

## 🚀 Installation

### 1. Clone or Extract the Project

```bash
cd "Baatchit - Chatbot"
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Streamlit for UI
- LangChain and LangGraph for orchestration
- OpenAI client library
- FAISS for vector search
- FastMCP for tool integration
- Additional supporting libraries

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Alpha Vantage Stock API (Optional)
# Note: API key is currently hardcoded in tools.py - recommend moving to env var
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

**Note:** The Alpha Vantage API key is currently hardcoded in [backend/tools.py](backend/tools.py). For security, it's recommended to move this to an environment variable and rotate the key if it's been exposed.

### OpenAI Models

The application uses:
- **Chat Model**: `gpt-4o-mini` - Latest small model (efficient and cost-effective)
- **Embeddings Model**: `text-embedding-3-small` - Latest small embedding model for semantic search

To use different models, modify [backend/llm_setup.py](backend/llm_setup.py)

### MCP Server Configuration

MCP servers are configured in [backend/tools.py](backend/tools.py):

```python
"arith": {             # Arithmetic operations server
    "transport": "stdio",
    "command": "python",
    "args": ["mcp_server\\main.py"],
}
"expense": {          # External expense tracking service
    "transport": "http",
    "url": "https://splendid-gold-dingo.fastmcp.app/mcp",
}
```

## 💻 Usage

### Starting the Application

```bash
python run.py
```

The Streamlit application will start on `http://localhost:8501`

### Basic Workflow

1. **Open the Application**: Navigate to the Streamlit app in your browser
2. **Upload a PDF** (Optional): Use the file uploader in the sidebar
3. **Start Chatting**: Type your query in the chat input box
4. **View Responses**: The AI will respond with streaming text
5. **Switch Conversations**: Click any conversation in the sidebar to switch threads
6. **Create New Chat**: Click "New Chat" to start a fresh conversation

### Example Queries

```
# Document queries (if PDF uploaded)
"Summarize the main points from the document"
"What does section 3 discuss?"

# Web searches
"What are the latest developments in AI?"
"Tell me about Python 3.13"

# Stock prices
"What's the current price of AAPL?"
"Get me TSLA stock information"

# Arithmetic (via MCP)
"What is 15 + 27?"
"Calculate 125 divided by 5"
```

### Advanced Features

**Multi-Thread Browsing**: In the sidebar, you can:
- View all previous conversation threads
- Click any thread to load its history
- See a preview of each conversation (first user message, truncated)

**Document Management**: 
- View the currently indexed PDF in the sidebar
- See statistics (chunks, pages) for indexed documents
- Upload different PDFs in different conversation threads

## 🏛️ Architecture

### Conversation Flow

```
User Input 
    ↓
[Streamlit Frontend] 
    ↓
[LangGraph Chat Node] → [LLM Decision]
    ↓
┌─ Tool Needed? 
│   ├─ YES → [Tool Node] → Execute Tool → [Chat Node] (loop)
│   └─ NO → [Direct Response]
    ↓
[Response Streaming] → [Streamlit Output]
    ↓
[SQLite Checkpoint] (persistence)
```

### Component Interaction

1. **Frontend (Streamlit)**
   - Handles user interface and I/O
   - Manages session state
   - Streams responses in real-time

2. **Backend (LangGraph)**
   - Orchestrates conversation flow
   - Manages chat state machine
   - Handles tool invocation logic

3. **LLM (OpenAI GPT-4o-mini)**
   - Generates responses
   - Determines tool usage
   - Maintains context and reasoning

4. **RAG System**
   - Stores PDF embeddings
   - Retrieves relevant documents
   - Augments generation with context

5. **Tools**
   - Web search (DuckDuckGo)
   - Stock data (Alpha Vantage)
   - MCP extensions (arithmetic, expense)

6. **Persistence**
   - SQLite checkpoint storage
   - Thread state management
   - Conversation recovery

## 📦 Dependencies

Key dependencies and their purposes:

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | Latest | Web UI framework |
| `python-dotenv` | Latest | Environment variable management |
| `requests` | Latest | HTTP requests for APIs |
| `langchain` | Latest | Core LLM framework |
| `langchain-core` | Latest | Core language chain components |
| `langchain-openai` | Latest | OpenAI integration |
| `langchain-mcp-adapters` | Latest | MCP protocol adapters |
| `langgraph` | Latest | State graph orchestration |
| `langgraph-checkpoint-sqlite` | Latest | SQLite state persistence |
| `openai` | Latest | OpenAI API client |
| `faiss-cpu` | Latest | Vector similarity search |
| `pypdf` | Latest | PDF processing |
| `duckduckgo-search` | Latest | Web search tool |
| `fastmcp` | Latest | MCP server framework |
| `aiosqlite` | Latest | Async SQLite support |

See [requirements.txt](requirements.txt) for the complete list.

## 🔌 API Reference

### Backend Exports (`backend/app.py`)

```python
from backend.app import (
    chatbot,                    # Compiled LangGraph application
    ingest_pdf,                # Ingest PDF for current thread
    retrieve_all_threads,      # Get list of all conversation threads
    submit_async_task,         # Submit async task to executor
    thread_document_metadata,  # Get metadata for thread's PDF
    thread_has_document,       # Check if thread has indexed PDF
)
```

### Core Functions

#### `ingest_pdf(file_bytes, thread_id, filename=None) -> dict`
Ingests a PDF file and creates a FAISS-based retriever for semantic search.

**Parameters**:
- `file_bytes` (bytes): Raw PDF file bytes
- `thread_id` (str): Unique conversation thread identifier
- `filename` (str, optional): Display name for the PDF

**Returns**:
```python
{
    "filename": str,      # Name of the PDF
    "documents": int,     # Number of pages
    "chunks": int,       # Number of text chunks created
}
```

#### `chatbot.invoke(input_dict, config) -> dict`
Invoke the chatbot with a message.

**Parameters**:
- `input_dict`: `{"messages": [HumanMessage]}`
- `config`: `{"configurable": {"thread_id": str}}`

**Returns**: Updated state with assistant message

#### `retrieve_all_threads() -> list[str]`
Retrieve all conversation thread IDs from the database.

**Returns**: List of thread UUIDs

#### `thread_document_metadata(thread_id) -> dict`
Get metadata about the PDF indexed for a specific thread.

**Returns**:
```python
{
    "filename": str,      # PDF filename
    "documents": int,     # Number of pages
    "chunks": int,       # Number of chunks
}
```

### Tool Functions

#### `rag_tool(query, thread_id) -> dict`
Retrieve relevant information from uploaded PDF.

**Returns**:
```python
{
    "query": str,              # Original query
    "context": [str],         # Retrieved text chunks
    "metadata": [dict],       # Chunk metadata (page numbers, etc.)
    "source_file": str,       # Original PDF filename
}
```

#### `get_stock_price(symbol) -> dict`
Fetch current stock price data.

**Parameters**:
- `symbol` (str): Stock ticker (e.g., "AAPL", "TSLA")

**Returns**: Alpha Vantage API response

### MCP Tools

#### Arithmetic Operations
- `add(a: float, b: float) -> float`
- `sub(a: float, b: float) -> float`
- `mul(a: float, b: float) -> float`
- `div(a: float, b: float) -> float` (with zero-division protection)
- `pow(a: float, b: float) -> float`
- `modulus(a: float, b: float) -> float` (with zero-division protection)

All arithmetic functions accept int, float, or numeric string values.

## 🧩 File Descriptions

### Backend Files

**[backend/app.py](backend/app.py)**
- Main application initialization
- Chatbot setup and configuration
- Tool and checkpoint initialization
- Public API exports

**[backend/graph.py](backend/graph.py)**
- LangGraph state machine definition
- Chat node implementation
- Tool invocation logic
- Graph compilation with checkpointing

**[backend/llm_setup.py](backend/llm_setup.py)**
- OpenAI LLM initialization (GPT-4o-mini)
- OpenAI embeddings setup (text-embedding-3-small)
- Model configuration

**[backend/pdf_index.py](backend/pdf_index.py)**
- PDF loading and processing
- Document chunking configuration
- FAISS vector store creation
- Thread-based retriever management
- PDF metadata tracking

**[backend/tools.py](backend/tools.py)**
- Tool definitions (search, stock, RAG)
- DuckDuckGo search tool setup
- Alpha Vantage stock price tool
- MCP client configuration
- Tool binding to LLM

**[backend/checkpoint.py](backend/checkpoint.py)**
- SQLite checkpoint initialization
- Async database setup
- Persistence layer implementation

**[backend/async_runtime.py](backend/async_runtime.py)**
- Async event loop management
- Task submission and execution
- Async helper functions

### Frontend Files

**[frontend/app.py](frontend/app.py)**
- Main Streamlit application
- UI layout and widgets
- Conversation display logic
- PDF upload handling
- Message input and output

**[frontend/conversation.py](frontend/conversation.py)**
- Conversation state loading
- Message history filtering
- Message type conversions

**[frontend/state.py](frontend/state.py)**
- Session state initialization
- Thread management
- Session persistence

**[frontend/streaming.py](frontend/streaming.py)**
- Real-time response streaming
- Tool status visualization
- Stream queue management

### MCP Server Files

**[mcp_server/main.py](mcp_server/main.py)**
- FastMCP-based arithmetic server
- Tool implementations (add, sub, mul, div, pow, modulus)
- Input type conversion and validation
- Error handling for invalid operations

## 🔒 Security Considerations

### Current Implementation

1. **API Key Hardcoding**: The Alpha Vantage API key is currently hardcoded in `tools.py`
   - **Recommendation**: Move to environment variables and rotate the key

2. **MCP Tool Failures**: Graceful degradation if MCP servers unavailable
   - No system-wide failure if tools fail to load

3. **Input Validation**: Stock symbols and numeric inputs are validated
   - Division by zero protection in arithmetic tools

### Best Practices

1. **Always use `.env` files** for sensitive credentials
2. **Never commit API keys** to version control
3. **Rotate exposed keys** immediately
4. **Use environment variables** for all configuration
5. **Validate user inputs** before passing to tools
6. **Monitor API usage** for unusual patterns

## 📈 Performance Considerations

- **FAISS Vector Store**: In-memory storage for fast similarity search
- **Async Processing**: Non-blocking I/O with async/await patterns
- **SQLite Checkpointing**: Efficient state persistence
- **Chunking Strategy**: 1000-character chunks with 200-character overlap for balanced retrieval
- **Top-K Retrieval**: Returns top 4 similar documents for context

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'backend'"**
- Ensure you're running from the project root
- Check your Python path includes the project directory

**"OPENAI_API_KEY not found"**
- Create a `.env` file in the project root
- Add your OpenAI API key to the `.env` file
- Restart the application

**PDF indexing fails**
- Ensure PDF is valid and not corrupted
- Check file size (very large PDFs may take longer)
- Verify sufficient disk space for vector store

**Stock price tool returns errors**
- Verify Alpha Vantage API key is valid
- Check API rate limits (free tier has limits)
- Ensure stock symbol is valid (e.g., "AAPL", not "Apple")

**MCP server connection errors**
- Check that MCP server processes can be spawned
- Verify Python path is correct in `tools.py`
- Look for error logs in the console

## 📝 Notes & Future Enhancements

### Current Limitations

1. RAG retrievers stored in memory (lost on restart)
   - **Suggestion**: Persist FAISS indexes to disk

2. Single PDF per thread
   - **Suggestion**: Support multiple PDFs per thread

3. No authentication or user management
   - **Suggestion**: Add user accounts and conversation sharing

4. Limited conversation pruning
   - **Suggestion**: Implement token limit management for long conversations

### Potential Enhancements

1. **Multi-document RAG**: Support querying across multiple PDFs
2. **Persistent Vector Stores**: Save FAISS indexes to disk for faster startup
3. **User Management**: Add authentication and user-specific conversations
4. **Advanced Search**: Implement hybrid search (BM25 + semantic)
5. **Custom Agents**: Allow users to define custom tool combinations
6. **Response Memory**: Summarize old conversations to save tokens
7. **Rate Limiting**: Implement usage limits and quotas
8. **API Endpoint**: Expose functionality via REST API
9. **Mobile UI**: Responsive design for mobile devices
10. **Analytics**: Track usage patterns and model performance

## 📚 Related Documentation

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastMCP Documentation](https://modelcontextprotocol.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/)