import React, { useEffect, useState } from 'react';
import axios from 'axios';
import appSettings from '../config/settings';
import { IoIosHeart, IoIosHeartEmpty } from 'react-icons/io';

interface FavoriteButtonProps {
    itemId: number;       // ClothesやStoresのID
    isFavorite: boolean;  // お気に入りかどうか
    type: 'clothes' | 'stores'; // エンドポイントを指定するためのタイプ
}

const FavoriteButton: React.FC<FavoriteButtonProps> = ({ itemId, isFavorite, type }) => {
    const [favorite, setFavorite] = useState(isFavorite);
    const [csrfToken, setCsrfToken] = useState('');

    useEffect(() => {
        const fetchCsrfToken = async () => {
            const response = await axios.get(`${appSettings.apiUrl}/api/get-csrf-token/`, { withCredentials: true });
            setCsrfToken(response.data.csrfToken);
        };
        fetchCsrfToken();
    }, []);

    const handleFavoriteToggle = async () => {
        try {
            const url = `${appSettings.apiUrl}/api/${type}/favorite/`;  // typeを使ってURLを動的に設定
            if (favorite) {
                // お気に入り解除リクエスト
                await axios.delete(
                    url,
                    { data: { item_id: itemId }, withCredentials: true, headers: { 'X-CSRFToken': csrfToken }}
                );
                setFavorite(false);
            } else {
                // お気に入り追加リクエスト
                await axios.post(
                    url,
                    { item_id: itemId },
                    { withCredentials: true, headers: { 'X-CSRFToken': csrfToken }}
                );
                setFavorite(true);
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
            alert('お気に入りの処理に失敗しました。ログインしてください。');
        }
    };

    return (
        <button onClick={handleFavoriteToggle}>
            {favorite ? <IoIosHeart className='h-6 w-6' /> : <IoIosHeartEmpty className='h-6 w-6' />}
        </button>
    );
};

export default FavoriteButton;
