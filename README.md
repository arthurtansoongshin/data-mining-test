`Prerequisites:`

1. [Python 3.9.6](https://www.python.org/downloads/)
2. [pipenv](https://pypi.org/project/pipenv/)

`Setup Instructions:`

1. Download the folder from Github and unzip it (if downloaded using browser). Git pull can also be another downloading option.
2. Run "pipenv install" to install the Python dependencies.
3. Run "python pba.py" to scrap the website.
4. Folders containing the logos and csv files will be generated automatically.
5. "logos" folder includes the images of the teams.
6. "out/players.csv" and "out/teams.csv" contain the details of the players and the teams respectively.

`Extra Note`

1. selenium-do-not-use.py contains the codes for the solution using Selenium and Chromedriver. The codes there aren't written into classes, it might be a little messy. As requested by Sanjay, I will share it over here as well. This file is not meant to be used for the test, it's only for the reference.
