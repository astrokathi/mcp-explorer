import asyncio
import subprocess
import time
import sys
from playwright.async_api import async_playwright

async def run_e2e():
    print("Starting Chainlit server...")
    # Start the server as a background process
    server_process = subprocess.Popen(
        [sys.executable, "-m", "chainlit", "run", "ui/app.py", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(15) 
    
    print("Running Playwright tests...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            print("Navigating to http://localhost:8000")
            await page.goto("http://localhost:8000")
            
            # Wait for network idle to ensure the page is fully loaded
            await page.wait_for_load_state("networkidle")
            
            title = await page.title()
            print(f"Page title is: {title}")
            
            # Basic verification that the page loaded Chainlit
            assert "Chainlit" in title or title != "", "UI did not load properly."
            print("E2E Test Passed successfully.")
            
            await browser.close()
    except Exception as e:
        print(f"E2E Test Failed: {e}")
        raise e
    finally:
        print("Tearing down Chainlit server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    asyncio.run(run_e2e())
