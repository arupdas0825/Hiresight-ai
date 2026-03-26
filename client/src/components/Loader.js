import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FileSearch, Target, Cpu, CheckCircle2 } from 'lucide-react';

const steps = [
  { icon: FileSearch, text: "Parsing resume structure..." },
  { icon: Target, text: "Extracting critical keywords..." },
  { icon: Cpu, text: "Matching with job description..." },
  { icon: CheckCircle2, text: "Generating AI insight report..." }
];

const Loader = () => {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1500); // 1.5s per step
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-md mx-auto bg-card rounded-2xl p-8 shadow-sm border border-gray-100">
      <div className="flex justify-center mb-8">
        <div className="relative">
          <motion.div 
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 rounded-full border-4 border-gray-100 border-t-accent1"
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <Cpu className="w-6 h-6 text-accent2 animate-pulse" />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === activeStep;
          const isPast = index < activeStep;
          
          return (
            <motion.div 
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: isActive || isPast ? 1 : 0.4, x: 0 }}
              className="flex items-center gap-4"
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors duration-300 ${isPast ? 'bg-green-100 text-green-600' : isActive ? 'bg-blue-100 text-blue-600 animate-pulse' : 'bg-gray-100 text-gray-400'}`}>
                <Icon className="w-4 h-4" />
              </div>
              <span className={`font-medium transition-colors duration-300 ${isPast || isActive ? 'text-textMain' : 'text-gray-400'}`}>
                {step.text}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default Loader;
