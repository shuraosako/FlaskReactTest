import math
from collections import deque

class NeckRotation:
    def __init__(self, history_length=90):
        self.rotation_history = deque(maxlen=history_length)

    def neck_rotation(self, keypoints, threshold_angle=15):
        # 必要なキーポイントを取得
        nose = next((kp for kp in keypoints if kp['name'] == 'nose'), None)
        left_eye = next((kp for kp in keypoints if kp['name'] == 'left_eye'), None)
        right_eye = next((kp for kp in keypoints if kp['name'] == 'right_eye'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)
        left_hip = next((kp for kp in keypoints if kp['name'] == 'left_hip'), None)
        right_hip = next((kp for kp in keypoints if kp['name'] == 'right_hip'), None)

        # キーポイントが検出されていない場合はFalseを返す
        if not all([nose, left_eye, right_eye, left_shoulder, right_shoulder, left_hip, right_hip]):
            return False

        # 顔の正中線のベクトルを計算
        face_midpoint = {
            'x': (left_eye['x'] + right_eye['x']) / 2,
            'y': (left_eye['y'] + right_eye['y']) / 2
        }
        face_vector = [nose['x'] - face_midpoint['x'], nose['y'] - face_midpoint['y']]

        # 肩のベクトルを計算
        shoulder_vector = [right_shoulder['x'] - left_shoulder['x'], right_shoulder['y'] - left_shoulder['y']]

        # 顔の正中線と肩の向きの角度を計算
        rotation_angle = self.angle_between(face_vector, shoulder_vector)

        # 背中がまっすぐかを確認
        hip_midpoint = {
            'x': (left_hip['x'] + right_hip['x']) / 2,
            'y': (left_hip['y'] + right_hip['y']) / 2
        }
        shoulder_midpoint = {
            'x': (left_shoulder['x'] + right_shoulder['x']) / 2,
            'y': (left_shoulder['y'] + right_shoulder['y']) / 2
        }
        back_angle = math.degrees(math.atan2(shoulder_midpoint['y'] - hip_midpoint['y'], 
                                             shoulder_midpoint['x'] - hip_midpoint['x']))
        back_straight = abs(back_angle - 90) <= 15

        # 両手が腰に当たっているかを確認
        hands_on_hips = self.validate_pose(keypoints, 0.1)

        # 首の回旋を判定
        neck_rotated = abs(rotation_angle - 90) <= threshold_angle and back_straight and hands_on_hips

        # 履歴に追加
        self.rotation_history.append(neck_rotated)

        # 3秒間維持されているかを確認
        if len(self.rotation_history) == self.rotation_history.maxlen and all(self.rotation_history):
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