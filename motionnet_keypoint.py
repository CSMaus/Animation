import json

mediapipe_keypoints_file = 'First-combo-side1-keypoints_2d.json'
motionnet_keypoints_file = 'motionnet_input_keypoints.json'

with open(mediapipe_keypoints_file, 'r') as f:
    mediapipe_keypoints = json.load(f)

motionnet_keypoints = []

for frame in mediapipe_keypoints:
    frame_data = []
    for keypoint in frame['keypoints']:
        frame_data.append([keypoint['x'], keypoint['y'], keypoint['visibility']])
    motionnet_keypoints.append(frame_data)

with open(motionnet_keypoints_file, 'w') as f:
    json.dump(motionnet_keypoints, f)

print(f"Keypoints converted and saved to {motionnet_keypoints_file}")
