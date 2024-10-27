import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Fitnes1.css';
import { HomeOutlined, DashboardOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';
import axios from 'axios';

const Fitnes1 = () => {
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [currentExercise, setCurrentExercise] = useState(null);
  const iframeRef = useRef(null);
  const sidebarRef = useRef(null);
  const hamburgerRef = useRef(null);

  const exercises = [
    {
      id: 'right_hand_raised',
      title: '右手上げ',
      description: '右手をゆっくりと上げてください。',
      videoUrl: 'https://www.youtube.com/embed/4-YHy0wMT2w'
    },
    {
      id: 'neck_flexion',
      title: '首の屈曲',
      description: '首を前に曲げてください。',
      videoUrl: 'https://www.youtube.com/embed/fw0DQBt3psM'
    },
    {
      id: 'neck_rotation',
      title: '首の回旋',
      description: '首を左右に回してください。',
      videoUrl: 'https://www.youtube.com/embed/4-YHy0wMT2w'
    },
    {
      id: 'neck_extension',
      title: '首の伸展',
      description: '首を後ろに伸ばしてください。',
      videoUrl: 'https://www.youtube.com/embed/fw0DQBt3psM'
    }
  ];

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isSidebarOpen && 
          sidebarRef.current && 
          hamburgerRef.current &&
          !sidebarRef.current.contains(event.target) &&
          !hamburgerRef.current.contains(event.target)) {
        setIsSidebarOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, [isSidebarOpen]);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleNavigation = (path) => {
    console.log('Navigating to:', path);
    navigate(path);
    setIsSidebarOpen(false);
  };

  const initializeCamera = async (exerciseId) => {
    try {
      console.log('Starting camera initialization for:', exerciseId);

      // 1. 姿勢タイプを設定
      const setPoseResponse = await axios.post('http://127.0.0.1:5000/set_pose', {
        pose_type: exerciseId
      });

      console.log('Set pose response:', setPoseResponse.data);

      if (setPoseResponse.data.success) {
        setCurrentExercise(exerciseId);
        setIsCameraOpen(true);
        
        // 少し遅延を入れてから iframe の src を設定
        await new Promise(resolve => setTimeout(resolve, 100));
        
        if (iframeRef.current) {
          console.log('Setting video feed URL');
          const videoFeedUrl = 'http://127.0.0.1:5000/video_feed';
          iframeRef.current.src = videoFeedUrl;
          console.log('Video feed URL set to:', iframeRef.current.src);
        }
      } else {
        throw new Error('Failed to set pose type');
      }
    } catch (error) {
      console.error('Error initializing camera:', error);
      alert('カメラの初期化中にエラーが発生しました。');
      setIsCameraOpen(false);
      setCurrentExercise(null);
    }
  };

  const stopCamera = async () => {
    if (iframeRef.current) {
      iframeRef.current.src = '';
    }
    try {
      await axios.post('http://127.0.0.1:5000/stop_video');
      console.log('Video stopped');
      setIsCameraOpen(false);
    } catch (error) {
      console.error('Error stopping video:', error);
      alert('カメラの停止中にエラーが発生しました。');
    }
  };

  const saveSessionData = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/stop_and_save');
      console.log('Save response:', response.data);
      alert('セッションデータが保存されました。');
    } catch (error) {
      console.error('Error saving session data:', error);
      alert('セッションデータの保存中にエラーが発生しました。');
    }
  };

  const handleMessage = (event) => {
    console.log('Received message:', event.data);
    if (event.data === 'COMPLETE') {
      setIsComplete(true);
      stopCamera();
    }
  };

  useEffect(() => {
    window.addEventListener('message', handleMessage);
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <div className="fitnes1-container">
      <div className="tab-bar">
        <div
          ref={hamburgerRef}
          className={`hamburger-icon ${isSidebarOpen ? 'active' : ''}`}
          onClick={toggleSidebar}
        >
          &#9776;
        </div>
        <Link to="/profile" className="profile-icon">
          <UserOutlined />
        </Link>
      </div>

      <div 
        ref={sidebarRef}
        className={`sidebar ${isSidebarOpen ? 'open' : ''}`}
      >
        <ul>
          <li onClick={() => handleNavigation('/dashboard')} style={{ cursor: 'pointer' }}>
            <DashboardOutlined /> Dashboard
          </li>
          <li onClick={() => handleNavigation('/calendar')} style={{ cursor: 'pointer' }}>
            <CalendarOutlined /> Calendar
          </li>
          <li onClick={() => handleNavigation('/profile')} style={{ cursor: 'pointer' }}>
            <UserOutlined /> Profile
          </li>
        </ul>
      </div>

      <h1>首の可動性トレーニング</h1>

      {!isCameraOpen ? (
        <div className="exercise-selection">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="exercise-card">
              <h2>{exercise.title}</h2>
              <p>{exercise.description}</p>
              <div className="video-wrapper">
                <iframe
                  width="560"
                  height="315"
                  src={exercise.videoUrl}
                  title={exercise.title}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>
              <button 
                className="start-button"
                onClick={() => initializeCamera(exercise.id)}
              >
                {exercise.title}を開始する
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="camera-feed-wrapper">
          {isComplete ? (
            <div className="complete-message">
              <h2>完了！</h2>
              <p>正しい姿勢が検出されました。お疲れ様でした。</p>
              <button onClick={() => {
                setIsCameraOpen(false);
                setIsComplete(false);
                setCurrentExercise(null);
                saveSessionData();
              }}>
                データを保存して終了
              </button>
            </div>
          ) : (
            <>
              <div className="camera-feed">
                <iframe
                  ref={iframeRef}
                  title="Video Feed"
                  width="100%"
                  height="100%"
                  style={{ border: 'none' }}
                  onLoad={() => console.log('iframe loaded')}
                  onError={(e) => console.error('iframe error:', e)}
                />
              </div>
              <button className="stop-button" onClick={() => {
                stopCamera();
                saveSessionData();
              }}>
                撮影を停止してデータを保存
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Fitnes1;