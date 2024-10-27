from flask import Flask, render_template, Response, jsonify, request
import cv2
from ultralytics import YOLO
import numpy as np
from datetime import datetime
import os
import traceback
import pandas as pd
import time
from components.pose_estimations import PoseEstimator, available_poses
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# YOLOv8モデルをロード
model = YOLO('yolov8n-pose.pt')

# カメラキャプチャの設定
camera = None

# FPSを30に設定
FPS = 30
FRAME_INTERVAL = 1.0 / FPS

# セッションデータを保存するグローバル変数
session_data = []

# PoseEstimatorのインスタンスを作成
pose_estimator = PoseEstimator()

# 選択された姿勢推定メソッド
selected_pose = None

# フレーム生成の停止フラグ
stop_generation = False

def initialize_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        time.sleep(1)  # カメラの初期化待ち
    return camera.isOpened()

def release_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    global session_data, selected_pose, stop_generation, camera
    last_frame_time = time.time()
    
    print("Starting generate_frames")  # デバッグ用
    
    if not initialize_camera():
        print("Failed to initialize camera")
        return

    print(f"Camera initialized successfully, selected_pose: {selected_pose}")  # デバッグ用
    
    while not stop_generation:
        current_time = time.time()
        elapsed_time = current_time - last_frame_time

        if elapsed_time >= FRAME_INTERVAL:
            success, frame = camera.read()
            if not success:
                print("Failed to read frame from camera")  # デバッグ用
                break
            else:
                print("Frame read successfully")  # デバッグ用
                # YOLOv8による推論を実行
                results = model(frame)

                # 結果を描画
                annotated_frame = results[0].plot()

                # 骨格データを抽出し整理
                skeleton_data = []
                timestamp = datetime.now().timestamp()
                stop_recording = False
                
                for result in results:
                    for pose in result.keypoints.data:
                        organized_data = pose_estimator.organize_skeleton_data(pose.tolist(), timestamp)
                        skeleton_data.append(organized_data)

                        # 選択された姿勢タイプに応じて適切な判定メソッドを呼び出す
                        print(f"Checking pose type: {selected_pose}")  # デバッグ用
                        if selected_pose == 'right_hand_raised':
                            stop_recording = pose_estimator.check_pose(organized_data, current_time)
                        elif selected_pose == 'neck_flexion':
                            stop_recording = pose_estimator.check_neck_flexion(organized_data['keypoints'])
                        elif selected_pose == 'neck_rotation':
                            stop_recording = pose_estimator.check_neck_rotation(organized_data['keypoints'])
                        elif selected_pose == 'neck_extension':
                            stop_recording = pose_estimator.check_neck_extension(organized_data['keypoints'])

                if stop_recording:
                    print(f"Detected {available_poses.get(selected_pose, 'unknown pose')}. Stopping video.")
                    yield (b'--frame\r\n'
                           b'Content-Type: text/plain\r\n\r\n'
                           b'COMPLETE\r\n')
                    break

                # セッションデータに追加
                session_data.extend(skeleton_data)

                try:
                    # JPEGにエンコード
                    ret, buffer = cv2.imencode('.jpg', annotated_frame)
                    if not ret:
                        print("Failed to encode frame")  # デバッグ用
                        continue
                    
                    frame = buffer.tobytes()
                    print("Frame encoded successfully")  # デバッグ用

                    last_frame_time = current_time

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    print(f"Error encoding frame: {e}")  # デバッグ用
        else:
            time.sleep(max(0, FRAME_INTERVAL - elapsed_time))

    print("Exiting generate_frames")  # デバッグ用

@app.route('/video_feed')
def video_feed():
    global stop_generation
    stop_generation = False
    print("Received video_feed request")  # デバッグ用
    try:
        if initialize_camera():
            print("Camera initialized in video_feed")  # デバッグ用
            return Response(generate_frames(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
        return jsonify({'error': 'Failed to initialize camera'}), 500
    except Exception as e:
        print(f"Error in video_feed: {str(e)}")  # デバッグ用
        traceback.print_exc()  # スタックトレースを出力
        return jsonify({'error': 'Error starting video feed'}), 500


@app.route('/set_pose', methods=['POST'])
def set_pose():
    global selected_pose
    try:
        pose_type = request.json.get('pose_type')
        if pose_type:
            selected_pose = pose_type
            print(f"Pose type set to: {pose_type}")
            return jsonify({
                'message': f'Pose set to {available_poses.get(pose_type, "unknown pose")}',
                'success': True
            })
        return jsonify({'error': 'No pose_type provided'}), 400
    except Exception as e:
        print(f"Error in set_pose: {str(e)}")
        return jsonify({'error': 'Error setting pose'}), 500

@app.route('/stop_video', methods=['POST'])
def stop_video():
    global stop_generation
    stop_generation = True
    release_camera()
    try:
        return jsonify({'message': 'Video stopped successfully.'})
    except Exception as e:
        print(f"Error in stop_video: {str(e)}")
        return jsonify({'error': 'Error stopping video'}), 500

@app.route('/stop_and_save', methods=['POST'])
def stop_and_save():
    global session_data, stop_generation, selected_pose
    stop_generation = True
    try:
        if not session_data:
            return jsonify({'message': 'No data to save. Please start the video feed first.'}), 400

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # ファイルを保存するディレクトリを指定
        save_dir = r'C:\Users\81809\Documents\学校\卒研\test-1\yolotest\ExcelFile'

        # データを整理
        organized_data = []
        for item in session_data:
            keypoints = item['keypoints']
            keypoint_dict = {kp['name']: (kp['x'], kp['y']) for kp in keypoints if kp['confidence'] > 0.5}
            organized_data.append({
                'timestamp': item['timestamp'],
                'pose_type': selected_pose,
                **keypoint_dict
            })

        # DataFrameに変換
        df = pd.DataFrame(organized_data)

        if df.empty:
            return jsonify({'message': 'No valid data to save.'}), 400

        # タイムスタンプでソート
        df = df.sort_values('timestamp')

        # X座標とY座標を別々の列に分割
        columns_to_split = df.columns.difference(['timestamp', 'pose_type'])
        for column in columns_to_split:
            df[f'{column}_x'] = df[column].apply(lambda x: x[0] if isinstance(x, tuple) else None)
            df[f'{column}_y'] = df[column].apply(lambda x: x[1] if isinstance(x, tuple) else None)
            df = df.drop(column, axis=1)

        # 列を並び替え
        columns = ['timestamp', 'pose_type'] + sorted([col for col in df.columns if col not in ['timestamp', 'pose_type']])
        df = df[columns]

        # Excelファイルとして保存
        excel_filename = f'keypoints_data_{selected_pose}_{timestamp}.xlsx'
        excel_path = os.path.join(save_dir, excel_filename)
        df.to_excel(excel_path, index=False)

        # セッションデータをリセット
        session_data = []

        print(f"Session data saved successfully as {excel_path}")
        return jsonify({'message': f'Session data saved as {excel_filename}'})
    except Exception as e:
        error_msg = f"Error saving session data: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)