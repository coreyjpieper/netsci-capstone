from pprint import pp
import re


def create_nodes(in_file, out_file):
    # result = content.find_all("h3", id=True)
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


clean_commencement_text("commencement_2020.txt", "commencement_2020_clean.txt")
