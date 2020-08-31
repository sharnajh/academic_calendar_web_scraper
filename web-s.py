from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

driver = webdriver.Chrome("./chromedriver")
driver.get("https://www.bmcc.cuny.edu/academics/academic-calendar/winter-2021/")
content = driver.page_source
soup = BeautifulSoup(content)

calendar = {
    "Subject": [],
    "Start Date": [],
    "Start Time": "12:00 AM",
    "End Date": [],
    "End Time": "11:59 PM",
    "All day event": "TRUE",
    "Description": "",
    "Location": ""
}

title = soup.find("h1", attrs={"class": "entry-title"}).text.strip().split(" ")
season = title[0]
year = title[-1]

dates = soup.find_all("td", attrs={"class": "column-1"})
events = soup.find_all("td", attrs={"class": "column-3"})

for event in events:
    calendar["Subject"].append(event.text.strip())


def check_month(cmonth):
    if len(calendar["Start Date"]) >= 1:
        ldate = calendar["Start Date"][-1].split("/")
        if not int(cmonth) >= int(ldate[0]):
            formatd = "/".join([*ldate[:-1], str(int(year) - 1)])
            calendar["Start Date"][-1] = calendar["End Date"][-1] = formatd


for date in dates:
    data = date.text.strip()

    if "-" in date.text:
        b = data.split("-")

        # Start Date
        start = b[0].strip().split(" ")
        start_month = datetime.strptime(start[0], "%B").month
        start_date = f'{start_month}/{start[1]}/{year}'

        check_month(start_month)

        # End Date
        end = b[1].strip().split(" ")
        if not end[0].isnumeric():
            end_month = datetime.strptime(end[0], "%B").month
            end_day = end[1]
        else:
            end_month = start_month
            end_day = end[0]
        end_date = f'{end_month}/{end_day}/{year}'
    else:
        m = data.split(" ")
        month = datetime.strptime(m[0], "%B").month
        check_month(month)
        start_date = end_date = f'{month}/{m[1]}/{year}'

    calendar["Start Date"].append(start_date)
    calendar["End Date"].append(end_date)


df = pd.DataFrame(calendar)
df.to_csv(f'{season}{year}_calendar.csv', index=False, encoding='utf-8')
