class ProblemContentHTMLProcessor:
    def tag_to_dict(self, tag, content):
        return {"tag": tag, "content": content}

    def section_to_dict(self, section, children):
        return {"section": section, "children": children}

    def process_child(self, tag):
        if tag.name == "img":
            return self.tag_to_dict(tag.name, tag.attrs["src"])
        if tag.name:
            return self.tag_to_dict(tag.name, tag.text)
        return tag
