import re
from pprint import pp
from typing import List, Tuple, Dict, Union


def create_nodes(in_file, out_file):
    pass


def clean_commencement_text(in_file, out_file):
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


clean_commencement_text("commencement_2020.txt", "mac_grads_2020.txt")
pp(count_grad_degrees("mac_grads_2020.txt"))
