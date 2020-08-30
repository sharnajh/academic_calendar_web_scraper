from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

year = 2021

driver = webdriver.Chrome("./chromedriver")
driver.get("https://www.bmcc.cuny.edu/academics/academic-calendar/winter-2021/")
content = driver.page_source
soup = BeautifulSoup(content)

start_dates = []
end_dates = []
subjects = []

for date in soup.find_all("td", attrs={"class": "column-1"}):
    data = date.text.strip()

    if "-" in date.text:
        # Start Date
        b = data.split("-")
        start = b[0].strip().split(" ")
        start_month = time.strptime(start[0], "%B").tm_mon
        start_day = start[1]
        start_date = f'{start_month}/{start_day}/{year}'

        # End Date
        end = b[1].strip().split(" ")
        if not end[0].isnumeric():
            end_month = time.strptime(end[0], "%B").tm_mon
            end_day = end[1]
        else:
            end_month = start_month
            end_day = end[0]
        end_date = f'{end_month}/{end_day}/{year}'
    else:
        m = data.split(" ")
        month = time.strptime(m[0], "%B").tm_mon
        day = m[1]
        start_date = end_date = f'{month}/{day}/{year}'

    start_dates.append(start_date)
    end_dates.append(end_date)

for event in soup.find_all("td", attrs={"class": "column-3"}):
    subjects.append(event.text.strip())

df = pd.DataFrame({'Subject': subjects, 'Start Date': start_dates,
                   'Start Time': "12:00 AM", 'End Date': end_dates, 'End Time': "11:59 PM", "All day event": "TRUE", "Description": "", "Location": ""})
df.to_csv('winter2021_calendar.csv', index=False, encoding='utf-8')
