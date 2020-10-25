# Mapping Macalester's Majors

## Introduction

One of the defining characteristics of a liberal arts curriculum is the emphasis in taking classes from a variety of subjects. At Macalester College, some courses are cross-listed between disciplines to show they draw on material from multiple departments, and students are known to juggle multiple majors and minors. These connections and interrelations between subjects provide a prime opportunity to study them through a network science perspective. Network science allows us to understand these invisible links between subjects in new ways. I think we all have a general idea of what disciplines are related to one another -- like how Political Science and International Studies go together, or how Biology and Environmental Studies go together -- but this is all just an abstract idea inside our heads. By creating a network of these relationships, we turn this mapping into something concrete and exact. Thus in building this network, what we are really doing is visualizing the abstract. 
 
 In the following analysis we will examine the areas of study at Macalester through two separate networks: 1) a network of cross-listed courses over a four semester period from fall 2018 to spring 2020, and 2) a network of double majors/minors/concentrations using data from the class of 2020. The advantage of using these two types of networks is that we get a sense of the department versus student perspective on connections between disciplines. What cross-listed opportunities do departments offer to students? And where do student interests truly lie? By examining these two distinct views, hopefully we can see how interdisciplinary Macalester really is, and whether it lives up to its liberal arts ideology.


## Network Model

In this section I will discuss the details of what vertices and edges signify in the two types of networks. In both networks each vertex represents an area of study, but the vertices are slightly different in either network because there is not an exact correspondence between the prefixes listed on the class schedule and the degree areas offered at Macalester. For instance, although there is a data science minor, there is no designated prefix for data science courses. Moreover, information on concentrations does not appear on the class schedule. The following outlines the two types of network models:

1. **Network of cross-listed courses from fall 2018 to spring 2020**
    - vertices: areas of study listed on the class schedule
    - edges: a cross-listed course
    - edge weights: (three varieties) the number of cross-listed courses, the number of cross-listed sections, and enrollment in cross-listed courses

    I choose the timeframe of fall 2018 to spring 2020 for several reasons. For one, since I was comparing this network to the graduating class of 2020 it made sense for the final semester to be spring 2020. I did a two year (or four semester) period because classes are often rotated within departments and offered every other semester or every other year. This all gives us a larger sample size of classes. Finally, since I wanted to incorporate enrollment information into my network, if I used the 2020-2021 school year I would either have to use fall 2020 and leave out spring 2021, which would be somewhat awkward, or I would have to use both semesters and deal with having no enrollment information for spring 2021.

2. **Network of double majors/minors/concentrations from the class of 2020**
    - vertices: areas of study listed for degrees
    - edges: a combination of two areas which a student earned a degree in
    - edge weight: calculated using the following formula
    
    ```
    edge_weight = 1 * (# of double majors) + 0.5 * (all other combinations) 
    ```

    Thus a double major would contribute an edge weight of 1, whereas a double minor or a major and a concentration for instance would contribute an edge weight of 0.5. I choose this weighting schema so that it would favor majors a little bit more since majors have more requirements, and I figured that minors and concentrations should be roughly equivalent. 

## Methodology

#### Cross-listed network

To gather data on cross-listed courses at Macalester I scraped course information from the registrar's [class schedule](https://www.macalester.edu/registrar/schedules/2020fall/class-schedule/). In order to do this, I used the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) web scraping library in Python and made extensive use of regular expressions, which is a syntax for specifying text patterns. The scraper works by searching for the string "cross-listed" within the whole class schedule, and for each match we get the course title, course number, enrollment, and what courses it's cross-listed with. To keep track of what courses we'd already seen, the data was organized in a Python dictionary where the keys were the course's name and the values were information about the course. This worked fairly well except in cases were the course names were slightly off between cross-listed courses. I resolved this by creating another dictionary of cross-listed numbers seen so far, and if a course number was previously mentioned that course got skipped. To generate the edges in the network, I got the list of prefixes for each course and for each combination of two prefixes I wrote an edge between those two subjects.

#### Graduates network

The network of double majors/minors/concentrations was created using text from a PDF of the 2020 Macalester Commencement Program. For each graduate the first line listed their name, the second line listed their hometown, and the third line listed their degrees. Because Macalester students love having degrees in multiple subjects, sometimes this third line would span multiple lines. This posed a problem since I couldn't reliably discern when one line was the continuation of a previous line or if it was a new person. To address this, I used a nifty little regular expression which found consecutive lines that mentioned the word "major", "minor", or "concentration" and combined those lines into one line. Then I generated the edges for the network by going through each line with degree information and for each combination of two subjects I made an edge connecting those two areas using the previously mentioned formula for edge weight.


## Results

#### Cross-listed network

![a network of cross-listed courses](assets/cross-listed.png)

<li style="color: #4cae4c">hello world</li>