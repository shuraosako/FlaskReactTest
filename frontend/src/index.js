import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import CreateAccount from './components/CreateAccount';
import Dashboard from './components/Dashboard';
import Fitnes1 from './components/Fitnes1';
import ErrorBoundary from './components/ErrorBoundary';

const App = () => {
  return (
    <Router>
      <ErrorBoundary>
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/fitnes1" element={<Fitnes1 />} />
          {/* 不適切なパスが入力された場合、ダッシュボードにリダイレクト */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </ErrorBoundary>
    </Router>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// エラー処理のためのグローバルハンドラー
window.addEventListener('error', (event) => {
  console.error('Global error caught:', event.error);
  // ここでエラーログをサーバーに送信するなどの処理を追加できます
});

// // サービスワーカーの登録（オプション）
// if ('serviceWorker' in navigator) {
//   window.addEventListener('load', () => {
//     navigator.serviceWorker.register('/service-worker.js').then(registration => {
//       console.log('SW registered: ', registration);
//     }).catch(registrationError => {
//       console.log('SW registration failed: ', registrationError);
//     });
//   });
// }