// src/components/Footer.tsx
import React, { useState } from 'react';
import { FaInstagram, FaTiktok } from 'react-icons/fa';
import appSettings from '../../config/settings';

const Footer: React.FC = () => {

  const [isHovered, setIsHovered] = useState(false);
  const defaultIcon = appSettings.apiUrl + "/static/vinbazz.png";
  const hoverIcon = appSettings.apiUrl + "/static/vinbazz_on.png";

  return (
    <footer className="bg-gray-800 text-white py-4">
      <div className="container mx-auto text-center">
        {/* ロゴ */}
        <div className="mb-2">
          <a href='/'>
            {/*<img src={appSettings.apiUrl + "/static/vinbazz.png"} alt="Logo" className="h-8 mx-auto" />*/}
            <img
                src={isHovered ? hoverIcon : defaultIcon}
                alt="Icon"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="h-8 mx-auto"
              />
          </a>
        </div>
        
        {/* リンク */}
        <div className="mb-2 space-x-4">
          <a href="/privacy" className="text-sm hover:underline">プライバシーポリシー</a>
          <a href="/terms" className="text-sm hover:underline">利用規約</a>
          <button className="hover:text-gray-700">
              <FaInstagram className="h-7 w-7" />
          </button>
          <button className="hover:text-gray-700">
              <FaTiktok className="h-7 w-7" />
          </button>
        </div>

        {/* コピーライト */}
        <div className="text-sm">
          © 2024 vinbazz. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
