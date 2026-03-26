const pdfParse = require('pdf-parse');

const handleUpload = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No PDF file uploaded.' });
    }

    if (req.file.mimetype !== 'application/pdf') {
      return res.status(400).json({ error: 'Only PDF files are allowed.' });
    }

    const dataBuffer = req.file.buffer;
    const data = await pdfParse(dataBuffer);

    if (!data.text || data.text.trim().length === 0) {
      return res.status(400).json({ error: 'Could not extract text from the PDF. It might be scanned or image-based.' });
    }

    return res.status(200).json({ text: data.text });

  } catch (error) {
    console.error('PDF Parse Error:', error);
    return res.status(500).json({ error: 'Failed to parse PDF document.' });
  }
};

module.exports = { handleUpload };
