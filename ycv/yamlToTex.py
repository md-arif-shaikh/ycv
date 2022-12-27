import glob
import os
import yaml
from .publications import get_publication_dict_from_bib
import datetime


class yamlToTeX:
    """Module for building materials for job applications."""

    def __init__(self, authinfo_file="authinfo.yaml", style_file="style.yaml",
                 job=None):
        """Init with yaml files for author info and styles.

        parameters:
        -----------
        authinfo_file:
            yaml file containg author information.
        style_file:
            yaml file containg styles to apply in TeX.
        job_name:
            Job name to create all files in a directory with job name.
        """
        self.authinfo_file = authinfo_file
        self.style_file = style_file
        self.job = job
        if not os.path.exists(self.authinfo_file):
            print("Can not find `authinfo.yaml` file in the current directory.\n"
                  "This file is required to create appropriate headers.\n")
            create_now = input("Enter `y` to create an `authinfo.yaml` file now?: ")
            if create_now:
                self.create_authinfo_file()
        self.authinfo = self.get_data_from_yaml_file(self.authinfo_file)
        if not os.path.exists(self.style_file):
            print("Can not find `style.yaml` file in the current directory.\n"
                  "This file is required to apply styles in the TeX files.\n")
            create_now = input("Enter `y` to create a `style.yaml` file now?: ")
            if create_now:
                self.create_style_file()
        self.style = self.get_data_from_yaml_file(self.style_file)
        self.header_style = self.style["header"]

    def create_authinfo_file(self):
        entries = ["Name",
                   "Email",
                   "Website",
                   "Position",
                   "Department",
                   "Department website",
                   "Institute",
                   "Institute Website",
                   "Institute Address"]
        authinfo_file = open(self.authinfo_file, "w")
        for entry in entries:      
            val = input(f"{entry}: ")
            ent = entry.lower().replace(" ", "-")
            authinfo_file.write(f"{ent}: {val}\n")
        bib_name = input("Abbreviated name to be used in list of Publications. Example A. Einstein for Albert Einstein: ")
        authinfo_file.write(f"bib-name: {bib_name}")
        authinfo_file.close()
        print("Created `authinfo.yaml` file.")

    def create_style_file(self):
        styles = ""
        # header
        styles +="header:\n"
        styles +="  align: left\n"
        styles +="  top-rule: n\n"
        styles +="  bottom-rule: y\n"
        styles +="  top-rule-thickness: 1\n"
        styles +="  bottom-rule-thickness: 1\n"
        styles +="  title-fontsize: Large\n"
        styles +="research_plan:\n"
        styles +="  title: Research Plan\n"
        styles +="  section: subsection\n"
        styles +="  section-color:\n"
        styles +="  section-font:\n"
        styles +="  section-fontsize:\n"
        styles +="  numbered-section: n\n"
        styles +="cv:\n"
        styles +=f"  title: {self.authinfo['name']}\n"
        styles +="  section: section\n"
        styles +="  section-color:\n"
        styles +="  section-font:\n"
        styles +="  section-fontsize:\n"
        styles +="  numbered-section: n\n"
        styles +="publications:\n"
        styles +="  title: List of Publications\n"
        styles +="  section: section\n"
        styles +="  section-color:\n"
        styles +="  section-font:\n"
        styles +="  section-fontsize:\n"
        styles +="  numbered-section: n\n"
        styles +="tex:\n"
        styles +="  preamble:\n"
        styles +="  linkcolor:\n"
        styles +="  citecolor:\n"
        styles +="  filecolor:\n"
        styles +="  urlcolor:\n"
        styles +="  margin: 1in\n"
        styles +="  compiler:\n"
        style_file = open(self.style_file, "w")
        style_file.write(styles)
        style_file.close()
        print("Create `style.yaml`")

    def get_data_from_yaml_file(self, yaml_file):
        fl = open(yaml_file, "r")
        data = yaml.load(fl, Loader=yaml.CLoader)
        fl.close()
        return data

    def create_tex_preamble(self):
        preamble = "\\documentclass[10pt]{article}\n"
        preamble +="\\usepackage[margin=0.8in]{geometry}\n"
        preamble +="\\usepackage[dvipsnames, usenames]{xcolor}\n"
        preamble +="\\definecolor{linkcolor}{rgb}{0.0,0.3,0.5}\n"
        hyperref_colors = {}
        for c in ["linkcolor", "citecolor", "filecolor", "urlcolor"]:
            if self.style["tex"][c] is not None:
                hyperref_colors[c] = self.style["tex"][c]
            else:
                hyperref_colors[c] = "linkcolor"
        preamble +=(f"\\usepackage[colorlinks=true, linkcolor={hyperref_colors['linkcolor']},"
                    f"citecolor={hyperref_colors['citecolor']},"
                    f"filecolor={hyperref_colors['filecolor']},"
                    f"urlcolor={hyperref_colors['filecolor']},pdfusetitle]{{hyperref}}\n")
        preamble += "\\usepackage{titlesec}\n"
        preamble += ("\\titleformat{\\section}\n"
                     "{\\normalfont\\Large\\bfseries}{\\thesection}{1em}{}[{\\titlerule[0.5pt]}]")
        if "preamble" in self.style["tex"] and self.style["tex"]["preamble"] is not None:
            preamble += self.style["tex"]["preamble"]
        return preamble
        
    def create_header(self, doc_type="cv"):
        """Create header for TeX.

        parameters:
        -----------
        doc_type:
            Type of documents the header is intended for.
            Default is "cv"

        returns:
        --------
            header string suitable to be used in TeX documents.
        """
        align_dict = {"left": "{flushleft}",
                      "right": "{flushright}",
                      "center": "{center}"}
        align = align_dict[self.header_style["align"]]
        title = self.style[doc_type]["title"]
        header = f"\\begin{align}\n"
        header += f"{{\\{self.header_style['title-fontsize']} \\bfseries {title}}}\n\n"
        header += "\\vspace{0.25cm}\n\n"
        if doc_type != "cv":
            header += f"{{\\bfseries {self.authinfo['name']}}}, "
        header += f"{self.authinfo['position']}\\\\\n"
        header += f"\\href{{{self.authinfo['department-website']}}}{{{self.authinfo['department']}}}, "
        header += f"\href{{{self.authinfo['institute-website']}}}{{{self.authinfo['institute']}}}\\\\\n"
        header += f"{self.authinfo['institute-address']}\\\\\n"
        header += f"Email: \href{{mailto:{self.authinfo['email']}}}{{{self.authinfo['email']}}}, "
        header += f"Web page: \href{{{self.authinfo['website']}}}{{{self.authinfo['website']}}}\\\\\n"
        if self.header_style['bottom-rule'] == "y":
            header += "\\rule{\\textwidth}{" + f"{self.header_style['bottom-rule-thickness']}" + "pt}\n"
        header += f"\\end{align}\n"
        return header

    def create_research_plan(self, research_plan_file):
        # Write a TeX file
        extra_name = ("_" + self.job) if self.job is not None else ""
        tex_file = "research_plan" + extra_name + ".tex"
        if self.job is not None:
            if not os.path.exists(self.job):
                os.mkdir(self.job)
            research_plan = open(f"{self.job}/{tex_file}", "w")
        else:
            research_plan = open(tex_file, "w")
        # Add preamble
        research_plan.write(self.create_tex_preamble())
        research_plan.write("\\begin{document}\n")
        # Add header
        research_plan.write(self.create_header(doc_type="research_plan"))
        # Add research plan
        research_plan.write(self.create_research_plan_body(research_plan_file))
        research_plan.write("\\end{document}\n")
        research_plan.close()
        if self.job is not None:
            current_dir = os.getcwd()
            os.chdir(self.job)
        os.system(f"pdflatex -interaction=nonstopmode -halt-on-error {tex_file}")
        if self.job is not None:
            os.chdir(current_dir)

    def create_research_plan_body(self, research_plan_file):
        rp = self.get_data_from_yaml_file(research_plan_file)
        section_number = "" if self.style["research_plan"]["numbered-section"] == "y" else "*"
        section = self.style["research_plan"]["section"]
        research_plan = ""
        for sec in rp.keys():
            research_plan += "\\" + section + section_number + "{" + rp[sec]["title"] + "}\n"
            if "collaborators" in rp[sec]:
                collaborators = rp[sec]['collaborators']
                research_plan += rf"{{\bfseries Collaborators}}: {collaborators}\\"
            research_plan += r"\indent " + rp[sec]["details"] + "\n"
        return research_plan

    def create_cv(self, cv_file):
        # Write a TeX file
        extra_name = ("_" + self.job) if self.job is not None else ""
        tex_file = "cv" + extra_name + ".tex"
        if self.job is not None:
            if not os.path.exists(self.job):
                os.mkdir(self.job)
            tex = open(f"{self.job}/{tex_file}", "w")
        else:
            tex = open(tex_file, "w")
        # Add preamble
        tex.write(self.create_tex_preamble())
        tex.write("\\begin{document}\n")
        # Add header
        tex.write(self.create_header(doc_type="cv"))
        # Add cv
        tex.write(self.create_cv_body(cv_file))
        tex.write("\\end{document}\n")
        tex.close()
        if self.job is not None:
            current_dir = os.getcwd()
            os.chdir(self.job)
        os.system(f"pdflatex -interaction=nonstopmode -halt-on-error {tex_file}")
        if self.job is not None:
            os.chdir(current_dir)

    def create_cv_body(self, cv_file):
        """Create CV body based on cv_file.

        parameters:
        -----------
        cv_file:
            yaml file containing data to build cv.

        returns:
        --------
            Text to be used in TeX file for CV.
        """
        self.cv_file = cv_file
        self.cv = self.get_data_from_yaml_file(self.cv_file)
        self.cv_section_number = "" if self.style["cv"]["numbered-section"] == "y" else "*"
        self.cv_section = self.style["cv"]["section"]
        cv_body = ""
        for sec in self.cv["layout"]:
            cv_body += self.add_cv_section(sec)()
        return cv_body

    def add_cv_section(self, sec):
        cv_section_generators_dict = {"positions": self.create_positions_for_cv,
                                      "education": self.create_education_for_cv,
                                      "publications": self.create_list_of_publications_for_cv,
                                      "presentations": self.create_presentations_for_cv,
                                      "references": self.create_list_of_references_for_cv,
                                      "achievements": self.create_achievements_for_cv}
        return cv_section_generators_dict[sec]

    def create_positions_for_cv(self):
        positions = self.cv["positions"]
        pos_text = "\\" + self.cv_section + self.cv_section_number + "{Positions}\n"
        pos_text += "\\begin{itemize}\n"
        for idx, pos in enumerate(positions):
            p = positions[pos]
            if p['to-year'] is None:
                p['to-year'] = r"{\itshape current}"
            pos_text += fr"\item {{\bfseries {p['position']}}} \hfill {p['from-year']}--{p['to-year']}\\" + "\n"
            pos_text += self.create_link(p['department-website'], p['department'])
            pos_text += self.create_link(p['institute-website'], p['institute'], False) + r"\\" + "\n"
            pos_text += fr"{p['institute-address']}\\" + "\n"
            if p["mentor"] is not None:
                pos_text += rf"{{\itshape Mentors}}: {p['mentor']}" + "\n\n"
        pos_text += "\\end{itemize}\n"
        return pos_text

    def create_education_for_cv(self):
        education = self.cv["education"]
        edu_text = "\\" + self.cv_section + self.cv_section_number + "{Education}\n"
        edu_text += "\\begin{itemize}\n"
        for idx, edu in enumerate(education):
            d = education[edu]
            if d['to-year'] is None:
                d['to-year'] = r"{\itshape current}"
            edu_text += fr"\item {{\bfseries {d['degree']}}} \hfill {d['from-year']}--{d['to-year']}\\" + "\n"
            edu_text += self.create_link(d['department-website'], d['department'])
            edu_text += self.create_link(d['institute-website'], d['institute'], False) + r"\\" + "\n"
            edu_text += fr"{d['institute-address']}\\" + "\n"
            if d["advisor"] is not None:
                edu_text += rf"{{\itshape Advisor}}: {d['advisor']}" + "\n\n"
        edu_text += "\\end{itemize}\n"
        return edu_text

    def create_list_of_publications_for_cv(self):
        pubsections = self.cv["publications"]
        pub_text = "\\" + self.cv_section + self.cv_section_number + "{Publications}\n"
        for sec in pubsections:
            if sec == "directory":
                continue
            bib_dict = pubsections[sec]
            pub_text += self.create_list_of_publications_body(bib_dict)
        return pub_text

    def create_list_of_publications(self, publication_file):
        # Write a TeX file
        self.pub = self.get_data_from_yaml_file(publication_file)
        extra_name = ("_" + self.job) if self.job is not None else ""
        tex_file = "list_of_publications" + extra_name + ".tex"
        if self.job is not None:
            if not os.path.exists(self.job):
                os.mkdir(self.job)
            tex = open(f"{self.job}/{tex_file}", "w")
        else:
            tex = open(tex_file, "w")
        # Add preamble
        tex.write(self.create_tex_preamble())
        tex.write("\\begin{document}\n")
        # Add header
        tex.write(self.create_header(doc_type="publications"))
        # Add publications
        pubsections = self.pub["publications"]
        pub_text = ""
        for sec in pubsections:
            if sec == "directory":
                continue
            bib_dict = pubsections[sec]
            pub_text += self.create_list_of_publications_body(bib_dict)
        tex.write(pub_text)
        tex.write("\\end{document}\n")
        tex.close()
        if self.job is not None:
            current_dir = os.getcwd()
            os.chdir(self.job)
        os.system(f"pdflatex -interaction=nonstopmode -halt-on-error {tex_file}")
        if self.job is not None:
            os.chdir(current_dir)

    def create_list_of_publications_body(self, bib_dict):
        """Create list of publications in TeX format."""
        bibtitle = bib_dict["title"]
        publist = f"\\subsection*{{{bibtitle}}}\n"
        subtitle_dict = {"reviewed": "Peer reviewed publications",
                         "preprints": "Preprints"}
        for bib in bib_dict:
            if bib == "title":
                continue
            bibfile = bib_dict[bib]
            if self.cv["publications"]["directory"] is not None:
                bibfile = self.cv["publications"]["directory"] + bibfile
            pub_dict = get_publication_dict_from_bib(bibfile, special_author=self.authinfo["bib-name"])
            publist += fr"\subsubsection*{{{subtitle_dict[bib]}}}" + "\n"
            publist += self.create_list_for_tex_from_dict(pub_dict)
        return publist

    def create_list_for_tex_from_dict(self, data):
        p = "\\begin{enumerate}\n"
        for k in data.keys():
            d = data[k]
            if "collaboration" in d:
                d["author"] = d["collaboration"]
            p += "\\item "
            p += d["author"] + ", " + "``" + d["title"] + "\"" + ", "
            if "journal" in d:
                p += "\href{" + "https://doi.org/" + d["doi"] + "}{" + d["journal"] + "}" + ", "
                p += "{\\bfseries " + d["volume"] + "}" + ", " + d["pages"] + ", "
            p += "(" + d["year"] + "), "
            p += "\href{" + "https://arxiv.org/abs/" + d["eprint"] + "}{arXiv:" + d["eprint"] + " [" + d["primaryclass"] +"]}" + "\n"
        p += "\\end{enumerate}\n"
        return p

    def create_list_of_references_for_cv(self):
        ref_text = "\\" + self.cv_section + self.cv_section_number + "{References}\n"
        ref_text += self.create_list_of_references_body(self.cv_file)
        return ref_text

    def create_list_of_references_body(self, references_file):
        self.references_file = references_file
        self.references = self.get_data_from_yaml_file(self.references_file)["references"]
        references_text = "\\begin{itemize}\n"
        for idx, k in enumerate(self.references):
            ref = self.references[k]
            references_text += f"\\item {{\\bfseries {ref['name']}}}, "
            references_text += (f"{{({ref['relation']})}}" if ref['relation'] is not None else "") + r"\\" + "\n"
            references_text += ref['position'] + ", "
            references_text += self.create_link(ref['institute-website'], ref['institute'], False) + r" \\" + "\n"
            references_text += ref['institute-address'] + r" \\" + "\n"
            references_text += rf"Email: \href{{mailto:{ref['email']}}}{{{ref['email']}}}"
            if "phone" in ref and ref["phone"] is not None:
                references_text += rf", Phone: {ref['phone']}" + "\n\n"
            else:
                references_text += "\n\n"
        references_text += "\\end{itemize}\n"
        return references_text

    def create_presentations_for_cv(self):
        tex = "\\" + self.cv_section + self.cv_section_number + "{Conferences, seminars \& workshops}\n"
        for presentation in self.cv["presentations"]:
            title = self.cv["presentations"][presentation]["title"]
            tex += f"\\sub{self.cv_section}" + self.cv_section_number + f"{{{title}}}\n"
            tex += self.create_list_of_talks_body(self.cv["presentations"][presentation]["file"])
        return tex

    def create_list_of_talks_body(self, talks_file):
        self.talks_file = talks_file
        self.talks = self.get_data_from_yaml_file(talks_file)
        tex = "\\begin{enumerate}\n"
        for talk in self.talks:
            t = self.talks[talk]
            if "date" in t:
                d = datetime.date.fromisoformat(f"{t['date']}")
                day = d.strftime("%d")
                month = d.strftime("%B")
                year = d.strftime("%Y")
                t.update({
                    "from-date": day,
                    "to-date": day,
                    "from-month": month,
                    "to-month": month,
                    "to-year": year,
                    "from-year": year})
            if t["from-date"] == t["to-date"]:
               date = f"{t['from-month']} {t['from-date']}, {t['from-year']}" + "\n" 
            elif t['from-month'] == t['to-month']:
                date = f"{t['from-month']} {t['from-date']} -- {t['to-date']}, {t['from-year']}" + "\n"
            else:
                date = f"{t['from-month']} {t['from-date']} -- {t['from-month']} {t['to-date']}, {t['from-year']}" + "\n"
            tex += r"\item "
            if "title" in t:
                tex += f"``{t['title']}\", "
            if "conference" in t:
                tex += self.create_link(t['conference-url'], t['conference'])
            if "institute" in t:
                tex += self.create_link(t['institute-url'], t['institute'])
            tex += f"{t['city']}, {t['country']}, " + "\n"
            tex += date
        tex += "\\end{enumerate}\n"
        return tex

    def create_achievements_for_cv(self):
        ach = self.get_data_from_yaml_file(self.cv["achievements"]["file"])
        tex = "\\" + self.cv_section + self.cv_section_number + f"{{{self.cv['achievements']['title']}}}" + "\n"
        tex += "\\begin{itemize}\n"
        for achievement in ach:
            a = ach[achievement]
            org = self.create_link(a['organization-website'], a['organization'], False)
            tex += f"\\item {a['description']}, {org}, {a['year']}\n"
        tex += "\\end{itemize}\n"
        return tex

    def create_link(self, link, description, add_comma_space=True):
        return f"\\href{{{link}}}{{{description}}}" + (", " if add_comma_space else "")


def cleanup_tex(dir="./"):
    """Clean up tex files in dir."""
    extensions = ["out", "log", "aux"]
    for ext in extensions:
        files = glob.glob(f"{dir}/*.{ext}")
        if len(files) > 0:
            filesList = " ".join(files)
            os.system(f"rm {filesList}")
