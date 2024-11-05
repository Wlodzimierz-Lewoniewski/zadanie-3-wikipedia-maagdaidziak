import re
import requests


def fetch_article_links(category):
    url = f'https://pl.wikipedia.org/wiki/Kategoria:{category}'
    response = requests.get(url)
    links = re.findall(r'href="(/wiki/[^":#]+)"', response.text)
    article_links = ['https://pl.wikipedia.org' + link for link in links[:2]]
    return article_links


def fetch_article_content(url):
    response = requests.get(url)
    return response.text


def extract_internal_links(content):
    links = re.findall(r'<a href="/wiki/([^":#]+)"[^>]*>(.*?)</a>', content)
    return [f"{link_text} ({link_url})" for link_url, link_text in links[:5]]


def extract_image_urls(content):
    image_urls = re.findall(r'src="(//upload\.wikimedia\.org[^"]+)"', content)
    return [f"https:{url}" for url in image_urls[:3]]


def extract_external_links(content):
    external_links = re.findall(r'href="(https?://[^"]+)"', content)
    return external_links[:3]


def extract_categories(content):
    categories = re.findall(r'<a href="/wiki/Kategoria:([^":#]+)"[^>]*>(.*?)</a>', content)
    return [name for name, _ in categories[:3]]


def main():
    category = input("Podaj nazwę kategorii: ")
    articles = fetch_article_links(category)

    for i, article_url in enumerate(articles, 1):
        content = fetch_article_content(article_url)

        print(f"\nArtykuł {i} URL: {article_url}")

        internal_links = extract_internal_links(content)
        print("Nazwy artykułów wewnętrznych (pierwsze 5):")
        print("\n".join(internal_links) if internal_links else "\n")

        image_urls = extract_image_urls(content)
        print("Adresy URL obrazków (pierwsze 3):")
        print("\n".join(image_urls) if image_urls else "\n")

        external_links = extract_external_links(content)
        print("Adresy URL źródeł (pierwsze 3):")
        print("\n".join(external_links) if external_links else "\n")

        categories = extract_categories(content)
        print("Kategorie artykułu (pierwsze 3):")
        print("\n".join(categories) if categories else "\n")


if __name__ == "__main__":
    main()

