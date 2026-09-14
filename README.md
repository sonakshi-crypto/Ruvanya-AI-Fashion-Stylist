# Ruvanya-AI-Fashion-Stylist

Ruvanya is an AI-powered fashion styling project that helps users choose suitable combinations of **outfits, makeup, footwear, and accessories** for different occasions.

## Project Objective

The main objective of Ruvanya is to provide personalized fashion recommendations using Artificial Intelligence. The system analyzes the user's selected fashion items and provides styling suggestions based on compatibility, color harmony, style, and occasion.

## Key Features

*  Outfit/dress recommendations
*  Makeup style suggestions
*  Footwear matching
*  Jewelry and accessory recommendations
*  Color harmony analysis
*  Fashion compatibility/match score
*  Occasion-based styling suggestions
*  AI-powered fashion analysis

## AI Module

The current AI module uses computer vision and AI-based analysis to process fashion-related information.

Technologies currently used include:

* Python
* OpenCV
* MediaPipe
* Google Gemini API

## Technology Stack

### Frontend

* HTML/CSS/JavaScript or project-selected frontend framework

### Backend

* Python
* FastAPI/Flask (as finalized by the team)

### AI

* Python
* OpenCV
* MediaPipe
* Google GenAI

### Testing

* Postman
* Python testing

### Repository

* Git
* GitHub

## Project Structure

```text
Ruvanya-AI-Fashion-Stylist/
│
├── ai/
│   ├── ai_analysis.py
│   ├── ai_module.py
│   └── test_ai.py
│
├── models/
│   └── pose_landmarker.task
│
├── tests/
│   └── test_image.png
│
├── backend/
├── frontend/
├── dataset/
├── docs/
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository and install the required Python packages.

```bash
pip install -r requirements.txt
```

The required packages include:

```text
opencv-python
mediapipe
google-genai
```

## Project Workflow

1. User provides/selects fashion-related inputs.
2. The system processes the inputs.
3. AI analyzes the fashion combination.
4. The system evaluates style and compatibility.
5. Ruvanya provides recommendations and suggestions.

## Testing

APIs will be tested using **Postman**.

Testing will include:

* API request/response validation
* Status code checking
* Input validation
* Error handling
* AI response checking

Bugs discovered during testing will be documented and reported to the development team.

## Dataset

The project will use an organized fashion/dress dataset for AI analysis and recommendation development.

The dataset will be organized according to relevant attributes such as:

* Dress type
* Color
* Style
* Occasion
* Category

## Team Responsibilities

The project is developed collaboratively, with responsibilities divided among team members.

## Future Enhancements

Possible future features include:

* Virtual/AR try-on
* Skin tone-based recommendations
* Body-shape-based styling
* Weather-based recommendations
* Budget-based fashion suggestions
* Save favorite outfits
* Social sharing and voting

## Project Status

**Currently under development.**


## License

This project is developed for educational/project purposes.
