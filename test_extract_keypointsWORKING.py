import cv2
import mediapipe as mp
import json
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

video_name = 'swordStrike1.mkv'
video_path = f'MainCombo/{video_name}'
output_dir = 'swordStrike1/'
frame_step = 1

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cap = cv2.VideoCapture(video_path)
frame_id = 0
file_id = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    if frame_id % frame_step == 0:
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            keypoints = []
            for landmark in results.pose_landmarks.landmark:
                keypoints.extend([landmark.x * frame.shape[1], landmark.y * frame.shape[0], 0.95])

            frame_data = {
                "version": 1.2,
                "people": [{
                    "pose_keypoints_2d": keypoints,
                    "face_keypoints_2d": [],
                    "hand_left_keypoints_2d": [],
                    "hand_right_keypoints_2d": [],
                    "pose_keypoints_3d": [],
                    "face_keypoints_3d": [],
                    "hand_left_keypoints_3d": [],
                    "hand_right_keypoints_3d": []
                }]
            }

            with open(os.path.join(output_dir, f'frame_{file_id:04d}_combo11.json'), 'w') as f:
                json.dump(frame_data, f)
            file_id += 1

    frame_id += 1

cap.release()

print(f"Keypoints extraction completed and saved to {output_dir}")
