const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  });
  const page = await browser.newPage();
  console.log("Navigating...");
  await page.goto('http://localhost:8000', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 5000));
  
  await page.waitForSelector('textarea');
  await page.screenshot({path: 'tests/manual/screenshots/chainlit1.png'});
  console.log("Typing...");
  const textarea = await page.$('textarea');
  await textarea.focus();
  await page.type('textarea', 'use arxiv and search for papers on H-LSTMs');
  await page.screenshot({path: 'tests/manual/screenshots/chainlit2.png'});
  
  console.log("Submitting...");
  await page.evaluate(() => {
    const ta = document.querySelector('textarea');
    if (ta) {
      const event = new KeyboardEvent('keydown', {
        key: 'Enter',
        code: 'Enter',
        which: 13,
        keyCode: 13,
        bubbles: true,
        cancelable: true
      });
      ta.dispatchEvent(event);
    }
  });
  
  console.log("Waiting for response...");
  await new Promise(r => setTimeout(r, 30000));
  await page.screenshot({path: 'tests/manual/screenshots/chainlit3.png'});
  await browser.close();
  console.log("Done");
})();
