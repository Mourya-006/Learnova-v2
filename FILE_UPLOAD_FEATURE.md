# 📎 File Upload Feature

## Overview
Learnova now supports file and image uploads! You can upload files and ask Gemini AI questions about them.

## Supported File Types
- **Images**: PNG, JPG, JPEG, GIF
- **Documents**: TXT, PDF, DOC, DOCX (TXT and PDF fully supported)

## How to Use

### 1. Upload a File
- Click the **paperclip icon** (📎) next to the chat input
- Select an image or document from your computer
- The file name will appear below the chat messages

### 2. Ask Questions
- Type your question in the chat input
- Press send to ask Gemini about the uploaded file
- Examples:
  - "What's in this image?"
  - "Explain this diagram"
  - "Summarize this document"
  - "What does this formula mean?"

### 3. Remove File
- Click the **X button** next to the file name to remove it
- Upload a new file anytime

## Features
✅ **Image Analysis**: Upload photos, diagrams, screenshots, formulas
✅ **Document Reading**: Upload study notes, PDFs, text files
✅ **Smart Context**: Gemini understands both your question and the file content
✅ **Auto Cleanup**: Files are automatically deleted after processing (privacy!)

## Requirements
- **Gemini API Key** must be configured
- **File size limit**: 10MB maximum
- **Pillow** and **PyPDF2** libraries installed (included in requirements.txt)

## Example Use Cases
📷 Upload a whiteboard photo → "Explain these formulas"
📊 Upload a graph → "What patterns do you see?"
📄 Upload study notes → "Create a quiz from this"
📐 Upload a math problem → "Walk me through the solution"
📚 Upload a textbook page → "Summarize this chapter"

## Technical Details
- Files are temporarily stored in the `uploads/` folder
- Automatically deleted after AI processes them
- Secure filename handling with `werkzeug.secure_filename`
- Image processing with Pillow (PIL)
- PDF text extraction with PyPDF2

Enjoy your enhanced AI study buddy! 🚀📚
