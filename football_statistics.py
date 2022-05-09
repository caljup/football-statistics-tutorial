"""

This script takes two approaches to scraping football
schedule data from ESPN.

The first method involves using requests and bs4
to grab and parse the data accordingly before
formatting into a pandas DataFrame.

The second method involves using pandas built-in
method read_html to accomplish similar results.

Both are implmented with concurrent python package
to capture multiple seasons using a Process or Thread Pool.

Note: Data lookback only encompasses 2003 - Present seasons
Time Comparisons:
bs4 method:

Process: 16.67 sec
Thread: 28.83 sec

pandas read_html method:

Process: 9.17 sec
Thread: 14.48 sec


Considerations:
>The bs4 method will naturally take longer since it has to parse through
the response, and the on page table is a slightly jumbled. Games yet
to be played for the current season have ticket and TV time information, causing those
headers to be different.

> When running pd.read_html on MacOS, SSL certification can throw an error.
Navigate to the respective application folder for Python3 and run
Install Certifications.command to resolve. 'lxml' also has to be installed.
If you see nothing appearing on the print line it's probably a lack of 'lxml'

>The pandas method will not return the respecitve season's year.
The data tables only contain the day/month for date. Since the ProcessPool
will return results in random order as they finish, a designation for the
year will need to be added in the tables to give proper context.

"""

import time

import concurrent.futures

import requests
from bs4 import BeautifulSoup
import pandas as pd



USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def scrape_espn(map_url):
    map_url, html = fetch_espn_results(map_url)
    results = parse_espn_results(html)
    return results


def fetch_espn_results(map_url):
    assert isinstance(map_url, str)
    response = requests.get(map_url, headers=USER_AGENT)
    response.raise_for_status()

    return map_url, response.text

def parse_espn_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    espn_table_name = soup.find('h1', class_='headline').text
    espn_table_columns = soup.find('colgroup').contents
    espn_table_body = soup.find('tbody')
    espn_table_rows = espn_table_body.find_all('tr')

    data_set = [[espn_table_name]]

    for row in espn_table_rows:
        espn_data_values = row.find_all('td')
        
        data_row = [data.get_text(separator=' ') for data in espn_data_values]

        data_set.append(data_row)
    
    pandas_column_names = [ 'Col_' + str(i) for i in range(1, len(espn_table_columns)+ 1)]

    df = pd.DataFrame(data_set, columns=pandas_column_names)

    df.fillna('', inplace=True)

    return df.head()


def read_html_espn_pandas(map_url):
    df2 = pd.read_html(map_url).pop()
    df2.fillna('', inplace=True)

    return df2.head()



MAX_PROCESS = 10

if __name__ == '__main__':

    base_url = 'https://www.espn.com/nfl/team/schedule/_/name/cin/season/'
    sample_url = 'https://www.espn.com/nfl/team/schedule/_/name/cin/season/2021'

    seasons = [base_url + str(i) for i in range(2003, 2022)] * 20

    start_time_bs4 = time.time()

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PROCESS) as executor:
            executor.map(scrape_espn, seasons)
    except Exception as e:
        print(e)
    
    print("Time to complete is: {}".format(time.time() - start_time_bs4))
    print(scrape_espn(sample_url))


    start_time_pandas = time.time()

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PROCESS) as executor:
            executor.map(read_html_espn_pandas, seasons)
    except Exception as e:
        print(e)

    print("Time to complete is Process: {}".format(time.time() - start_time_pandas))
    print(read_html_espn_pandas(sample_url))


    

