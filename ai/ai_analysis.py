import cv2
import mediapipe as mp
from google import genai
import os

# ==========================================
# GEMINI SETUP
# ==========================================

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ==========================================
# MEDIAPIPE SETUP
# ==========================================

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=r"C:\Users\DELL\Documents\fasion_ai\pose_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE
)


# ==========================================
# LOAD IMAGE
# ==========================================

image = cv2.imread("test_image.png")

if image is None:
    print("Image not found!")
    exit()

print("Image loaded successfully!")


# ==========================================
# CONVERT IMAGE TO RGB
# ==========================================

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

mp_image = mp.Image(
    image_format=mp.ImageFormat.SRGB,
    data=rgb_image
)


# ==========================================
# BODY LANDMARK DETECTION
# ==========================================

with PoseLandmarker.create_from_options(options) as landmarker:

    result = landmarker.detect(mp_image)

    if result.pose_landmarks:

        print("Body detected successfully!")

        landmarks = result.pose_landmarks[0]

        print("Number of landmarks:", len(landmarks))

        # Body landmarks
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
            left_shoulder.x - right_shoulder.x
        )

        hip_width = abs(
            left_hip.x - right_hip.x
        )

        if hip_width == 0:
            print("Unable to calculate body ratio.")
            exit()

        shoulder_hip_ratio = shoulder_width / hip_width

        shoulder_y = (
            left_shoulder.y + right_shoulder.y
        ) / 2

        hip_y = (
            left_hip.y + right_hip.y
        ) / 2

        ankle_y = (
            left_ankle.y + right_ankle.y
        ) / 2

        torso_length = abs(shoulder_y - hip_y)

        leg_length = abs(hip_y - ankle_y)


        # ==========================================
        # DISPLAY MEASUREMENTS
        # ==========================================

        print("\n========== BODY ANALYSIS ==========")

        print("Shoulder width:", shoulder_width)
        print("Hip width:", hip_width)
        print("Shoulder-to-hip ratio:", shoulder_hip_ratio)
        print("Torso length:", torso_length)
        print("Leg length:", leg_length)


        # ==========================================
        # DETERMINE BODY SHAPE
        # ==========================================

        if shoulder_hip_ratio > 1.15:
            body_shape = "Inverted Triangle"

        elif shoulder_hip_ratio < 0.85:
            body_shape = "Pear"

        else:
            # Compare torso and leg proportions
            if abs(torso_length - leg_length) < 0.15:
                body_shape = "Rectangle"

            else:
                body_shape = "Balanced"


        print("Body shape:", body_shape)


        # ==========================================
        # SEND RESULT TO GEMINI
        # ==========================================

        prompt = f"""
You are a professional fashion stylist.

A body-analysis system detected the following information:

Body shape: {body_shape}
Shoulder width: {shoulder_width:.3f}
Hip width: {hip_width:.3f}
Shoulder-to-hip ratio: {shoulder_hip_ratio:.3f}
Torso length: {torso_length:.3f}
Leg length: {leg_length:.3f}

Based on this information, provide simple and practical fashion recommendations.

Give recommendations for:

1. Suitable tops
2. Suitable bottoms
3. Suitable dresses
4. Suitable colors
5. Suitable outfit combinations
6. Styles that may be less flattering

Keep the answer clear and beginner-friendly.
"""


        print("\n========== GEMINI FASHION RECOMMENDATIONS ==========")

        response = client.models.generate_content(
            model="models/gemini-3.6-flash",
            contents=prompt
        )

        print(response.text)


    else:

        print("No body detected.")