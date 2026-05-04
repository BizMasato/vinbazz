import React, { useEffect, useState } from 'react';
import axios from 'axios';
import appSettings from '../config/settings';

interface BreadcrumbData {
    type: 'store' | 'area' | 'category';
    id: number;
    name: string;
    hierarchy?: { id: number; name: string }[]; // 階層構造用
}

interface ClothesBreadcrumbProps {
    store_id?: string;
    area_id?: string;
    category_id?: string;
    onBreadcrumbLoaded?: (breadcrumb: BreadcrumbData) => void; // 親コンポーネントにデータを渡すためのコールバック
}

const ClothesBreadcrumb: React.FC<ClothesBreadcrumbProps> = ({ store_id, area_id, category_id, onBreadcrumbLoaded }) => {
    const [breadcrumbData, setBreadcrumbData] = useState<BreadcrumbData | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchBreadcrumbData = async () => {
            try {
                let url = `${appSettings.apiUrl}/api/ClothesBreadcrumb/`;
                if (store_id) url += `?store_id=${store_id}`;
                else if (area_id) url += `?area_id=${area_id}`;
                else if (category_id) url += `?category_id=${category_id}`;

                const response = await axios.get(url, { withCredentials: true });
                setBreadcrumbData(response.data);  // データを設定

                // 親コンポーネントにデータを渡す
                if (onBreadcrumbLoaded) {
                    onBreadcrumbLoaded(response.data.title);
                }

            } catch (error) {
                console.error('Error fetching breadcrumb data:', error);
            } finally {
                setIsLoading(false); // ローディング完了
            }
        };

        fetchBreadcrumbData();
    }, [store_id, area_id, category_id, onBreadcrumbLoaded]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!breadcrumbData) {
        return <div style={{ color: 'red' }}>パンくずリストのデータが見つかりませんでした。</div>;
    }

    return (
        <nav className="text-sm text-gray-500 mb-4">
            <a href="/" className="hover:underline">Top</a> {'>'}{' '}
            {breadcrumbData.type === 'store' && (
                <>
                    <a href="/stores" className="hover:underline">Store</a> {'>'}{' '}
                    <span className="text-gray-700">
                        <a href={`/clothes?store=${breadcrumbData.id}`} className="hover:underline">{breadcrumbData.name}</a>
                    </span>
                </>
            )}
            {breadcrumbData.type === 'area' && (
                <>
                    <a href="/areas" className="hover:underline">Area</a> {'>'}{' '}
                    <span className="text-gray-700">
                        <a href={`/clothes?area=${breadcrumbData.id}`} className="hover:underline">{breadcrumbData.name}</a>
                    </span>
                </>
            )}
            {breadcrumbData.type === 'category' && breadcrumbData.hierarchy && (
                <>
                    <a href="/categories" className="hover:underline">Category</a> {'>'}{' '}
                    {breadcrumbData.hierarchy.map((cat, index) => (
                        <span key={cat.id}>
                            {index > 0 && ' > '}
                            <a href={`/clothes?category=${cat.id}`} className="hover:underline">{cat.name}</a>
                        </span>
                    ))}
                </>
            )}
        </nav>
    );
};

export default ClothesBreadcrumb;
