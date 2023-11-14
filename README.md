# cstat
This project scrapes the GFL CS:GO Zombie Escape Custom Stats page (https://cstat.snowy.gg/) to store individual player statistics.

### Background
This project was created to easily collect and compare player statistics. A player who was known for tracking weapon balance with advanced spreadsheets originally collected this data manually, so this project helped them call my stats "bad" more accurately.

## Requirements
- Selenium and Pandas python libraries (as well as their dependencies) can be installed by running `pip install -r requirements.txt`
- Mozilla Firefox web browser
- Web Driver for Firefox (may be pre-installed for linux distributions)

## Usage
Run `python cstat.py` for usage information.

## Future Improvements
### Efficient Order of Web Element Scraping
The critical performance bottleneck is the speed at which the Selenium Web Driver can capture web elements and scroll. Key elements must be within the window before they can be interacted with.
Currently, each player entry on a page is expanded, then each expanded table is scraped for information. This order of operations may be inefficient, but makes for the easiest implementation due to where key data points are located within the HTML elements and how the data is collected. If each table could be fully processed on the first pass, it would reduce the number of scroll/locate actions required, saving time (especially since scroll seems to be very slow!).

### Multithreading Support
Currently, many storage operations are made between web element fetching, which is ineffiicent. 
Ideally, we would want the Selenium engine to be running at full speed, with no actions between web fetches, however this is not how the current implementation works.
Web data extraction and storage should be done in parallel on multiple threads.
