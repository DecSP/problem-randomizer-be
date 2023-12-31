from bs4 import BeautifulSoup

from ..utils import ProblemContentHTMLProcessor


class CsesProblemContentHTMLProcessor(ProblemContentHTMLProcessor):
    def process_span(self, tag):
        return self.tag_to_dict("var", tag.text)

    def html_to_data(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        divs = soup.find("div", {"class": "content"}).find("div", {"class": "md"}).children

        re = []
        section = "Problem Statement"
        current_section = []
        for div in divs:
            if not div.name:
                continue
            if div.name == "h1":
                if current_section:
                    re.append(self.section_to_dict(section, current_section))
                    current_section = []
                section = div.text
                continue
            current_section.append(self.get_content(div))
        if current_section:
            re.append(self.section_to_dict(section, current_section))
            current_section = []

        return re
