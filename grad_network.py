import itertools
import re
from pprint import pp
from typing import List, Tuple, Dict, Union


subject_to_prefix = {
    "African Studies": "AFRI", "American Studies": "AMST",
    "Anthropology": "ANTH", "Applied Mathematics and Statistics": "AMS",
    "Art": "ART", "Asian Studies": "ASIA",
    "Biology": "BIOL", "Chemistry": "CHEM",
    "Chinese": "CHIN", "Classical Mediterranean and Middle East": "CLAS",
    "Cognitive Science": "CGSC", "Community and Global Health": "CGHC",
    "Computer Science": "COMP", "Critical Theory": "CRIT",
    "Data Science": "DATA", "Economics": "ECON",
    "Educational Studies": "EDUC", "English": "ENGL",
    "Environmental Studies": "ENVI", "Food, Agriculture and Society": "FASC",
    "French": "FREN", "Geography": "GEOG",
    "Geology": "GEOL", "German Studies": "GERM",
    "History": "HIST", "Human Rights and Humanitarianism": "HRHC",
    "Individually Designed Interdepartmental": "IDDI", "International Development": "INDE",
    "International Studies": "INTL", "Japanese": "JAPA",
    "Latin American Studies": "LATI", "Legal Studies": "LGLS",
    "Linguistics": "LING", "Mathematics": "MATH",
    "Media Studies": "MDST", "Media and Cultural Studies": "MCST",
    "Middle Eastern Studies and Islamic Civilization": "MEIC", "Music": "MUSI",
    "Neuroscience": "NSCI", "Performance Design and Technologies": "PFDT",
    "Philosophy": "PHIL", "Physics": "PHYS",
    "Political Science": "POLI", "Portuguese": "PORT",
    "Psychology": "PSYC", "Religious Studies": "RELI",
    "Russian Studies": "RUSS", "Sociology": "SOCI",
    "Spanish": "SPAN", "Statistics": "STAT",
    "Theater": "THTR", "Theater and Dance": "THDA",
    "Urban Studies": "URBN", "Women's, Gender, and Sexuality Studies": "WGSS"
}

prefix_to_subject = {v: k for k, v in subject_to_prefix.items()}


def create_nodes(in_file, out_file):
    degree_counts = count_grad_degrees(in_file)
    with open(out_file, 'w') as f:
        f.write("Id, Label, Weight, Size\n")
        for subject, counts in degree_counts.items():
            prefix = subject_to_prefix[subject.replace(" Concentration", "")]
            if type(counts) == int:     # concentration
                weight = 0.5 * counts
                size = counts
            else:                       # majors and minors
                weight = 1 * counts["major"] + 0.5 * counts["minor"]
                size = counts["major"] + counts["minor"]
            f.write(f'{prefix}, "{subject}", {weight}, {size}\n')    # ex: ANTH, "Anthropology", 17.5, 19


def create_edges(in_file, out_file):
    with open(in_file, 'r') as inp:
        with open(out_file, 'w') as out:
            out.write("Source, Target, Type, Weight\n")
            for line in inp:
                # read the subject and the word Major/Minor/Concentration,  ex: (Computer Science) (Major)
                degrees = re.findall(r"(?:, )?(.*?) (Major|Minor|Concentration)", line)
                subject_pairs = itertools.combinations(degrees, 2)
                # flatten tuples in the list
                # (('Chemistry', 'Major'), ('Biology', 'Minor')),  -->  ('Chemistry', 'Major', 'Biology', 'Minor'),
                subject_pairs = [i[0] + i[1] for i in subject_pairs]

                for pair in subject_pairs:
                    edge_weight = compute_edge_weight(pair[1], pair[3])
                    prefix_1, prefix_2 = subject_to_prefix[pair[0]], subject_to_prefix[pair[2]]
                    out.write(f'{prefix_1}, {prefix_2}, Undirected, {edge_weight}\n')


def compute_edge_weight(degree_type_1, degree_type_2):
    if degree_type_1 == "Major" and degree_type_2 == "Major":
        return 1
    else:
        return 0.5


def clean_commencement_text(in_file, out_file, separate_AMS=True, merge_majors=True, repl_apostrophe=True):
    new_text: str
    with open(in_file, 'r', encoding="utf-8") as f:
        text = f.read()
        # combine lines with major/minor/concentration info into one line
        new_text, num_subs = re.subn(r"""(?x) (.* (?:Major|Minor) .*)\n                   # match the first line
                                        (.* (?:Major|Minor|\b and\b|Concentration) .*)\n  # match the second line
                                        (.* (?:Major|Minor|Concentration) )? (\n)?      # match the third, optional line
                                    """, r"\1 \2 \3\n", text)                           # put the lines all on one line
        # the same regex without whitespace is:
        # "(.*(?:Major|Minor).*)\n(.*(?:Major|Minor|\band\b|Concentration).*)\n(.*(?:Major|Minor|Concentration))?(\n)?"
    print(f"{num_subs} substitutions made")

    if separate_AMS:
        new_text = re.sub(r"Mathematics \(Applied Mathematics and Statistics\)", "Applied Mathematics and Statistics", new_text)
    if merge_majors:
        new_text = re.sub(r" \(.*?\)", "", new_text)
    if repl_apostrophe:
        new_text = re.sub(r"’", "'", new_text)

    # get every third line from the text, these correspond to the lines with degree info
    degree_info = new_text.splitlines(keepends=True)[2::3]

    with open(out_file, 'w', encoding="utf-8") as f:
        f.write("".join(degree_info))


def count_grad_degrees(file):
    degree_counts: Dict[str, Union[Dict, int]] = {}
    degrees: List[Tuple[str, str]]
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        # read the subject and the word Major/Minor/Concentration,  ex: (Computer Science) (Major)
        degrees = re.findall(r"(?:, )?(.*?) (Major|Minor|Concentration)", text)

    for degree, degree_type in degrees:
        degree = degree + (" Concentration" if degree_type == "Concentration" else "")
        degree_type = degree_type.lower()
        if degree not in degree_counts:
            if degree_type == "concentration":
                degree_counts[degree] = 1
            else:
                degree_counts[degree] = {"major": 0, "minor": 0, degree_type: 1}
        else:
            if degree_type == "concentration":
                degree_counts[degree] += 1
            else:
                degree_counts[degree][degree_type] += 1

    return degree_counts


# clean_commencement_text("commencement_2020.txt", "mac_grads_2020_clean.txt")
# degree_counts = count_grad_degrees("mac_grads_2020_clean.txt")
# pp({k: degree_counts[k] for k in sorted(degree_counts.keys())})

create_nodes("nodes_grad.csv")
create_edges("mac_grads_2020_clean.txt", "edges_grad.csv")
