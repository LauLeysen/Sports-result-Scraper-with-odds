# NBA-Scraper-with-odds

### Introduction
This project is inspired by a curiosity-driven exploration into the world of sports betting, particularly focusing on the outcomes when betting solely on the home or away teams in basketball matches. This approach was driven by the question: "What would happen if you consistently bet on one side throughout the season?" Using a Python-based script, we scrape basketball match odds and results from a sports data website to analyze betting strategies over a series of games. We scrape [AI score ](https://www.aiscore.com) and the pre match odds(mostly bet365) / results and calculate whatever we want to know.

### EDIT
I did the same for MLB now with an extra file data_analyzer that uses pandas library to go more in depth for the analysis.
example output for scraped MLB matches in 2023 season:
```
cleaned_mlb_matches.xlsx
All bets over: 2.1
Total number of bets: 956
The average of the away odds is: 2.57
Win percentage when betting on away team with 2+ odds: 42.47%
Total profit/loss from betting $10 on each match: $537.30
Longest win streak: 6
Longest loss streak: 11
```

### Disclaimer
The bets discussed in this project were not actually placed; all scenarios and results are simulated based on historical data for research and curiosity purposes only.

### Project Summary
The script developed for this project uses Selenium for web navigation and BeautifulSoup for parsing HTML to extract data from a designated sports statistics website. The primary goal was to observe the fluctuation of profits and losses over a predefined set of basketball games, specifically betting €10 on either the home or the away team for each game.

### Project Summary
In the excel file you can see all processed data and the profit/loss after each bet.

### Outcomes Observed
- **Home Team Betting Strategy:**
  - Total loss recorded: -€983.4
  - This strategy indicated a consistent loss, reflecting the risks associated with betting on the home team alone.

- **Away Team Betting Strategy:**
  - Total profit recorded at its peak: €413.3
  - Lowest point reached: -€20.6
  - Total final profit: €66.5
  - Betting on the away team proved more volatile but reached higher profitability at certain points.

### Code Overview
The `WebNavigator` class encapsulates all the functionality required to interact with the web:
- **Setup and Navigation**: Initiates a Chrome WebDriver to navigate pages.
- **Element Interaction**: Waits for, locates, and interacts with page elements.
- **Data Extraction**: Extracts match details like teams, scores, and betting odds.
- **Session Management**: Manages browser sessions and cookies for continuity.

### Usage
1. **Setup**: Ensure you have Python and the necessary libraries installed (Selenium, BeautifulSoup, etc.).
2. **Execution**: Run the script to begin data extraction. The script will automatically navigate through the website, scraping data as configured.
3. **Data Review**: The extracted data is saved in JSON format, making it easy to review and analyze using various tools or scripts.

### Conclusion
This exploratory project reveals the unpredictable nature of betting based on fixed rules such as always selecting the home or away team. The insights from this exercise are invaluable for understanding betting dynamics and could be a stepping stone for developing more nuanced betting strategies in the future.

### Note
This project is intended for educational purposes only and should not be used as a guide for actual betting. Always consider the risks and legalities involved in sports betting.
"""