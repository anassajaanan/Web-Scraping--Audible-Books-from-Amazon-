from bs4 import BeautifulSoup
import requests
from csv import writer

# ========= Before starting ========
# KEYWORDS = "Put here the topic/keyword that you want to search about"
# NUM_PAGES = "Put here the number of pages that are related to this topic/keyword"

# Example:

KEYWORDS = "python"
NUM_PAGES = 22

# ==================================

for i in range(NUM_PAGES):
    URL = f"https://www.audible.com/search?keywords={KEYWORDS}&page={i + 1}"
    response = requests.get(URL)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')

    titles = soup.find_all("h3", class_="bc-heading bc-color-link bc-pub-break-word bc-size-medium")
    titles = [title.getText().replace("\n", "") for title in titles]
    # print(titles)

    authors = soup.find_all("li", class_="bc-list-item authorLabel")
    authors = [author.find("a").getText() for author in authors]
    # print(authors)

    dates = soup.find_all("li", class_="bc-list-item releaseDateLabel")
    dates = [date.find("span").get_text().replace(" ", "").split("\n")[1] for date in dates]
    # print(dates)

    ratings = soup.find_all("li", class_="bc-list-item ratingsLabel")
    num_ratings = [rating.find("span", class_="bc-text bc-size-small bc-color-secondary").get_text() for rating in
                   ratings]
    ratings_out_5 = []
    for _ in ratings:
        try:
            ratings_out_5.append(_.find("span", class_="bc-text bc-pub-offscreen").getText())
        except AttributeError:
            ratings_out_5.append("Not rated yet")
    # print(num_ratings)
    # print(ratings_out_5)

    prices = soup.find_all("div", class_="bc-section bc-spacing-none adblBuyBoxPrice")
    prices = [
        price.find_all("span", class_="bc-text bc-size-base bc-color-base")[1].get_text().replace(" ", "").replace("\n",
                                                                                                                   "")
        for price in prices]
    # print(prices)

    with open('book.csv', 'a', newline='', encoding="UTF-8") as file:
        for j in range(len(titles)):
            writer_object = writer(file)
            try:
                List = [titles[j], authors[j], dates[j], num_ratings[j], ratings_out_5[j], prices[j]]
            except:
                pass
            writer_object.writerow(List)
        file.close()
