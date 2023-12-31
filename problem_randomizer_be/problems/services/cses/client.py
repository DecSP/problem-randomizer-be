from urllib.parse import urljoin

import httpx
import requests
from bs4 import BeautifulSoup as bs

from problem_randomizer_be.problems.models import Problem

from .html import CsesProblemContentHTMLProcessor


class CsesClient:
    content_html_processor = CsesProblemContentHTMLProcessor()

    def get_cses_problems(self):
        url = "https://cses.fi/problemset"
        html = requests.get(url).text
        soup = bs(html, "html.parser")
        problems = []
        included_urls = set(Problem.objects.filter(source_type=Problem.SourceType.CSES).values_list("url", flat=True))

        for h2_tag in soup.find_all("h2")[1:]:
            next_sibling = h2_tag.find_next_sibling()
            if next_sibling and next_sibling.name == "ul":
                for link in next_sibling.find_all("a"):
                    path = link.get("href")
                    if path and path.startswith("/problemset/task"):
                        problem_url = urljoin(url, path)
                        if problem_url in included_urls:
                            continue
                        problems.append(
                            Problem(
                                name=link.text,
                                contest_name=h2_tag.text,
                                url=problem_url,
                                rating=1000,
                                source_type=Problem.SourceType.CSES,
                            )
                        )

        return problems

    def get_problem_content(self, url):
        html = httpx.get(url).text
        return self.content_html_processor.html_to_data(html)
