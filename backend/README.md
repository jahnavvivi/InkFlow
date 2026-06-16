# ✍️ InkFlow

**Transform handwritten characters into a custom TrueType Font (.ttf) file using deep learning, OCR, and font-generation techniques.**

InkFlow is a full-stack application that converts handwritten character samples into a usable digital font. Users upload handwriting samples through a web interface, and the backend processes the images through segmentation, classification, and font-generation pipelines to create a downloadable `.ttf` font file.

---

## 🚀 Features

* Upload handwritten character samples
* Automatic character segmentation
* Deep learning–based character classification
* OCR-assisted preprocessing
* Font glyph generation
* Export custom fonts as `.ttf` files
* Interactive web interface

---

## 🏗️ Backend Pipeline

### 1. Character Segmentation (`character_segmentation.py`)

The uploaded handwriting image is processed using computer vision techniques to isolate individual handwritten characters.

Key functions:

* Image preprocessing
* Noise removal
* Character extraction
* Bounding box generation

---

### 2. Character Classification (`character_classification.py`)

Segmented characters are classified using a trained deep learning model and OCR-assisted recognition techniques.

Key functions:

* Character recognition
* Confidence scoring
* OCR integration
* Character mapping

---

### 3. Font Generation (`font_creation.py`)

Recognized characters are converted into font glyphs and assembled into a TrueType Font (`.ttf`) using FontTools.

Key functions:

* Glyph creation
* Character-to-glyph mapping
* Font metadata generation
* TTF export

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* PyTorch
* PaddleOCR
* OpenCV
* FontTools

### Frontend

* React.js
* Vite
* JavaScript
* HTML5
* CSS3

---

## 📂 Project Structure

```text
InkFlow/
│
├── backend/
│   ├── character_classification.py
│   ├── character_segmentation.py
│   ├── font_creation.py
│   ├── document_renderer.py
│   ├── main.py
│   ├── server.py
│   ├── requirements.txt
│   ├── resources/
│   ├── templates/
│   └── examples/
│
├── frontend/
│
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/jahnavvivi/InkFlow.git
cd InkFlow
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Run the backend:

```bash
python server.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔄 Workflow

1. User uploads handwriting samples.
2. Images are processed by the backend.
3. Characters are segmented.
4. Characters are classified.
5. Glyphs are generated.
6. A custom `.ttf` font file is created.
7. User downloads the generated font.

---

## 👥 Contributors

* Jahnavi — Frontend Development (React + Vite)
* Vaibhav — Backend Development, Character Segmentation, Classification, OCR Integration, and Font Generation Pipeline

---

## 🔮 Future Improvements

* Multi-style handwriting support
* Real-time font preview
* Improved recognition accuracy
* Additional language support
* Cloud-based font storage

---

## 📄 License

This project is licensed under the MIT License.
