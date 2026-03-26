import React from 'react';
import { motion } from 'framer-motion';

const JobInput = ({ value, onChange }) => {
  const charCount = value.length;

  return (
    <motion.div 
      whileHover={{ y: -4, boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)' }}
      className="bg-card rounded-2xl p-6 shadow-sm border border-cardborder transition-all duration-300 group focus-within:ring-2 focus-within:ring-accent1/20 focus-within:border-accent1/50 h-full flex flex-col"
    >
      <h3 className="text-lg font-semibold text-textMain mb-4 flex justify-between items-center">
        <span>Job Description</span>
        <span className="text-xs font-normal text-textMuted bg-background px-2 py-1 rounded-md border border-cardborder transition-colors group-focus-within:bg-accent1/5 group-focus-within:text-accent1 group-focus-within:border-accent1/20">
          {charCount} chars
        </span>
      </h3>
      <textarea
        value={value}
        onChange={onChange}
        placeholder="Paste the target job description here..."
        className="w-full flex-grow min-h-[350px] resize-none bg-transparent outline-none text-textMain placeholder:text-textMuted leading-relaxed CustomScrollbar transition-colors mt-1"
        spellCheck="false"
      />
    </motion.div>
  );
};

export default JobInput;
