# Banan Website — Python + Flask

A responsive local website inspired by the four-page Banan Universal One Canva design.

## Requirements
- Python 3.10 or newer
- VS Code
- VS Code's Python extension (recommended)

## Run it in VS Code

1. Unzip `banan_website.zip`.
2. Open the `banan_website` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install Flask:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the website:
   ```bash
   python app.py
   ```

7. Open http://127.0.0.1:5000 in your browser.

## Pages
- `/` — Homepage and Universal One feature sections
- `/shop` — Phones and Laptops & PCs categories
- `/support` — Expert support and location cards
- `/onboarding` — Employee Onboarding Hub demo
- `/cart` — Demo shopping bag

## What works
- Responsive navigation, including a mobile menu
- Navigation between pages
- Add-to-bag button and session-based demo cart
- Clear demo bag
- Email links for support and onboarding

## Notes
- This is a local prototype, not a production ecommerce store.
- Product visuals are CSS illustrations rather than the original Canva assets.
- Product price, technical specifications, addresses, and contact details are demo content and should be confirmed before publishing.
- The cart does not process payments or collect customer details.
- For public deployment, change `app.secret_key`, disable debug mode, and configure real product data and contact details.


## Canva images
The product and support areas now reference image thumbnails from the Canva design's media assets. These are loaded from Canva's media CDN, so an internet connection is needed when viewing the site. Canva-signed thumbnail links can expire; if an image stops loading, download the original image from Canva and save it in `static/images/`, then update its `src` in the relevant template. The Canva API exposed asset thumbnails, not original downloadable files in this workflow.
