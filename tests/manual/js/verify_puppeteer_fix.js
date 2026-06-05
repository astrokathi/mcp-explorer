const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  });
  const page1 = await browser.newPage();
  console.log("Navigating to Chainlit App at http://localhost:8000...");
  await page1.goto('http://localhost:8000', { waitUntil: 'networkidle0' });
  
  console.log("Waiting for Chainlit input...");
  await page1.waitForSelector('textarea');
  
  console.log("Sending a message...");
  await page1.type('textarea', 'Hello agent! What is 5+7?');
  
  // Find the submit button and click it
  await page1.evaluate(() => {
    // Chainlit submit button
    const btn = document.querySelector('#submit-button') || document.querySelector('button[type="submit"]') || document.querySelector('.submit-button');
    if (btn) btn.click();
    else {
      // simulate enter key on textarea
      const ta = document.querySelector('textarea');
      const event = new KeyboardEvent('keydown', {
        key: 'Enter',
        code: 'Enter',
        which: 13,
        keyCode: 13,
      });
      ta.dispatchEvent(event);
    }
  });
  
  console.log("Waiting 30 seconds for agent to process and trace to be sent...");
  await new Promise(r => setTimeout(r, 30000));
  
  console.log("Navigating to Langfuse UI at http://localhost:3000...");
  const page2 = await browser.newPage();
  await page2.goto('http://localhost:3000/auth/sign-in', { waitUntil: 'networkidle0' });
  
  console.log("Logging into Langfuse...");
  await page2.waitForSelector('input[name="email"]');
  await page2.type('input[name="email"]', 'admin@langfuse.local');
  await page2.type('input[name="password"]', 'password123');
  await page2.click('button[type="submit"]');
  
  await page2.waitForNavigation({ waitUntil: 'networkidle0' });
  
  console.log("Navigating to Traces...");
  await page2.goto('http://localhost:3000/project/default_project/traces', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 5000)); // wait for table load
  
  console.log("Checking traces...");
  const pageText = await page2.evaluate(() => document.body.innerText);
  
  if (pageText.includes('0 IDs')) {
      console.log("❌ Trace not found on the page!");
  } else {
      console.log("✅ Trace found on Langfuse Dashboard!");
  }
  
  await browser.close();
})();
