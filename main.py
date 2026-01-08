

from flask import Flask, send_file, jsonify
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Base directory for mushaf images
MUSHAF_DIR = Path(__file__).parent / "mushaf"


@app.route('/')
def home():
    return jsonify({
        "message": "Quran Mushaf API",
        "endpoints": {
            "/mushafs": "List all available mushafs",
            "/mushaf/<mushaf_type>": "List pages in a specific mushaf",
            "/mushaf/<mushaf_type>/page/<page_number>": "Get a specific page image"
        }
    })


@app.route('/mushafs', methods=['GET'])
def list_mushafs():
    """List all available mushaf types"""
    try:
        if not MUSHAF_DIR.exists():
            return jsonify({"mushafs": [], "message": "No mushaf directory found"}), 404
        
        mushafs = [d.name for d in MUSHAF_DIR.iterdir() if d.is_dir()]
        return jsonify({"mushafs": mushafs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mushaf/<mushaf_type>', methods=['GET'])
def list_pages(mushaf_type):
    """List all pages available in a specific mushaf"""
    try:
        mushaf_path = MUSHAF_DIR / mushaf_type
        
        if not mushaf_path.exists():
            return jsonify({"error": f"Mushaf type '{mushaf_type}' not found"}), 404
        
        # Find all page files (supports multiple image formats)
        page_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.webp']:
            page_files.extend(mushaf_path.glob(ext))
        
        # Extract page numbers from filenames
        pages = []
        for file in page_files:
            # Expecting format: page1.png, page2.jpg, etc.
            if file.stem.startswith('page'):
                try:
                    page_num = int(file.stem[4:])
                    pages.append({
                        "page": page_num,
                        "filename": file.name
                    })
                except ValueError:
                    continue
        
        pages.sort(key=lambda x: x['page'])
        
        return jsonify({
            "mushaf_type": mushaf_type,
            "total_pages": len(pages),
            "pages": pages
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mushaf/<mushaf_type>/page/<int:page_number>', methods=['GET'])
def get_page(mushaf_type, page_number):
    """Get a specific page image from a mushaf"""
    try:
        mushaf_path = MUSHAF_DIR / mushaf_type
        
        if not mushaf_path.exists():
            return jsonify({"error": f"Mushaf type '{mushaf_type}' not found"}), 404
        
        # Look for the page file with various extensions and naming formats
        page_file = None
        for ext in ['.png', '.jpg', '.jpeg', '.webp']:
            # Try format: page2.png
            potential_file = mushaf_path / f"page{page_number}{ext}"
            if potential_file.exists():
                page_file = potential_file
                break
            # Try format: 2.png
            potential_file = mushaf_path / f"{page_number}{ext}"
            if potential_file.exists():
                page_file = potential_file
                break
        
        if page_file is None:
            return jsonify({"error": f"Page {page_number} not found in {mushaf_type}"}), 404
        
        return send_file(page_file, mimetype=f'image/{page_file.suffix[1:]}')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Create mushaf directory if it doesn't exist
    MUSHAF_DIR.mkdir(exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
