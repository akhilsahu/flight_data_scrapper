from playwright.sync_api import sync_playwright
import time

def scrape_mmt_flights(origin, destination, date):
    with sync_playwright() as p:
         
        browser = p.chromium.launch(
    headless=False,
    args=["--disable-http2", "--disable-features=UseChromeOSDirectVideoDecoder"]
)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
       
        page.goto("https://www.makemytrip.com/flights/")
        time.sleep(4)  # Let popups load

        # Dismiss login and other popups
        page.click("body")
        try:
            print('Checking for popups...')
            close_button = page.locator('[data-cy="closeModal"]')
            close_button.wait_for(state="visible", timeout=5000)
            close_button.click()
            print('Popup closed.')
        except Exception:
            print('No popup found or already closed')
        # Enter origin
        page.click("//label[@for='fromCity']")
        page.fill("//input[@placeholder='From']", origin)
        page.keyboard.press("Enter")

        # Enter destination
        page.click("//label[@for='toCity']")
        page.fill("//input[@placeholder='To']", destination)
        page.keyboard.press("Enter")

        # Select departure date
        page.click("//label[@for='departure']")
        page.click(f"//div[@aria-label='{date}']")

        # Click search
        page.click("//a[contains(@class, 'primaryBtn') and text()='Search']")
        page.wait_for_load_state("networkidle")
        time.sleep(6)  # Wait for results to fully load

        # Scrape flight info
        flight_cards = page.query_selector_all("div.fli-list")
        for flight in flight_cards:
            airline = flight.query_selector(".airlineInfo .airlineName").inner_text() if flight.query_selector(".airlineInfo .airlineName") else ""
            departure_time = flight.query_selector(".dept-time").inner_text() if flight.query_selector(".dept-time") else ""
            arrival_time = flight.query_selector(".arr-time").inner_text() if flight.query_selector(".arr-time") else ""
            price = flight.query_selector(".priceSection .fontSize18").inner_text() if flight.query_selector(".priceSection .fontSize18") else ""
            print({
                "airline": airline,
                "departure": departure_time,
                "arrival": arrival_time,
                "fare": price
            })

        browser.close()


import asyncio
from playwright.async_api import async_playwright

async def take_screenshot(page, label):
    path = f"{label}.png"
    await page.screenshot(path=path)
    print(f"Screenshot taken: {path}")

async def mmt_flight_search_flow(from_code, to_code, depart_date):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.makemytrip.com/")

        # Take screenshot before form actions
        await take_screenshot(page, 'before-form')

        # Handle initial popups
        try:
            print('Checking for popups...')
            await page.wait_for_selector('[data-cy="closeModal"]', timeout=5000)
            await page.click('[data-cy="closeModal"]')
            print('Popup closed.')
        except Exception:
            print('No popup found or already closed')

        print('Filling search form...')
        # Clear and fill origin
        print('Setting origin:', from_code)
        await page.wait_for_selector('[data-cy="fromCity"]', state="visible")
        await page.click('[data-cy="fromCity"]')
        await page.keyboard.type(from_code)
        await page.wait_for_timeout(2000)
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('Enter')

        # Clear and fill destination
        print('Setting destination:', to_code)
        await page.wait_for_selector('[data-cy="toCity"]', state="visible")
        await page.click('[data-cy="toCity"]')
        await page.keyboard.type(to_code)
        await page.wait_for_timeout(2000)
        await page.keyboard.press('ArrowDown')
        await page.keyboard.press('Enter')

        # Fill departure date (may need a custom selector based on MMT’s markup)
        print('Setting departure date:', depart_date)
        await page.wait_for_selector('[data-cy="departure"]', state="visible")
        await page.click('[data-cy="departure"]')
        await page.keyboard.type(depart_date)
        await page.keyboard.press('Enter')

        # (Continue: click the search button, grab results...)

        # Final screenshot after form filled
        await take_screenshot(page, 'after-form')

        await browser.close()

# Example usage
asyncio.run(mmt_flight_search_flow('DEL', 'BOM', '27/11/2025'))


# Example usage
#scrape_mmt_flights("Delhi", "Mumbai", "Wed Nov 20 2025")
