# PDF OCR App

A lightweight desktop application that adds a searchable text layer to scanned or image-based PDF files.

## What it does

This app processes unsearchable or image PDFs using OCR (Optical Character Recognition) and produces a new PDF with a hidden text layer, making the content fully searchable without changing how it looks.

## Features

- Batch process an entire folder of PDFs in one run
- Configurable thread limit to control CPU usage (important for shared environments)
- Live status display showing the current file, page count, and total pages processed
- Error handling for PDFs that already contain a text layer

## Dependencies

### Python packages
- [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) — core OCR engine and PDF processing
- [pikepdf](https://github.com/pikepdf/pikepdf) — reads PDF page counts

### System dependencies
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — text recognition engine
- [Ghostscript](https://www.ghostscript.com/) — PDF rendering and assembly

## Usage

1. Install Python dependencies: `pip install ocrmypdf pikepdf`
2. Install Tesseract and Ghostscript and ensure both are on your system PATH
3. Run the app: `python pdfocr.py`
4. Select an input folder containing PDFs and an output folder for the results
5. Set your preferred thread limit and click Run OCR

