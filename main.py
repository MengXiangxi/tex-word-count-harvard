from count_cite import count_cite
from extract_text import extract_text
from parser import parse_cite, parse_ref
import re
import os

with open("config", "rU") as config_file:
    config = config_file.read()
    # bib_path = re.search(r'bib_path = "(.+)"', config).group(1)
    tex_path = re.search(r'tex_path = "(.+)"', config).group(1)

section_list, subsection_list, par_list = extract_text(tex_path)


def count_word(list_of_text):
    tmp_list = []
    for each in list_of_text:
        tmp_list = tmp_list + (each.split(" "))
    return len(tmp_list)


count_headings = count_word(section_list) * 2
count_subheadings = count_word(subsection_list) * 2

for i in range(len(par_list)):
    tmp = parse_cite(par_list[i], flag="cite")
    tmp = parse_cite(tmp, flag="citeasnoun")
    tmp = parse_cite(tmp, flag="citeyear")
    tmp = parse_ref(tmp)
    par_list[i] = tmp

count_par = count_word(par_list)

print(os.linesep + "------------------")
print("Headings:", count_headings)
if not count_subheadings:
    print("Sub-headings", count_subheadings)
print("Main parts:", count_par)
print("------------------")
print(os.linesep + "*** Total:", count_headings + count_subheadings + count_par)


# text output for debugging use
# text_output = ""
# for each in section_list:
#     text_output += each
# for each in subsection_list:
#     text_output += each
# for each in par_list:
#     text_output += each
#
# print(text_output)