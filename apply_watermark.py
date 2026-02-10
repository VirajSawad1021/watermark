import os
from PIL import Image, ImageFont, ImageDraw
import glob
from typing import Optional
from dataclasses import dataclass

@dataclass
class WatermarkConfig:
    """Configuration for watermarking operations"""
    
    # Image watermark settings
    image_watermark_path: Optional[str] = "watermark.png"
    image_scale_factor: float = 0.18
    image_padding: int = 300
    
    # Text watermark settings
    font_name: str = "Times New Roman"
    font_size: int = 40
    text_color: tuple = (255, 255, 255)  # White
    text_outline_color: tuple = (0, 0, 0)  # Black
    text_outline_width: int = 2
    text_padding: int = 20
    text_position: str = "bottom-left"

def find_text_file(image_path: str) -> Optional[str]:
    """
    Find corresponding .txt file for an image
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Path to .txt file if exists, None otherwise
    """
    # Get the base name without extension
    base_path = os.path.splitext(image_path)[0]
    text_file_path = base_path + '.txt'
    
    # Check if the text file exists
    if os.path.exists(text_file_path):
        return text_file_path
    
    return None

def read_watermark_text(text_file_path: str) -> Optional[str]:
    """
    Read watermark text from file
    
    Args:
        text_file_path: Path to the .txt file
        
    Returns:
        Text content or None if read fails
    """
    try:
        # Try UTF-8 encoding first
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            return text if text else None
    except UnicodeDecodeError:
        # Fallback to system default encoding
        try:
            with open(text_file_path, 'r') as f:
                text = f.read().strip()
                return text if text else None
        except Exception as e:
            print(f"Error reading text file {text_file_path}: {str(e)}")
            return None
    except Exception as e:
        print(f"Error reading text file {text_file_path}: {str(e)}")
        return None

# Font cache to avoid repeated loading
_font_cache = {}

def load_font(font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
    """
    Load font with fallback support
    
    Args:
        font_name: Name of the font (e.g., "Times New Roman", "Inter")
        font_size: Size of the font in points
        
    Returns:
        ImageFont object (requested font or fallback)
    """
    # Check cache first
    cache_key = f"{font_name}_{font_size}"
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    font = None
    
    # Try to load Times New Roman font (primary)
    if font_name.lower() in ["times new roman", "times"]:
        times_paths = [
            # Windows
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/Times.ttf",
            "C:/Windows/Fonts/timesnewroman.ttf",
            "C:/Windows/Fonts/TimesNewRoman.ttf",
            # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/times/Times-Roman.ttf",
            # macOS
            "/Library/Fonts/Times New Roman.ttf",
            "/System/Library/Fonts/Times.ttc",
        ]
        
        for font_path in times_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"Loaded Times New Roman font from: {font_path}")
                    break
                except Exception as e:
                    continue
    
    # Try to load Inter font
    elif font_name.lower() == "inter":
        inter_paths = [
            # Windows
            "C:/Windows/Fonts/Inter-Regular.ttf",
            "C:/Windows/Fonts/inter.ttf",
            # Linux
            "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
            "/usr/share/fonts/Inter-Regular.ttf",
            # macOS
            "/Library/Fonts/Inter-Regular.ttf",
            "/System/Library/Fonts/Inter-Regular.ttf",
            # Local bundled font
            "fonts/Inter-Regular.ttf",
            "./Inter-Regular.ttf",
        ]
        
        for font_path in inter_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"Loaded Inter font from: {font_path}")
                    break
                except Exception as e:
                    continue
    
    # If requested font not found, try system default fonts
    if font is None:
        print(f"Warning: {font_name} font not found, trying fallback fonts...")
        fallback_fonts = [
            "times.ttf",  # Times New Roman (Windows)
            "Times.ttf",
            "arial.ttf",
            "Arial.ttf",
            "DejaVuSans.ttf",
            "LiberationSans-Regular.ttf",
        ]
        
        for fallback in fallback_fonts:
            try:
                font = ImageFont.truetype(fallback, font_size)
                print(f"Using fallback font: {fallback}")
                break
            except Exception:
                continue
    
    # Last resort: use PIL default font
    if font is None:
        print(f"Warning: Could not load {font_name} or fallback fonts, using PIL default font")
        font = ImageFont.load_default()
    
    # Cache the font
    _font_cache[cache_key] = font
    return font

def apply_text_watermark(
    image: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    position: str = "bottom-left",
    padding: int = 20,
    color: tuple = (255, 255, 255),
    outline_color: tuple = (0, 0, 0),
    outline_width: int = 2
) -> Image.Image:
    """
    Apply text watermark to an image
    
    Args:
        image: PIL Image object
        text: Text to render
        font: Font to use
        position: Position identifier ("bottom-left", "bottom-right", etc.)
        padding: Padding from edges in pixels
        color: RGB tuple for text color
        outline_color: RGB tuple for text outline
        outline_width: Width of text outline in pixels
        
    Returns:
        Image with text watermark applied
    """
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Calculate text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position based on position parameter
    if position == "bottom-left":
        x = padding
        y = image.height - text_height - padding
    elif position == "bottom-right":
        x = image.width - text_width - padding
        y = image.height - text_height - padding
    elif position == "top-left":
        x = padding
        y = padding
    elif position == "top-right":
        x = image.width - text_width - padding
        y = padding
    else:  # default to bottom-left
        x = padding
        y = image.height - text_height - padding
    
    # Draw text with outline for visibility
    # Draw outline
    for offset_x in range(-outline_width, outline_width + 1):
        for offset_y in range(-outline_width, outline_width + 1):
            if offset_x != 0 or offset_y != 0:
                draw.text(
                    (x + offset_x, y + offset_y),
                    text,
                    font=font,
                    fill=outline_color
                )
    
    # Draw main text
    draw.text((x, y), text, font=font, fill=color)
    
    return image

