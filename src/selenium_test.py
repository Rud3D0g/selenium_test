import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options


# Configure Edge options
edge_options = Options()
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-web-security")
edge_options.add_argument("--disable-extensions")
edge_options.add_argument("--disable-notifications")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--disable-software-rasterizer")
edge_options.add_argument("--remote-debugging-port=9222")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--disable-setuid-sandbox")

# Use existing Edge profile
edge_profile_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
edge_options.add_argument(f"--user-data-dir={edge_profile_path}")
edge_options.add_argument("--profile-directory=Default")

# Initialize Edge driver
driver = webdriver.Edge(options=edge_options)

try:
    # Navigate to Google
    driver.get("https://www.google.com")

    # Wait for Google to load by looking for the search box
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "q"))  # Wait for the search box
    )

    # Check if we're logged in by looking for the Google account menu
    try:
        account_menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "gb"))
        )
        print("Successfully logged into Google!")
    except Exception as _e:
        print("Not logged into Google. Please log in manually.")
        print(_e)
        time.sleep(10)  # Give time to manually log in

    # Find and use the search box
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("selenium stuff")
    search_box.submit()

    # Wait for the search results page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "search"))  # Wait for the search results container
    )

    # Wait for the first result to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.g h3"))  # Wait for the first result title
    )

    # Get all search results
    results = driver.find_elements(By.CSS_SELECTOR, "div.g")

    # Print each result's title and URL
    print("\nSearch Results:\n")
    for result in results:
        try:
            # Try multiple ways to get the title and URL
            title_element = result.find_elements(By.CSS_SELECTOR, "h3")
            url_element = result.find_elements(By.CSS_SELECTOR, "a[href]")
            if title_element and url_element:
                title = title_element[0].text
                url = url_element[0].get_attribute("href")
                print(f"Title: {title}")
                print(f"URL: {url}")
                print("-" * 50)
            else:
                print("Could not find title or URL for this result")
        except Exception as e:
            print(f"Error processing result: {str(e)}")

finally:
    # Close the browser
    driver.quit()
