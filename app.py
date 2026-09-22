import json
import os
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

CATEGORIES = [
    "organic / wet waste",
    "paper or cardboard",
    "plastic",
    "glass",
    "metal",
    "e-waste",
    "battery",
    "hazardous / medical waste",
]

CATEGORY_META = {
    "organic / wet waste": {
        "emoji": "🥬",
        "title": "Organic / Wet Waste",
        "bin": "Wet/organic waste stream",
        "tip": "Keep food scraps separate from dry recyclables and avoid mixing plastic with organic waste.",
    },
    "paper or cardboard": {
        "emoji": "📦",
        "title": "Paper / Cardboard",
        "bin": "Dry/recyclable waste stream",
        "tip": "Keep paper clean and dry. Flatten cardboard to save space.",
    },
    "plastic": {
        "emoji": "🧴",
        "title": "Plastic",
        "bin": "Dry/recyclable waste stream where accepted",
        "tip": "Empty and rinse containers when practical, and avoid contaminating recyclable material with food.",
    },
    "glass": {
        "emoji": "🍾",
        "title": "Glass",
        "bin": "Glass/recyclable stream where available",
        "tip": "Handle broken glass carefully and follow local collection rules.",
    },
    "metal": {
        "emoji": "🥫",
        "title": "Metal",
        "bin": "Dry/recyclable waste stream where accepted",
        "tip": "Empty cans and containers before placing them in the recyclable stream.",
    },
    "e-waste": {
        "emoji": "💻",
        "title": "E-waste",
        "bin": "Authorized e-waste collection/recycling point",
        "tip": "Do not place electronics in ordinary household waste. Use an authorized collection channel.",
    },
    "battery": {
        "emoji": "🔋",
        "title": "Battery",
        "bin": "Battery/e-waste collection point",
        "tip": "Keep batteries out of regular bins and avoid damaging or short-circuiting them.",
    },
    "hazardous / medical waste": {
        "emoji": "⚠️",
        "title": "Hazardous / Medical",
        "bin": "Authorized hazardous/medical waste collection channel",
        "tip": "Do not mix hazardous materials with normal household waste. Follow local authority instructions.",
    },
}

@st.cache_resource(show_spinner=False)
def load_clip():
    """Load a CLIP zero-shot image classifier on first use."""
    try:
        from transformers import pipeline
        return pipeline(
            "zero-shot-image-classification",
            model="openai/clip-vit-base-patch32"
        )
    except Exception as exc:
        return exc

@st.cache_data
def load_kb():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def retrieve_guidance(category, query):
    """Lightweight retrieval layer over the local sustainability knowledge base."""
    kb = load_kb()
    text = f"{category} {query}".lower()
    scored = []
    for item in kb:
        corpus = " ".join([
            item["category"],
            item["title"],
            item["guidance"],
            " ".join(item.get("keywords", []))
        ]).lower()
        score = sum(1 for token in set(text.split()) if len(token) > 2 and token in corpus)
        if item["category"].lower() == category.lower():
            score += 5
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored[:3]]

def classify_image(image):
    classifier = load_clip()
    if isinstance(classifier, Exception):
        return None, f"Model could not be loaded: {classifier}"

    prompts = [
        "a photo of organic food waste",
        "a photo of paper or cardboard waste",
        "a photo of plastic waste",
        "a photo of glass waste",
        "a photo of metal waste",
        "a photo of electronic waste",
        "a photo of a battery",
        "a photo of hazardous or medical waste",
    ]

    labels = [
        "organic / wet waste",
        "paper or cardboard",
        "plastic",
        "glass",
        "metal",
        "e-waste",
        "battery",
        "hazardous / medical waste",
    ]

    results = classifier(image, candidate_labels=prompts)
    # transformers returns labels based on candidate prompts
    top = results[0]
    prompt_to_label = dict(zip(prompts, labels))
    category = prompt_to_label.get(top["label"], "plastic")
    confidence = float(top["score"])
    return category, confidence

def generate_ai_guidance(category, retrieved):
    """Optional Gemini generation. Retrieval results are always shown as the evidence layer."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        evidence = "\n".join(
            f"- {x['title']}: {x['guidance']}" for x in retrieved
        )
        prompt = f"""
You are EcoSort AI, a sustainability assistant.
Waste category: {category}
Retrieved local knowledge:
{evidence}

Give concise disposal guidance in 3 bullet points.
Do not invent collection rules. If local rules are unknown, say so.
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception:
        return None

st.title("♻️ EcoSort AI")
st.caption("AI-powered waste identification and disposal assistant | 1M1B AI for Sustainability")

with st.sidebar:
    st.header("How it works")
    st.markdown("""
1. Upload a waste-item image.
2. Computer vision predicts a category.
3. Retrieval finds relevant disposal guidance.
4. Optional generative AI summarizes the guidance.
5. The result includes a sustainability tip.
""")
    st.divider()
    st.info("Prototype note: image classification is a zero-shot CLIP demonstration. Local waste rules can differ, so users should verify official municipal guidance before disposal.")

col1, col2 = st.columns([1, 1.2])

with col1:
    uploaded = st.file_uploader(
        "Upload a waste-item image",
        type=["jpg", "jpeg", "png", "webp"]
    )
    st.markdown("**Supported prototype categories:**")
    st.write(", ".join(CATEGORY_META.keys()))

with col2:
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded item", use_container_width=True)

        if st.button("🔍 Analyze Waste", type="primary", use_container_width=True):
            with st.spinner("Analyzing image with computer vision..."):
                category, confidence = classify_image(image)

            if category is None:
                st.error(confidence)
                st.warning("Install the dependencies and allow the CLIP model to download on first run.")
            else:
                meta = CATEGORY_META[category]
                retrieved = retrieve_guidance(category, category)
                generated = generate_ai_guidance(category, retrieved)

                st.success(f"{meta['emoji']} Predicted category: **{meta['title']}**")
                st.metric("Model confidence", f"{confidence * 100:.1f}%")

                st.subheader("Disposal guidance")
                st.write(f"**Recommended stream:** {meta['bin']}")
                st.write(meta["tip"])

                if generated:
                    st.subheader("AI-assisted explanation")
                    st.write(generated)

                st.subheader("Retrieved sustainability knowledge")
                for item in retrieved:
                    with st.expander(item["title"]):
                        st.write(item["guidance"])
                        st.caption("Keywords: " + ", ".join(item.get("keywords", [])))

                st.caption("Prototype limitation: CLIP is a general-purpose vision-language model and is not a substitute for a validated municipal waste-classification system.")

st.divider()
st.subheader("Project impact")
a, b, c = st.columns(3)
a.metric("Primary SDG", "SDG 12")
b.metric("AI component", "Computer Vision")
c.metric("Guidance layer", "Retrieval + optional GenAI")
