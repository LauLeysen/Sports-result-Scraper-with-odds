import pandas as pd

# Load data
file_path = 'mlb_matches24.xlsx'

# Load the Excel file
df = pd.read_excel(file_path, engine='openpyxl', sheet_name=0)

# Convert 'home_odd' and 'away_odd' to numeric, coercing errors which turns non-numeric (N/A) into NaN
df['home_odd'] = pd.to_numeric(df['home_odd'], errors='coerce')
df['away_odd'] = pd.to_numeric(df['away_odd'], errors='coerce')

# Remove rows where 'home_odd' or 'away_odd' are NA (which now includes original "N/A" strings)
df = df.dropna(subset=['home_odd', 'away_odd'])

# Remove rows where 'home_score' or 'away_score' is "-"
df = df[df['home_score'] != "-"]
df = df[df['away_score'] != "-"]

# Define the odds range for filtering
lower_odd_limit = 2.1
upper_odd_limit = 2.5

# Filter rows where away odds are within the specified range
filtered_df = df[(df['away_odd'] >= lower_odd_limit) & (df['away_odd'] <= upper_odd_limit)]

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

print(file_path)
print(f"All bets within odds range: {lower_odd_limit} to {upper_odd_limit}")
print(f"Total number of bets: {total_bets}")
print(f"The average of the away odds is: {average_away_odds:.2f}")
print(f"Win percentage when betting on away team within the specified odds range: {win_percentage:.2f}%")
print(f"Total profit/loss from betting $10 on each match within this range: ${total_profit:.2f}")
