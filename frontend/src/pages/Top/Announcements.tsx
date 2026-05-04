// src/components/Announcements.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import appSettings from '../../config/settings';

interface Announcement {
  id: number;
  title: string;
  updated_at: Date;
}

const Announcements: React.FC = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    const fetchAnnouncements = async () => {
      try {
        const response = await axios.get(`${appSettings.apiUrl}/api/announcements/`);
        console.log(response.data); // ここでデータを確認
        setAnnouncements(response.data.slice(0, 3)); // 先頭3つを設定
      } catch (error) {
        console.error('Error fetching announcements:', error);
      }
    };

    fetchAnnouncements();
  }, []);

  return (
    <div className="bg-gray-100 py-8 px-4 md:px-8 lg:px-16">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-semibold">News</h2>
        <a href="/announcements/" className="text-gray-600 hover:underline text-lg">view more</a>
      </div>
      <ul className="space-y-4"> {/* 行間を増やす */}
        {announcements.map((announcement) => (
          <li key={announcement.id} className="flex items-center text-lg"> {/* 文字サイズを大きくする */}
            <span className="text-gray-600 mr-10 text-base">
              {new Date(announcement.updated_at).toISOString().split('T')[0].replace(/-/g, '.')}
            </span>
            <a href={`/announcements/${announcement.id}`} className="hover:underline text-base">
              {announcement.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Announcements;
