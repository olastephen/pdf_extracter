#!/usr/bin/env python3
"""
Test client for the PDF Text Extractor API - Batch Extraction
This script demonstrates how to use the batch extraction endpoints.
"""

import requests
import json
import sys
import os
from pathlib import Path
from typing import List

# API base URL
BASE_URL = "http://localhost:8000"

def test_batch_extraction_basic(file_paths: List[str], method="pdfplumber", max_files=10):
    """Test basic batch text extraction"""
    print(f"\nTesting basic batch text extraction")
    print(f"Files: {len(file_paths)} files")
    print(f"Method: {method}")
    print(f"Max files: {max_files}")
    
    # Validate files exist
    valid_files = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            valid_files.append(file_path)
        else:
            print(f"Warning: File {file_path} not found, skipping...")
    
    if not valid_files:
        print("Error: No valid files found.")
        return None
    
    try:
        files = []
        for file_path in valid_files:
            with open(file_path, 'rb') as f:
                files.append(('files', (os.path.basename(file_path), f.read(), 'application/pdf')))
        
        data = {
            'method': method,
            'max_files': max_files
        }
        
        response = requests.post(f"{BASE_URL}/extract-text-batch", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Summary: {result['summary']}")
            print(f"Total files: {result['total_files']}")
            print(f"Successful: {result['successful_extractions']}")
            print(f"Failed: {result['failed_extractions']}")
            
            # Display results for each file
            for i, file_result in enumerate(result['results']):
                print(f"\n--- File {i+1}: {file_result['filename']} ---")
                print(f"Success: {file_result['success']}")
                print(f"Pages: {file_result['pages']}")
                print(f"Message: {file_result['message']}")
                print(f"Text length: {len(file_result['text'])} characters")
                
                if file_result['success']:
                    print(f"First 200 characters: {file_result['text'][:200]}...")
                    
                    if file_result.get('metadata'):
                        print(f"Metadata: {json.dumps(file_result['metadata'], indent=2)}")
                else:
                    print(f"Error: {file_result.get('error', 'Unknown error')}")
            
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

def test_batch_extraction_advanced(file_paths: List[str], include_metadata=True, page_range=None, max_files=10):
    """Test advanced batch text extraction"""
    print(f"\nTesting advanced batch text extraction")
    print(f"Files: {len(file_paths)} files")
    print(f"Include metadata: {include_metadata}")
    print(f"Page range: {page_range}")
    print(f"Max files: {max_files}")
    
    # Validate files exist
    valid_files = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            valid_files.append(file_path)
        else:
            print(f"Warning: File {file_path} not found, skipping...")
    
    if not valid_files:
        print("Error: No valid files found.")
        return None
    
    try:
        files = []
        for file_path in valid_files:
            with open(file_path, 'rb') as f:
                files.append(('files', (os.path.basename(file_path), f.read(), 'application/pdf')))
        
        data = {
            'include_metadata': include_metadata,
            'max_files': max_files
        }
        
        if page_range:
            data['page_range'] = page_range
        
        response = requests.post(f"{BASE_URL}/extract-text-batch-advanced", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Summary: {result['summary']}")
            print(f"Total files: {result['total_files']}")
            print(f"Successful: {result['successful_extractions']}")
            print(f"Failed: {result['failed_extractions']}")
            
            # Display results for each file
            for i, file_result in enumerate(result['results']):
                print(f"\n--- File {i+1}: {file_result['filename']} ---")
                print(f"Success: {file_result['success']}")
                print(f"Pages: {file_result['pages']}")
                print(f"Message: {file_result['message']}")
                print(f"Text length: {len(file_result['text'])} characters")
                
                if file_result['success']:
                    print(f"First 200 characters: {file_result['text'][:200]}...")
                    
                    if file_result.get('metadata'):
                        print(f"Metadata: {json.dumps(file_result['metadata'], indent=2)}")
                else:
                    print(f"Error: {file_result.get('error', 'Unknown error')}")
            
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
    """Test various error cases for batch extraction"""
    print("\nTesting batch extraction error cases...")
    
    # Test with no files
    print("\n1. Testing with no files...")
    try:
        response = requests.post(f"{BASE_URL}/extract-text-batch", files=[], data={'method': 'pdfplumber'})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test with too many files
    print("\n2. Testing with too many files...")
    try:
        # Create dummy files
        files = []
        for i in range(15):  # More than default max of 10
            dummy_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
            files.append(('files', (f'dummy{i}.pdf', dummy_content, 'application/pdf')))
        
        data = {'method': 'pdfplumber', 'max_files': 10}
        response = requests.post(f"{BASE_URL}/extract-text-batch", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test with mixed file types
    print("\n3. Testing with mixed file types...")
    try:
        files = []
        # Add a PDF file
        dummy_pdf = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        files.append(('files', ('dummy.pdf', dummy_pdf, 'application/pdf')))
        # Add a non-PDF file
        dummy_txt = b"This is a text file, not a PDF"
        files.append(('files', ('dummy.txt', dummy_txt, 'text/plain')))
        
        data = {'method': 'pdfplumber'}
        response = requests.post(f"{BASE_URL}/extract-text-batch", files=files, data=data)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Summary: {result['summary']}")
            for file_result in result['results']:
                print(f"File: {file_result['filename']}, Success: {file_result['success']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main test function"""
    print("PDF Text Extractor API - Batch Extraction Test Client")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("API is not running. Please start the server first:")
            print("python main.py")
            return
    except:
        print("Cannot connect to API. Please start the server first:")
        print("python main.py")
        return
    
    # Check if PDF files were provided as command line arguments
    if len(sys.argv) > 1:
        pdf_files = sys.argv[1:]
        print(f"Using provided PDF files: {pdf_files}")
        
        # Test basic batch extraction
        test_batch_extraction_basic(pdf_files, method="pdfplumber")
        test_batch_extraction_basic(pdf_files, method="pypdf2")
        
        # Test advanced batch extraction
        test_batch_extraction_advanced(pdf_files, include_metadata=True)
        test_batch_extraction_advanced(pdf_files, page_range="1-2")
        
    else:
        print("No PDF files provided. Testing error cases only.")
        print("Usage: python test_batch_client.py <path_to_pdf1> <path_to_pdf2> ...")
    
    # Test error cases
    test_error_cases()
    
    print("\nBatch extraction test completed!")

if __name__ == "__main__":
    main() 