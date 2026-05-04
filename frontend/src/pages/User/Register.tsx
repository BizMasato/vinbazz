// src/pages/User/Register.tsx
import React, { useEffect, useState } from 'react';
import { IoEye, IoEyeOff } from "react-icons/io5";
import appSettings from '../../config/settings';
import { useAuth } from '../../services/AuthContext';
import '../../styles/Spinner.css'; // スピナーのCSSをインポート

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] =useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegistered, setIsRegistered] = useState(false); // 登録完了かどうかを管理
  const [isLoading, setIsLoading] = useState(false); // ローディング状態を追加
  const { isLoggedIn } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const isPasswordValid = (password: string) => {
    return /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/.test(password);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  useEffect(() => {
    // ログインしていたらプロフィールページに遷移
    if (isLoggedIn) {
      window.location.href = '/profile';
    }
  }, [isLoggedIn]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('パスワードが一致しません。');
      return;
    }
    if (!isPasswordValid(password)) {
      setError('パスワードは8文字以上で、英字と数字を含めてください。');
      return;
    }

    setIsLoading(true); // ボタン押下時にローディング状態を開始

    const response = await fetch(`${appSettings.apiUrl}/api/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    setIsLoading(false); // 通信後にローディング状態を終了

    if (response.ok) {
      setIsRegistered(true); // 登録が完了したらフラグを立てる
    } else {
      const data = await response.json();
      setError(data.error || '登録に失敗しました。');
    }
  };

  return (
    <div className="register-container max-w-md mx-auto mt-16 mb-10 p-6 bg-white rounded-lg shadow-md">
      {isRegistered ? (
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">会員登録が完了しました</h2>
          <p>認証メールを送信しました。メール内のリンクをクリックして認証を完了してください。</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <h2 className="text-2xl font-bold text-center">新規会員登録</h2>
          {error && <p className="text-red-500 text-center">{error}</p>}
          <div>
            <label className="block text-sm font-medium mb-1">メールアドレス</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="border rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">パスワード</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="border rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="absolute inset-y-0 right-1 flex items-center text-gray-500 hover:text-gray-700 focus:outline-none"
              >
                {showPassword ? <IoEyeOff size={24} /> : <IoEye size={24} />}
              </button>
            </div>
            {!isPasswordValid(password) && password && (
              <p className="text-red-500 text-sm mt-1">
                パスワードは8文字以上で、英字と数字を含めてください。
              </p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">パスワード（確認用）</label>
            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="border rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                type="button"
                onClick={toggleConfirmPasswordVisibility}
                className="absolute inset-y-0 right-1 flex items-center text-gray-500 hover:text-gray-700 focus:outline-none"
              >
                {showConfirmPassword ? <IoEyeOff size={24} /> : <IoEye size={24} />}
              </button>
            </div>
            {confirmPassword && confirmPassword !== password && (
              <p className="text-red-500 text-sm mt-1">
                パスワードが一致しません。
              </p>
            )}
          </div>
          <button
            type="submit"
            className={`w-full bg-green-600 text-white font-bold py-2 rounded-lg hover:bg-green-500 transition duration-200 flex justify-center items-center ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isLoading} // ローディング中はボタンを非活性に
          >
            {isLoading ? <div className="spinner"></div> : '登録'}
          </button>
        </form>
      )}
    </div>
  );
};

export default Register;
