const express = require('express');
const router = express.Router();
const multer = require('multer');
const { handleUpload } = require('../controllers/uploadController');

// Multer memory storage configuration
const storage = multer.memoryStorage();
const upload = multer({ 
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});

router.post('/', upload.single('resumePdf'), handleUpload);

module.exports = router;
