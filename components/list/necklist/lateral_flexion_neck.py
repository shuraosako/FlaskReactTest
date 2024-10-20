import math
from collections import deque

class LateralFlexionNeck:
    def __init__(self, history_length=90):
        self.lateral_flexion_history = deque(maxlen=history_length)

    def lateral_flexion_neck(self, keypoints, threshold_angle=15):
        # 必要なキーポイントを取得
        left_eye = next((kp for kp in keypoints if kp['name'] == 'left_eye'), None)
        right_eye = next((kp for kp in keypoints if kp['name'] == 'right_eye'), None)
        nose = next((kp for kp in keypoints if kp['name'] == 'nose'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)
        left_elbow = next((kp for kp in keypoints if kp['name'] == 'left_elbow'), None)
        right_elbow = next((kp for kp in keypoints if kp['name'] == 'right_elbow'), None)
        left_hip = next((kp for kp in keypoints if kp['name'] == 'left_hip'), None)
        right_hip = next((kp for kp in keypoints if kp['name'] == 'right_hip'), None)

        # キーポイントが検出されていない場合はFalseを返す
        if not all([left_eye, right_eye, nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_hip, right_hip]):
            return False

        # 両目の中点を計算
        eyes_midpoint = {
            'x': (left_eye['x'] + right_eye['x']) / 2,
            'y': (left_eye['y'] + right_eye['y']) / 2
        }

        # V_center（両目の中点と鼻のベクトル）を計算
        v_center = [nose['x'] - eyes_midpoint['x'], nose['y'] - eyes_midpoint['y']]

        # 左右の V_arm（肩と肘のベクトル）を計算
        v_arm_left = [left_elbow['x'] - left_shoulder['x'], left_elbow['y'] - left_shoulder['y']]
        v_arm_right = [right_elbow['x'] - right_shoulder['x'], right_elbow['y'] - right_shoulder['y']]

        # 左右の角度を計算
        angle_left = self.angle_between(v_center, v_arm_left)
        angle_right = self.angle_between(v_center, v_arm_right)

        # 背中がまっすぐかを確認
        shoulder_midpoint = {
            'x': (left_shoulder['x'] + right_shoulder['x']) / 2,
            'y': (left_shoulder['y'] + right_shoulder['y']) / 2
        }
        hip_midpoint = {
            'x': (left_hip['x'] + right_hip['x']) / 2,
            'y': (left_hip['y'] + right_hip['y']) / 2
        }
        back_angle = math.degrees(math.atan2(shoulder_midpoint['y'] - hip_midpoint['y'], 
                                             shoulder_midpoint['x'] - hip_midpoint['x']))
        back_straight = abs(back_angle - 90) <= 15

        # 両手が腰に当たっているかを確認
        hands_on_hips = self.validate_pose(keypoints, 0.1)

        # 側屈の判定
        lateral_flexion = (angle_left <= threshold_angle or angle_right <= threshold_angle) and back_straight and hands_on_hips

        # 履歴に追加
        self.lateral_flexion_history.append(lateral_flexion)

        # 3秒間維持されているかを確認
        if len(self.lateral_flexion_history) == self.lateral_flexion_history.maxlen and all(self.lateral_flexion_history):
            return True

        return False

    @staticmethod
    def angle_between(v1, v2):
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_angle = dot_product / (magnitude1 * magnitude2)
        angle = math.acos(max(-1, min(cos_angle, 1)))  # アークコサインの定義域を確保
        return math.degrees(angle)

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