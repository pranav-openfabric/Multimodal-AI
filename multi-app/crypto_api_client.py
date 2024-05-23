import requests
from typing import Dict, Union, List
# from bs4 import BeautifulSoup
import spacy
nlp = spacy.load(".")

class CryptoAPIClient:
    BASE_URL = "https://pro-api.coinmarketcap.com"
    API_KEY = "1491e542-5af4-49b6-93bb-77df1a196765"

    def __init__(self):
        self.headers = {"X-CMC_PRO_API_KEY": self.API_KEY}

    def get_crypto_symbol(self, slug: str) -> Union[str, None]:
        url = f"{self.BASE_URL}/v2/cryptocurrency/info"
        params = {"slug": slug}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            if "data" in data:
                crypto_data = data["data"]
                for value in crypto_data.values():
                    if value["slug"] == slug:
                        return value["symbol"]
            return None
        except Exception as e:
            return f"Error occurred: {e}"

    def get_latest_crypto_data(self, symbol: str) -> Union[Dict, str]:
        url = f"{self.BASE_URL}/v1/cryptocurrency/listings/latest"
        params = {"start": "1", "limit": "100", "convert": "USD"}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()

            if 'data' in data:
                for crypto in data['data']:
                    if crypto['symbol'] == symbol:
                        market_data = {
                            "Name": crypto['name'],
                            "Symbol": crypto['symbol'],
                            "Price (USD)": crypto['quote']['USD']['price'],
                            "Volume 24h (USD)": crypto['quote']['USD']['volume_24h'],
                            "Market Cap (USD)": crypto['quote']['USD']['market_cap'],
                            "Max Supply": crypto['max_supply'],
                            "Circulating Supply": crypto['circulating_supply'],
                            "Total Supply": crypto['total_supply'],
                        }
                        return market_data
            return "Cryptocurrency not found"
        except Exception as e:
            return f"Error occurred: {e}"

    # def get_coinmarketcap_news(self, crypto_slug: str) -> Union[List[Dict], str]:
    #     url = f"https://coinmarketcap.com/currencies/{crypto_slug}/#News"

    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         soup = BeautifulSoup(response.text, 'html.parser')

    #         news_section = soup.find('div', class_='cmc-news__body')
    #         if not news_section:
    #             return "No news found"

    #         articles = news_section.find_all('a', class_='cmc-link', limit=5)  # Limit to first 5 articles
    #         news_list = []
    #         for article in articles:
    #             title = article.get_text().strip()
    #             link = article['href']
    #             news_list.append({"title": title, "link": link})

    #         return news_list
    #     except Exception as e:
    #         return f"Error occurred: {e}"

def extract_crypto_from_query(query: str) -> Union[str, None]:
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ == "CRYPTO":
            return ent.text.lower()
    return None
