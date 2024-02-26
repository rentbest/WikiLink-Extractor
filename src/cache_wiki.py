from bs4 import BeautifulSoup
import requests
import click
import json
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def save_graph_as_json(graph, filename):
    graph_json = json.dumps(graph, indent=4)

    with open(filename, 'w') as file:
        file.write(graph_json)


def extract_links(soup):
    links_on_page = soup.select('p > a')
    h2_tag = soup.select_one('h2:has(span.mw-headline#See_also)')
    if h2_tag:
        ul_tag = h2_tag.find_next_sibling('ul')
        if ul_tag:
            see_also = ul_tag.select('a')
            links_on_page += see_also
    return links_on_page


def download_page(url):
    response = requests.get(f'https://en.wikipedia.org{url}')
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_all_links_on_page(page, deep_level, visited_pages):
    if not deep_level or visited_pages[0] > 1000:
        return {}
    links = {}
    soup = download_page(page)
    links_on_page = extract_links(soup)
    for link in links_on_page:
        if 'title' in link.attrs:
            visited_pages[0] += 1
            href = link['href']
            logging.info(f"Visited page: {href}")
            links[link['title']] = get_all_links_on_page(
                href, deep_level - 1, visited_pages)
    return links


@click.command()
@click.option('-p', '--default_start', type=str, default='Erdős number', help='starting wiki page')
@click.option('-d', '--deep', type=int, default=3, help='starting wiki page')
def main(default_start, deep):
    default_start.replace(' ', '_')
    visited_pages = [0, ]
    page_tree = get_all_links_on_page(
        f'/wiki/{default_start}', deep, visited_pages)
    save_graph_as_json(page_tree, 'wiki.json')


if __name__ == "__main__":
    main()
