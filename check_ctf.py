import inquirer
from halo import Halo
from common import make_soup
from common import colors

URL = "https://ctftime.org/event/list/past"
ROOT_URL = "https://ctftime.org"


async def past_events():
    """Get names and URL of all the past events.

    :return: dictionary having name and URLs of CTFs
    """
    past = {}
    soup = await make_soup(URL)
    trs = soup.find_all("tr")
    trs.pop(0)
    for ctf in trs:
        link = ctf.find("a").get("href")
        name = ctf.find("a").text
        past[name.lower()] = link

    return past


def get_event(events, name):
    """Get specific events by the name

    :events: dictionary having name and URLs of the CTFs
    :name: Name of the CTF to search for

    :return: A dictionary containing the URL to the matched CTF
    """
    matched_ctfs = []
    for ctf in events.keys():
        if name.lower() in ctf:
            matched_ctfs.append({"name": ctf, "link": events[ctf]})

    return matched_ctfs


async def get_url(name):
    """Get URL of the specific event

    :name: Name of the CTF entered by user

    :return: A url of to the tasks of the CTF
            eg: https://ctftime.org/event/683/tasks/
    """

    spinner = Halo(text="Finding the URL", spinner="moon", color="red")
    spinner.start()
    past_ctfs = await past_events()
    ctfs = get_event(past_ctfs, name)

    if not ctfs:
        spinner.fail(colors("No CTF found", "32"))
        return

    if len(ctfs) != 1:
        spinner.stop()
        tables = [i["name"] for i in ctfs]
        question = [
            inquirer.List("choice", message="Choose one from below?", choices=tables)
        ]
        answer = inquirer.prompt(question)

        # Compare answer with name of CTF to get a link
        choice = list(filter(lambda ctf: ctf["name"] == answer["choice"], ctfs))
        url = ROOT_URL + choice[0]["link"] + "/tasks/"
        return url

    spinner.succeed("Got it")
    return ROOT_URL + ctfs[0]["link"] + "/tasks/"


async def show_prev_events():
    events = await past_events()
    ctfs = [i for i in events.keys()]
    question = [
        inquirer.List("choice", message="Choose one from below?", choices=ctfs[:10])
    ]
    answer = inquirer.prompt(question)

    return ROOT_URL + events[answer["choice"]] + "/tasks/"
