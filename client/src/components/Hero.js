import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <div className="text-center py-16 space-y-6">
      <motion.h1 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-5xl md:text-7xl font-extrabold text-textMain tracking-tight leading-tight"
      >
        Analyze. Match. <br className="hidden md:block"/>
        <span className="gradient-text">Get Hired.</span>
      </motion.h1>
      
      <motion.p 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="text-lg md:text-xl text-textMuted max-w-2xl mx-auto leading-relaxed"
      >
        Optimize your resume with our AI-powered ATS analyzer. Instantly find missing keywords, highlight your strengths, and increase your chances of landing your dream job.
      </motion.p>
    </div>
  );
};

export default Hero;
