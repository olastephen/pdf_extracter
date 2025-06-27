#!/usr/bin/env python3
"""
Test client for the PDF Text Extractor API
This script demonstrates how to use the API programmatically.
"""

import requests
import json
import sys
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running.")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        return False

def extract_text_basic(file_path, method="pdfplumber"):
    """Test basic text extraction"""
    print(f"\nTesting basic text extraction with method: {method}")
    print(f"File: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'method': method}
            response = requests.post(f"{BASE_URL}/extract-text", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Pages: {result['pages']}")
            print(f"Message: {result['message']}")
            print(f"Text length: {len(result['text'])} characters")
            print(f"First 500 characters: {result['text'][:500]}...")
            
            if result.get('metadata'):
                print(f"Metadata: {json.dumps(result['metadata'], indent=2)}")
            
            return result
        else:
            print(f"Error: {response.json()}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def extract_text_advanced(file_path, include_metadata=True, page_range=None):
    """Test advanced text extraction"""
    print(f"\nTesting advanced text extraction")
    print(f"File: {file_path}")
    print(f"Include metadata: {include_metadata}")
    print(f"Page range: {page_range}")
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'include_metadata': include_metadata,
                'page_range': page_range
            }
            response = requests.post(f"{BASE_URL}/extract-text-advanced", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Pages: {result['pages']}")
            print(f"Message: {result['message']}")
            print(f"Text length: {len(result['text'])} characters")
            print(f"First 500 characters: {result['text'][:500]}...")
            
            if result.get('metadata'):
                print(f"Metadata: {json.dumps(result['metadata'], indent=2)}")
            
            return result
        else:
            print(f"Error: {response.json()}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def test_error_cases():
    """Test various error cases"""
    print("\nTesting error cases...")
    
    # Test with non-PDF file
    print("\n1. Testing with non-PDF file...")
    try:
        with open(__file__, 'rb') as f:  # This script itself
            files = {'file': f}
            data = {'method': 'pdfplumber'}
            response = requests.post(f"{BASE_URL}/extract-text", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test with invalid method
    print("\n2. Testing with invalid method...")
    try:
        # Create a dummy PDF-like file
        dummy_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        
        files = {'file': ('dummy.pdf', dummy_content, 'application/pdf')}
        data = {'method': 'invalid_method'}
        response = requests.post(f"{BASE_URL}/extract-text", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main test function"""
    print("PDF Text Extractor API - Test Client")
    print("=" * 50)
    
    # Check if server is running
    if not test_health_check():
        print("\nPlease start the server first:")
        print("python main.py")
        return
    
    # Test root endpoint
    test_root_endpoint()
    
    # Check if a PDF file was provided as command line argument
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        print(f"\nUsing provided PDF file: {pdf_file}")
        
        # Test basic extraction with both methods
        extract_text_basic(pdf_file, "pdfplumber")
        extract_text_basic(pdf_file, "pypdf2")
        
        # Test advanced extraction
        extract_text_advanced(pdf_file, include_metadata=True)
        extract_text_advanced(pdf_file, page_range="1-2")
        
    else:
        print("\nNo PDF file provided. Testing error cases only.")
        print("Usage: python test_client.py <path_to_pdf_file>")
    
    # Test error cases
    test_error_cases()
    
    print("\nTest completed!")

if __name__ == "__main__":
    main() 