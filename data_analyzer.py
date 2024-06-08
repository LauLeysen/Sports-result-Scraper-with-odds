import pandas as pd

# Load data
file_path = 'cleaned_mlb_matches.xlsx'

# Load the Excel file
df = pd.read_excel(file_path, engine='openpyxl', sheet_name=0)
bets_above_odd = 2.1

# Remove rows where 'home_odd' or 'away_odd' are NA
df = df.dropna(subset=['home_odd', 'away_odd'])

# Filter rows where away odds are 2.0 or higher
filtered_df = df[df['away_odd'] >= bets_above_odd]

# Determine wins (where away score is greater than home score)
filtered_df['is_win'] = filtered_df['away_score'] > filtered_df['home_score']

# Calculate win percentage
win_percentage = filtered_df['is_win'].mean() * 100 if len(filtered_df) > 0 else 0

# Calculate the average of the away odds
average_away_odds = filtered_df['away_odd'].mean()

# Total number of bets placed
total_bets = len(filtered_df)

# Calculate profits/losses: $10 bet on each game
bet_amount = 10
profit_from_wins = sum((odds * bet_amount - bet_amount) for odds in filtered_df[filtered_df['is_win']]['away_odd'])
total_losses = (len(filtered_df) - filtered_df['is_win'].sum()) * bet_amount
total_profit = profit_from_wins - total_losses

# Calculate the longest win and loss streaks
longest_win_streak = 0
longest_loss_streak = 0
current_win_streak = 0
current_loss_streak = 0

for win in filtered_df['is_win']:
    if win:
        current_win_streak += 1
        current_loss_streak = 0
    else:
        current_loss_streak += 1
        current_win_streak = 0
    longest_win_streak = max(longest_win_streak, current_win_streak)
    longest_loss_streak = max(longest_loss_streak, current_loss_streak)

print(file_path)
print(f"All bets over: {bets_above_odd}")
print(f"Total number of bets: {total_bets}")
print(f"The average of the away odds is: {average_away_odds:.2f}")
print(f"Win percentage when betting on away team with 2+ odds: {win_percentage:.2f}%")
print(f"Total profit/loss from betting $10 on each match: ${total_profit:.2f}")
print(f"Longest win streak: {longest_win_streak}")
print(f"Longest loss streak: {longest_loss_streak}")
