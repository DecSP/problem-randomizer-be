from bs4 import BeautifulSoup


def tag_to_dict(tag, content):
    return {"tag": tag, "content": content}


def process_child(tag):
    if tag.name:
        return tag_to_dict(tag.name, tag.text)
    return tag


def get_content(x):
    if x.name in ["p", "li", "pre"]:
        return tag_to_dict(x.name, list(map(process_child, x.contents)))
    contents = []
    ll = x.contents
    for n in ll:
        if not n.name:
            continue
        contents.append(get_content(n))
    return tag_to_dict(x.name, contents)


def section_to_dict(section):
    key = None
    a1 = []
    for n in section.children:
        if n.name == "h3":
            key = n.text
        elif n.name:
            a1.append(get_content(n))
    return {"section": key, "children": a1}


def html_to_dict(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    span_with_lang_en = soup.find("span", {"class": "lang-en"})
    if not span_with_lang_en:
        return ""
    first_p_tag = span_with_lang_en.find("p")
    if first_p_tag and first_p_tag.text.startswith("Score"):
        first_p_tag.extract()

    elems = span_with_lang_en.find_all("div", {"class": "part"})
    re = []
    for elem in elems:
        re.append(section_to_dict(elem.find("section")))
    return re
