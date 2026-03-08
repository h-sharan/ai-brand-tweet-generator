# 🐦 TweetCraft — AI-Powered On-Brand Tweet Generator

> Generate 10 creative, on-brand tweets for any brand instantly. Auto-detects brand voice from brand name, industry, and objective — no API key or model download required.

---

## 📸 Overview

TweetCraft is a full-stack web application that helps marketers and social media managers generate 10 high-quality, brand-accurate tweets in seconds. It analyses the brand's voice, tone, target audience, and content themes automatically — then generates 10 tweets across 7 different styles.

---

## ✨ Features

- **Auto Brand Voice Detection** — Recognises 50+ popular brands (Zomato, Nike, Apple, CRED, Nykaa, Netflix etc.) and infers their exact tone automatically
- **10 Tweets in 7 Styles** — Engaging, Promotional, Witty, Informative, Conversational, Meme-style, Value-driven
- **Brand Voice Analysis** — Outputs tone, target audience, content themes, and brand personality
- **Filter by Style** — Filter all 10 tweets by style type
- **Copy & Export** — One-click copy per tweet, export all as `.txt`
- **No API Key Required** — Fully self-contained, rule-based generation engine
- **Instant Results** — No model download, no waiting — results in under 1 second
- **FindFluencr-inspired UI** — Clean SaaS interface with collapsible sidebar sections

---

## 🗂️ Project Structure

```
tweetcraft/
├── backend/
│   ├── app.py          # Flask REST API
│   ├── generator.py    # Tweet generation engine (brand profiles + templates)
│   └── requirements.txt
└── frontend/
    └── index.html      # Complete frontend (HTML + CSS + JS in one file)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation & Run

**Step 1 — Clone the repo**
```bash
git clone https://github.com/h-sharan/ai-brand-tweet-generator.git
cd ai-brand-tweet-generator
```

**Step 2 — Start the backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```
Backend runs at `http://localhost:5000`

**Step 3 — Start the frontend**
```bash
cd ../frontend
python -m http.server 8080
```
Open `http://localhost:8080` in your browser.

---

## 🧠 How It Works

### Brand Voice Analysis
The system identifies brand voice through a 3-level priority system:

1. **Known Brand Match** — If the brand name matches one of 50+ pre-profiled brands (Zomato, Apple, Nike, CRED etc.), it uses the exact known tone, personality and audience
2. **Industry Inference** — If the industry is provided, it maps to an industry-level tone profile
3. **User Override** — User can manually select tone chips to override auto-detection

### Tweet Generation
- 10 distinct creative templates per style category (70+ total templates)
- Each tweet uses dynamic variable substitution (`{adj}`, `{product}`, `{industry}` etc.)
- Objective-based angle modifiers shift the framing of tweets
- Randomisation ensures no two generations are identical

### Brand Voice Output
For each brand, the system outputs:
- **Tone** — e.g. "Witty & Relatable"
- **Target Audience** — e.g. "Urban food lovers and millennials aged 18–35"
- **Content Themes** — e.g. ["Food Cravings", "Relatable Humor", "Delivery Culture"]
- **Brand Personality** — e.g. "That food-obsessed friend who texts you memes at midnight..."

---

## 🎯 Tweet Styles

| Style | Description |
|---|---|
| Engaging | Questions and interactive prompts that invite replies |
| Promotional | Benefit-led product tweets with subtle CTAs |
| Witty | Clever wordplay and subverted expectations |
| Informative | Surprising facts and useful insights |
| Conversational | Human, casual tone — sounds like a real person |
| Meme-style | POV / Nobody / relatable scenario formats |
| Value-driven | Inspirational, mindset-shifting content |

---

## 🧪 Example Inputs

**Zomato**
| Field | Value |
|---|---|
| Brand Name | Zomato |
| Industry | Food & Beverage |
| Objective | Engagement / Conversation |
| Products | Food delivery app, restaurant discovery, Zomato Gold, quick commerce |

**Nykaa**
| Field | Value |
|---|---|
| Brand Name | Nykaa |
| Industry | Beauty & Skincare |
| Objective | Product Promotion |
| Products | Skincare, makeup, haircare, Nykaa Fashion, Kay Beauty |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Generation Engine | Rule-based template system with brand profiles |
| Deployment | Render (backend) + Netlify (frontend) |

---

## 🌐 Deployment

**Backend → Render**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

**Frontend → Netlify**
- Drag and drop the `frontend` folder
- Update `const API` in `index.html` to your Render backend URL

---

## 📋 API Reference

### `POST /api/generate`

**Request:**
```json
{
  "brand_name": "Zomato",
  "industry": "Food & Beverage",
  "objective": "Engagement / Conversation",
  "tones": ["Witty & Playful"],
  "products": "Food delivery app in India",
  "extra_context": "Late night cravings campaign"
}
```

**Response:**
```json
{
  "brand_voice": {
    "tone": "Witty & Relatable",
    "audience": "Urban food lovers and millennials aged 18-35",
    "themes": ["Food Cravings", "Relatable Humor", "Delivery Culture"],
    "personality": "That food-obsessed friend who texts you memes at midnight..."
  },
  "tweets": [
    {
      "text": "Hot take: hunger hits different at 2am and we are absolutely here for it.",
      "style": "Witty",
      "hashtags": ["Zomato", "LateNightCravings"]
    }
  ]
}
```

### `GET /api/health`
Returns server and model status.

---

## 👤 Author

**Sharan** — [github.com/h-sharan](https://github.com/h-sharan)

---

## 📄 Licence

This project was built as part of an internship assignment for **Confluencr**.
