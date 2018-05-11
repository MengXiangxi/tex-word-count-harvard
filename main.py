from extract_text import extract_text
from bib2dic import bib2dic
from parser import cite_parser, subjective_cite_pasrser, partially_cite_parser
import os
import re


def read_cfg(cfg_path) -> str:
    with open(cfg_path, "rt") as f:
        lines = f.read().split(os.linesep)
    tex_path = lines[0].replace("tex path =", "")
    tex_path = re.sub(r"\s", "", tex_path)
    bib_path = lines[1].replace("bib path =", "")
    bib_path = re.sub(r"\s", "", bib_path)
    return tex_path, bib_path


def main(tex_path, bib_path) -> str:
    with open(tex_path, "rt") as f:
        tex = f.read()
    section_list, subsection_list, par_list = extract_text(tex)

    with open(bib_path, "rt") as f:
        bib = f.read()
    bib_dic = bib2dic(bib)

    def list2wordcount(content_list) -> int:
        count = 0
        for each in content_list:
            parsed_s = cite_parser(each, bib_dic, "cite", 0)
            parsed_s = cite_parser(parsed_s, bib_dic, "citeaffixed", 0)
            parsed_s = subjective_cite_pasrser(parsed_s, bib_dic, "citeasnoun", 0)
            parsed_s = subjective_cite_pasrser(parsed_s, bib_dic, "possessivecite", 0)
            parsed_s = partially_cite_parser(parsed_s, bib_dic, "citename", 0)
            parsed_s = partially_cite_parser(parsed_s, bib_dic, "citeyear", 0)
            words = parsed_s.split(" ")
            while "" in words:
                words.remove("")
            count += len(words)
        return count


    count_section = list2wordcount(section_list) + len(section_list)
    count_subsection = list2wordcount(subsection_list)
    count_par = list2wordcount(par_list)

    return('''Word count for this file:
        section:    %i
        subsection: %i
        par:        %i
        Total:      %i''' % (count_section, count_subsection, count_par, \
                             count_section + count_subsection + count_par))


if __name__ == "__main__":
    tex_path, bib_path = read_cfg("config")
    wc = main(tex_path, bib_path)
    print(wc)
