import json
import numpy as np
from bvh import Bvh, BvhNode

video_name = 'First-combo-side1.mkv'

with open(f'{video_name}-keypoints_3d.json', 'r') as f:
    keypoints_data = json.load(f)

# simple BVH structure
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
def create_bvh_string(skeleton, keypoints_data):
    bvh_string = "HIERARCHY\n"
    bvh_string += create_hierarchy_string(skeleton, "ROOT", "Hips", indent="")
    bvh_string += "MOTION\n"
    bvh_string += f"Frames: {len(keypoints_data)}\n"
    bvh_string += "Frame Time: 0.0333333\n"  # 30 FPS
    bvh_string += create_motion_string(keypoints_data)
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


def create_motion_string(keypoints_data):
    motion_string = ""
    for frame in keypoints_data:
        frame_data = []
        for i, joint in enumerate(frame):
            frame_data.extend([joint['x'], joint['y'], joint['z'], 0.0, 0.0, 0.0])  # Simplified example: no rotation data
        motion_string += " ".join(map(str, frame_data)) + "\n"
    return motion_string


bvh_string = create_bvh_string(skeleton, keypoints_data)


with open(f'test-{video_name[:-4]}.bvh', 'w') as f:
    f.write(bvh_string)

print(f"BVH file saved as test-{video_name[:-4]}.bvh")
