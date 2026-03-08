"""
model.py — FLAN-T5 Tweet Generation Engine

Pipeline per request:
  Step A: Brand voice analysis  (4 focused inferences)
  Step B: 10 tweet generation   (1 inference per tweet, 7 rotating styles)
  Step C: Parse & return JSON
"""

import re
import logging
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

logger = logging.getLogger(__name__)

TWEET_STYLES = [
    "Engaging",
    "Promotional",
    "Witty",
    "Informative",
    "Conversational",
    "Meme-style",
    "Value-driven",
]

STYLE_INSTRUCTIONS = {
    "Engaging":       "Write an interactive tweet that asks a question or invites the audience to respond.",
    "Promotional":    "Write a tweet promoting a product feature or special offer with a subtle call to action.",
    "Witty":          "Write a clever, funny tweet with a surprising twist or wordplay.",
    "Informative":    "Write a tweet sharing a useful tip, fact, or insight relevant to the brand.",
    "Conversational": "Write a casual human-sounding tweet, like a friend talking — not a corporate ad.",
    "Meme-style":     "Write a tweet using a popular meme format or relatable cultural reference.",
    "Value-driven":   "Write an inspirational or motivational tweet that delivers genuine value.",
}


class TweetModel:
    MODEL_NAME = "google/flan-t5-large"

    def __init__(self):
        self.model_name = self.MODEL_NAME
        self.is_loaded  = False
        self._load()

    def _load(self):
        logger.info(f"Loading tokenizer: {self.MODEL_NAME}")
        self.tokenizer = T5Tokenizer.from_pretrained(self.MODEL_NAME)
        logger.info(f"Loading model weights: {self.MODEL_NAME}")
        self.model = T5ForConditionalGeneration.from_pretrained(
            self.MODEL_NAME, torch_dtype=torch.float32
        )
        self.model.eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.info(f"Model ready on device: {self.device}")
        self.is_loaded = True

    # ── Public entry point ────────────────────────────────────────
    def generate(self, brand_name, industry, objective, tones, products, extra_context):
        voice  = self._analyse_voice(brand_name, industry, tones, products)
        tweets = self._generate_tweets(brand_name, industry, objective,
                                       voice, products, extra_context)
        return {"brand_voice": voice, "tweets": tweets}

    # ── Step A: Brand Voice Analysis ──────────────────────────────
    def _analyse_voice(self, brand_name, industry, tones, products):
        ctx = " ".join(filter(None, [
            f"Industry: {industry}."      if industry else "",
            f"Products: {products}."      if products else "",
            f"Preferred tones: {', '.join(tones)}." if tones else "",
        ]))

        tone = self._infer(
            f"What is the brand communication tone for {brand_name}? {ctx} "
            f"Answer in 3 words or fewer. Example: Bold and Witty", 12)

        audience = self._infer(
            f"Who is the primary target audience for {brand_name}? {ctx} "
            f"Answer in one sentence.", 50)

        themes_raw = self._infer(
            f"List 3 social media content themes for {brand_name}. {ctx} "
            f"Format exactly: theme1, theme2, theme3", 30)
        themes = [t.strip().title() for t in themes_raw.split(",") if t.strip()][:3]
        defaults = ["Brand Stories", "Product Features", "Customer Love"]
        while len(themes) < 3:
            themes.append(defaults[len(themes)])

        personality = self._infer(
            f"Describe the personality of {brand_name} as if it were a person. {ctx} "
            f"One sentence.", 50)

        return {"tone": tone, "audience": audience,
                "themes": themes, "personality": personality}

    # ── Step B: Generate 10 Tweets ────────────────────────────────
    def _generate_tweets(self, brand_name, industry, objective,
                         voice, products, extra_context):
        styles = (TWEET_STYLES * 2)[:10]
        tweets = []
        for i, style in enumerate(styles):
            raw = self._one_tweet(brand_name, industry, objective,
                                  voice, products, extra_context, style, i + 1)
            text, hashtags = self._parse(raw, brand_name)
            tweets.append({"text": text, "style": style, "hashtags": hashtags})
        return tweets

    def _one_tweet(self, brand_name, industry, objective, voice,
                   products, extra_context, style, num):
        prompt = (
            f"You are the social media manager for {brand_name}, "
            f"a {industry or 'consumer'} brand. "
            f"Brand tone: {voice['tone']}. "
            f"Personality: {voice['personality']}. "
            f"Target audience: {voice['audience']}. "
            f"Campaign goal: {objective}. "
            + (f"Products: {products}. " if products else "")
            + (f"Context: {extra_context}. " if extra_context else "")
            + f"Write tweet #{num} in the {style} style. "
            f"{STYLE_INSTRUCTIONS[style]} "
            f"Under 200 characters. Authentic to {brand_name}. "
            f"No generic phrases. Add 2 relevant hashtags at the end."
        )
        return self._infer(prompt, 120)

    # ── Core inference ────────────────────────────────────────────
    def _infer(self, prompt: str, max_new_tokens: int = 80) -> str:
        inputs = self.tokenizer(
            prompt, return_tensors="pt",
            max_length=512, truncation=True, padding=True
        ).to(self.device)
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=4,
                no_repeat_ngram_size=3,
                early_stopping=True,
                temperature=0.9,
                do_sample=True,
            )
        return self.tokenizer.decode(out[0], skip_special_tokens=True).strip()

    # ── Parse hashtags ────────────────────────────────────────────
    @staticmethod
    def _parse(text: str, brand_name: str):
        found = re.findall(r"#(\w+)", text)
        clean = re.sub(r"#\w+", "", text).strip().rstrip(".")
        tag   = re.sub(r"\s+", "", brand_name)
        seen, unique = set(), []
        for h in found:
            if h.lower() not in seen:
                seen.add(h.lower()); unique.append(h)
        if tag.lower() not in seen:
            unique.insert(0, tag)
        return clean, unique[:3]
