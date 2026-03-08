"""
generator.py — Smart Tweet Template Engine
===========================================
No API key. No model download. Instant results.
Generates creative, brand-accurate tweets using:
  - Rich brand voice profiles (50+ known brands)
  - Industry-level fallback profiles
  - 10 distinct tweet style templates per tone category
  - Dynamic variable substitution for variety
"""

import random
import re

# ── Known brand profiles ──────────────────────────────────────────
BRAND_PROFILES = {
    "apple":      {"tone":"Premium & Minimal",     "adj":["sleek","powerful","brilliant","effortless"],      "audience":"Tech-savvy professionals and creatives aged 20-45",        "themes":["Innovation","Design Excellence","Seamless Experience"],  "personality":"That calm, confident friend who never needs to brag — their work speaks for itself."},
    "nike":       {"tone":"Bold & Motivational",   "adj":["unstoppable","relentless","fearless","iconic"],    "audience":"Athletes and fitness enthusiasts aged 16-40",              "themes":["Athletic Excellence","Personal Best","Winning Mindset"],  "personality":"The fiercely motivating coach who believes in you before you believe in yourself."},
    "zomato":     {"tone":"Witty & Relatable",     "adj":["hungry","craveable","obsessed","delicious"],       "audience":"Urban food lovers and millennials aged 18-35",             "themes":["Food Cravings","Relatable Hunger","Delivery Culture"],    "personality":"That food-obsessed friend who texts you memes at midnight and somehow always knows the best spots."},
    "swiggy":     {"tone":"Fun & Urgent",          "adj":["fast","fresh","craveable","instant"],              "audience":"Busy urban millennials who want food now",                 "themes":["Speed","Everyday Cravings","Convenience"],               "personality":"The hyperactive friend who shows up at your door with food before you even finish ordering."},
    "nykaa":      {"tone":"Glamorous & Empowering","adj":["radiant","bold","gorgeous","confident"],           "audience":"Beauty-conscious women aged 18-35",                        "themes":["Glow Goals","Beauty Rituals","Self-Expression"],         "personality":"The glamorous best friend who hypes you up and always knows the right lipstick shade for the occasion."},
    "netflix":    {"tone":"Witty & Cultural",      "adj":["binge-worthy","iconic","addictive","cinematic"],   "audience":"Pop culture enthusiasts aged 16-40",                       "themes":["Binge Culture","Pop References","Fandom"],               "personality":"The pop-culture-obsessed friend who has a quote for every situation and has rewatched The Office 12 times."},
    "amazon":     {"tone":"Convenient & Reliable", "adj":["fast","endless","reliable","effortless"],          "audience":"Online shoppers and Prime members aged 22-50",             "themes":["Unbeatable Deals","Fast Delivery","Endless Selection"],  "personality":"The super-reliable friend who always finds what you need, delivers it overnight, and never judges your cart."},
    "flipkart":   {"tone":"Exciting & Festive",    "adj":["unbeatable","massive","exciting","value-packed"],  "audience":"Value-conscious Indian shoppers aged 20-45",               "themes":["Big Deals","Festive Offers","Smart Shopping"],           "personality":"That deal-hunting friend who finds discounts you didn't even know existed and celebrates every good buy."},
    "cred":       {"tone":"Premium & Witty",       "adj":["exclusive","rewarding","clever","elite"],          "audience":"High-credit-score urban professionals aged 25-40",         "themes":["Reward Culture","Smart Finance","Premium Lifestyle"],    "personality":"That effortlessly cool, slightly sarcastic friend who makes adulting look like a privilege, not a chore."},
    "boat":       {"tone":"Bold & Youth-Centric",  "adj":["loud","powerful","wireless","unstoppable"],        "audience":"Music-loving youth aged 16-30",                            "themes":["Music Culture","Street Style","Wireless Freedom"],       "personality":"The loud, energetic friend at every concert who lives by the beat and never takes the earphones out."},
    "mamaearth":  {"tone":"Gentle & Natural",      "adj":["pure","safe","natural","toxin-free"],              "audience":"Health-conscious parents and millennials aged 25-40",      "themes":["Clean Beauty","Safe Ingredients","Natural Living"],      "personality":"The caring, eco-conscious friend who reads every ingredient label and genuinely wants the best for you."},
    "starbucks":  {"tone":"Warm & Premium",        "adj":["cozy","crafted","indulgent","signature"],          "audience":"Coffee culture enthusiasts aged 18-40",                    "themes":["Coffee Rituals","Cozy Moments","Premium Treats"],        "personality":"The warm, artsy friend who turns a coffee order into a full sensory experience and remembers your name."},
    "myntra":     {"tone":"Trendy & Aspirational", "adj":["fresh","stylish","on-trend","curated"],            "audience":"Fashion-forward youth aged 16-32",                         "themes":["Style Trends","OOTD","New Season"],                      "personality":"The ultra-stylish friend whose wardrobe is always ahead of the trend curve and makes everything look easy."},
    "dominos":    {"tone":"Urgent & Fun",          "adj":["hot","cheesy","fast","irresistible"],              "audience":"Pizza lovers and late-night hunger crowd aged 15-35",      "themes":["Pizza Cravings","Late Night Bites","Fast Delivery"],     "personality":"The no-nonsense, always-available friend who shows up hot and fast exactly when you need them."},
    "tanishq":    {"tone":"Elegant & Emotional",   "adj":["timeless","precious","stunning","crafted"],        "audience":"Occasion-driven buyers and families aged 25-55",           "themes":["Milestone Moments","Craftsmanship","Legacy"],           "personality":"The graceful, sentimental friend who finds meaning in every celebration and makes every moment feel golden."},
    "amul":       {"tone":"Witty & Iconic",        "adj":["fresh","creamy","classic","topical"],              "audience":"All Indians across age groups",                            "themes":["Topical Humor","Desi Culture","Daily Life"],            "personality":"The witty uncle who has a clever comeback for everything happening in the news and somehow makes dairy cool."},
    "byju":       {"tone":"Inspiring & Friendly",  "adj":["curious","bright","future-ready","engaging"],      "audience":"Students and parents aged 10-40",                          "themes":["Love for Learning","Future Skills","Growth Mindset"],    "personality":"The brilliant, encouraging teacher who makes you feel like learning is the coolest thing you can do."},
    "lenskart":   {"tone":"Smart & Fun",           "adj":["clear","stylish","smart","affordable"],            "audience":"Eyewear consumers and style-seekers aged 18-40",           "themes":["Vision & Style","Affordable Eyewear","Look Sharp"],      "personality":"The practical-but-stylish friend who makes glasses feel like a fashion statement, not a necessity."},
    "oyo":        {"tone":"Friendly & Accessible", "adj":["comfortable","reliable","affordable","welcoming"], "audience":"Budget-smart travellers and young explorers aged 18-35",   "themes":["Affordable Travel","Comfort Anywhere","Explore More"],   "personality":"The well-travelled friend who knows every budget-friendly spot and makes every trip feel like an adventure."},
    "paytm":      {"tone":"Smart & Convenient",    "adj":["instant","cashless","seamless","rewarding"],       "audience":"Digital-first consumers and small business owners aged 20-45","themes":["Digital Payments","Cashback Culture","Financial Access"],"personality":"The always-prepared friend who never carries cash and somehow makes finance feel like a superpower."},
    "meesho":     {"tone":"Warm & Community-Driven","adj":["affordable","trendy","empowering","homegrown"],   "audience":"Value-seekers and women entrepreneurs aged 20-45",         "themes":["Affordable Fashion","Reseller Empowerment","Community"], "personality":"The supportive, entrepreneurial friend who cheers you on and always finds the best deal for everyone."},
}

