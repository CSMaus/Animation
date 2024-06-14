import cv2
import mediapipe as mp
import mss
import numpy as np

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

monitor_index = 2

with mss.mss() as sct:
    monitor = sct.monitors[monitor_index]
    monitor_dimensions = {
        "top": monitor["top"],
        "left": monitor["left"],
        "width": monitor["width"],
        "height": monitor["height"],
        "mon": monitor_index,
    }

cv2.namedWindow('Pose and Hands', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Pose and Hands', 900, 700)

while True:
    with mss.mss() as sct:
        screen_image = sct.grab(monitor_dimensions)
        frame = np.array(screen_image)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

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
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2)
                )

        cv2.imshow('Pose and Hands', frame)
        k = cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q') or k % 256 == 27:
            break

cv2.destroyAllWindows()
