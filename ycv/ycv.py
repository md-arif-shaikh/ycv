import yaml
import os
import argparse
from .yamlToTex import cleanup_tex, yamlToTeX

parser = argparse.ArgumentParser()
parser.add_argument(
    "-j",
    type=str,
    required=True,
    help="Job/position name. A directory with this name will be created to host tex and generated files.")
parser.add_argument(
    "-y",
    nargs="+",
    help="yaml files to use. Space separated with format" " <doc>:<yaml>.",
    type=lambda kv: kv.split(":"),
)
parser.add_argument(
    "-clean_tex",
    action="store_true",
    help="clean tex files",
)

args = parser.parse_args()
args.y = dict(args.y)
if not os.path.exists(args.j):
    os.mkdir(args.j)

def build_materials():
    yt = yamlToTeX(authinfo_file="authinfo.yaml",
                   style_file="style.yaml",
                   job=args.j)
    doc_dict = {"cv": yt.create_cv,
                "research_plan": yt.create_research_plan,
                "publications": yt.create_list_of_publications}
    for k in args.y:
        if k not in doc_dict:
            raise Exception(f"Do not know how to create {k}")
        doc_dict[k](args.y[k])
    if args.clean_tex:
        cleanup_tex(args.j)