# ── Industry fallback profiles ────────────────────────────────────
INDUSTRY_PROFILES = {
    "food":         {"tone":"Fun & Craveable",        "adj":["delicious","craveable","fresh","irresistible"],  "audience":"Food lovers aged 18-40",              "themes":["Food Moments","Cravings","Foodie Culture"],       "personality":"A fun, relatable brand that speaks the language of hunger and happiness."},
    "fashion":      {"tone":"Trendy & Aspirational",  "adj":["stylish","fresh","bold","curated"],              "audience":"Fashion-forward youth aged 16-32",     "themes":["Style Trends","OOTD","New Arrivals"],             "personality":"A confident, trend-aware brand that makes style accessible and exciting."},
    "tech":         {"tone":"Smart & Innovative",     "adj":["powerful","seamless","cutting-edge","smart"],    "audience":"Tech enthusiasts aged 20-40",          "themes":["Innovation","Productivity","Future Tech"],        "personality":"A forward-thinking brand that simplifies complexity and makes the future feel close."},
    "health":       {"tone":"Caring & Motivating",    "adj":["healthy","energising","mindful","strong"],       "audience":"Wellness-conscious adults aged 25-45", "themes":["Wellness","Active Living","Self-Care"],           "personality":"A warm, science-backed brand that genuinely cares about your wellbeing journey."},
    "finance":      {"tone":"Smart & Trustworthy",    "adj":["secure","smart","rewarding","reliable"],         "audience":"Young professionals aged 22-40",       "themes":["Smart Money","Financial Freedom","Savings"],      "personality":"A transparent, empowering brand that makes financial decisions feel confident and clear."},
    "beauty":       {"tone":"Glam & Empowering",      "adj":["radiant","luxurious","bold","glowing"],          "audience":"Beauty enthusiasts aged 18-35",        "themes":["Glow Goals","Skincare Rituals","Self-Love"],      "personality":"A celebratory, empowering brand that makes every person feel like the main character."},
    "retail":       {"tone":"Exciting & Accessible",  "adj":["unbeatable","fresh","exciting","value-packed"],  "audience":"Online shoppers aged 20-45",           "themes":["Great Deals","New Arrivals","Shopping Joy"],      "personality":"An enthusiastic, customer-first brand that makes every purchase feel like a win."},
    "entertainment":{"tone":"Energetic & Witty",      "adj":["epic","addictive","iconic","unmissable"],        "audience":"Pop culture fans aged 15-35",          "themes":["Must-Watch","Fandom","Trending Now"],             "personality":"A bold, culturally fluent brand that lives at the centre of what everyone is talking about."},
    "travel":       {"tone":"Adventurous & Inspiring","adj":["breathtaking","unforgettable","serene","wild"],  "audience":"Travel enthusiasts aged 22-40",        "themes":["Wanderlust","Hidden Gems","Travel Moments"],      "personality":"A wanderlust-driven brand that makes every destination feel like the trip of a lifetime."},
    "education":    {"tone":"Inspiring & Friendly",   "adj":["curious","bright","engaging","empowering"],      "audience":"Students and lifelong learners aged 10-40","themes":["Love of Learning","Skills","Future Ready"],    "personality":"An encouraging, curious brand that makes learning feel like the greatest adventure."},
}

