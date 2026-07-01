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
- [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) core OCR engine and PDF processing
- [pikepdf](https://github.com/pikepdf/pikepdf) reads PDF page counts
- [pypdfium2](https://github.com/pypdfium2-team/pypdfium2) handles pdf rendering

### System dependencies
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) text recognition engine

## Usage

1. Install Python dependencies: `pip install ocrmypdf pikepdf pypdfium2`
2. Install Tesseract and ensure it is on the system PATH
3. Run the app: `python pdfocr.py`
4. Select an input folder containing PDFs and an output folder for the results
5. Set your preferred thread limit and click Run OCR

