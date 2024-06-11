import os
import json

input_dir = 'D:/ML_DL_AI_stuff/!playing_stuff/openpose/output_json_folder3/'
output_dir = 'D:/ML_DL_AI_stuff/!playing_stuff/openpose/keypointstest/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

for index, filename in enumerate(sorted(json_files)):
    with open(os.path.join(input_dir, filename), 'r') as f:
        data = json.load(f)

    data['version'] = 1.2  # Change the JSON version to 1.2
    for person in data['people']:
        if 'person_id' in person:
            del person['person_id']

    new_filename = f"frame_{index:04d}_keypoints.json"
    with open(os.path.join(output_dir, new_filename), 'w') as f:
        json.dump(data, f)

print("Post-processing completed. JSON files saved to", output_dir)
