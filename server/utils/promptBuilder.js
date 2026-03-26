const buildPrompt = (resumeText, jobDescription) => {
  return `
You are an expert ATS (Applicant Tracking System) and senior technical recruiter. 
Compare the following Resume to the Job Description.

Resume:
${resumeText}

Job Description:
${jobDescription}

You MUST return ONLY a strict JSON object with NO MARKDOWN formatting, NO backticks, and NO conversational text.
You MUST provide realistic scoring and ATS-focused analysis based on industry standards.

The response MUST match this EXACT schema:
{
  "matchScore": number (0-100),
  "atsScore": number (0-100),
  "impactScore": number (0-100),
  "summary": "string (2-3 sentences max summarizing the candidate's fit)",
  "foundKeywords": ["keyword1", "keyword2"],
  "missingKeywords": ["keyword1", "keyword2"],
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "suggestions": ["suggestion1", "suggestion2"]
}
`;
};

module.exports = { buildPrompt };
