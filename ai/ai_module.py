import cv2
import mediapipe as mp
import os
import re
from google import genai


# ==========================================
# GEMINI SETUP
# ==========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==========================================
# MEDIAPIPE SETUP
# ==========================================

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


# ==========================================
# MAIN AI FUNCTION
# ==========================================

def analyze_fashion(image_path):

    # ==========================================
    # LOAD IMAGE
    # ==========================================

    image = cv2.imread(image_path)

    if image is None:
        return {
            "error": "Image not found"
        }

    print("Image loaded successfully!")


    # ==========================================
    # CONVERT IMAGE
    # ==========================================

    rgb_image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_image
    )


    # ==========================================
    # MEDIAPIPE OPTIONS
    # ==========================================

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path=r"C:\Users\DELL\Documents\fasion_ai\pose_landmarker.task"
        ),
        running_mode=VisionRunningMode.IMAGE
    )


    # ==========================================
    # BODY ANALYSIS
    # ==========================================

    with PoseLandmarker.create_from_options(options) as landmarker:

        result = landmarker.detect(mp_image)

        if not result.pose_landmarks:

            return {
                "error": "No body detected"
            }

        print("Body detected successfully!")

        landmarks = result.pose_landmarks[0]

        print(
            "Number of landmarks:",
            len(landmarks)
        )


        # ==========================================
        # LANDMARKS
        # ==========================================

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        left_ankle = landmarks[27]
        right_ankle = landmarks[28]


        # ==========================================
        # BODY MEASUREMENTS
        # ==========================================

        shoulder_width = abs(
            left_shoulder.x -
            right_shoulder.x
        )

        hip_width = abs(
            left_hip.x -
            right_hip.x
        )


        # Prevent division by zero
        if hip_width == 0:

            return {
                "error": "Unable to calculate body proportions"
            }


        shoulder_hip_ratio = (
            shoulder_width /
            hip_width
        )


        shoulder_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2


        hip_y = (
            left_hip.y +
            right_hip.y
        ) / 2


        ankle_y = (
            left_ankle.y +
            right_ankle.y
        ) / 2


        torso_length = abs(
            shoulder_y -
            hip_y
        )


        leg_length = abs(
            hip_y -
            ankle_y
        )


        # ==========================================
        # PRINT MEASUREMENTS
        # ==========================================

        print(
            "Shoulder width:",
            shoulder_width
        )

        print(
            "Hip width:",
            hip_width
        )

        print(
            "Shoulder-to-hip ratio:",
            shoulder_hip_ratio
        )

        print(
            "Torso length:",
            torso_length
        )

        print(
            "Leg length:",
            leg_length
        )


        # ==========================================
        # GEMINI PROMPT
        # ==========================================

        prompt = f"""
You are a fashion recommendation assistant.

Analyze these approximate body-proportion measurements:

Shoulder width: {shoulder_width:.3f}
Hip width: {hip_width:.3f}
Shoulder-to-hip ratio: {shoulder_hip_ratio:.2f}
Torso length: {torso_length:.3f}
Leg length: {leg_length:.3f}

Give practical fashion recommendations.

IMPORTANT:
Return the answer in EXACTLY these 9 sections.

1. Recommended Dress:
Give 1 or 2 suitable dress types.

2. Dress Silhouette:
Give the most suitable silhouette and a short reason.

3. Best Colors:
Give 3 to 5 suitable colors.

4. Accessories:
Suggest suitable earrings, necklace, bag, or other accessories.

5. Hairstyle:
Suggest 1 or 2 suitable hairstyles.

6. Footwear:
Suggest suitable footwear.

7. Makeup:
Give a simple makeup suggestion.

8. Styling Tips:
Give 2 or 3 short styling tips.

9. Match Score:
Give one score from 0 to 100.

RULES:
- Use exactly these 9 numbered sections.
- Do NOT write one large paragraph.
- Keep each section short.
- Do NOT add extra sections.
- Match Score must be a number from 0 to 100.
- These are approximate image-based measurements.
- Do not present body-shape classification as a definitive fact.
"""


        # ==========================================
        # GEMINI REQUEST
        # ==========================================

        print("\n========== GEMINI FASHION RECOMMENDATION ==========\n")

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        # ==========================================
        # GET GEMINI TEXT
        # ==========================================

        text = response.text


        # ==========================================
        # REMOVE UNNECESSARY MARKDOWN
        # ==========================================

        text = text.replace("**", "")


        # ==========================================
        # EXTRACT EACH SECTION
        # ==========================================

        patterns = {

            "recommended_dress":
                r"1\.\s*Recommended Dress:\s*(.*?)(?=\n\s*2\.|\Z)",

            "dress_silhouette":
                r"2\.\s*Dress Silhouette:\s*(.*?)(?=\n\s*3\.|\Z)",

            "best_colors":
                r"3\.\s*Best Colors:\s*(.*?)(?=\n\s*4\.|\Z)",

            "accessories":
                r"4\.\s*Accessories:\s*(.*?)(?=\n\s*5\.|\Z)",

            "hairstyle":
                r"5\.\s*Hairstyle:\s*(.*?)(?=\n\s*6\.|\Z)",

            "footwear":
                r"6\.\s*Footwear:\s*(.*?)(?=\n\s*7\.|\Z)",

            "makeup":
                r"7\.\s*Makeup:\s*(.*?)(?=\n\s*8\.|\Z)",

            "styling_tips":
                r"8\.\s*Styling Tips:\s*(.*?)(?=\n\s*9\.|\Z)",

            "match_score":
                r"9\.\s*Match Score:\s*(.*?)(?=\n|\Z)"
        }


        # ==========================================
        # CREATE SECTIONS DICTIONARY
        # ==========================================

        sections = {}


        for key, pattern in patterns.items():

            match = re.search(
                pattern,
                text,
                re.DOTALL |
                re.IGNORECASE
            )

            if match:

                sections[key] = (
                    match.group(1)
                    .strip()
                )

            else:

                sections[key] = ""


        # ==========================================
        # CLEAN MATCH SCORE
        # ==========================================

        match_score_text = sections["match_score"]

        score_match = re.search(
            r"\d+(?:\.\d+)?",
            match_score_text
        )

        if score_match:

            match_score = int(
                float(
                    score_match.group()
                )
            )

        else:

            match_score = None


        # ==========================================
        # FINAL RESULT
        # ==========================================

        return {

            "body_measurements": {

                "shoulder_width":
                    round(shoulder_width, 3),

                "hip_width":
                    round(hip_width, 3),

                "shoulder_hip_ratio":
                    round(shoulder_hip_ratio, 2),

                "torso_length":
                    round(torso_length, 3),

                "leg_length":
                    round(leg_length, 3)
            },


            "recommendations": {

                "recommended_dress":
                    sections["recommended_dress"],

                "dress_silhouette":
                    sections["dress_silhouette"],

                "best_colors":
                    sections["best_colors"],

                "accessories":
                    sections["accessories"],

                "hairstyle":
                    sections["hairstyle"],

                "footwear":
                    sections["footwear"],

                "makeup":
                    sections["makeup"],

                "styling_tips":
                    sections["styling_tips"],

                "match_score":
                    match_score
            }
        }


