# https://github.com/kyawzazaw/macademics/blob/production/webscraper/webscraper/main.py
# Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import json
import re
import requests
import time
from pprint import pp
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    semester_url = "https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/"
    semester_requests = requests.get(semester_url).text
    bs4_content = BeautifulSoup(semester_requests, "lxml")

    # find course titles that contain the word "introduction"
    result = set(bs4_content.find_all(class_="class-schedule-course-title", string=re.compile("introduction", re.I)))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find course titles that contain a 4 digit number (year)
    result = set(bs4_content.find_all(class_="class-schedule-course-title", string=re.compile("\d{4}")))
    pp([course.text for course in result])
    print(len(result), "\n\n")

    # find info on cross-listed courses
    result = bs4_content.find_all(string=re.compile("cross-listed", re.I))
    for description in result:
        course_title = description.find_previous(class_="class-schedule-course-title").text
        cross_listed = re.search("cross-listed with (\w{4}[ -]\d{3}-\d{2}( and )?)*", description, re.I)
        assert cross_listed is not None
        print(course_title, "\n\t", cross_listed.group())
    print(len(result))
