import math
from collections import deque

class NeckFlexion:
    def __init__(self, time_window=5):
        self.flexion_history = deque(maxlen=time_window)

    def neck_flexion(self, keypoints, tolerance=0.1):
        # 必要なキーポイントを取得
        nose = next((kp for kp in keypoints if kp['name'] == 'nose'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)
        left_hip = next((kp for kp in keypoints if kp['name'] == 'left_hip'), None)
        right_hip = next((kp for kp in keypoints if kp['name'] == 'right_hip'), None)
        
        # キーポイントが検出されていない場合はFalseを返す
        if not all([nose, left_shoulder, right_shoulder, left_hip, right_hip]):
            return False

        # 肩の中点を計算
        shoulder_midpoint = {
            'x': (left_shoulder['x'] + right_shoulder['x']) / 2,
            'y': (left_shoulder['y'] + right_shoulder['y']) / 2
        }

        # 腰の中点を計算
        hip_midpoint = {
            'x': (left_hip['x'] + right_hip['x']) / 2,
            'y': (left_hip['y'] + right_hip['y']) / 2
        }

        # 肩幅を計算（スケール調整のため）
        shoulder_width = abs(left_shoulder['x'] - right_shoulder['x'])

        # 鼻と肩の中点の垂直距離を計算
        nose_to_shoulder_y = abs(nose['y'] - shoulder_midpoint['y'])

        # 背中の傾きを計算
        back_angle = math.atan2(shoulder_midpoint['y'] - hip_midpoint['y'], 
                                shoulder_midpoint['x'] - hip_midpoint['x'])
        back_angle_degrees = math.degrees(back_angle)

        # 首の屈曲を判定
        neck_flexed = nose_to_shoulder_y <= tolerance * shoulder_width

        # 背中がまっすぐかどうかを判定（許容範囲は±15度）
        back_straight = abs(back_angle_degrees - 90) <= 15

        # 時系列データを使用した判定
        self.flexion_history.append(neck_flexed and back_straight)
        
        # time_window内のフレームの半分以上でTrue判定された場合にTrueを返す
        return sum(self.flexion_history) > len(self.flexion_history) / 2

    def validate_pose(self, keypoints, tolerance):
        # 両手が腰に当たっているかを確認
        left_wrist = next((kp for kp in keypoints if kp['name'] == 'left_wrist'), None)
        right_wrist = next((kp for kp in keypoints if kp['name'] == 'right_wrist'), None)
        left_hip = next((kp for kp in keypoints if kp['name'] == 'left_hip'), None)
        right_hip = next((kp for kp in keypoints if kp['name'] == 'right_hip'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)

        if all([left_wrist, right_wrist, left_hip, right_hip, left_shoulder, right_shoulder]):
            shoulder_width = abs(left_shoulder['x'] - right_shoulder['x'])
            left_hand_on_hip = abs(left_wrist['y'] - left_hip['y']) < tolerance * shoulder_width
            right_hand_on_hip = abs(right_wrist['y'] - right_hip['y']) < tolerance * shoulder_width
            return left_hand_on_hip and right_hand_on_hip
        return False

    def assess_neck_flexion_pose(self, keypoints, tolerance=0.1):
        return self.neck_flexion(keypoints, tolerance) and self.validate_pose(keypoints, tolerance)