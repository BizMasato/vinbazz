import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import FavoriteButton from '../../components/FavoriteButton';
import ClothesBreadcrumb from '../../components/ClothesBreadcrumb';
import appSettings from '../../config/settings';

interface Clothes {
    id: number;
    name: string;
    price: number;
    image: string;
    is_favorite: boolean;
    store: {
        id: number;
        name: string;
    };
}

const ClothesList: React.FC = () => {
    const [clothesList, setClothesList] = useState<Clothes[]>([]);
    const location = useLocation();
    const [isLoading, setIsLoading] = useState(true); // ローディング状態
    const [breadcrumb, setBreadcrumb] = useState<any>(null);

    useEffect(() => {
        const fetchClothes = async () => {
            try {
                // クエリパラメータから検索条件を取得
                const query = new URLSearchParams(location.search);
                const filters = {
                    store_id: query.get('store'),
                    area_id: query.get('area'),
                    category_id: query.get('category'),
                };
                // フィルタのオブジェクトからクエリ文字列を作成
                const filterQuery = Object.entries(filters)
                    .filter(([, value]) => value !== null)
                    .map(([key, value]) => `${key}=${value}`)
                    .join('&');
                const url = `${appSettings.apiUrl}/api/allclothes/${filterQuery ? '?' + filterQuery : ''}`;
                const response = await axios.get(url, { withCredentials: true });
                setClothesList(response.data);
            } catch (error) {
                console.error('Error fetching clothes:', error);
            } finally {
            setIsLoading(false); // ローディング完了
        }
        };

        fetchClothes();
    }, [location.search]);

    const handleBreadcrumbLoaded = (breadcrumb: any) => {
        setBreadcrumb(breadcrumb); // Breadcumbデータを設定
      };

    return (
        <div className="container mx-auto p-4">
            <ClothesBreadcrumb 
                store_id={new URLSearchParams(location.search).get('store') || undefined}
                area_id={new URLSearchParams(location.search).get('area') || undefined}
                category_id={new URLSearchParams(location.search).get('category') || undefined}
                onBreadcrumbLoaded={handleBreadcrumbLoaded} // コールバックでデータを親に渡す
            />

            {breadcrumb ? (
                <h1 className="italic text-2xl font-medium mb-4">{breadcrumb}</h1>
            ) : (
                <h1 className="italic text-2xl font-medium mb-4">【すべての商品】</h1>
            )}

            {isLoading ? (
                <p className="text-gray-500 text-center mt-4 mb-4">Loading...</p> // ローディング中のメッセージ
            ) : clothesList.length === 0 ? (
                <p className="text-red-500 text-left mt-4 mb-4">表示できる古着が見つかりませんでした。</p>
            ) : (
                <div className="grid grid-cols-3 gap-4">
                    {clothesList.map((item) => (
                        <div key={item.id} className="border rounded-lg p-4 shadow-lg transition-transform transform hover:scale-105 duration-300">
                            <div className="overflow-hidden rounded-lg">
                                <img 
                                    src={item.image} 
                                    alt={item.name} 
                                    className="w-full h-42 object-cover rounded md:h-64 md:object-contain md:aspect-square"
                                />
                            </div>
                            <h1 className="text-xs font-semibold text-slate-400 mt-2 text-left hover:underline">{item.store.name}</h1>
                            <h2 className="text-sm font-semibold mt-1 text-center hover:underline">{item.name}</h2>
                            <p className="text-base mt-1 text-center">
                                ¥{item.price.toLocaleString()}
                            </p>
                            <div className="flex justify-end mt-2">
                                <FavoriteButton itemId={item.id} isFavorite={item.is_favorite} type="clothes" />
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ClothesList;
