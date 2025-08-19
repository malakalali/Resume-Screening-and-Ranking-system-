# Resume Screening App

AI-powered resume screening application using NLP and BERT embeddings for intelligent job-resume matching.

## Project Status

### ✅ Step 1: Environment Setup
- Python virtual environment created
- All required dependencies installed
- Compatible with macOS M3 (ARM64) architecture

### ✅ Step 2: Document Parsing and Embedding System
- PDF and DOCX document parsing
- Text extraction and cleaning
- Sentence embeddings using BERT/SBERT
- Embedding caching for performance

### ✅ Step 3: Resume Matching Logic
- Cosine similarity matching
- Keyword extraction and highlighting
- Resume ranking and scoring
- Match quality analysis

### ✅ Step 4: Streamlit User Interface
- Modern, responsive web interface
- File upload for PDF/DOCX resumes
- Job description input
- Real-time match scoring and display
- Keyword highlighting and statistics
- Beautiful gradient UI with animations

## Core Components

### Document Processing
- `document_parser.py` - PDF/DOCX parsing and text extraction
- `embedding_system.py` - BERT embeddings and similarity calculations
- `resume_processor.py` - Resume processing and management

### Matching Engine
- `matching_engine.py` - Core matching logic and scoring
- `resume_matcher.py` - Unified interface for all operations

### User Interface
- `app.py` - Main Streamlit application with modern UI

## Key Technologies

- **Python 3.9+** - Core programming language
- **Streamlit** - Web application framework
- **Sentence Transformers** - BERT/SBERT embeddings
- **PyTorch** - Deep learning framework
- **scikit-learn** - Machine learning utilities
- **PyPDF2** - PDF document parsing
- **python-docx** - DOCX document parsing

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ResumeSystem
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Upload resume files (PDF/DOCX)
   - Enter job description
   - View matching results

## Features

### Resume Processing
- Support for PDF and DOCX formats
- Automatic text extraction and cleaning
- Section identification (experience, education, skills)
- Embedding generation and caching

### Matching Engine
- BERT-based semantic similarity
- Cosine similarity scoring
- Keyword extraction and highlighting
- Multi-resume ranking and comparison

### User Interface
- Modern, responsive design
- Real-time file upload and processing
- Interactive job description input
- Match score visualization
- Keyword highlighting
- Statistics and analytics

## Performance

- Fast embedding generation with caching
- Efficient similarity calculations
- Real-time processing and display
- Optimized for macOS M3 architecture

## Next Steps

The MVP is now complete with all core functionality working:
- ✅ Document parsing and embedding
- ✅ Resume matching and scoring
- ✅ Modern web interface
- ✅ Real-time processing and display

The application is ready for production use and can be extended with additional features like:
- Database integration for persistent storage
- Advanced analytics and reporting
- Multi-user support
- API endpoints for integration 