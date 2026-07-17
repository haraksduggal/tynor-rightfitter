<div align="center">

# Tynor Decision Tree

**Personalised orthopaedic product finder for Tynor Orthotics**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-28a745?style=flat-square)
![Deployed](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-FF4B4B?style=flat-square)
![License](https://img.shields.io/badge/License-Proprietary-7B2D8B?style=flat-square)

</div>

---

<!-- Add a screenshot: place your image at assets/screenshot.png and it will appear below. -->
<div align="center">
  <img width="795" height="556" alt="image" src="https://github.com/user-attachments/assets/04d237cb-d078-4347-8ac9-5af41d891a48" />
  <br/>
  <sub>The product-finder interface — body region selection, guided question flow, and product recommendation.</sub>
</div>

---

## Overview

The **Tynor Decision Tree** is a customer-facing web tool that guides users to the most suitable Tynor orthopaedic product through a structured, conversational question flow. It replaces generic product catalogues with a personalised, medically-aware recommendation engine — reducing decision fatigue and improving product fit.

Tynor Orthotics is India's largest orthopaedic appliance manufacturer, with 250+ products across 12 body regions distributed in 60+ countries.

---

## Highlights

| Feature | Description |
|---|---|
| 12 Body Regions | Finger, Neck, Shoulder, Elbow, Wrist, Chest, Back, Abdominal, Knee, Thigh, Calf, Ankle |
| Three Product Lines | Cure (recovery), Sport (injury prevention), Lifestyle (daily comfort) |
| 193 Products | Full catalog with sizes, prices, descriptions, and availability |
| Gender-Aware Filtering | Automatically filters clinically irrelevant options by gender |
| AI Validation Layer | Groq LLM (Llama 3.1) validates answer consistency before recommendation |
| Safety Check | Flags fractures, surgery, numbness — redirects to clinician with interim product |
| Dark / Light Mode | Full theme toggle with Tynor brand styling (Poppins, #7B2D8B) |
| Editable Catalog | Master Excel + update script — no code changes needed to update products |
| Streamlit Cloud | Free, zero-infrastructure deployment with secret management |

---

## How It Works

The tool uses a deterministic rules-based decision tree, with an AI validation step before the final recommendation.

```
User selects body region (12 options, alphabetical)
        │
        ▼
Age → Gender → Intent (Cure / Sport / Lifestyle)
        │
        ├─ Cure ──► Safety check ──► Problem selection (gender-filtered)
        │                │
        │          [Flag detected] ──► Clinician warning + safe product
        │                │
        │          [Clear] ──► Sub-location ──► Severity
        │
        ├─ Sport ─► Activity ──► Support level
        │
        └─ Lifestyle ──► Relief type
                │
                ▼
        AI Validation (Groq / Llama 3.1)
        Checks for logical/clinical inconsistencies
                │
          ┌─────┴─────┐
        [Flag]      [Clear]
          │            │
     Confirm /      Contact form
     Go back           │
                       ▼
               Product recommendation
               (name, size, price, FAQs)
```

The resolver applies staged filtering: condition match → sub-location tags → severity → support type. The highest-rated product surviving all filters is shown. Free-text "Other" entries trigger keyword search across product names and descriptions.

---

## Quick Start

### Prerequisites

```bash
python3 --version   # 3.11+
pip3 install streamlit requests pillow openpyxl streamlit-image-coordinates
```

### Run Locally

```bash
git clone https://github.com/haraksduggal/tynor-rightfiter.git
cd tynor-rightfiter
streamlit run prototype.py
```

The app opens at `http://localhost:8501`. It requires `catalog.json` and `problems.json` in the same directory.

### Update the Product Catalog

1. Open `catalog_master.xlsx` and edit products (name, price, image URL, etc.)
2. Save the file
3. Run the update script:

```bash
python3 update_catalog.py
```

4. Push changes to GitHub — Streamlit Cloud auto-deploys within seconds.

---

## Deployment

<details>
<summary>Deploy to Streamlit Community Cloud (free)</summary>

1. Fork or push this repository to your GitHub account (public repo required).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → **Deploy a public app from GitHub**.
4. Set:
   - **Repository:** `your-username/tynor-rightfiter`
   - **Branch:** `main`
   - **Main file path:** `prototype.py`
5. Click **Deploy**.
6. Once deployed, go to **Settings → Secrets** and add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

7. The app restarts automatically and the AI validation layer activates.

**Live URL:** https://tynor-rightfitter-wuryfs5aq9hyzrzzbzxawy.streamlit.app

</details>

---

## Project Structure

```
tynor-rightfiter/
├── prototype.py              # Main Streamlit application
├── catalog.json              # Product catalog (193 products, auto-generated)
├── problems.json             # Condition-to-product mapping (107 conditions, 12 regions)
├── catalog_master.xlsx       # Editable master product catalog
├── update_catalog.py         # Script to regenerate catalog.json from Excel
├── requirements.txt          # Python dependencies
└── assets/
    └── screenshot.png        # UI screenshot (add your own)
```

---

## Configuration

### Adding or Editing Products

Edit `catalog_master.xlsx` (Catalog sheet). Columns:

| Column | Description |
|---|---|
| `product_id` | Unique ID — do not change |
| `name` | Product name (must match Tynor website exactly) |
| `brand` | `Cure` / `Sport` / `Life` |
| `body_part` | Body region (must match one of the 12 regions) |
| `sub_cat` | Subcategory (e.g. Knee Support, LS Belt) |
| `short_desc` | Product description |
| `rating` | Rating out of 5 |
| `image_url` | Direct image URL from Shopify CDN |
| `price_S/M/L/XL/XXL/OneSize` | Price per size (numbers only) |

Run `python3 update_catalog.py` after saving.

### Editing Conditions / Problem Mapping

Edit `problems.json` directly, or use the `Tynor_Product_Mapping_14Regions.xlsx` reviewed by Dr. Shreya Chauhan and regenerate via script.

### Groq AI Validation

The system prompt and flagging rules live in the `validate_with_ai()` function in `prototype.py`. The key is stored as a Streamlit secret (`GROQ_API_KEY`) and never hardcoded.

---

## Roadmap

- [x] 12-region decision tree with full question flows
- [x] 193-product catalog with size/price/availability
- [x] Gender-aware question filtering
- [x] AI validation layer (Groq / Llama 3.1)
- [x] Safety check with clinician redirect
- [x] Dark / light mode
- [x] Editable Excel catalog with update script
- [x] Deployed on Streamlit Community Cloud
- [ ] Live Shopify product images via CDN
- [ ] Real-time prices and stock via Shopify Storefront API
- [ ] Iframe embed on tynorstore.com
- [ ] Size chart images per region
- [ ] Conversational AI chatbot (separate project)
- [ ] Option A rule-based validation fallback

---

## Disclaimer

This tool suggests products for general guidance and convenience only. It is **not a substitute for professional medical advice, diagnosis, or treatment.** Users should consult a qualified doctor or physiotherapist for any health condition, injury, or post-surgical recovery. Tynor Orthotics bears no medical liability for product selections made through this tool.

---

<div align="center">
  <sub>Built as an internship project for <strong>Tynor Orthotics, Mohali</strong> · 2026</sub>
</div>
