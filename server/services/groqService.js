const { buildPrompt } = require('../utils/promptBuilder');

const analyzeResume = async (resumeText, jobDescription) => {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    throw new Error('GROQ_API_KEY is not defined in backend environment.');
  }

  const prompt = buildPrompt(resumeText, jobDescription);

  try {
    // Dynamic import for fetch if using older Node.js, otherwise native fetch works in Node 18+
    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3-70b-8192',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.1, // low temp for pure JSON
        response_format: { type: "json_object" }
      })
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.error?.message || 'Failed to fetch from Groq API');
    }

    const data = await response.json();
    const content = data.choices[0]?.message?.content;
    
    if (!content) {
      throw new Error('Received empty response from AI.');
    }

    // Attempt to parse JSON strictly
    try {
      return JSON.parse(content);
    } catch (parseError) {
      // Fallback regex if markdown block is attached
      const match = content.match(/\{[\s\S]*\}/);
      if (match) return JSON.parse(match[0]);
      throw new Error('AI did not return valid JSON.');
    }

  } catch (error) {
    throw error;
  }
};

module.exports = { analyzeResume };
