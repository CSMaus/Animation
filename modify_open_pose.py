import os
import json

input_dir = 'D:/ML_DL_AI_stuff/!playing_stuff/openpose/output_json_folder3/'
output_dir = 'D:/ML_DL_AI_stuff/!playing_stuff/openpose/output_json_folder3_modified/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        with open(os.path.join(input_dir, filename), 'r') as f:
            data = json.load(f)

        for person in data['people']:
            if 'person_id' in person:
                del person['person_id']

        with open(os.path.join(output_dir, filename), 'w') as f:
            json.dump(data, f)

print("Post-processing completed. JSON files saved to", output_dir)
