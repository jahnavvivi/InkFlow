print("SERVER IS ATTEMPTING TO START...")

from flask import Flask, render_template, request, send_file
import os
from document_renderer import create_handwritten_pdf 

app = Flask(__name__)

# Ensure directories exist
os.makedirs("static/pdfs", exist_ok=True)
os.makedirs("static/presets", exist_ok=True)
os.makedirs("static/user_fonts", exist_ok=True)

@app.route('/')
def index():
    presets = ["Dancing Script", "Pacifico", "Architect", "Block Caps", "Messy Doctor"]
    return render_template('index.html', presets=presets)

@app.route('/generate-document', methods=['POST'])
def generate_document():
    text_content = request.form.get('text_content')
    selected_style = request.form.get('style')
    add_realism = request.form.get('realism') == 'on'
    
    output_pdf_path = "static/pdfs/final_document.pdf"
    
    # Route to the correct font
    if selected_style == "custom":
        font_path = "static/user_fonts/custom_font.ttf"
    else:
        formatted_name = selected_style.replace(" ", "") + ".ttf"
        font_path = f"static/presets/{formatted_name}"

    # Fallback if font is missing
    if not os.path.exists(font_path):
        font_path = "static/presets/custom_font.ttf" 

    success = create_handwritten_pdf(text_content, font_path, output_pdf_path, add_realism)
    
    if success and os.path.exists(output_pdf_path):
        return send_file(output_pdf_path, as_attachment=True)
    else:
        return "Error generating document.", 500

# ==========================================
# THE MISSING PIECE: AI PERSONALIZATION
# ==========================================
@app.route('/personalize', methods=['POST'])
def personalize_style():
    # 1. Check if a file was actually uploaded
    if 'sample_image' not in request.files:
        return "No image uploaded", 400
        
    uploaded_file = request.files['sample_image']
    
    if uploaded_file.filename == '':
        return "No selected file", 400

    # 2. Save the uploaded photo to your machine
    image_path = os.path.join("static", "user_fonts", uploaded_file.filename)
    uploaded_file.save(image_path)
    
    # 3. WAKE UP THE AI ENGINE
    print("STARTING AI TRAINING...")
    from font_creation import update_font_from_images
    
    try:
        # Tell your OpenCV/PyTorch script to read the image, use the base font, and generate the .ttf
        update_font_from_images(image_path, "resources/DancingScript-Regular.ttf", "static/user_fonts/custom_font.ttf")
        print("AI TRAINING COMPLETE!")
    except Exception as e:
        print(f"AI CRASHED: {e}")
        return f"Error training AI: {e}", 500
    
    return "Custom style trained successfully! You can now hit the back button and select 'My Custom Uploaded Style' from the dropdown.", 200
# ==========================================

if __name__ == '__main__':
    print("STARTING FLASK ON PORT 5000...")
    app.run(debug=True, port=5000)