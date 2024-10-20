// src/components/CreateAccount.jsx

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/CreateAccount.css';
import { HomeOutlined, DashboardOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';

const CreateAccount = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [name, setName] = useState('');
  const [nationality, setNationality] = useState('');
  const [address, setAddress] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [gender, setGender] = useState('Male');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // アカウント作成のロジックを実装する
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="create-account-container">
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
      <div className="create-account-form">
        <div className="icon-placeholder"></div>
        <form onSubmit={handleSubmit}>
          <input
            type="name"
            placeholder="Please select your name title"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <select
            value={nationality}
            onChange={(e) => setNationality(e.target.value)}
            required
          >
            <option value="JP">Japan</option>
            <option value="US">United States of America</option>
            <option value="GB">United Kingdom</option>
            <option value="FR">France</option>
            <option value="DE">Germany</option>
          </select>
          <textarea
            placeholder="Address"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            rows="3"
            required
          ></textarea>
          <input
            type="date"
            placeholder="Birthday"
            value={dateOfBirth}
            onChange={(e) => setDateOfBirth(e.target.value)}
            required
          />
          <div className="gender-select">
            <div
              className={`gender-option ${gender === 'Male' ? 'selected' : ''}`}
              onClick={() => setGender('Male')}
            >
              Male
            </div>
            <div
              className={`gender-option ${gender === 'Female' ? 'selected' : ''}`}
              onClick={() => setGender('Female')}
            >
              Female
            </div>
          </div>
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <input
            type="tel"
            placeholder="Phone Number"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
          <button type="submit">Register new account</button>
        </form>
        <p className="login-link">
          Already have an account? <Link to="/">Login to your account</Link>
        </p>
      </div>
    </div>
  );
};

export default CreateAccount;