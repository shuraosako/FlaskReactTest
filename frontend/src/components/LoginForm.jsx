// src/components/LoginForm.jsx
import React, { useState, useEffect } from 'react';
import '../styles/LoginForm.css';
import logo from '../images/sport-agency.png';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // 初期値の取得は不要になったため、この部分は削除しました
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      const response = await axios.post('http://localhost:5000/auth/login', { email, password });
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        console.log('ログイン成功');
        navigate('Dashboard');
      }
    } catch (error) {
      console.error('ログインエラー:', error);
      setErrorMessage('メールアドレスまたはパスワードが正しくありません。');
    }
  };

  return (
    <div className="login-form-container">
      <div className="logo-container">
        <img src={logo} alt="スポーツ庁" className="logo" />
      </div>
      <div className="login-form">
        <div className="form-container">
          <div className="form-wrapper">
            <h2>SIGN IN</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="email"
                placeholder="Mail address"
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
              <button type="submit">Login</button>
            </form>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <p className="forgot-password">
              Forgot your <a href="#">password</a>?
            </p>
            <p className="create-account">
              <Link to="/create-account">Create account</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;