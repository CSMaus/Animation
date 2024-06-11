import cv2
import mediapipe as mp
import random

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(image_rgb)
    hand_results = hands.process(image_rgb)

    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),  # Green color for landmarks
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)  # Green color for connections
            )
    cv2.imshow('Pose and Hands', frame)
    k = cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q') or k % 256 == 27:
        break

cap.release()
cv2.destroyAllWindows()
