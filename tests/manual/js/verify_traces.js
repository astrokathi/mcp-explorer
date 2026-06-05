const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    try {
        console.log("Navigating to Langfuse...");
        await page.goto('http://localhost:3000', { waitUntil: 'networkidle2' });

        // Check if we need to log in
        console.log("Checking login...");
        const emailInput = await page.$('input[name="email"]');
        if (emailInput) {
            console.log("Logging in...");
            await page.type('input[name="email"]', 'admin@langfuse.local');
            await page.type('input[name="password"]', 'admin123');
            await page.click('button[type="submit"]');
            await page.waitForNavigation({ waitUntil: 'networkidle2' });
        }

        console.log("Navigating to Traces...");
        // Click on the traces menu item or navigate directly
        await page.goto('http://localhost:3000/project/default_project/traces', { waitUntil: 'networkidle2' });
        
        // Wait for traces table to load
        await page.waitForSelector('table', { timeout: 10000 });
        
        // Extract trace details
        const traces = await page.evaluate(() => {
            const rows = Array.from(document.querySelectorAll('table tbody tr'));
            return rows.slice(0, 5).map(row => {
                const cols = row.querySelectorAll('td');
                return {
                    name: cols[2]?.innerText?.trim(),
                    timestamp: cols[4]?.innerText?.trim(),
                };
            });
        });
        
        console.log("Found Traces:");
        console.log(traces);
        
        if (traces.length > 0 && traces[0].name.includes("Agent")) {
            console.log("SUCCESS: Trace found in the dashboard!");
        } else {
            console.log("WARNING: Trace might not be visible yet.");
        }

    } catch (e) {
        console.error("Error:", e);
    } finally {
        await browser.close();
    }
})();
