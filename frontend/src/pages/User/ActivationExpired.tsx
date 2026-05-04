import React, { useState, useEffect }  from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useNavigate をインポート

const ActivationExpired: React.FC = () => {
    const navigate = useNavigate(); // useNavigate フックを使用
    const location = useLocation();
    const [isValid, setisValid] = useState(false);

    const handleGoToTop = () => {
        navigate('/'); // TOP画面へ遷移
    };

    useEffect(() => {
        // クエリパラメータからメッセージを取得
        const queryParams = new URLSearchParams(location.search);
        const message = queryParams.get('message');
        if (message === 'isvalid') {
            setisValid(true);
        }
    }, [location]);

    return (
        <div className="container mx-auto mt-10 text-center">
            {isValid ? (
                <>
                  <h1 className="text-2xl font-bold">リンクが無効です。</h1>
                  <p className="mt-4">お手数ですが、再度登録をお願いします。</p>
                </>
            ) : (
                <>
                  <h1 className="text-2xl font-bold">認証リンクの有効期限が切れています。</h1>
                  <p className="mt-4">お手数ですが、再度登録をお願いします。</p>
                </>
            )}
            <button
                className="mt-6 mb-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                onClick={handleGoToTop}
            >
                TOP画面へ
            </button>
        </div>
    );
};

export default ActivationExpired;
