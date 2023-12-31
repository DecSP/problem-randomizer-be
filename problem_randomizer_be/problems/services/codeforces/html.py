from bs4 import BeautifulSoup

from ..utils import ProblemContentHTMLProcessor


class CodeforcesProblemContentHTMLProcessor(ProblemContentHTMLProcessor):
    def process_text(self, text):
        l_text = text.split("$$$")
        contents = []
        for index, item in enumerate(l_text):
            if index % 2 == 1:
                contents.append(self.tag_to_dict("var", item))
            else:
                contents.append(item)
        return contents

    def process_pre(self, pre):
        divs = pre.find_all("div")
        if len(divs):
            return ["\n".join(map(lambda x: x.text, divs))]
        return [pre.text.strip()]

    def get_content(self, tag):
        if tag.name in ["p", "li", "pre", "center"]:
            re = self.tag_to_dict(tag.name, list(map(self.process_child, tag.contents)))
            real_content = []
            for text in re["content"]:
                if isinstance(text, str):
                    real_content += self.process_text(text)
                else:
                    real_content.append(text)
            re["content"] = real_content
            return re
        contents = []
        children = tag.contents
        for child in children:
            if not child.name:
                continue
            contents.append(self.get_content(child))
        return self.tag_to_dict(tag.name, contents)

    def section_to_data(self, section):
        section_name = "Problem Statement"
        section_content = []
        for child in section.children:
            if child.name == "div":
                if child.attrs["class"] == ["section-title"]:
                    section_name = child.text
                elif child.attrs["class"] == ["sample-test"]:
                    for div in child.children:
                        if div.name != "div":
                            continue
                        if div.attrs["class"] == ["input"]:
                            section_content.append(self.tag_to_dict("p", ["Input"]))
                            pre = div.find("pre")
                            section_content.append(self.tag_to_dict("pre", self.process_pre(pre)))
                        if div.attrs["class"] == ["output"]:
                            section_content.append(self.tag_to_dict("p", ["Output"]))
                            pre = div.find("pre")
                            section_content.append(self.tag_to_dict("pre", self.process_pre(pre)))

            elif child.name:
                section_content.append(self.get_content(child))
        return self.section_to_dict(section_name, section_content)

    def html_to_data(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        prob_statement = soup.find("div", {"class": "problem-statement"})
        prob_statement.find("div", {"class": "header"}).extract()
        for span in prob_statement.find_all("span"):
            span.extract()

        divs = prob_statement.find_all("div", recursive=False)
        re = []
        for div in divs:
            re.append(self.section_to_data(div))
        # import json

        # print(json.dumps(re, indent=2))

        return re
