import React from 'react';
import { motion } from 'framer-motion';
import ThemeToggle from './ThemeToggle';

const Navbar = () => {
  return (
    <motion.nav 
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky top-0 z-50 glassmorphism border-b border-cardborder px-6 py-4 flex justify-between items-center"
    >
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-accent1 to-accent2 flex items-center justify-center text-white font-bold text-xl shadow-sm">
          H
        </div>
        <span className="text-xl font-bold tracking-tight text-textMain">
          HireSight <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent1 to-accent2">AI</span>
        </span>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 bg-card px-3 py-1.5 rounded-full border border-cardborder shadow-sm transition-all hover:shadow-md">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-xs font-semibold text-textMuted uppercase tracking-wider">AI Powered</span>
        </div>
        <ThemeToggle />
      </div>
    </motion.nav>
  );
};

export default Navbar;
