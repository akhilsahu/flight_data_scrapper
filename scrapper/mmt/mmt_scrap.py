from seleniumbase import SB

def scrap_sb(origin="LKO", destination="DEL", travel_date="28/12/2025"):
    with SB(uc=True, test=True) as sb:
        url = f"https://www.makemytrip.com/flight/search?itinerary={origin}-{destination}-{travel_date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng"
        sb.activate_cdp_mode(url)
        
        sb.sleep(9)
        #sb.click('button.priceLockProCtaButton.whiteText')
        sb.get_page_source()
        #sb.save_screenshot('./ss/mmt_res.png', full_page=True)
        sr = sb.get_page_source()
        
        with open("./ss/mmt_res.html", "w", encoding="utf-8") as f:
            f.write(sr)
        print("Scraping completed")
        sb.quit()

if __name__ == "__main__":
    scrap_sb()