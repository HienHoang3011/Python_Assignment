from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def format_age(x):
    if x != "":
        return x[:x.find('-')]
    return x

webdriver_path = r'C:\Windows\chromedriver.exe'
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
service = ChromeService(executable_path= webdriver_path)
driver = webdriver.Chrome(service= service, options= chrome_options)

url = {
    'standard_stat': 'https://fbref.com/en/comps/9/stats/Premier-League-Stats#all_stats_standard',
    'goalkeeping': "https://fbref.com/en/comps/9/keepers/Premier-League-Stats#all_stats_keeper",
    'shooting' : "https://fbref.com/en/comps/9/shooting/Premier-League-Stats#all_stats_shooting",
    'passing': "https://fbref.com/en/comps/9/passing/Premier-League-Stats#all_stats_passing",
    'goal_and_shot_creation': "https://fbref.com/en/comps/9/gca/Premier-League-Stats#all_stats_gca",
    'defensive_action' : "https://fbref.com/en/comps/9/defense/Premier-League-Stats#all_stats_defense",
    'possession' : "https://fbref.com/en/comps/9/possession/Premier-League-Stats#all_stats_possession",
    'misc' : "https://fbref.com/en/comps/9/misc/Premier-League-Stats#all_stats_misc"
}

driver.get(url['standard_stat'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find('table', class_ = "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
titles = table.find_all('tr')[1]
titles = titles.find_all('th')
for i in range(len(titles)):
    titles[i] = titles[i].text.strip()
titles = titles[1:]
titles[10], titles[11] ='Goals', 'Assists'
for i in range(25, 35):
    titles[i] = titles[i] +'/90'
dataframe = pd.DataFrame(columns=titles)
dataframe = dataframe.rename(columns= { 'MP': 'Match Played', 'Min': 'Minutes', 'CrdY': 'Yellow Cards', 'CrdR': 'Red Cards'})
rows = table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == 36:
        dataframe.loc[row_index] = row_data
        row_index += 1
dataframe['Age'] = dataframe['Age'].apply(format_age)
col_to_keep = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Match Played', 'Starts', 'Minutes', 'Goals', 'Assists', 'Yellow Cards', 'Red Cards', 'xG', 'xAG', "PrgC", "PrgP","PrgR", 'Gls/90', 'Ast/90', 'xG/90', 'xAG/90']
dataframe = dataframe[col_to_keep]

driver.get(url['shooting'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table', class_ = "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
titles = table.find_all('tr')[1]
titles = titles.find_all('th')[1:]
for i in range(len(titles)):
    titles[i] = titles[i].text.strip()
shooting_dataframe = pd.DataFrame(columns= titles)
rows = table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(titles):
        shooting_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player', 'Squad', 'SoT%', 'SoT/90', 'G/Sh', 'Dist']
shooting_dataframe = shooting_dataframe[col_to_keep]
dataframe = pd.merge(dataframe, shooting_dataframe, on = ['Player', 'Squad'], how = 'left')
dataframe = dataframe.drop_duplicates(keep='first')

driver.get(url['passing'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
passing_table = soup.find('table', class_ = "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
passing_titles = passing_table.find_all('tr')[1]
passing_titles = passing_titles.find_all('th')[1:]
for i in range(len(passing_titles)):
    passing_titles[i] = passing_titles[i].text.strip()
passing_titles[7], passing_titles[9], passing_titles[14], passing_titles[17], passing_titles[20] = 'Total_Cmp', 'Total_Cmp%' ,'Short_Cmp%', 'Medium_Cmp%','Long_Cmp%'
passing_dataframe = pd.DataFrame(columns= passing_titles)
rows = passing_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(passing_titles):
        passing_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player','Squad', 'Total_Cmp', 'Total_Cmp%', 'TotDist', 'Short_Cmp%', 'Medium_Cmp%', 'Long_Cmp%', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP']
passing_dataframe = passing_dataframe[col_to_keep].rename(columns={'PrgP':'(Passing)PrgP'})
dataframe = pd.merge(dataframe, passing_dataframe, on = ['Player', 'Squad'], how = 'left')
dataframe = dataframe.drop_duplicates(keep='first')

driver.get(url['goal_and_shot_creation'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
gasc_table = soup.find('table', class_ = "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
gasc_titles = gasc_table.find_all('tr')[1]
gasc_titles = gasc_titles.find_all('th')[1:]
for i in range(len(gasc_titles)):
    gasc_titles[i] = gasc_titles[i].text.strip()
gasc_dataframe = pd.DataFrame(columns=gasc_titles)
rows = gasc_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(gasc_titles):
        gasc_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player','Squad','SCA', 'SCA90', 'GCA', 'GCA90']
gasc_dataframe = gasc_dataframe[col_to_keep]
dataframe = pd.merge(dataframe, gasc_dataframe, on = ['Player','Squad'], how = 'left')
dataframe = dataframe.drop_duplicates(keep='first')

driver.get(url['defensive_action'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
defend_table = soup.find('table', id = "stats_defense")

defend_titles = defend_table.find_all('tr')[1]
defend_titles = defend_titles.find_all('th')

for i in range(len(defend_titles)):
    defend_titles[i] = defend_titles[i].text.strip()
defend_titles[13] = 'challenges' + defend_titles[13]
defend_titles = defend_titles[1:]
defend_dataframe = pd.DataFrame(columns= defend_titles)
rows = defend_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(defend_titles):
        defend_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player', 'Squad', 'Tkl', 'TklW', 'Att', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int']
defend_dataframe = defend_dataframe[col_to_keep]
dataframe = pd.merge(dataframe, defend_dataframe, on = ['Player', 'Squad'], how = 'left')
dataframe = dataframe.drop_duplicates(keep= 'first')

driver.get(url['possession'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
possess_table = soup.find('table', class_ ="min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
possess_titles = possess_table.find_all('tr')[1]
possess_titles = possess_titles.find_all('th')
possess_titles = possess_titles[1:]
for i in range(len(possess_titles)):
    possess_titles[i] = possess_titles[i].text.strip()
possess_titles[14], possess_titles[22], possess_titles[23], possess_titles[28] = 'Take-Ons_' + possess_titles[14], 'Carries_' + possess_titles[22], 'Carries_' + possess_titles[23], 'Receiving_' + possess_titles[28]
possess_dataframe = pd.DataFrame(columns= possess_titles)
rows = possess_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(possess_titles):
        possess_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player', 'Squad', 'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Take-Ons_Att', 'Succ%', 'Tkld%', 'Carries', 'PrgDist', 'Carries_PrgC', 'Carries_1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'Receiving_PrgR']
possess_dataframe = possess_dataframe[col_to_keep]
dataframe = pd.merge(dataframe, possess_dataframe, on = ['Player', 'Squad'], how = 'left')

driver.get(url['misc'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
misc_table = soup.find('table', class_ ="min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")
misc_titles = misc_table.find_all('tr')[1]
misc_titles = misc_titles.find_all('th')
misc_titles = misc_titles[1:]
for i in range(len(misc_titles)):
    misc_titles[i] = misc_titles[i].text.strip()
misc_dataframe = pd.DataFrame(columns= misc_titles)
rows = misc_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(misc_titles):
        misc_dataframe.loc[row_index] = row_data
        row_index += 1
col_to_keep = ['Player', 'Squad', 'Fls', 'Fld', 'Off', 'Crs', 'Recov', 'Won', 'Lost', 'Won%']
misc_dataframe = misc_dataframe[col_to_keep].rename(columns={'Lost': '(Misc)Lost'})
dataframe = pd.merge(dataframe, misc_dataframe, on = ['Player', 'Squad'], how='left')

driver.get(url['goalkeeping'])
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
goal_table = soup.find('table', id="stats_keeper")
goal_titles = goal_table.find_all('tr')[1]
goal_titles = goal_titles.find_all('th')[1:]
for i in range(len(goal_titles)):
    goal_titles[i] = goal_titles[i].text.strip()
goal_titles[24] = "Penalty_" + goal_titles[24] 
goal_dataframe = pd.DataFrame(columns= goal_titles)
rows = goal_table.find_all('tr')[2:]
row_index = 0
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text for cell in cells]
    if len(row_data) == len(goal_titles):
        goal_dataframe.loc[row_index] = row_data
        row_index += 1

col_to_keep = ['Player', 'Squad', 'GA90', 'Save%', 'CS%', 'Penalty_Save%']
goal_dataframe = goal_dataframe[col_to_keep]
dataframe = pd.merge(dataframe, goal_dataframe, on = ['Player', 'Squad'], how='left')

dataframe['Minutes'] = pd.to_numeric(
    dataframe['Minutes'].astype(str).str.replace(',', '', regex=False),
    errors='coerce'
)
dataframe = dataframe[dataframe['Minutes'] > 90].sort_values(by='Player').reset_index(drop=True)
dataframe = dataframe.replace('', np.nan)
dataframe = dataframe.fillna('N/a')
dataframe = dataframe.rename(columns= {'Pos':'Position', 'Squad' : 'Team'})
dataframe.to_csv('Exercise 1/result.csv', na_rep= 'N/a', index= False)

print("the result has been saved to result.csv")
driver.quit()