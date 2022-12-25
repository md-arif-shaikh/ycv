"""Create yaml files from bib files."""
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author, convert_to_unicode
import yaml
import argparse
import os

def format_authors(list_of_authors, special_author):
    authors = ""
    num_authors = len(list_of_authors)
    for idx, author in enumerate(list_of_authors):
        last, first = author.split(", ")
        initials = "".join([x[0] + ". " for x in first.split(" ")])
        if idx <= (num_authors - 3):
            joining_string = ", "
        elif idx == (num_authors - 2):
            joining_string = " \& "
        else:
            joining_string = ""
        author_name = initials + last
        if author_name == special_author:
            author_name = r"\underline{" + author_name + "}"
        authors += author_name + joining_string
    return authors

def customizations(record):
    record = author(record)
    record = convert_to_unicode(record)
    return record

def format_entries(entries_dict, special_author):
    for k in entries_dict.keys():
        if "collaboration" not in entries_dict[k]:
            entries_dict[k]["author"] = format_authors(
                entries_dict[k]["author"], special_author)

def get_publication_dict_from_bib(bibfile, special_author):
    bib_file = open(bibfile, "r")
    parser = BibTexParser()
    parser.customization = customizations
    bib_database = bibtexparser.load(bib_file, parser=parser)
    bib_file.close()
    entries_dict = bib_database.entries_dict
    format_entries(entries_dict, special_author)
    return entries_dict

def get_publication_list_from_dict(pub_dict):
    publist = "\\begin{enumerate}\n"
    for k in pub_dict:
        d = data[k]
        if "collaboration" in d:
            d["author"] = d["collaboration"]
        p = "\\item "
        p += d["author"] + ", " + "``" + d["title"] + "\"" + ", "
        if "journal" in d:
            p += "\href{" + "https://doi.org/" + d["doi"] + "}{" + d["journal"] + "}" + ", "
            p += "{\\bfseries " + d["volume"] + "}" + ", " + d["pages"] + ", "
        p += "(" + d["year"] + "), "
        p += "\href{" + "https://arxiv.org/abs/" + d["eprint"] + "}{arXiv:" + d["eprint"] + " [" + d["primaryclass"] +"]}" + ", "
        publist += "\\end{enumerate}\n"
