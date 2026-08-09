/**
 * GuardianAI Node.js Integration Sample Application
 */

const http = require('http');

async function scanUrl(targetUrl) {
  console.log(`=== GuardianAI Node.js Inspection Demo ===`);
  console.log(`Scanning target URL: ${targetUrl}`);

  const payload = JSON.stringify({ target_url: targetUrl });
  
  const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/v1/public/scan/url',
    method: 'POST',
    headers: {
      'Authorization': 'Bearer gai_live_88f92a110099xza21_prod',
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  };

  const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
      console.log(`HTTP Status: ${res.statusCode}`);
      console.log(`Response Body:`, JSON.parse(data));
    });
  });

  req.on('error', (err) => {
    console.error(`HTTP Error:`, err.message);
  });

  req.write(payload);
  req.end();
}

scanUrl('http://hdfc-verify.top');
