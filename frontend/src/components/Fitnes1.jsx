import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Fitnes1.css';
import { HomeOutlined, DashboardOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';
import axios from 'axios';

const Fitnes1 = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const iframeRef = useRef(null);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const startCamera = () => {
    setIsCameraOpen(true);
    if (iframeRef.current) {
      iframeRef.current.src = 'http://127.0.0.1:5000/video_feed';  // Flaskサーバーのカメラフィードを表示
    }
  };

  const stopCamera = async () => {
    setIsCameraOpen(false);
    if (iframeRef.current) {
      iframeRef.current.src = '';  // カメラフィードを停止
    }
    try {
      await axios.post('http://127.0.0.1:5000/stop_video');  // Flaskの`/stop_video`エンドポイントを呼び出してカメラを停止
      console.log('Video stopped');
    } catch (error) {
      console.error('Error stopping video:', error);
      alert('カメラの停止中にエラーが発生しました。');
    }
  };

  const saveSessionData = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/stop_and_save');  // Flaskの`/stop_and_save`エンドポイントを呼び出してセッションデータを保存
      console.log(response.data.message);
      alert('セッションデータが保存されました。');
    } catch (error) {
      console.error('Error saving session data:', error);
      alert('セッションデータの保存中にエラーが発生しました。');
    }
  };

  const handleMessage = (event) => {
    if (event.data === 'COMPLETE') {
      setIsComplete(true);
      stopCamera();
    }
  };

  React.useEffect(() => {
    window.addEventListener('message', handleMessage);
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <div className="fitnes1-container">
      {/* Tab Bar */}
      <div className="tab-bar">
        <div
          className={`hamburger-icon ${isSidebarOpen ? 'active' : ''}`}
          onClick={toggleSidebar}
        >
          &#9776;
        </div>
        <Link to="/profile" className="profile-icon">
          <UserOutlined />
        </Link>
      </div>

      {/* Sidebar */}
      <div className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <ul>
          <li><HomeOutlined /> Home</li>
          <li><DashboardOutlined /> Dashboard</li>
          <li><CalendarOutlined /> Calendar</li>
          <li><UserOutlined /> Profile</li>
        </ul>
      </div>

      {/* Main content */}
      <h1>首の可動性 - 右手を上げる動作</h1>
      <div className="description">
        <p>このエクササイズでは、右手を上げる動作を行います。</p>
        <p>カメラの前に立ち、右手をゆっくりと上げてください。</p>
        <p>システムが正しい姿勢を検出すると、自動的に撮影が停止します。</p>
      </div>

      {/* Embedded Videos */}
      <div className="video-container">
        <div className="video-item">
          <h2>自分の身体知っていますか？</h2>
          <p>ー 整体広沼のセルフチェック ー</p>
          <div className="video-wrapper">
            <iframe
              width="560"
              height="315"
              src="https://www.youtube.com/embed/4-YHy0wMT2w"
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
        <div className="video-item">
          <h2>自分の身体知っていますか？</h2>
          <p>ー 整体広沼の動作改善エクササイズ ー</p>
          <div className="video-wrapper">
            <iframe
              width="560"
              height="315"
              src="https://www.youtube.com/embed/fw0DQBt3psM"
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      </div>

      {/* Camera and Actions */}
      <div className={`video-container ${isCameraOpen ? 'camera-open' : ''}`}>
        {isComplete ? (
          <div className="complete-message">
            <h2>完了！</h2>
            <p>正しい姿勢が検出されました。お疲れ様でした。</p>
            <button onClick={() => {
              setIsCameraOpen(false);
              setIsComplete(false);
              saveSessionData();
            }}>
              データを保存して終了
            </button>
          </div>
        ) : isCameraOpen ? (
          <div className="camera-feed-wrapper">
            <div className="camera-feed">
              <iframe
                ref={iframeRef}
                title="Video Feed"
                width="640"
                height="480"
              ></iframe>
            </div>
            <button className="stop-button" onClick={() => {
              stopCamera();
              saveSessionData();
            }}>
              撮影を停止してデータを保存
            </button>
          </div>
        ) : (
          <button className="start-button" onClick={startCamera}>
            撮影を開始する
          </button>
        )}
      </div>
      <iframe ref={iframeRef} src={isCameraOpen ? 'http://127.0.0.1:5000/video_feed' : ''} width="600" height="400" title="Camera Feed" />
    </div>
  );
};

export default Fitnes1;