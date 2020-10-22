# https://github.com/kyawzazaw/macademics/blob/production/webscraper/webscraper/main.py
# Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import json
import re
import requests
import time
import itertools
from pprint import pp
from concurrent.futures import ThreadPoolExecutor


def exploratory_analysis(content):
    # find course titles that contain the word "introduction"
    result = set(content.find_all(class_="class-schedule-course-title", string=re.compile("introduction", re.I)))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find course titles that contain a 4 digit number (year)
    result = set(content.find_all(class_="class-schedule-course-title", string=re.compile(r"\d{4}")))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find info on cross-listed courses
    result = content.find_all(string=re.compile("cross-listed", re.I))
    for description in result:
        course_title = description.find_previous(class_="class-schedule-course-title").text
        cross_listed = re.search(r"cross-listed with (\w{4}[ -]\d{3}-\d{2}( and )?)*", description, re.I)
        assert cross_listed is not None
        print(course_title, "\n\t", cross_listed.group())
    print(len(result))


def get_cross_listed(content):
    """Return a dict with course names as keys and a list of prefixes (majors/minors) as values"""
    result = content.find_all(string=re.compile("cross-listed", re.I))
    courses = {}
    for description in result:
        course_title = description.find_previous(class_="class-schedule-course-title").text     # ex: Network Science
        course_number = description.find_previous(class_="class-schedule-course-number").text   # ex: COMP 479-01
        if course_number[-2] == 'L':  # course is a lab, do not add it
            print(f"Removed a lab: {course_title}")
            continue
        avail_max = description.find_previous(class_="class-schedule-label").text               # ex: Closed 1 / 16
        available_seats, max_capacity = map(int, re.search(r"(-?\d+) / (\d+)", avail_max).groups())  # 1, 16
        enrollment = max_capacity - available_seats

        if course_title not in courses:
            cross_listed_with = re.findall(r"\w{3,4}[ -]\d{3}-\d{2}", description)      # ex: MATH 479-01
            course_numbers = [course_number] + cross_listed_with                        # ex: [COMP 479-01, MATH 479-01]
            prefixes = [re.search(r"\w+", i).group() for i in course_numbers]           # ex: [COMP, MATH]
            courses[course_title] = {
                "prefixes": prefixes,
                "course-numbers": course_numbers,
                "total-sections": 1,
                "total-enrollment": enrollment
            }
        elif course_number not in courses[course_title]["course-numbers"]:  # found a new section
            cross_listed_with = re.findall(r"\w{3,4}[ -]\d{3}-\d{2}", description)
            courses[course_title]["course-numbers"].extend([course_number] + cross_listed_with)
            courses[course_title]["total-sections"] += 1
            courses[course_title]["total-enrollment"] += enrollment

    return courses


def create_dataset(courses, file):
    """Create a csv dataset from a dict of course information"""
    with open(file, 'w') as f:
        for course, info in courses.items():
            f.write(f'"{course}", ')
            # convert lists to comma-separated strings, removing brackets and surrounding them in quotes
            values = [str(i).translate(str.maketrans("", "", "[]'")) for i in info.values()]
            values = [f'"{i}"' if re.search(r"[A-Z]", i) else i for i in values]
            f.write(", ".join(values))
            f.write("\n")


def create_nodes(content, file):
    result = content.find_all("h3", id=True)
    with open(file, 'w') as f:
        f.write("Id, Label\n")
        for subject in result:
            f.write(f'{subject.get("id")}, "{subject.text.strip()}" \n')    # ex: ANTH, "Anthropology"


def create_edges(courses, file, weight_by):
    with open(file, 'w') as f:
        f.write("Source, Target, Type, Weight\n")
        for course, info in courses.items():
            subject_pairs = itertools.combinations(info["prefixes"], 2)
            assert weight_by in ["courses", "sections", "enrollment"]
            if weight_by == "courses":
                edge_weight = 1
            elif weight_by == "sections":
                edge_weight = info["total-sections"]
            elif weight_by == "enrollment":
                edge_weight = info["total-enrollment"]

            for pair in subject_pairs:
                f.write(f'{pair[0]}, {pair[1]}, Undirected, {edge_weight}\n')


if __name__ == '__main__':
    semester_url = "https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/"
    semester_requests = requests.get(semester_url).text
    bs4_content = BeautifulSoup(semester_requests, "lxml")

    cross_listed_courses = get_cross_listed(bs4_content)
    # create_dataset(cross_listed_courses, "cross-listed.csv")
    #
    #
    # pp(cross_listed_courses)

    create_nodes(bs4_content, "nodes.csv")
    create_edges(cross_listed_courses, "edges.csv")

