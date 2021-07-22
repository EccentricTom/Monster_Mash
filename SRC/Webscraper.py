# This script will scrap the required CR table that will form the backbone of the monster builder

# Import the necessary libraries
from selenium import webdriver
import pandas as pd
import os

# Set the Working directory as the project folder, makes it easier to organise project
os.chdir(os.path.split(os.getcwd())[0])
print(os.getcwd())
path = os.getcwd()

# Scrape the table cells from the url. In this case, the website is 5e.tools
url = 'https://5e.tools/crcalculator.html#0,13,0,3,false,Medium,1,10,false,0,false,0,'
options = webdriver.chrome.options.Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(executable_path=path+'\Driver\chromedriver.exe', options=options)
driver.implicitly_wait(50)
driver.get(url)
table_columns = driver.find_element_by_id('msbcr')
column_names = table_columns.text
contents = []
for i in range(2, 35):
    value = driver.find_element_by_xpath('//*[@id="msbcr"]/tbody/tr['+str(i)+']')
    row = value.text
    contents.append(row)
driver.close()
rows = []
for content in contents:
    if(content.find('or')!= -1):
        replaced = content.replace("0 or 10", "0/10")
        replaced = replaced.split()
        rows.append(replaced)
    else:
        new_contents = content.split()
        rows.append(new_contents)
column_names = column_names.split()
column_names[2:4] = [' '.join(column_names[2:4])]
column_names[3:5] = [' '.join(column_names[3:5])]
column_names[4:6] = [' '.join(column_names[4:6])]
column_names[5:7] = [' '.join(column_names[5:7])]
column_names[6:8] = [''.join(column_names[6:8])]
column_names[7:9] = [' '.join(column_names[7:9])]
df = pd.DataFrame(rows, columns=column_names)
df.to_csv('Data/CR_table.csv')

