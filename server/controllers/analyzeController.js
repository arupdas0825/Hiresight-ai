const { analyzeResume } = require('../services/groqService');

const handleAnalyze = async (req, res) => {
  try {
    const { resumeText, jobDescription } = req.body;

    if (!resumeText || !jobDescription) {
      return res.status(400).json({ error: 'Both resumeText and jobDescription are required.' });
    }

    const result = await analyzeResume(resumeText, jobDescription);
    return res.status(200).json(result);

  } catch (error) {
    console.error('Analyze Error:', error);
    return res.status(500).json({ error: error.message || 'Internal Server Error' });
  }
};

module.exports = { handleAnalyze };
