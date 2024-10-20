import math
from collections import deque

class NeckExtension:
    def __init__(self, history_length=90):
        self.extension_history = deque(maxlen=history_length)

    def neck_extension(self, keypoints, threshold_angle=15):
        # 必要なキーポイントを取得
        nose = next((kp for kp in keypoints if kp['name'] == 'nose'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)
        left_elbow = next((kp for kp in keypoints if kp['name'] == 'left_elbow'), None)
        right_elbow = next((kp for kp in keypoints if kp['name'] == 'right_elbow'), None)
        left_wrist = next((kp for kp in keypoints if kp['name'] == 'left_wrist'), None)
        right_wrist = next((kp for kp in keypoints if kp['name'] == 'right_wrist'), None)
        left_knee = next((kp for kp in keypoints if kp['name'] == 'left_knee'), None)
        right_knee = next((kp for kp in keypoints if kp['name'] == 'right_knee'), None)
        left_hip = next((kp for kp in keypoints if kp['name'] == 'left_hip'), None)
        right_hip = next((kp for kp in keypoints if kp['name'] == 'right_hip'), None)
        left_ankle = next((kp for kp in keypoints if kp['name'] == 'left_ankle'), None)
        right_ankle = next((kp for kp in keypoints if kp['name'] == 'right_ankle'), None)

        # キーポイントが検出されていない場合はFalseを返す
        if not all([nose, left_shoulder, right_shoulder, left_elbow, right_elbow, 
                    left_wrist, right_wrist, left_knee, right_knee, left_hip, right_hip,
                    left_ankle, right_ankle]):
            return False

        # スフィンクスのポーズを確認
        elbow_knee_angle = self.calculate_angle(left_elbow, left_knee, right_knee)
        back_horizontal = abs(self.calculate_angle(left_shoulder, left_hip, right_hip) - 180) <= threshold_angle

        # 首の伸展を確認
        neck_extended = nose['y'] < min(left_shoulder['y'], right_shoulder['y'])

        # 体の長さを推定（肩から足首までの距離）
        body_length = max(
            self.distance(left_shoulder, left_ankle),
            self.distance(right_shoulder, right_ankle)
        )

        # 「4足分」の距離を推定（体の長さの約2/3）
        required_distance = body_length * 2/3

        # 手首の位置が適切な距離にあるか確認
        wrist_to_shoulder_distance = min(
            self.distance(left_wrist, left_shoulder),
            self.distance(right_wrist, right_shoulder)
        )
        wrist_position_correct = abs(wrist_to_shoulder_distance - required_distance) <= required_distance * 0.1  # 10%の誤差を許容

        # 「印」の高さを推定（体の長さの約1/3）
        mark_height = body_length / 3

        # 頭が「印」の高さまで上がっているか確認
        head_reaches_mark = nose['y'] <= left_shoulder['y'] - mark_height

        # すべての条件を満たしているか確認
        extension_correct = (elbow_knee_angle >= 85 and elbow_knee_angle <= 95 and
                             back_horizontal and neck_extended and
                             wrist_position_correct and head_reaches_mark)

        # 履歴に追加
        self.extension_history.append(extension_correct)

        # 3秒間維持されているかを確認
        if len(self.extension_history) == self.extension_history.maxlen and all(self.extension_history):
            return True

        return False

    @staticmethod
    def calculate_angle(point1, point2, point3):
        # 3点間の角度を計算する補助関数
        angle = math.degrees(math.atan2(point3['y'] - point2['y'], point3['x'] - point2['x']) -
                             math.atan2(point1['y'] - point2['y'], point1['x'] - point2['x']))
        return abs(angle)

    @staticmethod
    def distance(point1, point2):
        # 2点間の距離を計算する補助関数
        return math.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)