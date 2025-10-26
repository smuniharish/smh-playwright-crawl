# smh-playwright-crawl

**Async, multi-tab, domain-constrained web crawler using Playwright and BeautifulSoup. CLI and Python API with losslessly compressed screenshots.**

---

## Features

* Fast, **concurrent crawling** with multiple browser tabs.
* Handles **JavaScript-heavy sites** using real browsers.
* Extracts **title, description, headings, links, and full text**.
* **Domain-restricted** recursive crawling—never leaves your target site.
* Skips duplicate, broken, and non-HTML resources.
* Automatically captures **screenshots** for every page, **losslessly compressed with Zstandard** and Base64 encoded.
* Compression runs in background threads to avoid blocking async crawling.
* Usable as **CLI tool** or **Python API**.

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

| Argument            | Default            | Description                 |
| ------------------- | ------------------ | --------------------------- |
| `url`               | (required)         | Seed/start URL              |
| `--headless`        | True               | Run browser headless        |
| `--no-headless`     |                    | Show browser window         |
| `--request-timeout` | 30000              | Timeout per page load in ms |
| `--max-tabs`        | 15                 | Max concurrent browser tabs |
| `--output`          | crawl_results.json | Output file (JSON)          |

---

## Python API Usage

```python
from smh_playwright_crawl import crawl
import asyncio

# Crawl pages (screenshots are compressed with Zstandard and included)
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
    "KLUvPwABAAAABGZzdGFuZGFyZA...",  // Zstandard compressed, Base64
    "KLUvPwABAAAAC2ZzdGFuZGFyZA..."
  ]
}
```

> Screenshots are **always compressed with Zstandard at max level** for optimal size reduction without losing any visual fidelity.

---

## Working with Screenshots

Screenshots are returned as **Base64-encoded, Zstandard-compressed strings**.

### Decompress and Display

```python
import base64, zstandard as zstd, io
from PIL import Image

def decompress_screenshot(b64_string: str) -> bytes:
    compressed = base64.b64decode(b64_string)
    dctx = zstd.ZstdDecompressor()
    return dctx.decompress(compressed)

screenshot_bytes = decompress_screenshot(page["screenshots"][0])
image = Image.open(io.BytesIO(screenshot_bytes))
image.show()
```

### Save to File

```python
with open("screenshot.png", "wb") as f:
    f.write(screenshot_bytes)
```

### Use in AI / Embeddings

```python
from transformers import CLIPProcessor, CLIPModel

# Load image from decompressed bytes
image = Image.open(io.BytesIO(screenshot_bytes))

# Load CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Generate image embeddings
inputs = processor(images=image, return_tensors="pt")
embeddings = model.get_image_features(**inputs)

# Zero-shot classification
classes = ["giraffe", "zebra", "elephant"]
inputs = processor(text=classes, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)
probs = outputs.logits_per_image.softmax(dim=1)
print(dict(zip(classes, probs[0].tolist())))
```

---

## Requirements

* Python 3.11+ (<=3.12)
* Playwright (`playwright install` required)
* BeautifulSoup4
* tldextract
* zstandard

---

## Responsible Use

* Respect `robots.txt` and site terms of use.
* Intended for **legitimate, ethical, and legal crawling only**.

---

## License

MIT License

---

## Author

[S MUNI HARISH](mailto:samamuniharish@gmail.com)