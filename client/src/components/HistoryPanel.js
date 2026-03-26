import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, ChevronRight, CheckCircle2, Trash2 } from 'lucide-react';

const HistoryPanel = ({ onSelectHistory }) => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('hiresight_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse history');
      }
    }
  }, []);

  const handleDelete = (e, index) => {
    e.stopPropagation();
    const updated = [...history];
    updated.splice(index, 1);
    setHistory(updated);
    localStorage.setItem('hiresight_history', JSON.stringify(updated));
  };

  if (history.length === 0) return null;

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-textMain flex items-center gap-2 mb-4">
        <Clock className="w-5 h-5 text-textMuted" /> Recent Analyses
      </h3>
      
      <div className="space-y-3">
        {history.map((item, index) => (
          <motion.div 
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            whileHover={{ scale: 1.01 }}
            onClick={() => onSelectHistory(item)}
            className="p-4 bg-card rounded-xl border border-cardborder shadow-sm cursor-pointer hover:border-accent1/50 transition-colors group flex justify-between items-center"
          >
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-textMain truncate max-w-[200px] md:max-w-xs text-sm">
                  Match Score: <span className="text-accent1">{item.results.matchScore}%</span>
                </span>
                <span className="text-xs text-textMuted">• {new Date(item.timestamp).toLocaleDateString()}</span>
              </div>
              <p className="text-xs text-textMuted truncate max-w-[250px] md:max-w-md">
                Job: {item.jobDescription.substring(0, 50)}...
              </p>
            </div>
            
            <div className="flex items-center gap-3">
               <button 
                 onClick={(e) => handleDelete(e, index)}
                 className="p-2 text-textMuted hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
               >
                 <Trash2 className="w-4 h-4" />
               </button>
               <ChevronRight className="w-5 h-5 text-textMuted group-hover:text-accent1 transition-colors" />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default HistoryPanel;
