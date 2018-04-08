from count_cite import count_cite
import re

with open("config", "rU") as config_file:
    config = config_file.read()
    bib_path = re.search(r'bib_path = "(.+)"', config).group(1)

with open(bib_path, "rU") as bib_file:
    bib_text = bib_file.read()

dic_key_wc = count_cite(bib_text)


# example text: "This is an example \cite{citation_key}. "
def parse_cite(text, flag="cite"):
    if flag == "cite":
        citation_keys = re.findall(r"cite{([\w,-]+)}", text)
    if flag == "citeasnoun":
        citation_keys = re.findall(r"citeasnoun{([\w,-]+)}", text)
    if flag == "citeyear":
        citation_keys = re.findall(r"citeyear{([\w,-]+)}", text)

    place_holder_list = []
    for each_key in citation_keys:
        word_count = 0
        if flag == "cite":
            for each in each_key.split(","):
                word_count += dic_key_wc[each]
        elif flag == "citeasnoun":
            word_count = dic_key_wc[each_key] - 1
        elif flag == "citeyear":
            word_count = 1
        tmp = "a"
        for i in range(word_count - 1):
            tmp += " a"
        place_holder_list.append(tmp)

    tmp_text = text
    for i in range(len(citation_keys)):
        if flag == "cite":
            tmp_text = tmp_text.replace("\cite{%s}" % citation_keys[i], place_holder_list[i])
        elif flag == "citeasnoun":
            tmp_text = tmp_text.replace("\citeasnoun{%s}" % citation_keys[i], place_holder_list[i])
        elif flag == "citeyear":
            tmp_text = tmp_text.replace("\citeyear{%s}" % citation_keys[i], place_holder_list[i])

    return tmp_text


def parse_ref(text):
    cross_ref = re.findall(r"ref{([\w,:]+)}", text)

    tmp_text = text
    for i in range(len(cross_ref)):
        tmp_text = tmp_text.replace(r"\ref{%s}" % cross_ref[i], "b")

    return tmp_text
