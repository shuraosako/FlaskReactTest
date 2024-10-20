// src/components/Dashboard.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Dashboard.css';
import { HomeOutlined, DashboardOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';
import fitnes1 from '../images/fitnes1.png';
import fitnes2 from '../images/fitnes2.png';
import fitnes3 from '../images/fitnes3.png';
import fitnes4 from '../images/fitnes4.png';
import fitnes5 from '../images/fitnes5.png';
import fitnes6 from '../images/fitnes6.png';
import fitnes7 from '../images/fitnes7.png';
import fitnes8 from '../images/fitnes8.png';
import fitnes9 from '../images/fitnes9.png';
import fitnes10 from '../images/fitnes10.png';
import fitnes11 from '../images/fitnes11.png';

const Dashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="dashboard-container">
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
      <div className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <ul>
          <li><HomeOutlined /> Home</li>
          <li><DashboardOutlined /> Dashboard</li>
          <li><CalendarOutlined /> Calendar</li>
          <li><UserOutlined /> Profile</li>
        </ul>
      </div>
      <div className="dashboard-grid">
        <Link to="/fitnes1" className="grid-item fitnes1">
          <div className="text">首の可動性</div>
        </Link>
        <Link to="/fitnes2" className="grid-item fitnes2">
          <div className="text">肩の可動性</div>
        </Link>
        <Link to="/fitnes3" className="grid-item fitnes3">
          <div className="text">首の回旋可動性</div>
        </Link>
        <Link to="/fitnes4" className="grid-item fitnes4">
          <div className="text">胸椎の可動性</div>
        </Link>
        <Link to="/fitnes5" className="grid-item fitnes5">
          <div className="text">上体の屈力</div>
        </Link>
        <Link to="/fitnes6" className="grid-item fitnes6">
          <div className="text">前腕の可動性</div>
        </Link>
        <Link to="/fitnes7" className="grid-item fitnes7">
          <div className="text">前腕の可動性</div>
        </Link>
        <Link to="/fitnes8" className="grid-item fitnes8">
          <div className="text">前腕の可動性</div>
        </Link>
        <Link to="/fitnes9" className="grid-item fitnes9">
          <div className="text">体幹の屈力</div>
        </Link>
        <Link to="/fitnes10" className="grid-item fitnes10">
          <div className="text">下半身の筋力</div>
        </Link>
        <Link to="/fitnes11" className="grid-item fitnes11">
          <div className="text">足首の柔らかさ</div>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;