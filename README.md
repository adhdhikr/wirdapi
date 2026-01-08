# Quran Mushaf API

A simple Flask API to serve Quran pages from different mushaf types. images taken from quran-pages-images repo

## Project Structure

```
api/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
└── mushaf/             # Directory for mushaf images
    ├── madani/         # Madani mushaf pages
    ├── uthmani/        # Uthmani mushaf pages
    └── indopak/        # Indopak mushaf pages
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your mushaf page images to the appropriate folders:
   - Place images in `mushaf/<mushaf_type>/` directories
   - Name files as: `page1.png`, `page2.png`, `page3.jpg`, etc.
   - Supported formats: PNG, JPG, JPEG, WEBP

## Running the API

```bash
python main.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### 1. Home
**GET** `/`
- Returns API information and available endpoints

### 2. List All Mushafs
**GET** `/mushafs`
- Returns a list of all available mushaf types

**Example Response:**
```json
{
  "mushafs": ["madani", "uthmani", "indopak"]
}
```

### 3. List Pages in a Mushaf
**GET** `/mushaf/<mushaf_type>`
- Returns all pages available in a specific mushaf

**Example:** `GET /mushaf/madani`

**Response:**
```json
{
  "mushaf_type": "madani",
  "total_pages": 604,
  "pages": [
    {"page": 1, "filename": "page1.png"},
    {"page": 2, "filename": "page2.png"}
  ]
}
```

### 4. Get a Specific Page
**GET** `/mushaf/<mushaf_type>/page/<page_number>`
- Returns the image file for a specific page

**Example:** `GET /mushaf/madani/page/1`

**Response:** Image file (PNG/JPG/WEBP)

## Usage Examples

### Using cURL
```bash
# List all mushafs
curl http://localhost:5000/mushafs

# List pages in madani mushaf
curl http://localhost:5000/mushaf/madani

# Get page 1 from madani mushaf
curl http://localhost:5000/mushaf/madani/page/1 --output page1.png
```

### Using JavaScript/Fetch
```javascript
// List all mushafs
fetch('http://localhost:5000/mushafs')
  .then(res => res.json())
  .then(data => console.log(data));

// Get a specific page as image
fetch('http://localhost:5000/mushaf/madani/page/1')
  .then(res => res.blob())
  .then(blob => {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(blob);
    document.body.appendChild(img);
  });
```

## Notes

- The API supports CORS, so it can be accessed from web browsers
- Make sure to add your actual mushaf page images to the respective folders
- The Quran typically has 604 pages in most mushafs
