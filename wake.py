import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wake_streamlit():
    url = os.environ.get("https://rajeshxdatascience-flights-analytics-dashboard-app-9l1fbh.streamlit.app/")
    print(f"Checking app at: {url}")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Modern headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        # Wait up to 30 seconds for Streamlit's wake button to appear
        wait = WebDriverWait(driver, 30)
        
        # Target the button by its exact text
        button_xpath = "//button[contains(text(), 'Yes, get this app back up')]"
        
        try:
            wake_button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            # Using JavaScript click to bypass any overlapping layers
            driver.execute_script("arguments[0].click();", wake_button)
            print("✅ Wake-up button clicked! App is initializing.")
            time.sleep(10) # Give it a moment to start the reboot
        except:
            print("ℹ️ No wake-up button found. Your app is likely already awake.")
            # Save a screenshot to see what's actually happening
            driver.save_screenshot("debug_view.png")
            
    except Exception as e:
        print(f"❌ Automation Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    wake_streamlit()
