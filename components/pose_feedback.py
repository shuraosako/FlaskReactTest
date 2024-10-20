# File: C:\Users\81809\Documents\学校\卒研\test-1\yolotest\components\pose_feedback.py

def generate_feedback(pose_type, pose_data):
    if pose_type == 'right_hand_raised':
        return right_hand_raised_feedback(pose_data)
    elif pose_type == 'neck_flexion':
        return neck_flexion_feedback(pose_data)
    elif pose_type == 'lateral_flexion_neck':
        return lateral_flexion_neck_feedback(pose_data)
    elif pose_type == 'neck_rotation':
        return neck_rotation_feedback(pose_data)
    elif pose_type == 'neck_extension':
        return neck_extension_feedback(pose_data)
    else:
        return ["姿勢が選択されていません"]

def right_hand_raised_feedback(data):
    feedback = []
    if not data['is_raised']:
        feedback.append("右手をもっと高く上げてください")
    else:
        if data['duration'] < 2:
            feedback.append(f"あと{2-data['duration']:.1f}秒維持してください")
        else:
            feedback.append("素晴らしい！右手を上げたままです")
    return feedback

def neck_flexion_feedback(data):
    feedback = []
    if not data['is_flexed']:
        feedback.append("首をもっと前に曲げてください")
    if not data['back_straight']:
        feedback.append("背筋をまっすぐに保ってください")
    if data['duration'] < 3:
        feedback.append(f"あと{3-data['duration']:.1f}秒維持してください")
    return feedback

def lateral_flexion_neck_feedback(data):
    feedback = []
    if not data['is_flexed']:
        feedback.append("首をもっと横に傾けてください")
    if not data['back_straight']:
        feedback.append("背筋をまっすぐに保ってください")
    if not data['hands_on_hips']:
        feedback.append("両手を腰に当ててください")
    if data['duration'] < 3:
        feedback.append(f"あと{3-data['duration']:.1f}秒維持してください")
    return feedback

def neck_rotation_feedback(data):
    feedback = []
    if not data['is_rotated']:
        feedback.append("首をもっと回転させてください")
    if not data['back_straight']:
        feedback.append("背筋をまっすぐに保ってください")
    if not data['hands_on_hips']:
        feedback.append("両手を腰に当ててください")
    if data['duration'] < 3:
        feedback.append(f"あと{3-data['duration']:.1f}秒維持してください")
    return feedback

def neck_extension_feedback(data):
    feedback = []
    if not data['elbow_knee_angle_correct']:
        feedback.append("肘と膝の角度を90度に近づけてください")
    if not data['back_horizontal']:
        feedback.append("背中を水平に保ってください")
    if not data['neck_extended']:
        feedback.append("首をもっと後ろに伸ばしてください")
    if not data['wrist_position_correct']:
        feedback.append("手首の位置を調整してください")
    if not data['head_reaches_mark']:
        feedback.append("頭をもっと上げてください")
    if data['duration'] < 3:
        feedback.append(f"あと{3-data['duration']:.1f}秒維持してください")
    return feedback