from pprint import pp
import re


def create_nodes(in_file, out_file):
    # result = content.find_all("h3", id=True)
    pass


def clean_commencement_text(in_file, out_file):
    new_text: str

    with open(in_file, 'r', encoding="utf-8") as f:
        text = f.read()
        # the same regex w/o whitespace is:
        # "(.*(?:Major|Minor).*)\n(.*(?:Major|Minor|\band\b|Concentration).*)\n(.*(?:Major|Minor|Concentration))?(\n)?"
        new_text, num_subs = re.subn(r"""(?x) (.* (?:Major|Minor) .*)\n                   # match the first line
                                        (.* (?:Major|Minor|\b and\b|Concentration) .*)\n  # match the second line
                                        (.* (?:Major|Minor|Concentration) )? (\n)?        # match the third, optional line                                        
                                    """, r"\1 \2 \3\n", text)   # put the lines all on one line

    print(f"{num_subs} substitutions made")
    # get every third line from the text, the extra "\n" appended to new_text is needed to include the last person
    new_text = re.sub(r"(?x) .*\n .*\n (.*\n)", r"\1", new_text + "\n")

    with open(out_file, 'w', encoding="utf-8") as f:
        f.write(new_text)


clean_commencement_text("commencement_2020.txt", "commencement_2020_clean.txt")
