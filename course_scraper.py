# https://github.com/kyawzazaw/macademics/blob/production/webscraper/webscraper/main.py
# Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import json
import re
import requests
import time
from pprint import pp
from concurrent.futures import ThreadPoolExecutor


def exploratory_analysis(content):
    # find course titles that contain the word "introduction"
    result = set(content.find_all(class_="class-schedule-course-title", string=re.compile("introduction", re.I)))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find course titles that contain a 4 digit number (year)
    result = set(content.find_all(class_="class-schedule-course-title", string=re.compile("\d{4}")))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find info on cross-listed courses
    result = content.find_all(string=re.compile("cross-listed", re.I))
    for description in result:
        course_title = description.find_previous(class_="class-schedule-course-title").text
        cross_listed = re.search("cross-listed with (\w{4}[ -]\d{3}-\d{2}( and )?)*", description, re.I)
        assert cross_listed is not None
        print(course_title, "\n\t", cross_listed.group())
    print(len(result))


def get_cross_listed(content):
    """Return a dict with course names as keys and a list of prefixes (majors/minors) as values"""
    result = content.find_all(string=re.compile("cross-listed", re.I))
    courses = {}
    for description in result:
        course_title = description.find_previous(class_="class-schedule-course-title").text
        course_number = description.find_previous(class_="class-schedule-course-number").text
        cross_listed_courses = re.findall("\w{4}[ -]\d{3}-\d{2}", description, re.I)
        if course_title not in courses:
            courses[course_title] = [course_number] + cross_listed_courses

    return courses


if __name__ == '__main__':
    semester_url = "https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/"
    semester_requests = requests.get(semester_url).text
    bs4_content = BeautifulSoup(semester_requests, "lxml")

    cross_listed = get_cross_listed(bs4_content)
    # find courses where there is only one cross-listed course; this needs to be fixed
    one_crosslist = {k: cross_listed[k] for k in cross_listed if len(cross_listed[k]) == 1}
    for i in one_crosslist:
        print(i, one_crosslist[i])

    # TODO: check for courses with different numbers