# ==========================================
# TEST DIRECTLY
# ==========================================

if __name__ == "__main__":

    result = analyze_fashion(
        "test_image.png"
    )

    print("\n")
    print("==========================================")
    print("             AI RESULT")
    print("==========================================")

    if "error" in result:

        print(
            "ERROR:",
            result["error"]
        )

    else:

        print("\nBODY MEASUREMENTS:")
        print(
            result["body_measurements"]
        )

        print("\nRECOMMENDATIONS:")

        recommendations = (
            result["recommendations"]
        )

        print(
            "\n1. Recommended Dress:"
        )
        print(
            recommendations["recommended_dress"]
        )

        print(
            "\n2. Dress Silhouette:"
        )
        print(
            recommendations["dress_silhouette"]
        )

        print(
            "\n3. Best Colors:"
        )
        print(
            recommendations["best_colors"]
        )

        print(
            "\n4. Accessories:"
        )
        print(
            recommendations["accessories"]
        )

        print(
            "\n5. Hairstyle:"
        )
        print(
            recommendations["hairstyle"]
        )

        print(
            "\n6. Footwear:"
        )
        print(
            recommendations["footwear"]
        )

        print(
            "\n7. Makeup:"
        )
        print(
            recommendations["makeup"]
        )

        print(
            "\n8. Styling Tips:"
        )
        print(
            recommendations["styling_tips"]
        )

        print(
            "\n9. Match Score:"
        )
        print(
            recommendations["match_score"],
            "/100"
        )
