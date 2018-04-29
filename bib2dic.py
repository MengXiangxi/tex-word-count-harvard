import os
import re


def bib2dic(bib_text: str) -> dict:
    bib_lines = bib_text.split(os.linesep)
    while "" in bib_lines:
        bib_lines.remove("")
    dic = {}
    tmp = ""
    for each_line in bib_lines:
        if re.match(r"}", each_line):
            tmp += (os.linesep + each_line)
            dic[key] = tmp
            tmp = ""
        if re.match(r"^@", each_line):
            key = re.search(r"@.+{(.+),", each_line).group(1)
            tmp = each_line
        else:
            tmp += (os.linesep + each_line)
    for key in dic:
        tmp_dic = {}
        lines = dic[key].split(os.linesep)
        for each_line in lines:
            match = re.match(r"\s(.+) = {(.+)},", each_line)
            if match:
                tmp_key = match.group(1)
                tmp_value = match.group(2)
                tmp_dic[tmp_key] = tmp_value
        dic[key] = tmp_dic
    return dic


if __name__ == "__main__":
    with open("test/references.bib", "rt") as f:
        c = f.read()

    r = bib2dic(c)
    print(r["lake_tailoring_1998"]["author"])
