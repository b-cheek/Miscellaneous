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
    text = soup.get_text().lower()
    words = text.split()
    return Counter(words)

specifics = [
    'Unit Testing', 'Oracle', 'Python', 'Docker', 'Pig', 'HTML', 'SQL', 'Azure', 'Microservices', 'Shell Scripting',
    'Processing', 'OOP', 'Angular', 'Embedded processors', 'API', 'RESTful API', 'Cloud Services', 'Linux', 'C', 'Data Modeling',
    'Client-Server protocol', 'Microsoft SQL Server', 'OS', 'Client-Sever', 'Go', 'Clojure', 'Hadoop', 'Debugging',
    'React', 'AWS', 'MS Office', 'C#', 'DB2', 'Real time operating system concepts', 'Unix', 'Spring Boot', 'Kubernetes',
    'Embedded Software', 'Node', 'PHP', '.NET', 'JSF', 'VBA', 'SproutCore', 'MySQL', 'DSA', 'Ruby', 'C++', 'Objective-C',
    'JS', 'Sybase', 'PostgreSQL', 'MapReduce', 'Networking', 'Perl', 'Docker', 'Java', 'Virtualization', 'ERP', 'ASP', 'Mongo',
    'noSQL', 'Scala', 'SVN', 'Cosmos DB', 'MongoDB', 'CSS', 'JSP', 'Validation', 'TCP/IP', 'Test', 'embedded', 'Scripting', 'Shell',
    'Object Oriented', 'Object-oriented', 'rest api', 'cloud', 'operating system', 'golang', 'data structures', 'algorithm', 'Spring',
    'javascript'
]

def get_specific_counts(url):
    page_content = requests.get(url, timeout=5).text
    soup = BeautifulSoup(page_content, 'html.parser')
    text = soup.get_text().lower()
    word_counter = Counter()
    for tech in specifics:
        count = page_content.count(tech.lower())
        word_counter[tech] = count
    return word_counter


# Example usage
def scrape_website(website_url):
    links = extract_links_from_page(website_url)
    common_words = Counter()
    specific_words = Counter()
    common_words.update(get_most_common_words(website_url))
    specific_words.update(get_specific_counts(website_url))

    for num, link in enumerate(links):
        # if "software" not in link: continue
        print(f"link {num} of {len(links)}: {link}")
        try:
            common_words.update(get_most_common_words(link))
            specific_words.update(get_specific_counts(link))
        except:
            print("FAILED")

    return common_words, specific_words


website_url = "https://github.com/pittcsc/Summer2024-Internships"
common_words, specific_words = scrape_website(website_url)
newLineCounter = 0
print(f"Most common buzzwords on links from {website_url}:")
for key, val in specific_words.most_common():
    print(key, val, end="\t")
    otherRef = 0
    for i in [key, f'/{key}', f'{key}/', f'{key},', f'{key}.']:
        if i.lower() in common_words:
            otherRef += common_words[i.lower()]
    print("Total other word references:", otherRef)

##for key, val in common_words.most_common():
##    print(key, val, end="\n")
##    if newLineCounter%3==0: print("")
##    newLineCounter += 1

input('Wait!')
