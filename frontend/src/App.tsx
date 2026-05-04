// import React from 'react';
// import logo from './logo.svg';
import { useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './services/AuthContext';
import Header from './pages/Top/Header'
import Footer from './pages/Top/Footer'
import Home from './pages/Top/Home'
import Login from './pages/User/Login'
import Register from './pages/User/Register';
import ActivationComplete from './pages/User/ActivationComplete';
import ActivationExpired  from './pages/User/ActivationExpired';
import Clothes from './pages/Clothes/Clothes'

function App() {
  return (
      <AuthProvider>
          <Router>
              <Main />
          </Router>
      </AuthProvider>
  );
}

const Main = () => {

  const { checkSession } = useAuth(); // checkSession 関数を取得

  useEffect(() => {
      checkSession(); // セッションチェックをここで実行
  }, [checkSession]);

  return (
      <div>
          <Header />
          <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/activation_complete" element={<ActivationComplete />} />
              <Route path="/activation_expired" element={<ActivationExpired />} />
              <Route path="/clothes" element={<Clothes />} />
          </Routes>
          <Footer />
      </div>
  );
};
/*
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
*/

export default App;
