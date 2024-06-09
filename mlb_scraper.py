from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import json
from time import sleep


class WebNavigator:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
        except WebDriverException as e:
            print(f"Error setting up the driver: {e}")
            raise

    def navigate(self):
        if self.driver is not None:
            try:
                self.driver.get(self.url)
            except WebDriverException as e:
                print(f"Error navigating to {self.url}: {e}")
                self.close_browser()
                raise
        else:
            raise Exception("Driver is not set up. Call setup_driver() first.")

    def wait_for_element_and_click(self, selector):
        try:
            wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.click()
        except TimeoutException as e:
            print(f"Timeout while waiting for element: {e}")
            raise

    def get_element_text(self, selector):
        try:
            wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return element.text
        except TimeoutException as e:
            print(f"Timeout while waiting for element: {e}")
            raise

    def click_next_button(self, selector):
        try:
            wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            # Scroll to the element before clicking
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
        except TimeoutException as e:
            print(f"Timeout while waiting for next button: {e}")
            raise

    def extract_data(self):
        
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        matches_data = []

        for event in soup.find_all(attrs={"itemtype": "http://schema.org/SportsEvent"}):
            match_info = {}

            # Safer extraction using try-except to handle cases where elements may be missing
            try:
                start_date = event.find(attrs={"itemprop": "startDate"})
                home_team = event.find(attrs={"itemprop": "homeTeam"})
                away_team = event.find(attrs={"itemprop": "awayTeam"})
                total_scores = event.find_all(class_='total')

                match_info["start_date"] = start_date.text.strip() if start_date else None
                match_info["home_team"] = home_team.text.strip() if home_team else None
                match_info["away_team"] = away_team.text.strip() if away_team else None

                match_info["home_score"] = total_scores[0].text.strip()
                match_info["away_score"] = total_scores[1].text.strip()

                print(match_info["home_score"])
                print(match_info["away_score"])

                odd_href = event.find(attrs={"itemprop": "url"})
                match_info["odd_href"] = "https://www.aiscore.com" + odd_href['href'] if odd_href else None

                if odd_href:
                    # Open a new tab
                    self.driver.execute_script("window.open('');")
                    # Switch to the new tab
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    # Load the page with odds
                    self.driver.get("https://www.aiscore.com" + odd_href['href'] + "/odds")

                    try:
                        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.innerMatchInfo.detail.view.border-box > div:nth-child(4) > div > div.newOdds > div:nth-child(3) > div > div.flex-1 > div > div:nth-child(1) > div.box.flex.w100.brr.preMatchBg1")))

                        # Improved wait condition: Wait until the text changes from "-" and is non-empty
                        odds_selector = "#app > div.innerMatchInfo.detail.view.border-box > div:nth-child(4) > div > div.newOdds > div:nth-child(3) > div > div.flex-1 > div > div:nth-child(1) > div.box.flex.w100.brr.preMatchBg1"
                        WebDriverWait(self.driver, 1.5).until(
                            lambda driver: driver.find_element(By.CSS_SELECTOR, odds_selector).text.strip() != '-' and
                                        driver.find_element(By.CSS_SELECTOR, odds_selector).text.strip() != "")

                        odds_div = self.driver.find_element(By.CSS_SELECTOR, odds_selector)
                        odds_list = [odds.strip() for odds in odds_div.text.split('\n') if odds.strip()]

                        if len(odds_list) >= 2:
                            match_info["home_odd"] = odds_list[0]
                            match_info["away_odd"] = odds_list[1]
                        else:
                            match_info["home_odd"] = "N/A"
                            match_info["away_odd"] = "N/A"

                    except TimeoutException:
                        print("Odds did not load in time.")
                        match_info["home_odd"] = "N/A"
                        match_info["away_odd"] = "N/A"


                    # Close the current tab
                    self.driver.close()
                    # Switch back to the main tab
                    self.driver.switch_to.window(self.driver.window_handles[0])

                matches_data.append(match_info)
            except IndexError as e:
                print(f"Skipping an event due to missing data: {e}")

        return matches_data

    def close_browser(self):
        if self.driver is not None:
            try:
                self.driver.quit()
            except WebDriverException as e:
                print(f"Error closing the browser: {e}")
        else:
            raise Exception("Driver is not set up. Call setup_driver() first.")
    
    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies
        
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    url = "https://www.aiscore.com/baseball/tournament-major-league-baseball/xo17pnc0dgs3kjw/matches/edq0pcpn1ntd7xg"
    selector_type = "#app > div.competition.view.border-box > div:nth-child(3) > div > div > div > ul > li.number.active"
    pagination_selector = "#app > div.competition.view.border-box > div:nth-child(3) > div > div > div > ul > li:nth-child(8)"
    next_button_selector = "#app > div.competition.view.border-box > div:nth-child(3) > div > div > div > button.btn-next"
    game_data = []
    navigator = WebNavigator(url)
    
    try:
        navigator.setup_driver()
        navigator.navigate()
        navigator.wait_for_element_and_click(selector_type)
        

        # Get the value of the pagination element
        pagination_value = navigator.get_element_text(pagination_selector)
        print(f"Pages detected: {pagination_value}")
        try:
            total_pages = int(pagination_value)
        except ValueError:
            print(f"Error converting pagination value to integer: {pagination_value}")
            total_pages = 0

        # Loop through the number of pages
        for _ in range(total_pages-1):
            game_data.append(navigator.extract_data())
            navigator.click_next_button(next_button_selector)

        save_to_json(game_data, 'matches_data_MLB.json')

        input("Press Enter to close the browser...")  # Keeps the browser open until user input
        
    finally:
        navigator.close_browser()

if __name__ == "__main__":
    main()