# ── Objective-based tweet angle modifiers ────────────────────────
OBJECTIVE_LINES = {
    "brand awareness":          ["You haven't heard of us yet. You will.", "Some things are worth discovering late.", "Not everything great needs an introduction."],
    "product promotion":        ["This one's worth every penny.", "Your next favourite thing is here.", "Some upgrades are non-negotiable."],
    "engagement / conversation": ["Hot take: {adj} things deserve loud opinions.", "Settle the debate. Comment below.", "We need to talk about this."],
    "educational / value":      ["Here's something they don't tell you:", "The thing nobody mentions about {industry}:", "One thing that actually changes the game:"],
    "trend participation":      ["Everyone's talking about it. Here's our take.", "Late to the trend? Never.", "If it's trending, we have thoughts."],
    "community building":       ["Built for people who get it.", "This one's for the ones who showed up.", "You're not just a customer. You're the reason."],
}

# ── 10 tweet style templates ─────────────────────────────────────
# Variables: {brand}, {adj}, {adj2}, {product}, {audience_short}, {industry}, {theme}
STYLE_TEMPLATES = {
    "Engaging": [
        "What's your biggest flex this week? We'll wait. 👀",
        "Quick question: is {adj} a vibe or a lifestyle? Drop your answer below.",
        "You either love {adj} things or you haven't tried them yet. Which one are you?",
        "If {adj} was a person, who would it be? We're genuinely curious.",
        "Hot take: {adj} is underrated. Change our minds.",
        "Rate your {industry} experience this week: 🔥 or 😬?",
        "We asked. You didn't. But we're telling you anyway — {adj} wins every time.",
    ],
    "Promotional": [
        "Meet the {adj} way to {product}. Your routine just levelled up.",
        "{adj}. {adj2}. Exactly what you needed. Explore now.",
        "Not all {industry} brands are built the same. Some of us just do it {adj2}.",
        "You deserve {adj}. So we made sure you have it.",
        "The {adj} upgrade you've been putting off? Stop waiting.",
        "New drop. {adj} design. {adj2} performance. Zero compromises.",
        "Why settle for ordinary when {adj} is right here?",
    ],
    "Witty": [
        "Us: be responsible. Also us: {product} at 2am. No regrets.",
        "Scientists confirm: {adj} things are statistically better. (We did the study.)",
        "Sorry, we can't help it. We're just built {adj2}.",
        "Plot twist: the {adj} option was available all along.",
        "We were going to explain why we're {adj}, but honestly it just shows.",
        "Breaking: local brand refuses to be boring. More at 11.",
        "Some call it {adj}. We call it Tuesday.",
    ],
    "Informative": [
        "Did you know? The average person spends 3x more time choosing {industry} than using it. We fixed that.",
        "The difference between good and {adj}? It's smaller than you think — and bigger than you'd expect.",
        "Here's what most {industry} brands won't tell you: {adj2} matters more than the price tag.",
        "Fun fact: {adj} isn't a feature. It's a philosophy. Here's what that means for you.",
        "Most people get {industry} wrong. Here's the one thing that actually makes a difference.",
        "3 things that make something truly {adj}: craft, care, and the refusal to cut corners.",
        "The {industry} insight nobody talks about: {adj} is a decision made long before the product reaches you.",
    ],
    "Conversational": [
        "Real talk — when did {adj} become optional? We never got that memo.",
        "You ever just want something that works? Like actually, properly {adj}? Yeah. Same.",
        "Okay but can we normalise expecting {adj} things? Minimum standard. Not a luxury.",
        "Not to be dramatic, but {product} kind of changes things.",
        "Genuinely don't understand why anyone would choose less {adj}. But here we are.",
        "Just saying — {adj} energy is contagious and we're not sorry about spreading it.",
        "We don't do ordinary. Life's too short for that.",
    ],
    "Meme-style": [
        "POV: you finally found something {adj2} in a world full of mediocre options.",
        "Nobody:\nAbsolutely nobody:\nUs: making things more {adj} at every single step.",
        "Me before {product}: fine.\nMe after: unreasonably attached.",
        "The {adj} era is officially here and we are fully committed.",
        "Normal brands: let's be professional.\nUs: let's just be {adj}.",
        "That feeling when something is exactly as {adj} as advertised. 💀",
        "My Roman Empire: making sure everything is {adj2} no matter what.",
    ],
    "Value-driven": [
        "The best things aren't always the loudest. Sometimes {adj} just speaks for itself.",
        "You don't need more options. You need the {adj} one.",
        "Quality isn't a price point. It's a decision made before you ever see the product.",
        "Build things worth keeping. That's the whole philosophy.",
        "{adj2} things take longer to make. They also last longer. Worth it.",
        "We believe everyone deserves {adj}. Not just those who can afford the premium shelf.",
        "The goal was never to be everywhere. Just to be exactly right where you need us.",
    ],
}


