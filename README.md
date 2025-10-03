# smh-playwright-crawl

**Async, multi-tab, domain-constrained web crawler using Playwright and BeautifulSoup. CLI and Python API with screenshots.**

---

## Features

- Fast, **concurrent crawling** with multiple browser tabs.  
- Handles **JavaScript-heavy sites** using real browsers.  
- Extracts **title, description, headings, links, and full text**.  
- **Domain-restricted** recursive crawling—never leaves your target site.  
- Skips duplicate, broken, and non-HTML resources.  
- Automatically captures **screenshots** for every page (Base64 encoded).  
- Usable as **CLI tool** or **Python API**.  

---

## Installation

```bash
pip install smh-playwright-crawl
playwright install
```

> **Important:** Run `playwright install` to download necessary browser drivers.

---

## CLI Usage

```bash
smh-playwright-crawl "https://example.com"
--headless        # (default: True, runs headless)
--no-headless     # Show browser window
--request-timeout 30000
--max-tabs 10
--output output.json
```

**Example:**

```bash
smh-playwright-crawl "https://integramicro.com/" --no-headless --output site.json
```

### CLI Options

| Argument            | Default             | Description                           |
| ------------------- | ----------------- | ------------------------------------- |
| `url`               | (required)        | Seed/start URL                        |
| `--headless`        | True              | Run browser headless                  |
| `--no-headless`     |                   | Show browser window                   |
| `--request-timeout` | 30000             | Timeout per page load in ms           |
| `--max-tabs`        | 15                | Max concurrent browser tabs           |
| `--output`          | crawl_results.json | Output file (JSON)                   |

---

## Python API Usage

```python
from smh_playwright_crawl import crawl
import asyncio

# Crawl pages (screenshots are always included)
results = asyncio.run(crawl(
    "https://example.com",
    headless=True,
    request_timeout=30000,
    max_tabs=8
))

print("Pages crawled:", len(results))

# Access first page data
page = results[0]
print("Title:", page["title"])
print("Raw text:", page["raw_text"])
print("Number of screenshots:", len(page["screenshots"]))
```

**Each result object contains:**

```json
{
  "url": "https://example.com/...",
  "title": "...",
  "description": "...",
  "headings": ["..."],
  "links": [{"text": "...", "url": "..."}],
  "summary": "",
  "domain": "...",
  "tokens": 234,
  "word_count": 564,
  "raw_text": "...",
  "screenshots": [
    "iVBORw0KGgoAAAANSUhEUgAA...",  // Base64
    "iVBORw0KGgoAAAABBBCC..."
  ]
}
```

---

## Working with Screenshots

Screenshots are returned as **Base64 strings**.

### Display in Web App:

```html
<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAA..." />
```

### Save to File:

```python
import base64

screenshot_b64 = page["screenshots"][0]
with open("screenshot.png", "wb") as f:
    f.write(base64.b64decode(screenshot_b64))
```

### Generate Embeddings / Zero-Shot Classification (AI):

```python
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io, base64

image = Image.open(io.BytesIO(base64.b64decode(page["screenshots"][0])))

# Load CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Option 1: Generate image embeddings
inputs = processor(images=image, return_tensors="pt")
embeddings = model.get_image_features(**inputs)

# Option 2: Zero-shot classification
classes = ["giraffe", "zebra", "elephant"]
inputs = processor(text=classes, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)
logits_per_image = outputs.logits_per_image
probs = logits_per_image.softmax(dim=1)
print(dict(zip(classes, probs[0].tolist())))
```

---

## Requirements

- Python 3.11+ (<=3.12)  
- Playwright (`playwright install` required)  
- BeautifulSoup4  
- tldextract  

---

## Responsible Use

- Respect `robots.txt` and site terms of use.  
- Intended for **legitimate, ethical, and legal crawling only**.  

---

## License

MIT License.  

---

## Author

[S MUNI HARISH](mailto:samamuniharish@gmail.com)  

---

**👍 Highlights:**  

- Screenshots are **always included**, no optional flags.  
- Clear API & CLI examples.  
- Includes usage for display, saving, and embeddings/AI.
