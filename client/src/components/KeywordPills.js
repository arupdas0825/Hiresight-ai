import React from 'react';
import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';

const KeywordPills = ({ keywords, type }) => {
  if (!keywords || keywords.length === 0) return <p className="text-textMuted italic text-sm">None detected.</p>;

  const isFound = type === 'found';

  return (
    <div className="flex flex-wrap gap-2">
      {keywords.map((keyword, index) => (
        <motion.span
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.05 }}
          key={index}
          className={`
            inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium border shadow-sm
            ${isFound 
              ? 'bg-green-50 text-green-700 border-green-200 hover:bg-green-100' 
              : 'bg-red-50 text-red-700 border-red-200 hover:bg-red-100'}
            transition-colors
          `}
        >
          {isFound ? (
            <Check className="w-3.5 h-3.5" />
          ) : (
             <X className="w-3.5 h-3.5" />
          )}
          {keyword}
        </motion.span>
      ))}
    </div>
  );
};

export default KeywordPills;
