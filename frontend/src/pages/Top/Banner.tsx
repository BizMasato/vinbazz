// Banner.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Slider from 'react-slick';
import appSettings from '../../config/settings';
import '../../styles/Banner.css';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { PrevArrow, NextArrow } from '../../components/Arrows'

interface Banner {
  id: number;
  title: string;
  link:  string;
  image_url: string; // Djangoから取得する画像のURL
}

const BannerComponent: React.FC = () => {
  const [banners, setBanners] = useState<Banner[]>([]);

  useEffect(() => {
    const fetchBanners = async () => {
      try {
        const response = await axios.get(`${appSettings.apiUrl}/api/banners/`);
        console.log(response.data); // ここでデータを確認
        setBanners(response.data.slice(0, 5)); // 先頭5枚を設定
      } catch (error) {
        console.error('Error fetching banners:', error);
      }
    };

    fetchBanners();
  }, []);

  const sliderSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    arrows: true, // 矢印を表示
    prevArrow: <PrevArrow />,
    nextArrow: <NextArrow />,
    responsive: [
      {
        breakpoint: 768, // スマホの場合
        settings: {
          slidesToShow: 1,
          centerMode: true, // 中央のスライドを強調
          centerPadding: '10%', // スマホ用に少し縮小（必要に応じて調整）
        },
      },
    ],
  };

  return (
    <div className="banner-slider">
      <Slider {...sliderSettings}>
        {banners.map((banner) => (
          <div key={banner.id} className="banner-item">
            <a href={banner.link}>
              <img src={banner.image_url} alt={banner.title} className="w-full h-auto" />
            </a>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default BannerComponent;
