from bs4 import BeautifulSoup

from ..utils import ProblemContentHTMLProcessor


class AtcoderProblemContentHTMLProcessor(ProblemContentHTMLProcessor):
    def get_content(self, tag):
        if tag.name in ["p", "li", "pre"]:
            return self.tag_to_dict(tag.name, list(map(self.process_child, tag.contents)))
        contents = []
        children = tag.contents
        for child in children:
            if not child.name:
                continue
            contents.append(self.get_content(child))
        return self.tag_to_dict(tag.name, contents)

    def section_to_data(self, section):
        section_name = None
        section_content = []
        for child in section.children:
            if child.name == "h3":
                section_name = child.text
            elif child.name:
                section_content.append(self.get_content(child))
        return self.section_to_dict(section_name, section_content)

    def html_to_data(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        span_with_lang_en = soup.find("span", {"class": "lang-en"})
        if not span_with_lang_en:
            return {}
        first_p_tag = span_with_lang_en.find("p")
        if first_p_tag and first_p_tag.text.startswith("Score"):
            first_p_tag.extract()

        elems = span_with_lang_en.find_all("div", {"class": "part"})
        re = []
        for elem in elems:
            re.append(self.section_to_data(elem.find("section")))
        return re


class AtcoderProblemSubmissionHTMLProcessor:
    def get_submission_link(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Find the first link within the table
        tbody_element = soup.find("tbody")

        if tbody_element:
            tr_element = tbody_element.find("tr")
            if tr_element:
                # Find the first link within the tr
                link_element = tr_element.find("a", string="Detail", href=True)
                if link_element:
                    link = link_element["href"]
                    return link
        return None
