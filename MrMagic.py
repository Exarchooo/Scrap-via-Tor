# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, simpledialog
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import requests
import zipfile
import os
import datetime

# Tor identify              Mr Maaagic, take a token
def renew_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# Selenium
def fetch_links(query, start_date, end_date, driver):
    date_filter = ""
    if start_date and end_date:
        date_filter = f"&df={start_date}..{end_date}"
    
    # DuckDuckGo syntax
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}{date_filter}&ia=web"
    
    renew_tor_identity()
    driver.get(url)
    
    links = []
    while True:
        time.sleep(random.uniform(3, 7))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        results = soup.find_all('a', href=True)
        if not results:
            break
        
        for result in results:
            href = result['href']
            if 'http' in href:
                links.append(href)
        
        try:
            more_button = driver.find_element(By.ID, "more-results")
            more_button.click()
        except:
            break

    return links

class PageSpider(Spider):
    name = "page_spider"
    
    def __init__(self, *args, **kwargs):
        super(PageSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])
    
    def parse(self, response):
        paragraphs = response.css('p::text').getall()
        clean_text = " ".join(paragraph.strip() for paragraph in paragraphs)
        
        yield {
            'text': clean_text,  # Cleared text
        }

# Function to add uBlock Origin to Firefox profile
def add_ublock_origin_to_profile(profile):
    ublock_origin_xpi_path = "uBlock0@raymondhill.net.xpi"
    if not os.path.exists(ublock_origin_xpi_path):
        # Download uBlock Origin
        ublock_origin_url = "https://addons.mozilla.org/firefox/downloads/file/3620447/ublock_origin-1.41.6-fx.xpi"
        response = requests.get(ublock_origin_url)
        with open(ublock_origin_xpi_path, "wb") as f:
            f.write(response.content)
    
    profile.add_extension(ublock_origin_xpi_path)

# GUI Application
class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper App")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Labels and Entry widgets for user inputs
        tk.Label(self.root, text="Insert a phrase to search:").grid(row=0, column=0, padx=10, pady=5)
        self.phrase_entry = tk.Entry(self.root, width=50)
        self.phrase_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Enter the phrase you want in the headline (optional):").grid(row=1, column=0, padx=10, pady=5)
        self.title_phrase_entry = tk.Entry(self.root, width=50)
        self.title_phrase_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Enter the start date (YYYY-MM-DD, optional):").grid(row=2, column=0, padx=10, pady=5)
        self.start_date_entry = tk.Entry(self.root, width=50)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Enter the end date (YYYY-MM-DD, optional):").grid(row=3, column=0, padx=10, pady=5)
        self.end_date_entry = tk.Entry(self.root, width=50)
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Enter the sites to scrape, separated by commas:").grid(row=4, column=0, padx=10, pady=5)
        self.sites_entry = tk.Entry(self.root, width=50)
        self.sites_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Button to start the scrapping process
        self.start_button = tk.Button(self.root, text="Start Scraping", command=self.start_scraping)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=20)
    
    def start_scraping(self):
        phrase = self.phrase_entry.get()
        title_phrase = self.title_phrase_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        sites_input = self.sites_entry.get()
        
        if not phrase:
            messagebox.showwarning("Input Error", "Please enter a search phrase.")
            return
        
        site_list = [site.strip() for site in sites_input.split(',')]
        
        if not site_list:
            messagebox.showwarning("Input Error", "Please enter at least one site to scrape.")
            return
        
        # Selenium+Tor configuration
        options = Options()
        options.headless = True

        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", 9050)
        profile.set_preference("network.proxy.socks_version", 5)
        profile.set_preference("places.history.enabled", False)
        profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        profile.set_preference("privacy.clearOnShutdown.passwords", True)
        profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
        profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        
        # Add uBlock Origin to the profile
        add_ublock_origin_to_profile(profile)
        
        options.profile = profile

        driver = webdriver.Firefox(options=options)

        links = []
        for site in site_list:
            query = f"{phrase} site:{site}"
            if title_phrase:
                query += f" intitle:{title_phrase}"

            links.extend(fetch_links(query, start_date, end_date, driver))

        driver.quit()

        if not links:
            messagebox.showinfo("Result", "No results found.")
        else:
            # Scrapy
            # Generate a timestamped filename
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            output_filename = f"results_{timestamp}.json"
            
            process = CrawlerProcess(settings={
                "FEEDS": {
                    output_filename: {"format": "json"},
                },
                "FEED_EXPORT_ENCODING": "utf-8",
            })

            process.crawl(PageSpider, start_urls=links)
            process.start()

            messagebox.showinfo("Result", f"Scraping completed. Results saved in {output_filename}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
