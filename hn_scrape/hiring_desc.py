from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import csv
import time

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)

urls = ["https://news.ycombinator.com/item?id=39562984",
        "https://news.ycombinator.com/item?id=39217308",
        "https://news.ycombinator.com/item?id=38842975",
        "https://news.ycombinator.com/item?id=38490809",
        "https://news.ycombinator.com/item?id=38099084",
        "https://news.ycombinator.com/item?id=37739026",
        "https://news.ycombinator.com/item?id=37351665"]

with open('1000_output.csv', 'a') as csvfile:
    fieldnames = ['location', 'remote', 'relocate', 'technologies', 'resume', 'email', 'description']
    writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        driver.get(url)
        time.sleep(3)
        comment_tree = driver.find_element(By.CLASS_NAME, 'comment-tree')
        tbody = comment_tree.find_element(By.TAG_NAME, 'tbody')

        for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
            text_lines = tr.text.split('\n')
            resp = {
                'location': '',
                'remote': '',
                'relocate': '',
                'technologies': '',
                'resume': '',
                'email': '',
                'description': '',
            }
            description_lines = []
            
            for line in text_lines:
                line_lower = line.lower().strip()
                parts = line.split(':', 1)
                key = ''
                if len(parts) == 2:
                    key, value = parts[0].lower().strip(), parts[1].strip()
                if line_lower.startswith("location:"):
                    resp['location'] = value
                elif line_lower.startswith("remote:"):
                    resp['remote'] = value
                elif line_lower.startswith("willing to relocate:"):
                    resp['relocate'] = value
                elif line_lower.startswith("technologies:"):
                    resp['technologies'] = value
                elif line_lower.startswith("résumé/cv:") or line_lower.startswith("resume:"):
                    resp['resume'] = value
                elif line_lower.startswith("email:"):
                    resp['email'] = value
                else:
                    description_lines.append(line.strip())
            
            resp['description'] = ''.join(description_lines)
            
            if resp['location'] and resp['remote']: # Improve filtering for junk and job postings
                writer.writerow(resp)
            
        time.sleep(1)

driver.quit()
        
        # break