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
from PIL import Image, ImageDraw, ImageFont

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

def draw_japanese_text(img, text, position, font_path, font_size=32, color=(255, 255, 255)):
    # OpenCV画像をPIL画像に変換
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # 描画用のオブジェクトを作成
    draw = ImageDraw.Draw(img_pil)
    
    # フォントを読み込む
    font = ImageFont.truetype(font_path, font_size)
    
    # テキストを描画（縁取り効果を追加）
    # 黒い縁取り
    outline_color = (0, 0, 0)
    for offset in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
        pos = (position[0] + offset[0], position[1] + offset[1])
        draw.text(pos, text, font=font, fill=outline_color)
    
    # メインのテキスト
    draw.text(position, text, font=font, fill=color)
    
    # PIL画像をOpenCV画像に戻す
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def generate_frames():
    global session_data, selected_pose, stop_generation, camera
    last_frame_time = time.time()
    
    # 日本語フォントのパス
    font_path = r"C:\Users\81809\Documents\学校\卒研\FlaskIntoReactTest\yolotest\fonts\NotoSansJP-Regular.ttf"
    
    print("Starting generate_frames")
    
    if not initialize_camera():
        print("Failed to initialize camera")
        return

    print(f"Camera initialized successfully, selected_pose: {selected_pose}")
    
    while not stop_generation:
        current_time = time.time()
        elapsed_time = current_time - last_frame_time

        if elapsed_time >= FRAME_INTERVAL:
            success, frame = camera.read()
            if not success:
                print("Failed to read frame from camera")
                break
            else:
                # YOLOv8による推論を実行
                results = model(frame)
                annotated_frame = results[0].plot()
                
                # 骨格データを抽出し整理
                skeleton_data = []
                timestamp = datetime.now().timestamp()
                
                for result in results:
                    for pose in result.keypoints.data:
                        organized_data = pose_estimator.organize_skeleton_data(pose.tolist(), timestamp)
                        skeleton_data.append(organized_data)

                        if selected_pose == 'neck_flexion':
                            pose_result = pose_estimator.neck_flexion_checker.assess_neck_flexion_pose(organized_data['keypoints'])
                            
                            # 日本語テキストを描画
                            message = pose_result.get("message", "")
                            annotated_frame = draw_japanese_text(
                                annotated_frame,
                                message,
                                (10, 30),
                                font_path,
                                font_size=32,
                                color=(255, 255, 255)
                            )
                            
                            if pose_result.get("status") == "COMPLETE":
                                yield (b'--frame\r\n'
                                      b'Content-Type: text/plain\r\n\r\n'
                                      b'COMPLETE\r\n')
                                return

                        elif selected_pose == 'right_hand_raised':
                            stop_recording = pose_estimator.check_pose(organized_data, current_time)
                            if stop_recording:
                                yield (b'--frame\r\n'
                                       b'Content-Type: text/plain\r\n\r\n'
                                       b'COMPLETE\r\n')
                                return

                        elif selected_pose == 'neck_rotation':
                            stop_recording = pose_estimator.check_neck_rotation(organized_data['keypoints'])
                            if stop_recording:
                                yield (b'--frame\r\n'
                                       b'Content-Type: text/plain\r\n\r\n'
                                       b'COMPLETE\r\n')
                                return

                        elif selected_pose == 'neck_extension':
                            stop_recording = pose_estimator.check_neck_extension(organized_data['keypoints'])
                            if stop_recording:
                                yield (b'--frame\r\n'
                                       b'Content-Type: text/plain\r\n\r\n'
                                       b'COMPLETE\r\n')
                                return

                # セッションデータに追加
                session_data.extend(skeleton_data)

                try:
                    # JPEGにエンコード
                    ret, buffer = cv2.imencode('.jpg', annotated_frame)
                    if not ret:
                        print("Failed to encode frame")
                        continue
                    
                    frame = buffer.tobytes()
                    last_frame_time = current_time

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    print(f"Error encoding frame: {e}")
        else:
            time.sleep(max(0, FRAME_INTERVAL - elapsed_time))

@app.route('/video_feed')
def video_feed():
    global stop_generation
    stop_generation = False
    print("Received video_feed request")
    try:
        if initialize_camera():
            print("Camera initialized in video_feed")
            return Response(generate_frames(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
        return jsonify({'error': 'Failed to initialize camera'}), 500
    except Exception as e:
        print(f"Error in video_feed: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Error starting video feed'}), 500

@app.route('/set_pose', methods=['POST'])
def set_pose():
    global selected_pose
    try:
        pose_type = request.json.get('pose_type')
        if pose_type:
            selected_pose = pose_type
            # 新しいポーズが設定されたときに、関連するチェッカーをリセット
            if pose_type == 'neck_flexion':
                pose_estimator.neck_flexion_checker.reset()

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