# PDF Text Extractor API

A FastAPI-based REST API that extracts text from PDF files using multiple extraction methods.

## Features

- **Multiple Extraction Methods**: Supports both PyPDF2 and pdfplumber libraries
- **File Upload**: Accepts PDF files via multipart form data
- **Batch Processing**: Extract text from multiple PDF files in a single request
- **Metadata Extraction**: Extracts PDF metadata (title, author, creation date, etc.)
- **Page Range Support**: Extract text from specific page ranges
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin resource sharing enabled
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-text-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## API Endpoints

### 1. Basic Text Extraction
**POST** `/extract-text`

Extract text from a PDF file using the specified method.

**Parameters:**
- `file` (file): PDF file to upload
- `method` (string, optional): Extraction method - "pypdf2" or "pdfplumber" (default: "pdfplumber")

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/extract-text" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf" \
     -F "method=pdfplumber"
```

### 2. Advanced Text Extraction
**POST** `/extract-text-advanced`

Advanced text extraction with additional options.

**Parameters:**
- `file` (file): PDF file to upload
- `include_metadata` (boolean, optional): Include PDF metadata (default: true)
- `page_range` (string, optional): Specific page range (e.g., "1-3" or "1,3,5")

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/extract-text-advanced" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf" \
     -F "include_metadata=true" \
     -F "page_range=1-3"
```

### 3. Batch Text Extraction
**POST** `/extract-text-batch`

Extract text from multiple PDF files in batch.

**Parameters:**
- `files` (files): Multiple PDF files to upload
- `method` (string, optional): Extraction method - "pypdf2" or "pdfplumber" (default: "pdfplumber")
- `max_files` (integer, optional): Maximum number of files to process (default: 10)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/extract-text-batch" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@document1.pdf" \
     -F "files=@document2.pdf" \
     -F "files=@document3.pdf" \
     -F "method=pdfplumber" \
     -F "max_files=10"
```

### 4. Advanced Batch Text Extraction
**POST** `/extract-text-batch-advanced`

Advanced batch text extraction with additional options.

**Parameters:**
- `files` (files): Multiple PDF files to upload
- `include_metadata` (boolean, optional): Include PDF metadata (default: true)
- `page_range` (string, optional): Specific page range (e.g., "1-3" or "1,3,5")
- `max_files` (integer, optional): Maximum number of files to process (default: 10)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/extract-text-batch-advanced" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@document1.pdf" \
     -F "files=@document2.pdf" \
     -F "include_metadata=true" \
     -F "page_range=1-3" \
     -F "max_files=10"
```

### 5. Health Check
**GET** `/health`

Check if the API is running.

### 6. Root Endpoint
**GET** `/`

Get API information and available endpoints.

## Response Format

### Single File Success Response
```json
{
  "success": true,
  "text": "Extracted text content...",
  "pages": 5,
  "message": "Successfully extracted text from 5 pages",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "subject": "Document Subject",
    "creator": "Creator Software",
    "producer": "Producer Software",
    "creation_date": "2023-01-01T00:00:00Z",
    "modification_date": "2023-01-01T00:00:00Z"
  }
}
```

### Batch Success Response
```json
{
  "success": true,
  "total_files": 3,
  "successful_extractions": 2,
  "failed_extractions": 1,
  "summary": "Processed 3 files: 2 successful, 1 failed",
  "results": [
    {
      "filename": "document1.pdf",
      "success": true,
      "text": "Extracted text from document1...",
      "pages": 5,
      "message": "Successfully extracted text from 5 pages",
      "metadata": {
        "title": "Document 1",
        "author": "Author 1"
      }
    },
    {
      "filename": "document2.pdf",
      "success": true,
      "text": "Extracted text from document2...",
      "pages": 3,
      "message": "Successfully extracted text from 3 pages",
      "metadata": {
        "title": "Document 2",
        "author": "Author 2"
      }
    },
    {
      "filename": "invalid.txt",
      "success": false,
      "text": "",
      "pages": 0,
      "message": "File must be a PDF",
      "error": "Invalid file type"
    }
  ]
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

## Python Client Example

```python
import requests

