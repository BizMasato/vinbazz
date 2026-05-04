import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FavoriteButton from '../../components/FavoriteButton';
import appSettings from '../../config/settings';

interface Store {
    id: number;
    name: string;
    image: string;
    is_favorite: boolean;
}

interface Area {
    id: number;
    name: string;
}

const Stores: React.FC = () => {
    const [areas, setAreas] = useState<Area[]>([]);
    const [stores, setStores] = useState<Store[]>([]);
    const [selectedArea, setSelectedArea] = useState<number | null>(0);

    // エリア情報を取得
    useEffect(() => {
        const fetchAreas = async () => {
            try {
                const response = await axios.get(`${appSettings.apiUrl}/api/areas/`);
                // "All"タブをエリアのリストの先頭に追加
                setAreas([{ id: 0, name: "All" }, ...response.data]);
            } catch (error) {
                console.error('エリアの取得に失敗しました', error);
            }
        };
        fetchAreas();
    }, []);

    // 選択されたエリアの店舗情報を取得
    useEffect(() => {
        const fetchStores = async () => {
            try {
                const response = await axios.get(`${appSettings.apiUrl}/api/stores/`, {
                    params: selectedArea !== 0 ? { area: selectedArea } : {},
                    withCredentials: true
                });
                setStores(response.data);
            } catch (error) {
                console.error('店舗情報の取得に失敗しました', error);
            }
        };
        fetchStores();
    }, [selectedArea]);

    return (
        <div className="container mx-auto p-4">
            {/* エリア切り替えタブ */}
            <div className="flex space-x-4 mb-4">
                {areas.map((area) => (
                  <button
                    key={area.id}
                    className={`px-4 py-2 ${selectedArea === area.id ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} rounded`}
                    onClick={() => setSelectedArea(area.id)}
                  >
                    {area.name}
                  </button>
                ))}
            </div>

            {/* 店舗リスト */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {stores.map((store) => (
                    <div key={store.id} className="border rounded p-4 shadow-lg">
                        <img
                            src={store.image}
                            alt={`${store.name}の画像`}
                            className="w-full h-40 object-cover rounded"
                        />
                        <h2 className="text-lg font-bold mt-2">{store.name}</h2>
                        <div className="flex justify-between items-center mt-2">
                            <button className="bg-blue-500 text-white px-3 py-1 rounded">詳細を見る</button>
                            <button className="bg-green-500 text-white px-3 py-1 rounded">商品を見る</button>
                            {/* お気に入りボタン */}
                            <FavoriteButton itemId={store.id} isFavorite={store.is_favorite} type="stores" />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Stores;
