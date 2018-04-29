"""
@warning:   Citation of multiple keys with options (e.g. \cite[p.1,p.2]{key1,key2})
            is not handled well by "harvard" packages, so it is not supported by
            this parser.

            In this parser, \cite[p.1,p.2]{key1,key2} is parsed into:
                (author1 year1, p.1,p.2, author2 year2, p.1,p.2)

            This will result in word count errors. Do not use this command.
"""


from bib2dic import bib2dic
import re


''' complete = 1 is designed to handle the abbr mode.
 
        |   abbr == 0 : use complete citation at the first time, 
        |               and use et al. for the following cases (authors >= 2)
        |   abbr == 1 : always use et al. (authors >= 2)
    
    The abbr mode has not been supported yet. 
'''


def concatenate_last_name(citation_key: str, bib_dic, complete_return=0) -> str:
    authors = bib_dic[citation_key]["author"].split(" and ")
    last_names = [each.split(", ")[0] for each in authors]
    if complete_return == 0:
        if len(authors) == 1:
            return last_names[0]
        if len(authors) == 2:
            return "%s & %s" % (last_names[0], last_names[1])
        if len(authors) >= 3:
            return "%s et al." % (last_names[0])
    if complete_return == 1:
        tmp = ""
        for each in last_names:
            tmp += (each + " & ")
        return tmp.strip(" & ")


def cite_parser(string, bib_dic, command: str, complete_parse=0) -> str:
    # citation_list = re.findall(r"(\\cite(\[.*\])*{\S+})", string)
    citation_list = re.findall(r"(\\%s(\[[^\]]*\])*{\S+}({[^}]+})*)" % command, string)
    for each_citation in citation_list:
        each_citation = each_citation[0]
        try:
            # option = re.search(r"cite\[(.+)\]{(.+)}", each_citation).group(1)
            option = re.search(r"%s\[(.+)\]{(.+)}({.*})*" % command, each_citation).group(1)
        except AttributeError:
            option = None
        # citation_keys = re.search(r"cite\[*(.*)\]*{(.+)}", each_citation).group(2).split(",")
        citation_keys = re.search(r"%s(\[.*\])*{([^\s}]+)}({.+})*" % command, each_citation).group(2).split(",")
        try:
            affix = re.search(r"%s(\[.*\])*{([^\s}]+)}{([^}]+)}*" % command, each_citation).group(3)
        except AttributeError:
            affix = None
        tmp_string = ""
        for each_key in citation_keys:
            author = concatenate_last_name(each_key, bib_dic, complete_parse)
            year = bib_dic[each_key]["year"]
            if option is None:
                tmp_string += "(%s, %s)" % (author, year)
            else:
                tmp_string += "(%s, %s, %s)" % (author, year, option)
        tmp_string = tmp_string.replace(")(", ", ")
        if command == "citeaffixed":
            tmp_string = tmp_string.replace("(", "(%s " % affix)
        string = string.replace(each_citation, tmp_string)
    return string


def subjective_cite_pasrser(string, bib_dic, command: str, complete_parse=0) -> str:
    citation_list = re.findall(r"(\\%s(\[[^\]]*\])*{\S+})" % command, string)
    for each_citation in citation_list:
        each_citation = each_citation[0]
        try:
            option = re.search(r"%s\[(.+)\]{(.+)}" % command, each_citation).group(1)
        except AttributeError:
            option = None
        citation_key = re.search(r"%s\[*(.*)\]*{(.+)}" % command, each_citation).group(2)
        author = concatenate_last_name(citation_key, bib_dic, complete_parse)
        year = bib_dic[citation_key]["year"]
        if command == "citeasnoun":
            if option is None:
                string = string.replace(each_citation, "%s (%s)" % (author, year))
            else:
                string = string.replace(each_citation, "%s (%s, %s)" % (author, year, option))
        if command == "possessivecite":
            if option is None:
                string = string.replace(each_citation, "%s's (%s)" % (author, year))
            else:
                string = string.replace(each_citation, "%s's (%s, %s)" % (author, year, option))
    return string


def partially_cite_parser(string, bib_dic, command: str, complete_parse=0) -> str:
    citation_list = re.findall(r"\\%s{[^\s}]+}" % command, string)
    for each_citation in citation_list:
        citation_key = re.search(r"\\%s{([^\s}]+)}" % command, each_citation).group(1)
        author = concatenate_last_name(citation_key, bib_dic, complete_parse)
        year = bib_dic[citation_key]["year"]
        if command == "citename":
            string = string.replace(each_citation, author)
        if command == "citeyear":
            string = string.replace(each_citation, year)
    return string


if __name__ == "__main__":
    with open("test/references.bib", "rt") as f:
        c = f.read()

    dic = bib2dic(c)

    test_s = '''
cite_parser:
    cite{key1}                   :  \cite{lake_tailoring_1998}
    cite[p.6]{key1}              :  \cite[p.6]{lock_visibility_2014}
    cite{key1,key2}              :  \cite{renfrew_investigations_1979,lake_tailoring_1998}
    citeaffixed{key1}{e.g.}      :  \citeaffixed{lock_visibility_2014}{e.g.}
    citeaffixed{key1,ket2}{e.g.} :  \citeaffixed{renfrew_investigations_1979,lake_tailoring_1998}{e.g.}

subjective_cite_pasrser:
    citeasnoun{key1}             :  \citeasnoun{lock_visibility_2014}
    citeasnoun[p.6]{key1}        :  \citeasnoun[p.6]{renfrew_investigations_1979}
    possessivecite{key1}         :  \possessivecite{lake_tailoring_1998}
    possessivecite[p.6]{key1}    :  \possessivecite[p.6]{lock_visibility_2014}

partially_cite_parser:
    citename{key1}               :  \citename{renfrew_investigations_1979}
    citeyear{key1}               :  \citeyear{lake_tailoring_1998}
    '''

    parsed_s = cite_parser(test_s, dic, "cite", 0)
    parsed_s = cite_parser(parsed_s, dic, "citeaffixed", 0)
    parsed_s = subjective_cite_pasrser(parsed_s, dic, "citeasnoun", 0)
    parsed_s = subjective_cite_pasrser(parsed_s, dic, "possessivecite", 0)
    parsed_s = partially_cite_parser(parsed_s, dic, "citename", 0)
    parsed_s = partially_cite_parser(parsed_s, dic, "citeyear", 0)
    print(parsed_s)
