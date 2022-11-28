from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from yaml import FullLoader
from yaml import load as yaml_load

from emailSender import send_email
from googleDriveDownload import download_file_from_google_drive


def get_title(book_url):
    scraper = create_scraper(delay=10, browser={"custom": "ScraperBot/1.0"})
    req = scraper.get(book_url)
    book_soup = BeautifulSoup(req.content, 'html.parser')

    return book_soup.find("title").get_text().removesuffix(" - Google Drive")


def get_drive_link(viet_link):
    print("Processing this link: " + viet_link)
    driver = webdriver.Chrome()
    driver.get(viet_link)
    driver.implicitly_wait(30)
    python_button = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "CLICK LINK")))
    python_button.click()

    return_link = None

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.current_url.startswith("https://drive.google.com"):
            return_link = driver.current_url
            break

    driver.implicitly_wait(100)

    return return_link


def get_viet_links(url):
    scraper = create_scraper(delay=10, browser={"custom": "ScraperBot/1.0"})
    req = scraper.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    links = set()

    for url in soup.find_all("div", {"class": "action"}):
        for a in url.find_all('a', href=True):
            link = a['href']
            if (link.startswith("https://sachhoc.com/ngon-tinh/")):
                links.add(link)

    return links


input_file = "/Users/kindle_automator_viet/resources/input.yaml"

viet_links = set()

with open(input_file, "r") as read_file:
    yamlFile = yaml_load(read_file, Loader=FullLoader)

    for link in yamlFile["links"]:
        viet_links |= get_viet_links(link)

    for link in viet_links:
        try:
            drive_link = get_drive_link(link)
        except TimeoutException:
            print("No gdrive link found for " + link)
            continue

        if drive_link is None:
            print("Exception on " + link)
            continue

        book_title = None
        try:
            book_title = get_title(drive_link)
        except:
            print("Failed to get title for " + drive_link)

        drive_id = drive_link.removeprefix("https://drive.google.com/file/d/")
        drive_id = drive_id.removesuffix("/view")

        download_folder = yamlFile["download_folder"]
        book_path = download_folder + "/" + book_title

        print("Downloading " + book_title)
        download_file_from_google_drive(drive_id, book_path)

        print("Sending " + book_title + " to email")
        send_email(book_path, book_title, yamlFile["email_subject"],
                   yamlFile["email_contents"], yamlFile["from_email"],
                   yamlFile["dest_email"], yamlFile["email_password"])

    read_file.close()
