import re
import os


def extract_text(tex_text: str) -> list:
    lines = tex_text.split(os.linesep)
    section_list = []
    subsection_list = [] 
    par_list = []
    for each in lines:
        # print each
        try:
            section = re.search(r".*section{(.+)}.*", each).group(1)
            section_list.append(section)
        except AttributeError:
            pass
        try:
            subsection = re.search(r".*subsection{(.+).*}", each).group(1)
            subsection_list.append(subsection)
        except AttributeError:
            pass
        try:
            par = re.search(r".*par{(.+)}.*", each).group(1)
            par_list.append(par)
        except AttributeError:
            pass
    return section_list, subsection_list, par_list


if __name__ == "__main__":
    with open("test/test.tex", "rt") as f:
        text = f.read()
    section_list, subsection_list, par_list = extract_text(text)
    print(section_list)
    print(subsection_list)
    print(par_list)
