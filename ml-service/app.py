#!/usr/bin/env python3
import os
import tempfile
import traceback
import logging

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import joblib
import numpy as np

# -----------------------
# Config
# -----------------------
APP_HOST = "0.0.0.0"
APP_PORT = int(os.environ.get("PORT", 5000))
MODEL_DIR = os.environ.get("MODEL_DIR", "./models")
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./uploads")
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", 8))  # limit upload size
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"}

# Optional: path to tesseract binary (set if tesseract isn't in PATH)
TESSERACT_CMD = os.environ.get("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# -----------------------
# App init
# -----------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Optional CORS for frontend testing (set env FLASK_CORS=1)
if os.environ.get("FLASK_CORS") == "1":
    try:
        from flask_cors import CORS
        CORS(app)
    except Exception:
        logging.warning("flask_cors not installed; skipping CORS setup")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# -----------------------
# Helpers
# -----------------------
def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXT

def load_model(name: str):
    path = os.path.join(MODEL_DIR, f"{name}_model.joblib")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)

def predict_prob_or_score(model, X: np.ndarray) -> float:
    """Return probability between 0-1 if available, else predicted class as 0/1."""
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0][1]
        return float(prob)
    # fallback: use predict (0 or 1)
    pred = model.predict(X)[0]
    return float(pred)

# -----------------------
# Routes
# -----------------------
@app.route("/ocr", methods=["POST"])
def ocr():
    """OCR endpoint - accepts form-data with 'image' file."""
    if "image" not in request.files:
        return jsonify({"error": "no image uploaded"}), 400

    f = request.files["image"]
    filename = secure_filename(f.filename or "upload.png")
    if not allowed_file(filename):
        return jsonify({"error": "unsupported file type"}), 400

    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
        f.save(tmp.name)
        tmp.close()

        # Open and optionally preprocess the image
        img = Image.open(tmp.name)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # OCR
        text = pytesseract.image_to_string(img)
        return jsonify({"text": text}), 200
    except Exception as e:
        logging.exception("OCR error")
        return jsonify({"error": str(e)}), 500
    finally:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    """Predict diabetes risk. Expects JSON body with age,bmi,sugar,bp (numbers)."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        age = float(data.get("age", 40))
        bmi = float(data.get("bmi", 25))
        sugar = float(data.get("sugar", 110))
        bp = float(data.get("bp", 120))

        X = np.array([[age, bmi, sugar, bp]])
        model = load_model("diabetes")
        score = predict_prob_or_score(model, X)
        return jsonify({"score": score}), 200
    except FileNotFoundError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.exception("Diabetes prediction error")
        return jsonify({"error": str(e)}), 500

@app.route("/predict/cardiac", methods=["POST"])
def predict_cardiac():
    """Predict cardiac risk. Expects JSON body with age,chol,bp,smoker."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        age = float(data.get("age", 50))
        chol = float(data.get("chol", 200))
        bp = float(data.get("bp", 130))
        smoker = float(data.get("smoker", 0))

        X = np.array([[age, chol, bp, smoker]])
        model = load_model("cardiac")
        score = predict_prob_or_score(model, X)
        return jsonify({"score": score}), 200
    except FileNotFoundError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.exception("Cardiac prediction error")
        return jsonify({"error": str(e)}), 500

@app.route("/models/<path:name>", methods=["GET"])
def download_model(name):
    """Download a model file from MODEL_DIR (debug use only)."""
    try:
        p = os.path.join(MODEL_DIR, name)
        if not os.path.exists(p):
            return jsonify({"error": "not found"}), 404
        return send_file(p, as_attachment=True)
    except Exception as e:
        logging.exception("Model download error")
        return jsonify({"error": str(e)}), 500

# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    logging.info(f"Starting app on {APP_HOST}:{APP_PORT} (models: {MODEL_DIR}, uploads: {UPLOAD_DIR})")
    app.run(host=APP_HOST, port=APP_PORT, debug=os.environ.get("FLASK_DEBUG") == "1")
