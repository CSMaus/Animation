import cv2
import mediapipe as mp
import random


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

image = cv2.imread('test.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = pose.process(image_rgb)

if results.pose_landmarks:
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    for landmark in results.pose_landmarks.landmark:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.putText(image, f'Z: {landmark.z:.2f}', (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)


cv2.imshow('Pose', image)
cv2.waitKey(0)
# cv2.destroyAllWindows()
