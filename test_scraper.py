import importlib
import requests
from bs4 import BeautifulSoup
import os
from pprint import pp

course_scraper = importlib.import_module("course_scraper")


def test_more_than_one_prefix(courses):
    """Debug manually"""
    one_cross_list = {k: v for k, v in courses.items() if len(v["prefixes"]) <= 1}
    for i in one_cross_list:
        print(i, one_cross_list[i])


if __name__ == '__main__':
    semester_url = "https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/"
    semester_requests = requests.get(semester_url).text
    bs4_content = BeautifulSoup(semester_requests, "lxml")

    cross_listed_courses = course_scraper.get_cross_listed(bs4_content)
    test_more_than_one_prefix(cross_listed_courses)