def apply_watermark(
    image_path, 
    watermark_path, 
    output_path, 
    scale_factor=0.15, 
    padding=10,
    text_watermark: Optional[str] = None,
    font_size: int = 40,
    text_color: tuple = (255, 255, 255),
    text_padding: int = 20,
    text_outline_color: tuple = (0, 0, 0),
    text_outline_width: int = 2
):
    """
    Apply image and/or text watermark to an image and save it
    
    Args:
        image_path: Path to the source image
        watermark_path: Path to the watermark image (must be PNG with transparency)
        output_path: Path where the watermarked image will be saved
        scale_factor: Size of watermark relative to the main image (default: 0.15)
        padding: Padding from the bottom-right corner in pixels (default: 10)
        text_watermark: Optional text to render as watermark
        font_size: Size of text watermark font
        text_color: RGB color for text
        text_padding: Padding for text from edges
        text_outline_color: RGB color for text outline
        text_outline_width: Width of text outline in pixels
    """
    # Open the main image
    with Image.open(image_path) as base_image:
        # Convert image to RGBA for processing
        if base_image.mode != 'RGBA':
            base_image = base_image.convert('RGBA')
        
        output_image = base_image.copy()
        
        # Apply image watermark if path provided and file exists
        if watermark_path and os.path.exists(watermark_path):
            # Open and resize watermark
            with Image.open(watermark_path) as watermark:
                # Calculate new size for watermark based on the main image size
                watermark_width = int(base_image.width * scale_factor)
                watermark_height = int(watermark_width * watermark.height / watermark.width)
                
                # Resize watermark maintaining aspect ratio
                watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
                
                # Calculate position (bottom-right with padding)
                position = (
                    base_image.width - watermark_width - padding,
                    base_image.height - watermark_height - padding
                )
                
                # Create a new transparent layer for the watermark
                transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                transparent.paste(watermark, position, watermark)
                
                # Combine the images
                output_image = Image.alpha_composite(output_image, transparent)
        
        # Apply text watermark if provided
        if text_watermark:
            try:
                # Load font
                font = load_font("Times New Roman", font_size)
                
                # Apply text watermark
                output_image = apply_text_watermark(
                    image=output_image,
                    text=text_watermark,
                    font=font,
                    position="bottom-left",
                    padding=text_padding,
                    color=text_color,
                    outline_color=text_outline_color,
                    outline_width=text_outline_width
                )
            except Exception as e:
                print(f"Error applying text watermark: {str(e)}")
        
        # Convert back to RGB if saving as JPEG
        output_extension = os.path.splitext(output_path)[1].lower()
        if output_extension in ['.jpg', '.jpeg']:
            # Create white background and paste RGBA image on top
            final_image = Image.new('RGB', output_image.size, (255, 255, 255))
            final_image.paste(output_image, mask=output_image.split()[3])  # Use alpha channel as mask
        else:
            final_image = output_image
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the image
        final_image.save(output_path, quality=95)

def process_images(
    input_folder, 
    output_folder, 
    watermark_path, 
    scale_factor=0.15, 
    padding=10,
    font_size=40,
    text_color=(255, 255, 255),
    text_padding=20
):
    """
    Process all images in input folder and its subfolders
    
    Args:
        input_folder: Root folder containing images to process
        output_folder: Root folder where processed images will be saved
        watermark_path: Path to the watermark image
        scale_factor: Size of watermark relative to the main image
        padding: Padding from the bottom-right corner in pixels
        font_size: Size of text watermark font
        text_color: RGB color for text watermark
        text_padding: Padding for text from edges
    """
    # Supported image formats (case-insensitive)
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', 
                       '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.TIFF']
    
    # Get all image files recursively
    processed_files = set()  # To avoid processing duplicates due to case variations
    
    for extension in image_extensions:
        pattern = os.path.join(input_folder, '**', extension)
        for image_path in glob.glob(pattern, recursive=True):
            # Skip if we've already processed this file (case-insensitive check)
            if image_path.lower() in processed_files:
                continue
                
            processed_files.add(image_path.lower())
            
            # Calculate relative path to maintain folder structure
            rel_path = os.path.relpath(image_path, input_folder)
            output_path = os.path.join(output_folder, rel_path)
            
            # Check for corresponding text file
            text_file_path = find_text_file(image_path)
            text_watermark = None
            if text_file_path:
                text_watermark = read_watermark_text(text_file_path)
                if text_watermark:
                    print(f"Found text watermark for {rel_path}: {text_watermark}")
            
            try:
                apply_watermark(
                    image_path=image_path,
                    watermark_path=watermark_path,
                    output_path=output_path,
                    scale_factor=scale_factor,
                    padding=padding,
                    text_watermark=text_watermark,
                    font_size=font_size,
                    text_color=text_color,
                    text_padding=text_padding
                )
                print(f"Processed: {rel_path}")
            except Exception as e:
                print(f"Error processing {rel_path}: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"
    watermark_path = "watermark.png"  # Your watermark image (must be PNG with transparency)
    scale_factor = 0.18  # Watermark size relative to main image
    padding = 300  # Pixels from bottom-right corner
    
    # Text watermark settings
    font_size = 40  # Font size for text watermark
    text_color = (255, 255, 255)  # White text
    text_padding = 20  # Padding from edges for text
    
    process_images(
        input_folder=input_folder,
        output_folder=output_folder,
        watermark_path=watermark_path,
        scale_factor=scale_factor,
        padding=padding,
        font_size=font_size,
        text_color=text_color,
        text_padding=text_padding
    )