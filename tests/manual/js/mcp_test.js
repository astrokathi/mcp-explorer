const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
  });
  const page1 = await browser.newPage();
  console.log("Navigating to Chainlit App at http://localhost:8000...");
  await page1.goto('http://localhost:8000', { waitUntil: 'networkidle0' });
  
  await new Promise(r => setTimeout(r, 5000));
  
  console.log("Waiting for Chainlit input...");
  await page1.waitForSelector('textarea');
  
  console.log("Sending a message...");
  await page1.type('textarea', 'Hello agent! What is 5+7?');
  
  const textarea = await page1.$('textarea');
  await textarea.press('Enter');

  console.log("Waiting 30 seconds for agent to process and trace to be sent...");
  await new Promise(r => setTimeout(r, 30000));
  
  await browser.close();
})();
