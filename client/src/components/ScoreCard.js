import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { getScoreColor, getRingColor } from '../utils/helpers';

const ScoreCard = ({ title, score, delay = 0 }) => {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  // Make sure not to set offset below 0 or above circumference safely.
  const safeScore = Math.min(Math.max(score, 0), 100);
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  useEffect(() => {
    let interval;
    const timeout = setTimeout(() => {
      let current = 0;
      const step = Math.max(1, Math.floor(safeScore / 30));
      interval = setInterval(() => {
        current += step;
        if (current >= safeScore) {
          setAnimatedScore(safeScore);
          clearInterval(interval);
        } else {
          setAnimatedScore(current);
        }
      }, 20);
    }, delay * 1000);

    return () => {
      clearTimeout(timeout);
      if (interval) clearInterval(interval);
    };
  }, [safeScore, delay]);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      className="bg-card rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-gray-100 flex flex-col items-center hover:shadow-[0_8px_30px_-4px_rgba(0,0,0,0.1)] transition-shadow duration-300"
    >
      <h4 className="text-textMuted font-semibold mb-4 text-center">{title}</h4>
      
      <div className="relative w-32 h-32 flex items-center justify-center">
        {/* Background Circle */}
        <svg className="absolute inset-0 w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle 
            cx="50" cy="50" r="38" 
            className="stroke-gray-100" 
            strokeWidth="8" fill="transparent" 
          />
          {/* Progress Circle */}
          <motion.circle 
            cx="50" cy="50" r="38" 
            className={`${getRingColor(safeScore)} transition-all duration-300 ease-out`}
            strokeWidth="8" 
            fill="transparent" 
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
          />
        </svg>
        
        <div className="text-center absolute">
          <motion.span 
            className={`text-3xl font-bold ${getScoreColor(safeScore)}`}
          >
            {animatedScore}
          </motion.span>
          <span className="text-sm text-gray-400 block">%</span>
        </div>
      </div>
    </motion.div>
  );
};

export default ScoreCard;
