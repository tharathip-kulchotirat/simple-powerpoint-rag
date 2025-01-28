from pdf2image import convert_from_path
import os
import io

def get_slide(name: str, slide_number: int):
    try:
        pdf_path = f"src/assets/slides/{name.replace(".pptx", ".pdf")}"
        
        # Check if the file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        
        # Convert the PDF into images (one image per page)
        images = convert_from_path(pdf_path, dpi=150)
        total_pages = len(images)

        # Check if the requested slide number is valid
        if slide_number < 1 or slide_number > total_pages:
            raise ValueError(f"Slide number must be between 1 and {total_pages}.")

        # Get the specific slide image (1-indexed)
        slide_image = images[slide_number - 1]

        img_byte_arr = io.BytesIO()
        slide_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Return the byte data of the image
        return img_byte_arr
    
    except Exception as e:
        raise RuntimeError(f"Error extracting slide: {str(e)}")