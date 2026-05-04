import React from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate をインポート

const ActivationComplete: React.FC = () => {
    const navigate = useNavigate(); // useNavigate フックを使用

    const handleGoToTop = () => {
        navigate('/'); // TOP画面へ遷移
    };

    return (
        <div className="container mx-auto mt-10 text-center">
            <h1 className="text-2xl font-bold">認証が完了しました！</h1>
            <p className="mt-4">ご登録いただきありがとうございます。メールアドレスの認証が成功しました。</p>
            <button
                className="mt-6 mb-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                onClick={handleGoToTop}
            >
                TOP画面へ
            </button>
        </div>
    );
};

export default ActivationComplete;
