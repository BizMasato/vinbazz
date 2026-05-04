// src/pages/Header.tsx
import React, { useEffect, useState } from 'react';
import { IoSearch, IoClose } from "react-icons/io5";
import { FiMenu } from 'react-icons/fi';
import axios from 'axios';
import appSettings from '../../config/settings';
import { useAuth } from '../../services/AuthContext';
import UserIcon from '../../components/UserIcon';
import HeartIcon from '../../components/HeartIcon';

const Header: React.FC = () => {
  const [categories, setCategories] = useState<any[]>([]);
  const [storeAreas, setStoreAreas] = useState<any[]>([]);
  const [isSearchVisible, setIsSearchVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('category'); // タブの選択状態
  const [isHovered, setIsHovered] = useState(false);
  const { isLoggedIn, username } = useAuth();
  const [query, setQuery] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get(`${appSettings.apiUrl}/api/header/categories/`);
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    const fetchStoreAreas = async () => {
      try {
        const response = await axios.get(`${appSettings.apiUrl}/api/header/stores/`);
        setStoreAreas(response.data);
      } catch (error) {
        console.error('Error fetching store:', error);
      }
    };

    fetchCategories();
    fetchStoreAreas();
  }, []);

  const toggleSearch = () => {
    setIsSearchVisible(!isSearchVisible);
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${appSettings.apiUrl}/api/logout`, {}, { withCredentials: true });
      window.location.href = '/login?message=logged_out';
    } catch (error) {
      console.error("ログアウトエラー:", error);
    }
  };

  const handleClear = () => {
    setQuery('');
  };

  const defaultIcon = appSettings.apiUrl + "/static/vinbazz.png";
  const hoverIcon = appSettings.apiUrl + "/static/vinbazz_on.png";

  return (
    <>
      <header className="bg-white shadow-md p-4 fixed top-0 left-0 w-full z-50" style={{ height: '64px', paddingTop: '16px' }}>
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <a href='/'>
              {/*<img src={appSettings.apiUrl + "/static/vinbazz.png"} alt="Logo" className="h-8 mr-4" />*/}
              <img
                src={isHovered ? hoverIcon : defaultIcon}
                alt="Icon"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="h-8 mr-4"
              />
            </a>
          </div>

          <nav className="flex space-x-4 lg:space-x-8">
            {/* Search Vintage Dropdown */}
            <div className="group relative">
              <button className="text-black py-2 px-2 font-medium rounded-md transition-all duration-300 transform hover:bg-black hover:text-white hover:scale-95 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-black-500 focus:ring-opacity-50">
                古着を探す
              </button>
              <div className="invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-all duration-300 absolute left-0 mt-2 w-80 bg-white text-black rounded-lg shadow-md p-4invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-all duration-300 absolute left-0 mt-2 w-48 bg-white text-black rounded-md shadow-md transform scale-95 group-hover:scale-100 group-hover:translate-x-0 opacity-0 group-hover:opacity-100">
                {/* タブ */}
                <div className="flex border-b mb-4">
                  <button
                    className={`flex-1 py-2 text-center ${activeTab === 'category' ? 'border-b-2 border-black-700 text-black-500' : 'text-gray-200'}`}
                    onClick={() => setActiveTab('category')}
                  >
                    Category
                  </button>
                  <button
                    className={`flex-1 py-2 text-center ${activeTab === 'store' ? 'border-b-2 border-black-700 text-black-500' : 'text-gray-200'}`}
                    onClick={() => setActiveTab('store')}
                  >
                    Store
                  </button>
                </div>

                {/* タブのコンテンツ */}
                {activeTab === 'category' ? (
                  <ul className="space-y-2">
                    <li className="py-2">
                      <a
                        href='/clothes'
                        className="block px-4 py-2 font-bold text-gray-800 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                      >
                        All
                      </a>
                    </li>
                    {categories.map((category) => (
                      <li key={category.id} className="py-2">
                        <a
                          href={`/clothes?category=${category.id}`}
                          className="block px-4 py-2 font-bold text-gray-800 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                        >
                          {category.name}
                        </a>
                        {category.children && category.children.length > 0 && (
                          <ul className="pl-6 mt-2 space-y-1">
                            {category.children.map((child: any) => (
                              <li key={child.id} className="py-1">
                                <a
                                  href={`/clothes?category=${child.id}`}
                                  className="block px-4 py-2 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                                >
                                  {child.name}
                                </a>
                              </li>
                            ))}
                          </ul>
                        )}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <ul className="space-y-2">
                    <li className="py-2">
                      <a
                        href='/clothes'
                        className="block px-4 py-2 font-bold text-gray-800 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                      >
                        All
                      </a>
                    </li>
                    {storeAreas.map((area) => (
                      <li key={area.id} className="py-2">
                        <a
                          href={`/clothes?area=${area.id}`}
                          className="block px-4 py-2 font-bold text-gray-800 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                        >
                          {area.name}
                        </a>
                        {area.stores && area.stores.length > 0 && (
                          <ul className="pl-6 mt-2 space-y-1">
                            {area.stores.map((store: any) => (
                              <li key={store.id} className="py-1">
                                <a
                                  href={`/clothes?store=${store.id}`}
                                  className="block px-4 py-2 hover:bg-gray-100 hover:text-gray-700 hover:underline rounded-lg"
                                >
                                  {store.name}
                                </a>
                              </li>
                            ))}
                          </ul>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            {/* Static Links */}
            <a href="/about/" className="hidden lg:inline-block font-medium text-black py-2 px-2 rounded-md transition-all duration-300 transform hover:bg-black hover:text-white hover:scale-95 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-black-500 focus:ring-opacity-50">About</a>
            <a href="/topics/" className="hidden lg:inline-block font-medium text-black py-2 px-2 rounded-md transition-all duration-300 transform hover:bg-black hover:text-white hover:scale-95 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-black-500 focus:ring-opacity-50">Topics</a>
          </nav>

          {/* Search & Icons */}
          <div className="flex items-center space-x-4">
            <button onClick={toggleSearch} className="hover:text-gray-700 lg:hidden">
              <IoSearch className="h-7 w-7" />
            </button>
            <div className="hidden lg:block w-80 relative">
              <input 
                type="text" 
                placeholder="キーワードから検索" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="border rounded-full px-4 py-2 w-full pl-10 pr-10"
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                <IoSearch />
              </span>
              <button 
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
                onClick={handleClear}
              >
                <IoClose />
              </button>
            </div>
            <button className="hover:text-gray-700">
              <a href="/favorite/">
                <HeartIcon />
              </a>
            </button>

            {/* User Icon with conditional dropdown */}
            <div className="group relative">
              <a href={isLoggedIn ? "/profile/" : "/login/"} className="hover:text-gray-700">
                <UserIcon />
              </a>
              {isLoggedIn && (
                <div className="invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-all duration-300 absolute right-0 mt-2 w-48 bg-white border rounded-lg shadow-lg z-10">
                  <div className="p-2 font-bold text-gray-800">{username}様</div>
                  <a href="/profile/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">プロフィールを表示</a>
                  <a href="/favorite/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">お気に入り</a>
                  <button 
                    onClick={handleLogout} 
                    className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
                  >
                    ログアウト
                  </button>
                </div>
              )}
              {!isLoggedIn && (
                <div className="invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-all duration-300 absolute right-0 mt-2 w-48 bg-white border rounded-lg shadow-lg z-10">
                  <a href="/login/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">ログイン</a>
                  <a href="/register/" className="block px-4 py-2 text-gray-700 hover:bg-gray-100">新規会員登録</a>
                </div>
              )}
            </div>

            <button className="hover:text-gray-700">
              <FiMenu className="h-8 w-8" />
            </button>
          </div>
        </div>

        {/* Mobile Search Bar */}
        {isSearchVisible && (
          <div className="lg:hidden mt-4 relative">
            <input type="text" placeholder="キーワードから検索" className="w-full border rounded-full px-4 py-2 pl-10 pr-10" />
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
              <IoSearch />
            </span>
            <button 
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
              onClick={handleClear}
            >
              <IoClose />
            </button>
          </div>
        )}
      </header>

      {/* ヘッダーの高さに合わせて下のコンテンツにパディングを追加 */}
      <div style={{ paddingTop: '64px' }} />
    </>
  );
};

export default Header;
