import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def create_handwritten_pdf(text_content, font_path, output_pdf_path, apply_realism=False):
    # --- 1. Document Settings (A4 Size at 150 DPI) ---
    PAGE_WIDTH = 1240
    PAGE_HEIGHT = 1754
    MARGIN_LEFT = 150
    MARGIN_RIGHT = 100
    MARGIN_TOP = 150
    MARGIN_BOTTOM = 150
    
    # Load the font (Set size to 50 for realistic handwriting size)
    try:
        font = ImageFont.truetype(font_path, 50)
    except IOError:
        raise Exception(f"Could not load font at {font_path}. Make sure the file exists!")

    # Calculate line height
    # We use a standard character like 'A' to get a consistent baseline height
    bbox = font.getbbox("A") 
    line_height = (bbox[3] - bbox[1]) + 40 # Add 40px for comfortable line spacing

    pages = []
    current_page = _create_blank_page(PAGE_WIDTH, PAGE_HEIGHT)
    draw = ImageDraw.Draw(current_page)
    
    current_y = MARGIN_TOP
    max_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

    # --- 2. Text Wrapping & Rendering ---
    # Split the input text by actual line breaks the user typed
    paragraphs = text_content.split('\n')

    for paragraph in paragraphs:
        if paragraph.strip() == "":
            current_y += line_height # Add space for empty lines
            continue
            
        # Wrap the paragraph so it doesn't go off the right edge of the page
        # 'width' is roughly character count. 55 is a safe average for font size 50.
        wrapped_lines = textwrap.wrap(paragraph, width=55)

        for line in wrapped_lines:
            # Multi-Page Logic: If we hit the bottom margin, start a new page!
            if current_y + line_height > PAGE_HEIGHT - MARGIN_BOTTOM:
                pages.append(current_page) # Save the full page
                current_page = _create_blank_page(PAGE_WIDTH, PAGE_HEIGHT) # Make a new one
                draw = ImageDraw.Draw(current_page)
                current_y = MARGIN_TOP # Reset to top

            # Draw the text onto the image
            # Fill (20, 20, 40) is a very dark blue/black ink color
            draw.text((MARGIN_LEFT, current_y), line, font=font, fill=(20, 20, 40))
            current_y += line_height
            
        # Add a little extra space after a paragraph finishes
        current_y += (line_height // 2)

    # Save the very last page we were working on
    pages.append(current_page)

    # --- 3. Export to Multi-Page PDF ---
    # Pillow handles this beautifully. We take the first page, and 'append' the rest.
    if pages:
        pages[0].save(
            output_pdf_path, 
            "PDF", 
            resolution=150.0, 
            save_all=True, 
            append_images=pages[1:]
        )
        return True
    return False

def _create_blank_page(width, height):
    # Creates a slightly off-white paper color (Hex #FDFBF7)
    return Image.new('RGB', (width, height), color=(253, 251, 247))