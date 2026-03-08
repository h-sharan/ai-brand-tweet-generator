"""
app.py — Flask Backend (No API Key Required)
"""
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from generator import TweetGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
gen = TweetGenerator()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "rule-based + template engine"})

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    brand_name = data.get("brand_name", "").strip()
    if not brand_name:
        return jsonify({"error": "brand_name is required"}), 400
    try:
        result = gen.generate(
            brand_name    = brand_name,
            industry      = data.get("industry", ""),
            objective     = data.get("objective", "Brand Awareness"),
            tones         = data.get("tones", []),
            products      = data.get("products", ""),
            extra_context = data.get("extra_context", ""),
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