# Basic extraction
def extract_text_basic(file_path, method="pdfplumber"):
    url = "http://localhost:8000/extract-text"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'method': method}
        response = requests.post(url, files=files, data=data)
    
    return response.json()

# Advanced extraction
def extract_text_advanced(file_path, include_metadata=True, page_range=None):
    url = "http://localhost:8000/extract-text-advanced"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'include_metadata': include_metadata,
            'page_range': page_range
        }
        response = requests.post(url, files=files, data=data)
    
    return response.json()

# Batch extraction
def extract_text_batch(file_paths, method="pdfplumber", max_files=10):
    url = "http://localhost:8000/extract-text-batch"
    
    files = []
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            files.append(('files', f))
    
    data = {
        'method': method,
        'max_files': max_files
    }
    response = requests.post(url, files=files, data=data)
    
    return response.json()

# Advanced batch extraction
def extract_text_batch_advanced(file_paths, include_metadata=True, page_range=None, max_files=10):
    url = "http://localhost:8000/extract-text-batch-advanced"
    
    files = []
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            files.append(('files', f))
    
    data = {
        'include_metadata': include_metadata,
        'max_files': max_files
    }
    if page_range:
        data['page_range'] = page_range
    
    response = requests.post(url, files=files, data=data)
    
    return response.json()

# Usage examples
# Single file
result = extract_text_basic("document.pdf")
print(result['text'])

# Extract only pages 1-3
result = extract_text_advanced("document.pdf", page_range="1-3")
print(result['text'])

# Batch extraction
file_list = ["document1.pdf", "document2.pdf", "document3.pdf"]
batch_result = extract_text_batch(file_list)
print(f"Processed {batch_result['total_files']} files")
for file_result in batch_result['results']:
    print(f"{file_result['filename']}: {file_result['success']}")

# Advanced batch extraction
batch_result = extract_text_batch_advanced(file_list, page_range="1-2")
print(f"Summary: {batch_result['summary']}")
```

## JavaScript/Node.js Client Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function extractText(filePath, method = 'pdfplumber') {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('method', method);
    
    try {
        const response = await axios.post('http://localhost:8000/extract-text', form, {
            headers: form.getHeaders()
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
        throw error;
    }
}

async function extractTextBatch(filePaths, method = 'pdfplumber', maxFiles = 10) {
    const form = new FormData();
    
    for (const filePath of filePaths) {
        form.append('files', fs.createReadStream(filePath));
    }
    form.append('method', method);
    form.append('max_files', maxFiles);
    
    try {
        const response = await axios.post('http://localhost:8000/extract-text-batch', form, {
            headers: form.getHeaders()
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
        throw error;
    }
}

// Usage
extractText('document.pdf')
    .then(result => console.log(result.text))
    .catch(error => console.error(error));

// Batch usage
const files = ['document1.pdf', 'document2.pdf', 'document3.pdf'];
extractTextBatch(files)
    .then(result => {
        console.log(`Processed ${result.total_files} files`);
        result.results.forEach(fileResult => {
            console.log(`${fileResult.filename}: ${fileResult.success ? 'SUCCESS' : 'FAILED'}`);
        });
    })
    .catch(error => console.error(error));
```

## Extraction Methods

### PyPDF2
- **Pros**: Fast, lightweight, good for simple text extraction
- **Cons**: May struggle with complex layouts, tables, and images
- **Best for**: Simple text documents, basic PDFs

### pdfplumber
- **Pros**: Better handling of complex layouts, tables, and positioning
- **Cons**: Slightly slower, larger memory footprint
- **Best for**: Complex documents, tables, forms, and precise text positioning

## Error Handling

The API handles various error scenarios:
- Invalid file types (non-PDF files)
- Empty or corrupted files
- Invalid page ranges
- Extraction failures
- Server errors

## Development

### Project Structure
```
pdf-text-extractor/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features
1. Add new endpoints in `main.py`
2. Update requirements.txt if new dependencies are needed
3. Test with various PDF types
4. Update documentation

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request 