from collections import deque
import numpy as np
import math

class NeckFlexion:
    def __init__(self):
        # 初期姿勢のキャリブレーション用パラメータ
        self.calibration_history = deque(maxlen=90)  # 3秒分 (30fps × 3)
        self.flexion_history = deque(maxlen=90)      # 屈曲維持の判定用
        self.is_calibrated = False
        self.initial_vector = None
        self.flexion_start_time = None
        
        # 状態管理
        self.current_state = "NOT_CALIBRATED"  # NOT_CALIBRATED, CALIBRATED, FLEXION_DETECTED, COMPLETED
        
        # 設定パラメータ
        self.VERTICAL_ANGLE_THRESHOLD = 10    # 垂直判定の閾値（度）
        self.NECK_FLEXION_THRESHOLD = 45      # 首の屈曲判定の閾値（度）
        self.CALIBRATION_DURATION = 3         # キャリブレーション時間（秒）
        self.FLEXION_HOLD_DURATION = 3        # 屈曲維持時間（秒）

    def calculate_vector(self, point1, point2):
        return [point2['x'] - point1['x'], point2['y'] - point1['y']]
    
    def calculate_vector_magnitude(self, vector):
        return math.sqrt(vector[0]**2 + vector[1]**2)
    
    def calculate_angle(self, vector1, vector2):
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = self.calculate_vector_magnitude(vector1)
        magnitude2 = self.calculate_vector_magnitude(vector2)
        
        try:
            cos_angle = dot_product / (magnitude1 * magnitude2)
            cos_angle = min(1.0, max(-1.0, cos_angle))
            angle_rad = math.acos(cos_angle)
            return math.degrees(angle_rad)
        except ZeroDivisionError:
            return 0
    
    def calculate_eye_midpoint(self, keypoints):
        left_eye = next((kp for kp in keypoints if kp['name'] == 'left_eye'), None)
        right_eye = next((kp for kp in keypoints if kp['name'] == 'right_eye'), None)
        
        if left_eye and right_eye:
            return {
                'x': (left_eye['x'] + right_eye['x']) / 2,
                'y': (left_eye['y'] + right_eye['y']) / 2
            }
        return None

    def check_vertical_alignment(self, eye_midpoint, nose):
        vector = self.calculate_vector(eye_midpoint, nose)
        angle = self.calculate_angle(vector, [0, 1])
        return abs(angle) <= self.VERTICAL_ANGLE_THRESHOLD

    def assess_neck_flexion_pose(self, keypoints):
        nose = next((kp for kp in keypoints if kp['name'] == 'nose'), None)
        left_shoulder = next((kp for kp in keypoints if kp['name'] == 'left_shoulder'), None)
        
        if not all([nose, left_shoulder]):
            return {"status": "ERROR", "message": "キーポイントが検出できません"}
            
        eye_midpoint = self.calculate_eye_midpoint(keypoints)
        if not eye_midpoint:
            return {"status": "ERROR", "message": "目のキーポイントが検出できません"}

        # キャリブレーション段階
        if self.current_state == "NOT_CALIBRATED":
            if self.check_vertical_alignment(eye_midpoint, nose):
                current_vector = self.calculate_vector(left_shoulder, nose)
                self.calibration_history.append(current_vector)
                
                if len(self.calibration_history) == 90:  # 3秒間のデータが集まった
                    vectors = np.array(self.calibration_history)
                    self.initial_vector = vectors.mean(axis=0).tolist()
                    self.current_state = "CALIBRATED"
                    return {"status": "CALIBRATED", "message": "首を前に曲げてください"}
            else:
                self.calibration_history.clear()
            return {"status": "CALIBRATING", "message": "真っ直ぐな姿勢を3秒間維持してください"}

        # キャリブレーション完了後の姿勢判定
        elif self.current_state in ["CALIBRATED", "FLEXION_DETECTED"]:
            current_vector = self.calculate_vector(left_shoulder, nose)
            angle = self.calculate_angle(self.initial_vector, current_vector)
            
            if angle >= self.NECK_FLEXION_THRESHOLD:
                self.flexion_history.append(True)
                if len(self.flexion_history) == 90:  # 3秒間45度を維持
                    self.current_state = "COMPLETED"
                    return {"status": "COMPLETE", "message": "完了しました！"}
                self.current_state = "FLEXION_DETECTED"
                return {"status": "HOLDING", "message": "その姿勢を維持してください"}
            else:
                self.flexion_history.clear()
                return {"status": "WAITING", "message": "首を前に曲げてください"}

        elif self.current_state == "COMPLETED":
            return {"status": "COMPLETE", "message": "完了しました！"}

        return {"status": "ERROR", "message": "予期せぬエラーが発生しました"}

    def reset(self):
        self.__init__()