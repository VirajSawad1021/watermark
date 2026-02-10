# 🖼️ Image Watermarker

A powerful and user-friendly web application for adding text and logo watermarks to images. Built with Python and Streamlit.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.37+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📤 **Easy Upload** - Drag and drop or browse for images
- 🎨 **Real-time Preview** - See changes instantly as you adjust settings
- 📏 **Smart Recommendations** - Automatic font size and padding based on image dimensions
- 🎯 **Flexible Positioning** - Place watermarks in any corner
- 🖋️ **Custom Text** - Add text watermarks with customizable:
  - Font size
  - Text color
  - Outline color and width
  - Position (4 corners)
  - Padding from edges
- 🏷️ **Logo Support** - Add PNG logo watermarks with transparency
- 👀 **Before/After View** - Compare original and watermarked images side by side
- ⬇️ **One-Click Download** - Download watermarked images instantly

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone git@github.com:VirajSawad1021/watermark.git
cd watermark
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit web interface:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage

### Web Interface (Recommended)

1. **Upload an Image** - Click "Upload Image" in the sidebar or drag and drop
2. **Add Text Watermark** - Enter your desired text in the sidebar
3. **Customize Settings** - Adjust font size, colors, and position
4. **Add Logo (Optional)** - Upload a PNG logo with transparency
5. **Preview** - See the result in real-time
6. **Download** - Click "Download Watermarked Image" to save

### Command Line Interface

For batch processing, use the command-line script:

1. Place images in the `input` folder
2. Create `.txt` files with the same name as your images (e.g., `photo.jpg` → `photo.txt`)
3. Add your watermark text to each `.txt` file
4. Run the script:
```bash
python apply_watermark.py
```

Watermarked images will be saved in the `output` folder.

## 📁 Project Structure

```
watermark/
├── app.py                  # Streamlit web interface
├── apply_watermark.py      # Core watermarking functions
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── watermark.png          # Your logo watermark (optional)
├── input/                 # Input images folder
│   ├── image1.jpg
│   └── image1.txt         # Text for image1.jpg
└── output/                # Watermarked images output
```

## ⚙️ Configuration

### Default Settings

The application uses these default settings (can be adjusted in the web interface):

- **Font**: Times New Roman
- **Font Size**: Auto-calculated based on image size (typically 5% of image width)
- **Text Color**: White (#FFFFFF)
- **Outline Color**: Black (#000000)
- **Outline Width**: 2px
- **Text Position**: Bottom-left
- **Logo Size**: 15% of image width
- **Logo Position**: Bottom-right

### Customizing Defaults

Edit `apply_watermark.py` to change default values:

```python
# Text watermark settings
font_size = 40              # Font size for text watermark
text_color = (255, 255, 255)  # White text (RGB)
text_padding = 20           # Padding from edges for text

# Image watermark settings
scale_factor = 0.18         # Logo size relative to image
padding = 300               # Logo padding from edges
```

## 🎨 Supported Formats

### Input Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

### Output Formats
- Same as input format
- High quality (95% for JPEG)

## 💡 Tips

1. **Font Size** - The app automatically recommends optimal font sizes based on your image dimensions
2. **Text Visibility** - Use the outline feature to ensure text is visible on any background
3. **Logo Transparency** - Use PNG format with transparency for best logo results
4. **Batch Processing** - Use the command-line interface for processing multiple images
5. **Position** - Text and logo are positioned in opposite corners by default to avoid overlap

## 🛠️ Dependencies

- **Pillow** (10.4.0) - Image processing
- **Streamlit** (1.37+) - Web interface
- **Python** (3.10+) - Runtime

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Issues

If you encounter any issues or have suggestions, please [open an issue](https://github.com/VirajSawad1021/watermark/issues).

## 👨‍💻 Author

**Viraj Sawad**
- GitHub: [@VirajSawad1021](https://github.com/VirajSawad1021)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Image processing powered by [Pillow](https://python-pillow.org/)

---

Made with ❤️ by Viraj Sawad
