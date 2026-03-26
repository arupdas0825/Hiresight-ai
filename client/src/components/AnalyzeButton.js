import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';

const AnalyzeButton = ({ onClick, disabled, loading }) => {
  return (
    <motion.button
      whileHover={!disabled ? { scale: 1.05 } : {}}
      whileTap={!disabled ? { scale: 0.95 } : {}}
      onClick={onClick}
      disabled={disabled}
      className={`
        relative overflow-hidden group px-8 py-4 rounded-full font-bold text-lg text-white
        transition-all duration-300 shadow-lg flex items-center gap-2
        ${disabled 
          ? 'bg-gray-300 cursor-not-allowed shadow-none' 
          : 'bg-gradient-to-r from-accent1 to-accent2 hover:shadow-[0_0_20px_rgba(37,99,235,0.4)]'}
      `}
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Analyzing...
        </>
      ) : (
        <>
          <Sparkles className="w-5 h-5 group-hover:animate-pulse" />
          Analyze Match
        </>
      )}
      
      {!disabled && !loading && (
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 rounded-full" />
      )}
    </motion.button>
  );
};

export default AnalyzeButton;
