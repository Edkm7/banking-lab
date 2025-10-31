const express = require('express');
const router = express.Router();
const axios = require('axios');
const PDFDocument = require('pdfkit');

const ACCOUNTS_URL = process.env.ACCOUNTS_URL || 'http://accounts-service:8082';

// ✅ Endpoint JSON
router.get('/json', async (req, res) => {
  try {
    const { data } = await axios.get(`${ACCOUNTS_URL}/accounts`);
    res.json({ reportDate: new Date(), accounts: data });
  } catch (error) {
    res.status(500).json({ error: 'Unable to fetch accounts data' });
  }
});

// ✅ Endpoint PDF
router.get('/pdf', async (req, res) => {
  try {
    const { data } = await axios.get(`${ACCOUNTS_URL}/accounts`);
    const doc = new PDFDocument();

    res.setHeader('Content-Type', 'application/pdf');
    doc.pipe(res);

    doc.fontSize(20).text('Banking Report', { align: 'center' });
    doc.moveDown();

    data.forEach((account, index) => {
      doc.fontSize(12).text(`${index + 1}. Account: ${account.name} | Balance: ${account.balance}`);
    });

    doc.end();
  } catch (error) {
    res.status(500).json({ error: 'Unable to generate report' });
  }
});

module.exports = router;
