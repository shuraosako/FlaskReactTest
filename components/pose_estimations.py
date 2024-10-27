from datetime import datetime
import math
from collections import deque
from components.list.necklist.right_hand_raised import RightHandRaised
from components.list.necklist.neck_flexion import NeckFlexion  # 既存のクラスをインポート

class PoseEstimator:
    def __init__(self):
        self.keypoint_names = [
            'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
            'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
            'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
            'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
        ]
        # 各判定クラスのインスタンスを作成
        self.right_hand_raised_checker = RightHandRaised()
        self.neck_flexion_checker = NeckFlexion()  # 修正: 正しいNeckFlexionクラスのインスタンス化
        
        self.lateral_flexion_history = deque(maxlen=90)  # 首の側屈3秒間
        self.LATERAL_FLEXION_DURATION = 3  # 首の側屈
        self.rotation_history = deque(maxlen=90)  # 首の回旋3秒間
        self.ROTATION_DURATION = 3  # 首の回旋
        self.extension_history = deque(maxlen=90)  # 首の伸展3秒間
        self.EXTENSION_DURATION = 3  # 首の伸展

    #右手上げ
    def check_pose(self, organized_data, current_time):
        return self.right_hand_raised_checker.check_pose(organized_data, current_time)
    
    #首の屈曲
    def check_neck_flexion(self, keypoints):
        # 修正: assess_neck_flexion_poseメソッドを直接呼び出す
        return self.neck_flexion_checker.assess_neck_flexion_pose(keypoints)

    #首の側屈
    def check_lateral_flexion(self, keypoints, threshold_angle=15):
        return self.lateral_flexion_checker.lateral_flexion_neck(keypoints, threshold_angle)

    #首の回旋
    def check_neck_rotation(self, keypoints, threshold_angle=15):
        return self.neck_rotation_checker.neck_rotation(keypoints, threshold_angle)

    #首の伸展
    def check_neck_extension(self, keypoints, threshold_angle=15):
        return self.neck_extension_checker.neck_extension(keypoints, threshold_angle)

    def organize_skeleton_data(self, skeleton_data, timestamp):
        organized_skeleton = {
            'timestamp': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'keypoints': []
        }
        
        for i, keypoint in enumerate(skeleton_data):
            if len(keypoint) == 3:  # x, y, confidence がある場合
                organized_skeleton['keypoints'].append({
                    'name': self.keypoint_names[i],
                    'x': round(float(keypoint[0]), 2),
                    'y': round(float(keypoint[1]), 2),
                    'confidence': round(float(keypoint[2]), 2)
                })
        
        return organized_skeleton

# 姿勢推定辞書
available_poses = {
    'right_hand_raised': '右手上げる',
    'neck_flexion': '首の屈曲',
    'lateral_flexion_neck': '首の側屈',
    'neck_rotation': '首の回旋',
    'neck_extension': '首の伸展'
}