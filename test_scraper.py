import importlib
import requests
from bs4 import BeautifulSoup
import os
from pprint import pp

course_scraper = importlib.import_module("course_scraper")


def test_more_than_one_prefix(courses):
    """
    Find courses where there is one or fewer prefixes listed. This should not be possible because each
    cross-listed course should have at least two prefixes.

    Usually this is caused by invalid cross-listed course numbers in the class schedule causing the regex
    to not pick up the course number, for example:

        *Cross-listed with MCST 2904-03*    # should be MCST 294-03
    """
    one_cross_list = {k: v for k, v in courses.items() if len(v["prefixes"]) <= 1}
    for i in one_cross_list:
        print(i, one_cross_list[i])


def test_prefixes_in_order(courses):
    """
    Find courses where the prefixes are not listed in alphabetical order. This should not be possible
    because the courses on the class schedule are listed and read alphabetically, and in the dictionary the course
    number comes before the cross-listed courses numbers.

    Usually this is caused by errors in the class schedule such as the same course being listed under different
    names, for example:

        Introduction to Analysis of Hispanic Texts
        Introduction to the Analysis of Hispanic Texts

        Queer and Trans Oral Hist Proj
        Queer and Trans Oral History Project

    or a cross-listed course missing from the description.
    """
    prefixes_out_of_order = {k: v for k, v in courses.items() if v["prefixes"] != sorted(v["prefixes"])}
    for i in prefixes_out_of_order:
        print(i, str(prefixes_out_of_order[i]))


if __name__ == '__main__':
    semester_url = "https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/"
    semester_requests = requests.get(semester_url).text
    bs4_content = BeautifulSoup(semester_requests, "lxml")

    cross_listed_courses = course_scraper.get_cross_listed(bs4_content)
    test_more_than_one_prefix(cross_listed_courses)
    print("\n\n")
    test_prefixes_in_order(cross_listed_courses)
