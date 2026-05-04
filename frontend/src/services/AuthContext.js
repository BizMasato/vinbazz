import React, { createContext, useContext, useState } from 'react';
import appSettings from '../config/settings';

// Contextを作成
const AuthContext = createContext();

// AuthProviderを作成
export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState(''); // username用のstateを追加

    const checkSession = async () => {
        try {
            const response = await fetch(`${appSettings.apiUrl}/api/check-session`, { credentials: 'include' });
            const data = await response.json();
            setIsLoggedIn(data.isAuthenticated);
            setUsername(data.username); // usernameを設定
        } catch (error) {
            console.error("ログイン状態の確認エラー:", error);
        }
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, username, checkSession }}>
            {children}
        </AuthContext.Provider>
    );
};

// Contextを使いやすくするためのカスタムフック
export const useAuth = () => {
    return useContext(AuthContext);
};
