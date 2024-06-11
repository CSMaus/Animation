import json
import numpy as np

video_name = 'First-combo-side1.mkv'

with open(f'{video_name}-keypoints_3d.json', 'r') as f:
    keypoints_data = json.load(f)

# Mapping of MediaPipe keypoints to BVH joints
mediapipe_bvh_mapping = {
    'Hips': 0,
    'Spine': 11,
    'Spine1': 12,
    'Neck': 0,
    'Head': 0,
    'LeftShoulder': 11,
    'LeftArm': 13,
    'LeftForeArm': 15,
    'LeftHand': 17,
    'RightShoulder': 12,
    'RightArm': 14,
    'RightForeArm': 16,
    'RightHand': 18,
    'LeftUpLeg': 23,
    'LeftLeg': 25,
    'LeftFoot': 27,
    'RightUpLeg': 24,
    'RightLeg': 26,
    'RightFoot': 28
}

# BVH skeleton structure
skeleton = {
    'Hips': {
        'Spine': {
            'Spine1': {
                'Neck': {
                    'Head': {}
                },
                'LeftShoulder': {
                    'LeftArm': {
                        'LeftForeArm': {
                            'LeftHand': {}
                        }
                    }
                },
                'RightShoulder': {
                    'RightArm': {
                        'RightForeArm': {
                            'RightHand': {}
                        }
                    }
                }
            }
        },
        'LeftUpLeg': {
            'LeftLeg': {
                'LeftFoot': {}
            }
        },
        'RightUpLeg': {
            'RightLeg': {
                'RightFoot': {}
            }
        }
    }
}


# Create a BVH string
def create_bvh_string(skeleton, keypoints_data, mapping):
    bvh_string = "HIERARCHY\n"
    bvh_string += create_hierarchy_string(skeleton, "ROOT", "Hips", indent="")
    bvh_string += "MOTION\n"
    bvh_string += f"Frames: {len(keypoints_data)}\n"
    bvh_string += "Frame Time: 0.0333333\n"  # 30 FPS
    bvh_string += create_motion_string(keypoints_data, mapping)
    return bvh_string


def create_hierarchy_string(skeleton, node_type, node_name, indent):
    hierarchy_string = f"{indent}{node_type} {node_name}\n"
    hierarchy_string += f"{indent}{{\n"
    hierarchy_string += f"{indent}\tOFFSET 0.00 0.00 0.00\n"
    if node_type == "ROOT":
        hierarchy_string += f"{indent}\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n"
    else:
        hierarchy_string += f"{indent}\tCHANNELS 3 Zrotation Xrotation Yrotation\n"

    for child_name, child_skeleton in skeleton.get(node_name, {}).items():
        hierarchy_string += create_hierarchy_string(skeleton, "JOINT", child_name, indent + "\t")

    hierarchy_string += f"{indent}\tEnd Site\n"
    hierarchy_string += f"{indent}\t{{\n"
    hierarchy_string += f"{indent}\t\tOFFSET 0.00 0.00 0.00\n"
    hierarchy_string += f"{indent}\t}}\n"
    hierarchy_string += f"{indent}}}\n"
    return hierarchy_string


def create_motion_string(keypoints_data, mapping):
    motion_string = ""
    for frame in keypoints_data:
        frame_data = []
        for joint_name, joint_index in mapping.items():
            if joint_index < len(frame):
                joint = frame[joint_index]
                if joint_name == 'Hips':
                    frame_data.extend([joint['x'], joint['y'], joint['z'], 0.0, 0.0, 0.0])
                else:
                    frame_data.extend([0.0, 0.0, 0.0])  # Simplified: no rotation data for now
        motion_string += " ".join(map(str, frame_data)) + "\n"
    return motion_string


bvh_string = create_bvh_string(skeleton, keypoints_data, mediapipe_bvh_mapping)

with open(f'test-{video_name[:-4]}.bvh', 'w') as f:
    f.write(bvh_string)

print(f"BVH file saved as test-{video_name[:-4]}.bvh")
