// src/components/Login.tsx

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import appSettings from '../../config/settings';
import { useAuth } from '../../services/AuthContext';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);
    const location = useLocation();
    const [logoutMessage, setLogoutMessage] = useState('');
    const [loginErrorMessage, setLoginErrorMessage] = useState('');
    const { isLoggedIn } = useAuth();

    const registerView = () => {
        window.location.href = '/register';
    } 

    useEffect(() => {
        // クエリパラメータからメッセージを取得
        const queryParams = new URLSearchParams(location.search);
        const message = queryParams.get('message');
        if (message === 'logged_out') {
            setLogoutMessage('ログアウトしました。');
        }
    }, [location]);

    useEffect(() => {
        // ログインしていたらプロフィールページに遷移
        if (isLoggedIn) {
          window.location.href = '/profile';
        }
      }, [isLoggedIn]);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                `${appSettings.apiUrl}/api/login`,
                { email, password },
                { headers: { 'Content-Type': 'application/json' } , withCredentials: true }
            );
            if (response.status === 200) {
                // ログイン成功後にトップページへリダイレクト
                window.location.href = '/';
            }
        } catch (error) {
            console.error('ログイン失敗:', error);
            setError(true);
            setLoginErrorMessage('メールアドレス、またはパスワードが違います。再度確認して入力してください。');
        }
    };

    return (
        <div>
            <div className="login-container max-w-md mx-auto mt-16 p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-center text-2xl font-bold mb-4">ログイン</h2>
                <div>
                {/* ログアウトメッセージの表示 */}
                {logoutMessage && (
                    <div className="text-red-500 mb-4 text-center">{logoutMessage}</div>
                )}
                {/* ログインエラーメッセージの表示 */}
                {loginErrorMessage && error && (
                    <div className="text-red-500 mb-4 text-center">{loginErrorMessage}</div>
                )}
                </div>
                {/* ログイン画面の内容 */}
                <form onSubmit={handleLogin}>
                    <div className="mb-4">
                        <label className="block">メールアドレス</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className={`w-full p-2 border border-gray-300 ${error ? 'bg-red-100' : ''}`}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block">パスワード</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className={`w-full p-2 border border-gray-300 ${error ? 'bg-red-100' : ''}`}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-500 text-white hover:bg-blue-400 p-2 rounded"
                    >
                        ログイン
                    </button>
                </form>
            </div>
            <div className="login-container max-w-md mx-auto mt-16 mb-10 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-center text-2xl font-bold mb-4">初めてご利用の方</h2>
                <button 
                    type="button"
                    className="w-full bg-transparent hover:bg-blue-500 text-blue-500 hover:text-white p-2 border border-blue-500 hover:border-transparent rounded"
                    onClick={registerView}
                >
                    <a href="/register">新規会員登録</a>
                </button>
            </div>
        </div>
    )
};

export default Login;
