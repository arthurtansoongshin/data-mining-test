from bs4 import BeautifulSoup
import requests
import csv
import os


def loadPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup


def saveCSV(filename, data):
    os.makedirs(os.path.abspath("out"), exist_ok=True)
    with open(f"out/{filename}.csv", "w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        for data_arr in data:
            writer.writerow(data_arr)


class TeamInfoExtract:
    def __init__(self, main_page_url):
        self.main_page_url = main_page_url
        self.team_urls = []
        self.team_img_urls = []
        self.team_names = []
        self.team_coaches = []
        self.team_managers = []
        self.soup = loadPage(main_page_url)

    def getImgUrls(self):
        els = self.soup.select(".team-page-team-logos")
        for el in els:
            self.team_img_urls.append(el["src"])

    def getLogos(self):
        for url in self.team_img_urls:
            filename = url.split("/")[-1]
            res = requests.get(url)
            os.makedirs(os.path.abspath("logos"), exist_ok=True)
            if res.status_code == 200:
                with open(f"logos/{filename}", "wb") as file:
                    file.write(res.content)

    def getUrl(self):
        team_url_els = self.soup.select(".team-page-img a")
        for el in team_url_els:
            self.team_urls.append(el["href"])

    def getInfo(self):
        for url in self.team_urls:
            self.soup = loadPage(url)
            team_name_el = self.soup.select_one(".team-profile-data h3")
            self.team_coach_manager_el = self.soup.select(".team-personal-bar .team-mgmt-data")
            self.team_names.append(team_name_el.get_text())
            self.team_coaches.append(self.team_coach_manager_el[0].get_text())
            self.team_managers.append(self.team_coach_manager_el[1].get_text())

    def saveToCSV(self):
        teams_data = [["url", "image", "name", "coach", "manager"]]
        for i in range(len(self.team_urls)):
            teams_data.append([self.team_urls[i], self.team_img_urls[i], self.team_names[i], self.team_coaches[i], self.team_managers[i]])
            i += 1
        saveCSV("teams", teams_data)


class PlayerInfoExtract:
    def __init__(self, main_page_url):
        self.main_page_url = main_page_url
        self.pl_names = []
        self.pl_teams = []
        self.pl_nums = []
        self.pl_positions = []
        self.pl_urls = []
        self.pl_mugshots = []
        self.soup = loadPage(main_page_url)

    def getInfo(self, team_ref):
        pl_name_els = self.soup.select(".playersBox a[href] > h5")
        pl_team_url_els = self.soup.select(".playersBox span > img")
        pl_num_position_els = self.soup.select(".playersBox span > h6")
        pl_url_els = self.soup.select(".playersBox center > a[href]")
        pl_mugshot_els = self.soup.select(".playersBox .stndrdImage")
        self.pl_names = list(map(lambda n: n.get_text(), pl_name_els))
        self.pl_teams = list(map(lambda n: team_ref[1][team_ref[0].index(n["src"])], pl_team_url_els))
        self.pl_nums = list(map(lambda n: n.get_text().split(" |")[0].strip(), pl_num_position_els))
        self.pl_positions = list(map(lambda n: n.get_text().split(" |")[1].strip(), pl_num_position_els))
        self.pl_urls = list(map(lambda n: f"https://www.pba.ph/{n['href']}", pl_url_els))
        self.pl_mugshots = list(map(lambda n: n["src"], pl_mugshot_els))

    def saveToCSV(self):
        players_data = [["team", "name", "number", "position", "url", "mugshot"]]
        for i in range(len(self.pl_names)):
            players_data.append([self.pl_teams[i], self.pl_names[i], self.pl_nums[i], self.pl_positions[i], self.pl_urls[i], self.pl_mugshots[i]])
            i += 1
        saveCSV("players", players_data)


try:
    print("Extracting teams info and downloading logos...")
    team_info_extract = TeamInfoExtract("https://www.pba.ph/teams")
    team_info_extract.getImgUrls()
    team_info_extract.getLogos()
    team_info_extract.getUrl()
    team_info_extract.getInfo()
    team_info_extract.saveToCSV()
    print("Done extracting teams info and downloading logos.")

    print("Extracting players info and downloading logos...")
    player_info_extract = PlayerInfoExtract("https://www.pba.ph/players")
    player_info_extract.getInfo([team_info_extract.team_img_urls, team_info_extract.team_names])
    player_info_extract.saveToCSV()
    print("Done extracting players info and downloading logos.")

except Exception as e:
    print(f"An error occured: {e}")