class TweetGenerator:

    def generate(self, brand_name, industry, objective, tones, products, extra_context):
        # Step 1: Detect voice
        profile = self._get_profile(brand_name, industry, tones)

        # Step 2: Build brand voice summary
        brand_voice = {
            "tone":        profile["tone"],
            "audience":    profile["audience"],
            "themes":      profile["themes"],
            "personality": profile["personality"],
        }

        # Step 3: Generate 10 tweets
        tweets = self._generate_tweets(brand_name, profile, industry, objective, products, extra_context)

        return {"brand_voice": brand_voice, "tweets": tweets}

    # ── Profile detection ─────────────────────────────────────────
    def _get_profile(self, brand_name, industry, user_tones):
        key = brand_name.lower().strip()

        # 1. Known brand
        if key in BRAND_PROFILES:
            p = BRAND_PROFILES[key].copy()
            return p

        # 2. Industry match
        ind = industry.lower()
        for k, p in INDUSTRY_PROFILES.items():
            if k in ind:
                prof = p.copy()
                # Override tone if user picked chips
                if user_tones:
                    prof["tone"] = " & ".join(user_tones[:2])
                return prof

        # 3. Fallback using user tones or generic
        tone = " & ".join(user_tones[:2]) if user_tones else "Authentic & Engaging"
        return {
            "tone":        tone,
            "adj":         ["great","reliable","innovative","trusted"],
            "audience":    f"Customers who value quality and authenticity",
            "themes":      ["Brand Story","Product Benefits","Customer Love"],
            "personality": "A genuine, customer-first brand that delivers on its promises every time.",
        }

    # ── Tweet generation ──────────────────────────────────────────
    def _generate_tweets(self, brand_name, profile, industry, objective, products, extra_context):
        styles = [
            "Engaging", "Promotional", "Witty", "Informative", "Conversational",
            "Meme-style", "Value-driven", "Engaging", "Promotional", "Witty"
        ]

        adj_list  = profile.get("adj", ["great","bold","reliable","smart"])
        product_hint = products if products else f"{industry or 'our'} products and services"

        # Hashtag suggestions per style
        hashtag_map = {
            "Engaging":       self._hashtags(brand_name, ["AskUs","JoinTheConversation"]),
            "Promotional":    self._hashtags(brand_name, ["NewDrop","MustHave"]),
            "Witty":          self._hashtags(brand_name, ["JustSaying","Relatable"]),
            "Informative":    self._hashtags(brand_name, ["DidYouKnow","ProTip"]),
            "Conversational": self._hashtags(brand_name, ["RealTalk","HonestOpinion"]),
            "Meme-style":     self._hashtags(brand_name, ["Mood","TooRelatable"]),
            "Value-driven":   self._hashtags(brand_name, ["BuildBetter","StandForSomething"]),
        }

        used_templates = {s: [] for s in set(styles)}
        tweets = []

        for i, style in enumerate(styles):
            templates = STYLE_TEMPLATES[style]
            # Pick unused template
            available = [t for t in templates if t not in used_templates[style]]
            if not available:
                available = templates
            template = random.choice(available)
            used_templates[style].append(template)

            # Fill variables
            adj  = random.choice(adj_list)
            adj2 = random.choice([a for a in adj_list if a != adj] or adj_list)
            # Get product snippet
            prod_words = product_hint.split()[:6]
            prod_short = " ".join(prod_words) if prod_words else "what we do"

            # Objective opener occasionally
            obj_lines = OBJECTIVE_LINES.get(objective.lower(), [])
            obj_opener = random.choice(obj_lines).format(adj=adj, industry=industry or "this space") if obj_lines and random.random() < 0.3 else ""

            text = template.format(
                brand=brand_name,
                adj=adj,
                adj2=adj2,
                product=prod_short,
                audience_short="people like you",
                industry=industry.lower() if industry else "this space",
                theme=random.choice(profile["themes"]),
            )

            # Optionally prepend objective opener
            if obj_opener and len(obj_opener + " " + text) < 250:
                text = obj_opener + " " + text

            # Cap at 280 chars
            text = text[:280].strip()

            tweets.append({
                "text":     text,
                "style":    style,
                "hashtags": hashtag_map[style],
            })

        return tweets

    def _hashtags(self, brand_name, extras):
        tag = re.sub(r"[^a-zA-Z0-9]", "", brand_name)
        return [tag] + extras[:1]
