const API_BASE_URL = 'http://localhost:5000/api';

export const analyzeResume = async (resumeText, jobDescription) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ resumeText, jobDescription })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to analyze resume. Make sure backend is running.');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const uploadPdf = async (file) => {
  try {
    const formData = new FormData();
    formData.append('resumePdf', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to upload PDF.');
    }

    return await response.json(); // returns { text: '...' }
  } catch (error) {
    throw error;
  }
};
