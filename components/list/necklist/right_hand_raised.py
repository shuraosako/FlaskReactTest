from datetime import datetime

class RightHandRaised:
    def __init__(self):
        self.right_hand_raised = False
        self.right_hand_raised_start_time = None
        self.RIGHT_HAND_RAISED_DURATION = 5

    def is_right_hand_raised(self, keypoints):
        right_shoulder = next((kp for kp in keypoints if kp['name'] == 'right_shoulder'), None)
        right_wrist = next((kp for kp in keypoints if kp['name'] == 'right_wrist'), None)
        
        if right_shoulder and right_wrist:
            # 右手首の y 座標が 1 以上かつ右肩の y 座標以下であることを確認
            if (right_wrist['y'] is not None and right_shoulder['y'] is not None and 
                1 <= right_wrist['y'] <= right_shoulder['y']):
                return right_wrist['y'] < right_shoulder['y']
        return False

    def check_pose(self, organized_data, current_time):
        if self.is_right_hand_raised(organized_data['keypoints']):
            if not self.right_hand_raised:
                self.right_hand_raised = True
                self.right_hand_raised_start_time = current_time
        else:
            self.right_hand_raised = False
            self.right_hand_raised_start_time = None

        if self.right_hand_raised and (current_time - self.right_hand_raised_start_time) >= self.RIGHT_HAND_RAISED_DURATION:
            return True  # complete条件
        return False