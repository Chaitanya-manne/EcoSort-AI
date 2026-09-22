# EcoSort AI – Project Report

## Abstract
EcoSort AI is an AI-powered waste segregation and disposal assistant developed as a sustainability-focused student prototype. The system accepts a photograph of a waste item and uses a computer-vision zero-shot classification model to estimate its waste category. A retrieval layer then finds relevant disposal guidance from a curated local knowledge base. An optional generative-AI layer can summarize the retrieved evidence for the user. The design demonstrates how AI can support everyday waste-segregation decisions while recognizing that actual disposal rules vary by location.

## Problem Statement
Improper waste segregation is partly caused by uncertainty about how everyday objects should be classified and disposed of. A user may recognize an item but still not know whether it belongs in an organic, recyclable, e-waste, battery or hazardous stream. A simple visual assistant can reduce this information gap by giving immediate, understandable guidance.

## Objectives
1. Build an easy-to-use image-based waste classification interface.
2. Demonstrate computer vision using a pretrained vision-language model.
3. Connect predictions to retrieval-based sustainability knowledge.
4. Provide concise disposal guidance and sustainability tips.
5. Create a prototype that can later be adapted to local municipal rules.

## AI Components
### Computer Vision
CLIP is used for zero-shot image classification. Instead of training a new classifier in the internship prototype, the model compares the uploaded image with text descriptions representing waste categories.

### Retrieval
A local JSON knowledge base contains disposal guidance. The application retrieves the most relevant entries for the predicted category and displays them as supporting information.

### Generative AI
If a Gemini API key is configured, retrieved evidence is supplied to a generative model to create a concise explanation. The retrieval layer is shown separately so that the generated response is grounded in project-maintained information.

## Technology Stack
- Python
- Streamlit
- PyTorch
- Hugging Face Transformers
- CLIP
- Pillow
- JSON knowledge base
- Gemini API (optional)
- GitHub

## SDG Alignment
**SDG 12 – Responsible Consumption and Production** is the primary alignment because the project focuses on responsible handling of waste and improving segregation awareness.

The project can also be discussed in relation to SDG 11 and SDG 13, but these are secondary rather than direct measurements of impact.

## Target Users
Students, households, schools, colleges, offices, apartment communities and environmentally conscious citizens.

## Expected Impact
The prototype is intended to improve awareness and reduce uncertainty around waste segregation. A production system could measure classification volume, user corrections, recurring confusion categories and engagement over time. This prototype does not claim measured environmental impact because no field study has been conducted.

## Evaluation Plan
For a future trained model:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Per-category performance

For the application:
- Classification response time
- User correction rate
- Retrieval relevance
- Number of items analyzed
- User feedback

## Limitations
1. CLIP is a general-purpose model, not a dedicated waste classifier.
2. A photograph may not contain enough visual information to identify an item safely.
3. Waste rules differ between locations.
4. The prototype does not independently verify municipal collection schedules.
5. Environmental impact has not been measured through a controlled field study.

## Future Scope
- Fine-tune a waste-specific image classifier using a documented dataset.
- Add multilingual support.
- Add location-based municipal guidance.
- Add a user feedback loop for correcting predictions.
- Add analytics for common waste types.
- Add barcode/OCR support for packaged products.
- Deploy the application to a public cloud service.
- Build a mobile version for easier household use.

## Conclusion
EcoSort AI demonstrates a practical way to combine computer vision, retrieval and generative AI concepts for a sustainability problem. The project prioritizes transparent guidance and acknowledges model and local-rule limitations rather than presenting an experimental classifier as a certified waste-management system.
