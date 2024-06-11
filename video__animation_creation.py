import cv2
import mediapipe as mp
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

video_name = 'First-combo-side1.mkv'
video_path = f'MainCombo/{video_name}'

cap = cv2.VideoCapture(video_path)

keypoints_data = []

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    frame_keypoints = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            frame_keypoints.append({
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            })
    keypoints_data.append(frame_keypoints)

cap.release()

with open(f'{video_name}-keypoints_3d.json', 'w') as f:
    json.dump(keypoints_data, f)

print(f"Keypoints extraction completed and saved to {video_name}-keypoints_3d.json")
