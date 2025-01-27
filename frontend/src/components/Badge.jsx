import React from 'react'
import { PiMedalFill } from "react-icons/pi";

const Badge = ({ badge }) => {

  let badgeColor = '';
  if (badge.tier === 'bronze') {
    badgeColor = 'text-amber-700';
  } else if (badge.tier === 'silver') {
    badgeColor = 'text-gray-400';
  } else if (badge.tier === 'gold') {
    badgeColor = 'text-yellow-400';
  }

  return (
    <div className='flex flex-col items-center'>
      <PiMedalFill className={`text-4xl ${badgeColor}`} />
      <p className='text-center'>{badge.badge_name}</p>
    </div>
  )
}

export default Badge