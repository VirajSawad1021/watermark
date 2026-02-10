"""
Streamlit Web Interface for Image Watermarking
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
from apply_watermark import load_font, apply_text_watermark

# Page configuration
st.set_page_config(
    page_title="Image Watermarker",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Image Watermarker")
st.markdown("Upload images and add custom text and logo watermarks with adjustable settings")

# Sidebar for settings
st.sidebar.header("⚙️ Watermark Settings")

# File uploaders
uploaded_image = st.sidebar.file_uploader(
    "Upload Image",
    type=['jpg', 'jpeg', 'png', 'bmp'],
    help="Upload the image you want to watermark"
)

uploaded_logo = st.sidebar.file_uploader(
    "Upload Logo (Optional)",
    type=['png'],
    help="Upload a PNG logo with transparency"
)

# Text watermark settings
st.sidebar.subheader("📝 Text Watermark")
text_watermark = st.sidebar.text_input(
    "Watermark Text",
    value="Sample Watermark",
    help="Enter the text you want to display"
)

# Main content area
if uploaded_image:
    # Load the image
    image = Image.open(uploaded_image)
    img_width, img_height = image.size
    
    # Display image info
    st.sidebar.info(f"📐 Image Size: {img_width} x {img_height} px")
    
    # Calculate recommended font size based on image dimensions
    recommended_font_size = int(min(img_width, img_height) * 0.05)
    
    # Font size slider with recommended value
    font_size = st.sidebar.slider(
        "Font Size",
        min_value=10,
        max_value=200,
        value=min(recommended_font_size, 100),
        help=f"Recommended: {recommended_font_size}px for this image"
    )
    
    # Text color picker
    text_color = st.sidebar.color_picker(
        "Text Color",
        value="#FFFFFF",
        help="Choose the text color"
    )
    
    # Convert hex to RGB
    text_color_rgb = tuple(int(text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # Outline settings
    outline_color = st.sidebar.color_picker(
        "Outline Color",
        value="#000000",
        help="Choose the outline color for better visibility"
    )
    outline_color_rgb = tuple(int(outline_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    outline_width = st.sidebar.slider(
        "Outline Width",
        min_value=0,
        max_value=10,
        value=2,
        help="Width of the text outline"
    )
    
    # Text position
    text_position = st.sidebar.selectbox(
        "Text Position",
        options=["bottom-left", "bottom-right", "top-left", "top-right"],
        index=0
    )
    
    # Calculate recommended padding based on image size
    recommended_padding = int(min(img_width, img_height) * 0.02)
    
    text_padding = st.sidebar.slider(
        "Text Padding",
        min_value=5,
        max_value=200,
        value=min(recommended_padding, 50),
        help=f"Recommended: {recommended_padding}px for this image"
    )
    
    # Logo watermark settings
    st.sidebar.subheader("🏷️ Logo Watermark")
    
    if uploaded_logo:
        logo_scale = st.sidebar.slider(
            "Logo Size (% of image width)",
            min_value=5,
            max_value=50,
            value=15,
            help="Logo size relative to image width"
        ) / 100
        
        logo_position = st.sidebar.selectbox(
            "Logo Position",
            options=["bottom-right", "bottom-left", "top-right", "top-left"],
            index=0
        )
        
        logo_padding = st.sidebar.slider(
            "Logo Padding",
            min_value=5,
            max_value=200,
            value=min(recommended_padding, 50),
            help=f"Recommended: {recommended_padding}px for this image"
        )
    
    # Create two columns for before/after
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)
    
    with col2:
        st.subheader("Watermarked Preview")
        
        # Create watermarked image
        watermarked_image = image.copy()
        
        # Convert to RGBA if needed
        if watermarked_image.mode != 'RGBA':
            watermarked_image = watermarked_image.convert('RGBA')
        
        # Apply logo watermark if uploaded
        if uploaded_logo:
            try:
                logo = Image.open(uploaded_logo)
                
                # Calculate logo size
                logo_width = int(img_width * logo_scale)
                logo_height = int(logo_width * logo.height / logo.width)
                logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                
                # Calculate logo position
                if logo_position == "bottom-right":
                    logo_pos = (img_width - logo_width - logo_padding, 
                               img_height - logo_height - logo_padding)
                elif logo_position == "bottom-left":
                    logo_pos = (logo_padding, img_height - logo_height - logo_padding)
                elif logo_position == "top-right":
                    logo_pos = (img_width - logo_width - logo_padding, logo_padding)
                else:  # top-left
                    logo_pos = (logo_padding, logo_padding)
                
                # Create transparent layer and paste logo
                transparent = Image.new('RGBA', watermarked_image.size, (0, 0, 0, 0))
                transparent.paste(logo, logo_pos, logo)
                watermarked_image = Image.alpha_composite(watermarked_image, transparent)
            except Exception as e:
                st.error(f"Error applying logo: {str(e)}")
        
        # Apply text watermark
        if text_watermark:
            try:
                font = load_font("Times New Roman", font_size)
                watermarked_image = apply_text_watermark(
                    image=watermarked_image,
                    text=text_watermark,
                    font=font,
                    position=text_position,
                    padding=text_padding,
                    color=text_color_rgb,
                    outline_color=outline_color_rgb,
                    outline_width=outline_width
                )
            except Exception as e:
                st.error(f"Error applying text: {str(e)}")
        
        # Display watermarked image
        st.image(watermarked_image, use_column_width=True)
        
        # Download button
        # Convert to RGB for JPEG
        if uploaded_image.name.lower().endswith(('.jpg', '.jpeg')):
            final_image = Image.new('RGB', watermarked_image.size, (255, 255, 255))
            final_image.paste(watermarked_image, mask=watermarked_image.split()[3])
        else:
            final_image = watermarked_image
        
        # Save to bytes
        buf = io.BytesIO()
        output_format = 'JPEG' if uploaded_image.name.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
        final_image.save(buf, format=output_format, quality=95)
        buf.seek(0)
        
        st.download_button(
            label="⬇️ Download Watermarked Image",
            data=buf,
            file_name=f"watermarked_{uploaded_image.name}",
            mime=f"image/{output_format.lower()}"
        )

else:
    # Show instructions when no image is uploaded
    st.info("👈 Upload an image from the sidebar to get started!")
    
    st.markdown("""
    ### How to use:
    1. **Upload an image** using the sidebar
    2. **Adjust settings** for text and logo watermarks
    3. **Preview** the result in real-time
    4. **Download** the watermarked image
    
    ### Features:
    - ✅ Automatic font size recommendations based on image dimensions
    - ✅ Real-time preview
    - ✅ Customizable text color and outline
    - ✅ Adjustable positioning for both text and logo
    - ✅ Support for multiple image formats
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
