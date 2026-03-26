import React from 'react';
import { motion } from 'framer-motion';
import FileUpload from './FileUpload';

const ResumeInput = ({ value, onChange, onFileParsed, onError }) => {
  const charCount = value.length;

  return (
    <motion.div 
      whileHover={{ y: -4, boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)' }}
      className="bg-card rounded-2xl p-6 shadow-sm border border-cardborder transition-all duration-300 group focus-within:ring-2 focus-within:ring-accent1/20 focus-within:border-accent1/50 flex flex-col items-stretch h-full"
    >
      <h3 className="text-lg font-semibold text-textMain mb-4 flex justify-between items-center">
        <span>Your Resume</span>
        <span className="text-xs font-normal text-textMuted bg-background px-2 py-1 rounded-md border border-cardborder transition-colors group-focus-within:bg-accent1/5 group-focus-within:text-accent1 group-focus-within:border-accent1/20">
          {charCount} chars
        </span>
      </h3>
      
      <FileUpload onFileParsed={onFileParsed} onError={onError} />

      <textarea
        value={value}
        onChange={onChange}
        placeholder="Or paste your resume content here manually..."
        className="w-full flex-grow min-h-[250px] md:min-h-[350px] resize-none bg-transparent outline-none text-textMain placeholder:text-textMuted leading-relaxed CustomScrollbar transition-colors"
        spellCheck="false"
      />
    </motion.div>
  );
};

export default ResumeInput;
