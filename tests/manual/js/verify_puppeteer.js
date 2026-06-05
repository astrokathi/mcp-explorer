const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  
  console.log("Navigating to Chainlit App at http://localhost:8000...");
  const page1 = await browser.newPage();
  await page1.goto('http://localhost:8000', { waitUntil: 'networkidle2' });
  
  console.log("Waiting for Chainlit input...");
  // Chainlit input uses an element with id id='chat-input'
  await page1.waitForSelector('#chat-input', { timeout: 15000 }).catch(e => console.log("Input selector not found, attempting fallback..."));
  
  console.log("Sending a message...");
  // We can just use the generic textarea selector for chainlit
  await page1.type('textarea', 'Hello agent! What is 5+7?');
  // Press Enter to submit
  await page1.keyboard.press('Enter');
  
  console.log("Waiting 30 seconds for agent to process and trace to be sent...");
  await new Promise(r => setTimeout(r, 30000));
  
  console.log("Navigating to Langfuse UI at http://localhost:3000...");
  const page2 = await browser.newPage();
  await page2.goto('http://localhost:3000/auth/sign-in', { waitUntil: 'networkidle2' });
  
  console.log("Logging into Langfuse...");
  await page2.waitForSelector('input[name="email"]');
  await page2.type('input[name="email"]', 'admin@langfuse.local');
  await page2.type('input[name="password"]', 'admin123');
  await Promise.all([
    page2.click('button[type="submit"]'),
    page2.waitForNavigation({ waitUntil: 'networkidle2' })
  ]);
  
  console.log("Currently at URL: " + page2.url());
  
  // If we are at the setup page, click "Skip for now"
  if (page2.url().includes('setup') || await page2.$('text/Skip for now') !== null) {
      console.log("Clicking 'Skip for now' on setup page...");
      try {
         const elements = await page2.$$('button');
         for (const el of elements) {
             const text = await page2.evaluate(e => e.textContent, el);
             if (text && text.includes('Skip for now')) {
                 await el.click();
                 break;
             }
         }
         await new Promise(r => setTimeout(r, 2000));
      } catch (e) {
         console.log("Could not find skip button");
      }
  }
  
  console.log("Navigating to Traces...");
  await page2.goto('http://localhost:3000/project/default_project/traces', { waitUntil: 'networkidle2' });
  
  console.log("Currently at URL: " + page2.url());
  console.log("Checking traces...");
  
  // Look for traces in the table
  const traces = await page2.evaluate(() => {
     // Get all text content on the page to search for our prompt
     return document.body.innerText;
  });
  
  if (traces.includes('Hello agent! What is 5+7?')) {
     console.log("✅ SUCCESS! Trace for our message was found in the Langfuse Dashboard!");
  } else {
     console.log("❌ Trace not found on the page!");
     console.log("Page text snippet:");
     console.log(traces.substring(0, 500));
  }

  await browser.close();
})();
