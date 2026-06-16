from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from fontTools.ttLib import TTFont

# --- 1. IMPORT THE AI BRAIN ---
from main import (
    DETECTION_MODEL,
    CLASSIFICATION_MODEL,
    segment_characters,
    classify_characters,
    update_font_from_images
)

app = FastAPI()

# Allow React to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def apply_cursive_kerning(input_font_path, output_font_path, squish_factor=0.75):
    """
    Phase 2 Logic: Opens the generated font and reduces the Advance Width 
    of every letter, forcing them to overlap and create a connected cursive flow.
    """
    print("[Phase 2] Applying cursive overlap logic...")
    font = TTFont(input_font_path)
    
    # Access the Horizontal Metrics table
    hmtx = font['hmtx']
    
    # Iterate through every letter in the font
    for glyph_name in hmtx.metrics.keys():
        # Do not squish the spacebar, otherwise words will merge together
        if glyph_name not in ['space', 'uni0020']:
            advance_width, left_side_bearing = hmtx.metrics[glyph_name]
            
            # Reduce the advance width to pull the next letter closer
            new_advance = int(advance_width * squish_factor)
            
            # Save the new tighter boundary back to the table
            hmtx.metrics[glyph_name] = [new_advance, left_side_bearing]
            
    # Save the modified font
    font.save(output_font_path)
    print("[Phase 2] Cursive font saved!")

@app.post("/api/generate-font")
async def generate_font(file: UploadFile = File(...)):
    # 1. Save the incoming image from React
    input_image_path = f"temp_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Setup Output Paths
    raw_ttf_path = "output/raw_font.ttf"
    final_ttf_path = "output/cursive_font.ttf"
    intermediate_dir = "output/intermediate"
    base_font_path = "resources/DancingScript-Regular.ttf"
    
    os.makedirs("output", exist_ok=True)
    os.makedirs(intermediate_dir, exist_ok=True)

    # 3. RUN THE FULL PIPELINE
    try:
        print("[Step 1] Segmenting...")
        char_images_list = segment_characters(input_image_path, det_model=DETECTION_MODEL)
        if not char_images_list:
            return {"error": "Segmentation failed. Could not find letters."}

        print("[Step 2] Classifying...")
        classified_chars = classify_characters(
            char_images_list,
            model=CLASSIFICATION_MODEL,
            OUTPUT_PATH=intermediate_dir
        )
        if not classified_chars:
            return {"error": "Classification failed."}

        print("[Step 3] Vectorizing and Building Font...")
        update_font_from_images(
            font_path=base_font_path,
            char_image_list=classified_chars,
            output_path=raw_ttf_path,
            desired_thickness=40,
            new_family_name="MyHandwriting",
            new_style_name="Regular"
        )
        print("Raw font successfully generated!")

        # --- PHASE 2 WIRING ---
        # Run the squish function (0.75 means letters overlap by 25%)
        apply_cursive_kerning(raw_ttf_path, final_ttf_path, squish_factor=0.90)

    except Exception as e:
        print(f"Pipeline crashed: {e}")
        return {"error": str(e)}
        
    finally:
        # 4. Clean up the uploaded image (runs whether it succeeds or crashes)
        if os.path.exists(input_image_path):
            os.remove(input_image_path)
    
    # 5. Send the FINAL cursive font back to React!
    return FileResponse(final_ttf_path, media_type="font/ttf", filename="CursiveHandwriting.ttf")