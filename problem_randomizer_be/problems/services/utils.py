class ProblemContentHTMLProcessor:
    para_tag_list = ["p", "li", "pre", "center"]

    def tag_to_dict(self, tag, content):
        return {"tag": tag, "content": content}

    def section_to_dict(self, section, children):
        return {"section": section, "children": children}

    def process_text(self, text):
        return text

    def process_img(self, tag):
        return self.tag_to_dict(tag.name, tag.attrs["src"])

    def process_child(self, tag):
        tag_name = getattr(tag, "name", None) or "text"
        process_method_name = f"process_{tag_name}"
        process_method = getattr(self, process_method_name, None)

        if callable(process_method):
            return process_method(tag)
        return self.tag_to_dict(tag.name, tag.text)

    def process_para(self, tag):
        return self.tag_to_dict(tag.name, list(map(self.process_child, tag.contents)))

    def get_content(self, tag):
        if tag.name in self.para_tag_list:
            return self.process_para(tag)
        contents = []
        children = tag.contents
        for child in children:
            if not child.name:  # skip normal text
                continue
            contents.append(self.get_content(child))
        return self.tag_to_dict(tag.name, contents)
