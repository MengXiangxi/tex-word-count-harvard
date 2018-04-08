import os
import re


def count_cite(bib_text):
    bib_lines = bib_text.split(os.linesep)
    while "" in bib_lines:
        bib_lines.remove("")

    # make a list of entries
    entry_list = []
    i = -1
    for each_line in bib_lines:
        if re.match(r"@.+{.+", each_line):
            entry_list.append(each_line)
            i += 1
        entry_list[i] = entry_list[i] + os.linesep + each_line

    # make a dictionary of id to authors
    dic_id_authors = {}
    for each in entry_list:

        entry_id = re.search(r"@.+{(.+),", each).group(1)

        # extract author = {...}
        author_search = re.search(r"author = {(.+)},", each)
        if author_search:
            authors = author_search.group(1)
        # alternatives when author is missing
        else:
            author_search = re.search(r"editora = {(.+)},", each)
            if author_search:
                authors = author_search.group(1)
            # reserved space for handling more exceptions

        dic_id_authors[entry_id] = authors

    # make a dictionary of the citation keys to their actual word count
    dic_id_wc = {}
    for each_key in dic_id_authors:
        authors = dic_id_authors[each_key]
        authors_list = authors.split(" and ")
        author_count = len(authors_list)

        wc_of_first_author = len(authors_list[0].split(",")[0].split(" "))
        try:
            wc_of_second_author = len(authors_list[1].split(",")[0].split(" "))
        except IndexError:
            pass

        if author_count == 1:
            final_word_count = wc_of_first_author + 1   # e.g. (Clark, 1996)
        if author_count == 2:
            final_word_count = wc_of_first_author + wc_of_second_author + 1
        #                                               # e.g. (Lake and Conolly, 2006)
        if author_count >= 3:
            final_word_count = wc_of_first_author + 3   # e.g. (Kvamme et al. 2006)

        dic_id_wc[each_key] = final_word_count

    return dic_id_wc
