import { FaRegHeart, FaHeart } from 'react-icons/fa6';
import { useState } from 'react';

const HeartIcon = () => {
  // ホバー状態を管理するステート
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}  // ホバー時
      onMouseLeave={() => setHovered(false)} // ホバー解除時
      className="text-2xl cursor-pointer"
    >
      {hovered ? <FaHeart className='h-6 w-6' /> : <FaRegHeart className='h-6 w-6' />}  {/* ホバー状態に応じてアイコンを切り替え */}
    </div>
  );
};

export default HeartIcon;
