from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv
import os

# Download the images. Using extraction of the src attribute and download using "requests" in Python. It's OK for this use-case because the images are small. If wanting to avoid double downloads (browser and Python), we can use other methods. The current method is simpler and generate better image quality and it's also more stable.
def downloadImg(url):
    filename = url.split("/")[-1]
    res = requests.get(url)
    os.makedirs(os.path.abspath("logos"), exist_ok=True)
    if res.status_code == 200:
        with open(f"logos/{filename}", "wb") as file:
            file.write(res.content)


def saveCSV(filename, data):
    os.makedirs(os.path.abspath("out"), exist_ok=True)
    with open(f"out/{filename}.csv", "w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        for data_arr in data:
            writer.writerow(data_arr)


def selectEls(type, value):
    return wait.until(EC.presence_of_all_elements_located((type, value)))


class ValueValidator:
    @staticmethod
    def text(a):
        return a.text if a is not None else ""

    @staticmethod
    def getAttribute(a, b):
        return a.get_attribute(b) if a is not None else ""


try:
    # Comment out the next 2 lines if wanting to see the chrome in action :)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Remove options=chrome_options for Chrome with GUI
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.pba.ph/teams")
    team_page_els = selectEls(By.CLASS_NAME, "team-page-img")
    team_urls = []
    team_img_urls = []
    print("Downloading images...")
    for el in team_page_els:
        team_img_url_el = el.find_element(By.CLASS_NAME, "team-page-team-logos")
        team_img_url = ValueValidator.getAttribute(team_img_url_el, "src")
        team_url_el = el.find_element(By.CSS_SELECTOR, "a[href]")
        team_url = ValueValidator.getAttribute(team_url_el, "href")
        team_urls.append(team_url)
        team_img_urls.append(team_img_url)
        downloadImg(team_img_url)
    print("Done downloading images.")
    print("Getting team info...")
    team_names = []
    team_coaches = []
    team_managers = []
    for url in team_urls:
        driver.get(url)
        team_name_el = selectEls(By.CSS_SELECTOR, ".team-profile-data h3")[0]
        team_name = ValueValidator.text(team_name_el)
        team_coach_el = selectEls(By.CLASS_NAME, "team-mgmt-data")[0]
        team_coach = ValueValidator.text(team_coach_el)
        team_manager_el = selectEls(By.CLASS_NAME, "team-mgmt-data")[1]
        team_manager = ValueValidator.text(team_manager_el)
        team_names.append(team_name)
        team_coaches.append(team_coach)
        team_managers.append(team_manager)
    teams_data = [["url", "image", "name", "coach", "manager"]]
    for i in range(len(team_urls)):
        teams_data.append([team_urls[i], team_img_urls[i], team_names[i], team_coaches[i], team_managers[i]])
        i += 1
    saveCSV("teams", teams_data)
    print("Done getting team info...")
    print("Getting players info...")
    pl_names = []
    pl_teams = []
    pl_nums = []
    pl_positions = []
    pl_urls = []
    pl_mugshots = []
    driver.get("https://www.pba.ph/players")
    player_el = selectEls(By.CLASS_NAME, "playersBox")
    for el in player_el:
        pl_name_el = el.find_element(By.CSS_SELECTOR, "a[href] > h5")
        pl_name = ValueValidator.getAttribute(pl_name_el, "value")
        pl_names.append(pl_name)
        pl_team_url_el = el.find_element(By.CSS_SELECTOR, "span > img")
        pl_team_url = ValueValidator.getAttribute(pl_team_url_el, "src")
        pl_teams.append(team_names[team_img_urls.index(pl_team_url)])
        pl_num_position_el = el.find_element(By.CSS_SELECTOR, "span > h6")
        pl_num_position = ValueValidator.text(pl_num_position_el)
        pl_num_position_split = pl_num_position.split(" |") if pl_num_position != "" else ""
        pl_nums.append(pl_num_position_split[0].strip())
        pl_positions.append(pl_num_position_split[1].strip())
        pl_url_el = el.find_element(By.CSS_SELECTOR, "center > a[href]")
        pl_url = ValueValidator.getAttribute(pl_url_el, "href")
        pl_urls.append(pl_url)
        pl_mugshot_el = el.find_element(By.CLASS_NAME, "stndrdImage")
        pl_mugshot = ValueValidator.getAttribute(pl_mugshot_el, "src")
        pl_mugshots.append(pl_mugshot)
    players_data = [["team", "name", "number", "position", "url", "mugshot"]]
    for i in range(len(pl_names)):
        players_data.append([pl_teams[i], pl_names[i], pl_nums[i], pl_positions[i], pl_urls[i], pl_mugshots[i]])
        i += 1
    saveCSV("players", players_data)
    print("Done getting players info...")
except Exception as e:
    print(f"An error occured: {e}")
finally:
    driver.quit()
