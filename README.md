# EcoSort AI – Intelligent Waste Segregation and Disposal Assistant

**1M1B AI for Sustainability Virtual Internship – Final Project**

## 1. Problem
People often struggle to identify the correct waste stream for everyday items. Incorrect segregation can contaminate recyclables and increase waste-management challenges.

## 2. Solution
EcoSort AI is a Streamlit prototype that:
- accepts an image of a waste item;
- uses a CLIP vision-language model for zero-shot image classification;
- maps the prediction to a waste category;
- retrieves disposal guidance from a local sustainability knowledge base;
- optionally uses Gemini to summarize retrieved guidance;
- displays a sustainability tip and a model-confidence value.

## 3. SDGs
Primary: **SDG 12 – Responsible Consumption and Production**

Secondary relevance:
- **SDG 11 – Sustainable Cities and Communities**
- **SDG 13 – Climate Action**

Only select SDGs in the submission form that you can explain and defend.

## 4. AI architecture

User image
→ Streamlit interface
→ CLIP zero-shot computer vision
→ Waste category
→ Retrieval layer over `data/knowledge_base.json`
→ Optional Gemini generation
→ Disposal guidance + sustainability tip

## 5. Run locally

### Windows
```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The first analysis may download the CLIP model from Hugging Face, so internet access is required once.

## 6. Optional Gemini integration

Set an environment variable before starting Streamlit.

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
streamlit run app.py
```

Linux/macOS:
```bash
export GEMINI_API_KEY="YOUR_KEY"
streamlit run app.py
```

If no key is provided, the application still works with the computer-vision prediction and retrieval-based guidance.

## 7. Important limitation
This is a student prototype, not a certified municipal waste classifier. CLIP is a general-purpose vision-language model, so predictions can be wrong for visually ambiguous items. Local disposal rules vary by municipality. The project therefore presents guidance as recommendations and tells users to verify local official rules.

## 8. Suggested demo
1. Start the app.
2. Upload a clear image of a plastic bottle.
3. Click **Analyze Waste**.
4. Show the predicted category, confidence, disposal stream, retrieved guidance and sustainability tip.
5. Repeat with a cardboard box and an electronic item.
6. Explain the architecture and limitations honestly.

## 9. Suggested GitHub structure
```text
EcoSort-AI/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── knowledge_base.json
└── assets/
    ├── architecture.png
    └── demo_preview.png
```
