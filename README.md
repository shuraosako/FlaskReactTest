# YOLOv8を用いたKojiawarenessの自動化

## 概要
このプロジェクトはYOLOv8を使用して、Kojiawarenessの自動化を実現することが目的です

## 機能
- リアルタイムの姿勢推定
- 複数の姿勢検出モード
- 検出結果のビジュアル表示

## 必要条件
- Python 3.8以上
- OpenCV
- Flask
- Ultralytics YOLOv8
- pandas

## セットアップ
1. リポジトリをクローン：
   ```
   git clone [リポジトリURL]
   cd [プロジェクトディレクトリ]
   ```

2. 必要なパッケージをインストール：
   ```
   pip install -r requirements.txt
   ```

3. YOLOv8モデルをダウンロード：
   ```
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-pose.pt
   ```

## 使用方法
1. アプリケーションを起動：
   ```
   python app.py
   ```

2. Reactを起動
   ```
   npm start
   ```


## 注意事項
- このアプリケーションはローカル環境での使用を想定
- カメラへのアクセス権限が必要

## 今後の展望
- モバイルデバイスへの対応


## 連絡先
大迫汐欄 - s21m1012@bene.fit.ac.jp

---

© 2024 大迫汐欄, 藤岡研究室