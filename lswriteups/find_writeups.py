import re
from halo import Halo
from tabulate import tabulate
from common import make_soup
from common import colors

ROOT_URL = "https://ctftime.org"


async def original_writeups(link):
    """Get all the information about events along with
       link to original writeups

    :link: A URL to the tasks of a CTF

    :return: Information about the all the task along with URL
             to original writeups in tabulated form
    """
    spinner = Halo(text=colors("Grabing writeups", "32"), spinner="moon", color="green")
    spinner.start()

    info = []
    headers = ["S.no", "Name", "Points", "tags", "URL"]
    soup = await make_soup(link)
    trs = soup.findAll("tr")

    # For getting tasks links
    for ind, tr in enumerate(trs[1:]):
        rated = {}
        gen = tr.text.split("\n")

        # Check if writeup exists or not
        if gen[-1] == str(0):
            tags = ",".join(gen[3:-2])
            info.append([ind, gen[0], gen[1], tags, "No writeups"])
            continue

        url = ROOT_URL + tr.find("a").get("href")
        soup = await make_soup(url)
        trs1 = soup.findAll("tr")

        # For getting "all" the writeups of one task
        for tr1 in trs1[1:]:
            para = soup.findAll("p")
            name = soup.find("h2").text
            point = para[0].text.split(":")[-1].strip()
            tags = para[1].text.split(":")[-1].split("\xa0")
            tags = ", ".join(i for i in tags[:-1])
            rated[tr1.find("a").get("href")] = tr1.find("div").text

        # Get writeup link which has the max rating.
        Link = await original_writeup_link(max(rated, key=rated.get))

        info.append([ind, name, point, tags, Link])

    table = tabulate(info, headers, tablefmt="fancy_grid")

    spinner.succeed("Voila!!")
    return table


async def original_writeup_link(url):
    """Extract link to original_writeup from a given URL
       If writeup is present on the same page of ctftimes
       then returned value is URL to that ctftime page


    :url: A URL to writeup page

    :return: A URL to original writeup
    """
    url = ROOT_URL + url
    soup = await make_soup(url)
    divs = soup.findAll("div", {"class": "well"})
    pattern = "https://?[a-z]+\S[a-z]+/[a-zA-Z0-9]+/"

    for div in divs:

        # When an orginial writeup link is given
        if div.text == "Original writeup.":
            return div.find("a").get("href")

        # When a URL to writeup is given but not in original writeup form
        if re.match(pattern, div.find("p").text):
            return div.find("p").text

        # When there is no link provided and writeup is present on ctftime
        if len("".join(i.text for i in soup.findAll("p"))) > 1000:
            return url
