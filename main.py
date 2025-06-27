from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import pdfplumber
import io
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Text Extractor API",
    description="A FastAPI application that extracts text from PDF files",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextExtractionResponse(BaseModel):
    success: bool
    text: str
    pages: int
    message: str
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool
    error: str
    message: str

def extract_text_with_pypdf2(pdf_file: bytes) -> Dict[str, Any]:
    """Extract text using PyPDF2 library"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        metadata = {}
        
        # Extract metadata
        if pdf_reader.metadata:
            metadata = {
                'title': pdf_reader.metadata.get('/Title', ''),
                'author': pdf_reader.metadata.get('/Author', ''),
                'subject': pdf_reader.metadata.get('/Subject', ''),
                'creator': pdf_reader.metadata.get('/Creator', ''),
                'producer': pdf_reader.metadata.get('/Producer', ''),
                'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                'modification_date': pdf_reader.metadata.get('/ModDate', '')
            }
        
        # Extract text from each page
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
        
        return {
            'text': text.strip(),
            'pages': len(pdf_reader.pages),
            'metadata': metadata
        }
    except Exception as e:
        logger.error(f"PyPDF2 extraction error: {str(e)}")
        raise Exception(f"PyPDF2 extraction failed: {str(e)}")

def extract_text_with_pdfplumber(pdf_file: bytes) -> Dict[str, Any]:
    """Extract text using pdfplumber library (better for complex layouts)"""
    try:
        with pdfplumber.open(io.BytesIO(pdf_file)) as pdf:
            text = ""
            metadata = {}
            
            # Extract metadata
            if pdf.metadata:
                metadata = {
                    'title': pdf.metadata.get('Title', ''),
                    'author': pdf.metadata.get('Author', ''),
                    'subject': pdf.metadata.get('Subject', ''),
                    'creator': pdf.metadata.get('Creator', ''),
                    'producer': pdf.metadata.get('Producer', ''),
                    'creation_date': pdf.metadata.get('CreationDate', ''),
                    'modification_date': pdf.metadata.get('ModDate', '')
                }
            
            # Extract text from each page
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return {
                'text': text.strip(),
                'pages': len(pdf.pages),
                'metadata': metadata
            }
    except Exception as e:
        logger.error(f"pdfplumber extraction error: {str(e)}")
        raise Exception(f"pdfplumber extraction failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PDF Text Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "extract_text": "/extract-text",
            "extract_text_advanced": "/extract-text-advanced",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/extract-text", response_model=TextExtractionResponse)
async def extract_text(
    file: UploadFile = File(...),
    method: str = Form("pdfplumber", description="Extraction method: 'pypdf2' or 'pdfplumber'")
):
    """
    Extract text from a PDF file
    
    - **file**: PDF file to extract text from
    - **method**: Extraction method ('pypdf2' or 'pdfplumber')
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Choose extraction method
        if method.lower() == "pypdf2":
            result = extract_text_with_pypdf2(content)
        elif method.lower() == "pdfplumber":
            result = extract_text_with_pdfplumber(content)
        else:
            raise HTTPException(status_code=400, detail="Invalid method. Use 'pypdf2' or 'pdfplumber'")
        
        return TextExtractionResponse(
            success=True,
            text=result['text'],
            pages=result['pages'],
            message=f"Successfully extracted text from {result['pages']} pages",
            metadata=result['metadata']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")

@app.post("/extract-text-advanced", response_model=TextExtractionResponse)
async def extract_text_advanced(
    file: UploadFile = File(...),
    include_metadata: bool = Form(True, description="Include PDF metadata"),
    page_range: Optional[str] = Form(None, description="Page range (e.g., '1-3' or '1,3,5')")
):
    """
    Advanced text extraction with additional options
    
    - **file**: PDF file to extract text from
    - **include_metadata**: Whether to include PDF metadata
    - **page_range**: Specific page range to extract (e.g., '1-3' or '1,3,5')
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Parse page range
        pages_to_extract = None
        if page_range:
            try:
                pages_to_extract = []
                for part in page_range.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_extract.extend(range(start, end + 1))
                    else:
                        pages_to_extract.append(int(part))
                # Convert to 0-based indexing
                pages_to_extract = [p - 1 for p in pages_to_extract if p > 0]
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid page range format")
        
        # Use pdfplumber for advanced extraction
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = ""
            metadata = {}
            
            # Extract metadata if requested
            if include_metadata and pdf.metadata:
                metadata = {
                    'title': pdf.metadata.get('Title', ''),
                    'author': pdf.metadata.get('Author', ''),
                    'subject': pdf.metadata.get('Subject', ''),
                    'creator': pdf.metadata.get('Creator', ''),
                    'producer': pdf.metadata.get('Producer', ''),
                    'creation_date': pdf.metadata.get('CreationDate', ''),
                    'modification_date': pdf.metadata.get('ModDate', '')
                }
            
            # Extract text from specified pages
            total_pages = len(pdf.pages)
            if pages_to_extract:
                for page_num in pages_to_extract:
                    if 0 <= page_num < total_pages:
                        page = pdf.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            else:
                # Extract from all pages
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            extracted_pages = len(pages_to_extract) if pages_to_extract else total_pages
            
            return TextExtractionResponse(
                success=True,
                text=text.strip(),
                pages=extracted_pages,
                message=f"Successfully extracted text from {extracted_pages} pages",
                metadata=metadata if include_metadata else None
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Advanced extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Advanced text extraction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 