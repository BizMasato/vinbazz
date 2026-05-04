import React from 'react';

// 左矢印ボタン
const PrevArrow: React.FC<{ onClick?: () => void }> = ({ onClick }) => (
  <button className="prev-arrow" onClick={onClick}>
    &#10094;
  </button>
);

// 右矢印ボタン
const NextArrow: React.FC<{ onClick?: () => void }> = ({ onClick }) => (
  <button className="next-arrow" onClick={onClick}>
    &#10095;
  </button>
);

export { PrevArrow, NextArrow };
