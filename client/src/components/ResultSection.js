import React from 'react';
import ScoreCard from './ScoreCard';
import KeywordPills from './KeywordPills';
import { CheckCircle, AlertTriangle, Lightbulb } from 'lucide-react';

const ResultSection = ({ results }) => {
  return (
    <div className="space-y-8 mt-12 bg-white rounded-3xl p-6 md:p-10 shadow-[0_8px_30px_-4px_rgba(0,0,0,0.05)] border border-gray-100 relative overflow-hidden">
      {/* Decorative gradient blur in background */}
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-accent1 opacity-5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-accent2 opacity-5 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-textMain mb-3">Analysis Complete</h2>
          <p className="text-textMuted max-w-2xl mx-auto text-lg leading-relaxed">{results.summary}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <ScoreCard title="Overall Match" score={results.matchScore || 0} delay={0.1} />
          <ScoreCard title="ATS Score" score={results.atsScore || 0} delay={0.3} />
          <ScoreCard title="Impact Score" score={results.impactScore || 0} delay={0.5} />
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2 text-textMain">
              <span className="w-8 h-8 rounded-lg bg-green-100 text-green-600 flex items-center justify-center">
                <CheckCircle className="w-5 h-5" />
              </span>
              Keywords Found
            </h3>
            <div className="p-5 bg-gray-50 rounded-2xl border border-gray-100 min-h-[100px]">
               <KeywordPills keywords={results.foundKeywords} type="found" />
            </div>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2 text-textMain">
              <span className="w-8 h-8 rounded-lg bg-red-100 text-red-600 flex items-center justify-center">
                 <AlertTriangle className="w-5 h-5" />
              </span>
              Missing Keywords
            </h3>
            <div className="p-5 bg-gray-50 rounded-2xl border border-gray-100 min-h-[100px]">
               <KeywordPills keywords={results.missingKeywords} type="missing" />
            </div>
          </div>
        </div>

        <div className="space-y-6">
           <h3 className="text-lg font-semibold flex items-center gap-2 text-textMain">
              <span className="w-8 h-8 rounded-lg bg-yellow-100 text-yellow-600 flex items-center justify-center">
                 <Lightbulb className="w-5 h-5" />
              </span>
              Actionable Insights
            </h3>
            
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-card p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-green-700 mb-4 flex items-center gap-2"><CheckCircle className="w-4 h-4"/> Strengths</h4>
                <ul className="space-y-3 text-sm text-textMuted">
                  {results.strengths?.map((s, i) => <li key={i} className="flex gap-3 leading-snug"><span className="text-green-500 flex-shrink-0 mt-0.5">•</span> {s}</li>)}
                  {(!results.strengths || results.strengths.length === 0) && <li className="text-gray-400 italic">No particular strengths found.</li>}
                </ul>
              </div>
              <div className="bg-card p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-red-700 mb-4 flex items-center gap-2"><AlertTriangle className="w-4 h-4"/> Improvements</h4>
                <ul className="space-y-3 text-sm text-textMuted">
                  {results.improvements?.map((s, i) => <li key={i} className="flex gap-3 leading-snug"><span className="text-red-500 flex-shrink-0 mt-0.5">•</span> {s}</li>)}
                  {(!results.improvements || results.improvements.length === 0) && <li className="text-gray-400 italic">No critical improvements needed.</li>}
                </ul>
              </div>
              <div className="bg-card p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-blue-700 mb-4 flex items-center gap-2"><Lightbulb className="w-4 h-4"/> Suggestions</h4>
                <ul className="space-y-3 text-sm text-textMuted">
                  {results.suggestions?.map((s, i) => <li key={i} className="flex gap-3 leading-snug"><span className="text-blue-500 flex-shrink-0 mt-0.5">•</span> {s}</li>)}
                  {(!results.suggestions || results.suggestions.length === 0) && <li className="text-gray-400 italic">No extra suggestions right now.</li>}
                </ul>
              </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ResultSection;
