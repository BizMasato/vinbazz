import { FaRegUser, FaUser } from 'react-icons/fa';
import { useState } from 'react';

const UserIcon = () => {
  // ホバー状態を管理するステート
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}  // ホバー時
      onMouseLeave={() => setHovered(false)} // ホバー解除時
      className="text-2xl cursor-pointer"
    >
      {hovered ? <FaUser className='h-6 w-6' /> : <FaRegUser className='h-6 w-6' />}  {/* ホバー状態に応じてアイコンを切り替え */}
    </div>
  );
};

export default UserIcon;
