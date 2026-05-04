// src/pages/Home.tsx
import React from 'react';
import Banner from './Banner';
import RecommendedClothes from './RecommendedClothes';
import RecommendedStores from './RecommendedStores';
import Announcements from './Announcements';
import Stores from './Stores';
import ContactUs from './ContactUs';

const Home: React.FC = () => {
  return (
    <div>
      <Banner />
      <RecommendedClothes />
      <RecommendedStores />
      <Announcements />
      <Stores />
      <ContactUs />
    </div>
  );
};

export default Home;
