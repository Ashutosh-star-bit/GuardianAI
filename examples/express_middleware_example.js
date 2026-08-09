/**
 * GuardianAI Express.js Middleware Integration Example
 */

const express = require('express');
const app = express();

app.use(express.json());

// GuardianAI Anti-Scam Pre-screening Middleware
function guardianaiAntiScamShield(req, res, next) {
  if (req.method === 'POST' && req.body && req.body.url) {
    console.log(`[GuardianAI Shield] Pre-screening submitted URL: ${req.body.url}`);
    
    // Simulate SDK inspection
    const isPhishing = req.body.url.includes('verify.top') || req.body.url.includes('login.top');
    if (isPhishing) {
      return res.status(400).json({
        error: 'SCAM_DETECTED',
        message: 'Link submission blocked due to phishing threat.',
        threat_score: 98
      });
    }
  }
  next();
}

app.use(guardianaiAntiScamShield);

app.post('/api/submit-link', (req, res) => {
  res.json({ success: true, message: 'Link verified safe and posted successfully.' });
});

app.listen(3000, () => {
  console.log('Express partner app listening on port 3000 with GuardianAI Shield.');
});
