import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin


def extract_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for tr in soup.find_all('tr'):
        for link in tr.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                links.append(href)
    return links


def get_most_common_words(url, num_words=100):
    page_content = requests.get(url, timeout=5).text
    soup = BeautifulSoup(page_content, 'html.parser')
    text = soup.get_text()
    words = text.split()
    return Counter(words)


# Example usage
def scrape_website(website_url):
    links = extract_links_from_page(website_url)
    common_words = Counter()
    common_words.update(get_most_common_words(website_url))

    for num, link in enumerate(links):
        # if "software" not in link: continue
        print(f"link {num} of {len(links)}: {link}")
        try:
            common_words.update(get_most_common_words(link))
        except:
            print("FAILED")

    return common_words


website_url = "https://github.com/pittcsc/Summer2024-Internships"
common_words = scrape_website(website_url)
newLineCounter = 0;
print(f"Most common words on SW links from {website_url}:")
for key, val in common_words.most_common():
    print(key, val, end="\t\t\t")
    if newLineCounter%3==0: print("")
    newLineCounter += 1

input('Wait!')
