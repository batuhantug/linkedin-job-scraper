import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from urllib.parse import quote
import logging
from utils import setup_logging, clean_text

class LinkedInJobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "https://www.linkedin.com/jobs/search"
        setup_logging()
        self.logger = logging.getLogger(__name__)

    def search_jobs(self, keywords, location="", work_type=None, experience_level=None, job_type=None, page=1):
        """
        Search LinkedIn jobs with additional filters
        """
        try:
            # Construct search URL with filters
            params = {
                'keywords': keywords,
                'location': location,
                'start': (page - 1) * 25,  # LinkedIn uses 25 jobs per page
            }

            # Add work type filter (f_WT)
            if work_type:
                work_type_codes = {
                    'remote': 1,
                    'on-site': 2,
                    'hybrid': 3
                }
                if work_type.lower() in work_type_codes:
                    params['f_WT'] = work_type_codes[work_type.lower()]

            # Add experience level filter (f_E)
            if experience_level:
                experience_codes = {
                    'internship': 1,
                    'entry': 2,
                    'associate': 3,
                    'mid-senior': 4,
                    'director': 5,
                    'executive': 6
                }
                if experience_level.lower() in experience_codes:
                    params['f_E'] = experience_codes[experience_level.lower()]

            # Add job type filter (f_JT)
            if job_type:
                job_type_codes = {
                    'full-time': 'F',
                    'part-time': 'P',
                    'contract': 'C',
                    'temporary': 'T',
                    'internship': 'I',
                    'volunteer': 'V',
                }
                if job_type.lower() in job_type_codes:
                    params['f_JT'] = job_type_codes[job_type.lower()]
            
            # Add delay to be respectful
            time.sleep(2)
            
            url = f"{self.base_url}?{self._build_query_string(params)}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_jobs(soup)
            
        except Exception as e:
            self.logger.error(f"Error scraping LinkedIn: {str(e)}")
            return []

    def _build_query_string(self, params):
        """Build URL query string from parameters"""
        return "&".join([f"{k}={quote(str(v))}" for k, v in params.items() if v])

    def _parse_jobs(self, soup):
        """Extract job listings from the page"""
        jobs = []
        job_cards = soup.find_all('div', {'class': 'base-card'})
        
        for card in job_cards:
            try:
                job = {
                    'title': clean_text(card.find('h3', {'class': 'base-search-card__title'}).text),
                    'company': clean_text(card.find('h4', {'class': 'base-search-card__subtitle'}).text),
                    'location': clean_text(card.find('span', {'class': 'job-search-card__location'}).text),
                    'link': card.find('a', {'class': 'base-card__full-link'}).get('href'),
                    'posted_date': clean_text(card.find('time', {'class': 'job-search-card__listdate'}).text)
                }
                jobs.append(job)
            except AttributeError as e:
                self.logger.warning(f"Error parsing job card: {str(e)}")
                continue
                
        return jobs

    def get_job_details(self, job_url):
        """Get detailed information about a specific job"""
        try:
            time.sleep(2)  # Respectful delay
            response = requests.get(job_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            details = {
                'description': clean_text(soup.find('div', {'class': 'description__text'}).text),
                'seniority': clean_text(soup.find('span', {'class': 'description__job-criteria-text'}).text),
            }
            return details
            
        except Exception as e:
            self.logger.error(f"Error getting job details: {str(e)}")
            return None

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_website(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            raise Exception(f"Error scraping website: {str(e)}") 