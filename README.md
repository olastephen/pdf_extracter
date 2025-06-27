# PDF Text Extractor API

A FastAPI-based REST API that extracts text from PDF files using multiple extraction methods.

## Features

- **Multiple Extraction Methods**: Supports both PyPDF2 and pdfplumber libraries
- **File Upload**: Accepts PDF files via multipart form data
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

### 3. Health Check
**GET** `/health`

Check if the API is running.

### 4. Root Endpoint
**GET** `/`

Get API information and available endpoints.

## Response Format

### Success Response
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

# Usage
result = extract_text_basic("document.pdf")
print(result['text'])

# Extract only pages 1-3
result = extract_text_advanced("document.pdf", page_range="1-3")
print(result['text'])
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

// Usage
extractText('document.pdf')
    .then(result => console.log(result.text))
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