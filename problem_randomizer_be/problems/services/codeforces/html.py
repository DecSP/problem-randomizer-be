from bs4 import BeautifulSoup

from ..utils import ProblemContentHTMLProcessor


class CodeforcesProblemContentHTMLProcessor(ProblemContentHTMLProcessor):
    def process_pre(self, pre):
        divs = pre.find_all("div")
        if len(divs):
            return self.tag_to_dict("pre", ["\n".join(map(lambda x: x.text, divs))])
        return self.tag_to_dict("pre", [pre.text.strip()])

    def text_to_contents(self, text):
        l_text = text.split("$$$")
        contents = []
        for index, item in enumerate(l_text):
            if index % 2 == 1:
                contents.append(self.tag_to_dict("var", item))
            else:
                contents.append(item)
        return contents

    def process_para(self, tag):
        para = super().process_para(tag)
        real_content = []
        for text in para["content"]:
            if isinstance(text, str):
                real_content += self.text_to_contents(text)
            else:
                real_content.append(text)
        para["content"] = real_content
        return para

    def section_to_data(self, section):
        section_name = "Problem Statement"
        section_content = []
        for child in section.children:
            if child.name == "div":
                if child.attrs["class"] == ["section-title"]:
                    section_name = child.text
                elif child.attrs["class"] == ["sample-test"]:
                    sample_no = 1
                    for div in child.children:
                        if div.name != "div":
                            continue
                        if div.attrs["class"] == ["input"]:
                            section_content.append(self.tag_to_dict("p", [f"Sample Iput {sample_no}"]))
                            section_content.append(self.process_pre(div.find("pre")))
                        if div.attrs["class"] == ["output"]:
                            section_content.append(self.tag_to_dict("p", [f"Sample Output {sample_no}"]))
                            section_content.append(self.process_pre(div.find("pre")))
                            sample_no += 1

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

        return re
