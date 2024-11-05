import requests
import re

def fetch_article_links(category):
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{category}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Nie udało się pobrać strony kategorii: {url}")
        return []
    
    # Wyciągnięcie linków do dwóch pierwszych artykułów
    article_links = re.findall(r'href="/wiki/([^":]+)"', response.text)[:2]
    article_links = [f"https://pl.wikipedia.org/wiki/{link}" for link in article_links]
    return article_links

def fetch_article_data(article_url):
    response = requests.get(article_url)
    if response.status_code != 200:
        print(f"Nie udało się pobrać artykułu: {article_url}")
        return None

    text = response.text
    
    # Pierwsze 5 wewnętrznych odnośników (tytuły i tekst odnośników)
    internal_links = re.findall(r'href="/wiki/([^":]+)" title="([^"]+)"', text)[:5]
    internal_links = [f"{title}" for _, title in internal_links]
    
    # Pierwsze 3 obrazy (adresy URL)
    images = re.findall(r'src="//upload\.wikimedia\.org/[^"]+\.(?:jpg|png|svg)', text)[:3]
    images = [f"//{img}" for img in images]
    
    # Pierwsze 3 zewnętrzne linki (adresy URL)
    external_links = re.findall(r'href="(http[^"]+)"', text)[:3]
    
    # Pierwsze 3 kategorie
    categories = re.findall(r'href="/wiki/Kategoria:([^"]+)"', text)[:3]
    
    # Formatowanie danych zgodnie z wymogami
    return (
        " | ".join(internal_links) if internal_links else "",
        " | ".join(images) if images else "",
        " | ".join(external_links) if external_links else "",
        " | ".join(categories) if categories else ""
    )

def main(category):
    articles = fetch_article_links(category)
    for article in articles:
        internal_links, images, external_links, categories = fetch_article_data(article)
        print(internal_links)
        print(images)
        print(external_links)
        print(categories)
        print()

# Wywołanie funkcji main z przykładową kategorią
main("Miasta_na_prawach_powiatu")
