# football-statistics-tutorial

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
