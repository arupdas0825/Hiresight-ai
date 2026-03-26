import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileText, X, Loader2 } from 'lucide-react';
import { uploadPdf } from '../services/api';

const FileUpload = ({ onFileParsed, onError }) => {
  const [isDragActive, setIsDragActive] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [fileName, setFileName] = useState('');
  const fileInputRef = useRef(null);

  const handleFile = async (file) => {
    if (!file) return;
    if (file.type !== 'application/pdf') {
      onError('Please upload a valid PDF file.');
      return;
    }

    setFileName(file.name);
    setIsParsing(true);
    
    try {
      const data = await uploadPdf(file);
      onFileParsed(data.text);
    } catch (err) {
      onError(err.message);
      setFileName('');
    } finally {
      setIsParsing(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragActive(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const clearFile = (e) => {
    e.stopPropagation(); // prevent bubbling to the click container
    setFileName('');
    if (fileInputRef.current) fileInputRef.current.value = '';
    onFileParsed(''); // clear parent text
  };

  return (
    <div className="mb-4">
      <input 
        type="file" 
        accept="application/pdf" 
        ref={fileInputRef}
        onChange={(e) => handleFile(e.target.files[0])}
        className="hidden"
        id="file-upload"
      />
      
      {!fileName && !isParsing ? (
        <motion.div
           whileHover={{ y: -2 }}
           onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
           onDragLeave={() => setIsDragActive(false)}
           onDrop={handleDrop}
           onClick={() => fileInputRef.current.click()}
           className={`relative p-6 border-2 border-dashed rounded-xl cursor-pointer transition-colors duration-200 flex flex-col items-center justify-center gap-2
            ${isDragActive ? 'border-accent1 bg-accent1/5' : 'border-cardborder bg-card'}`
           }
        >
          <UploadCloud className={`w-8 h-8 ${isDragActive ? 'text-accent1' : 'text-textMuted'}`} />
          <p className="text-sm font-medium text-textMain">Click to upload PDF or drag and drop</p>
          <p className="text-xs text-textMuted">Automatically extracts your resume text</p>
        </motion.div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 rounded-xl border border-accent1/30 bg-accent1/5 flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
            {isParsing ? (
               <Loader2 className="w-5 h-5 text-accent1 animate-spin" />
            ) : (
               <FileText className="w-5 h-5 text-accent1" />
            )}
            <span className="text-sm font-medium text-textMain max-w-[200px] truncate">
              {isParsing ? 'Extracting text...' : fileName}
            </span>
          </div>
          
          {!isParsing && (
            <button 
              onClick={clearFile}
              className="p-1 rounded-md hover:bg-red-50 hover:text-red-500 text-textMuted transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default FileUpload;
