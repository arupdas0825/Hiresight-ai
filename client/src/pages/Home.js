import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from '../components/Hero';
import ResumeInput from '../components/ResumeInput';
import JobInput from '../components/JobInput';
import AnalyzeButton from '../components/AnalyzeButton';
import Loader from '../components/Loader';
import ResultSection from '../components/ResultSection';
import HistoryPanel from '../components/HistoryPanel';
import { analyzeResume } from '../services/api';

const Home = () => {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!resumeText.trim() || !jobDescription.trim()) {
      setError('Please provide both resume and job description.');
      return;
    }

    setError('');
    setLoading(true);
    setResults(null);

    try {
      const data = await analyzeResume(resumeText, jobDescription);
      setResults(data);
      
      // Save history to local storage
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        resumeText,
        jobDescription,
        results: data
      };
      
      const existingHistory = JSON.parse(localStorage.getItem('hiresight_history') || '[]');
      const updatedHistory = [historyItem, ...existingHistory].slice(0, 50); // Keep last 50
      localStorage.setItem('hiresight_history', JSON.stringify(updatedHistory));
      
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to analyze. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectHistory = (historyItem) => {
    setResumeText(historyItem.resumeText);
    setJobDescription(historyItem.jobDescription);
    setResults(historyItem.results);
    setError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleError = (msg) => {
    setError(msg);
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-12 pb-20 relative">
      <Hero />
      
      <div className="grid lg:grid-cols-12 gap-8">
        {/* Left Col: Inputs */}
        <div className="lg:col-span-8 flex flex-col gap-8">
          <div className="grid md:grid-cols-2 gap-8 h-full">
            <ResumeInput 
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              onFileParsed={(text) => { setResumeText(text); setError(''); }}
              onError={handleError}
            />
            <JobInput 
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>
        </div>
        
        {/* Right Col: History */}
        <div className="lg:col-span-4">
           {/* If results exist, maybe hide history or push it down */}
           <HistoryPanel onSelectHistory={handleSelectHistory} />
        </div>
      </div>

      <AnimatePresence>
        {error && (
          <motion.div 
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-200 shadow-sm text-center max-w-2xl mx-auto"
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex justify-center relative z-20">
        <AnalyzeButton 
          onClick={handleAnalyze} 
          disabled={loading || !resumeText.trim() || !jobDescription.trim()} 
          loading={loading}
        />
      </div>

      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            className="flex justify-center"
          >
            <Loader />
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {results && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            <ResultSection results={results} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Home;
