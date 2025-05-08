import matplotlib.pyplot as plt
import os
import pandas as pd

def get_top_3(stat):
    stat_df = df[['Player', 'Team', stat]].dropna()
    top_high = stat_df.nlargest(3, stat)
    top_low = stat_df.nsmallest(3, stat)
    return top_high, top_low

df = pd.read_csv('Exercise 1/result.csv', na_values= ['N/a'])
df.drop(columns= ["Age"], inplace= True)
df.replace("N/a", pd.NA, inplace= True)
numeric_cols = df.select_dtypes(include = ['number']).columns

with open('Exercise 2/top_3.txt', 'w', encoding='utf-8') as f:
    for stat in numeric_cols:
        top_high, top_low = get_top_3(stat)
        f.write(f"Statistic: {stat}\n")
        f.write("Top 3 Highest:\n")
        row_index = 1
        for _, row in top_high.iterrows():
            f.write(f" {row_index}. {row['Player']} ({row['Team']}) : {row[stat]}\n")
            row_index += 1
        row_index = 1
        f.write("Top 3 Lowest:\n")
        for _, row in top_low.iterrows():
            f.write(f" {row_index}. {row['Player']} ({row['Team']}): {row[stat]}\n")
            row_index += 1
        f.write("\n")
print("Results have been saved to top_3.txt")

numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
all_median = df[numerical_cols].median()
all_mean = df[numerical_cols].mean()
all_std = df[numerical_cols].std()

team_stats = df.groupby('Team')[numerical_cols].agg(['median', 'mean', 'std'])
team_stats.columns = [f'{measure.capitalize()} of {stat}' for stat, measure in team_stats.columns]
team_stats = team_stats.reset_index()

all_dict = {'Team': 'All'}
for col in numerical_cols:
    all_dict[f'Median of {col}'] = all_median[col]
    all_dict[f'Mean of {col}'] = all_mean[col]
    all_dict[f'Std of {col}'] = all_std[col]
all_df = pd.DataFrame([all_dict])

results_df = pd.concat([all_df, team_stats], ignore_index=True)
results_df['STT'] = range(len(results_df))

stat_columns = [col for col in results_df.columns if col not in ['STT', 'Team']]
results_df = results_df[['STT', 'Team'] + stat_columns]

results_df.to_csv('Exercise 2/results2.csv', index=False)
print("The result has been saved in results2.csv")

attack_stats = ['Goals', 'Assists', 'xG']
defense_stats = ['Tkl', 'Blocks', 'Int']
selected_stats = attack_stats + defense_stats

if not os.path.exists('Exercise 2/histograms'):
    os.makedirs('Exercise 2/histograms')

# Plot histograms for each selected statistic
for stat in selected_stats:
    # Histogram for all players
    df[stat].hist(bins=20)
    plt.title(f'Distribution of {stat} for all players')
    plt.xlabel(stat)
    plt.ylabel('Frequency')
    plt.savefig(f'Exercise 2/histograms/hist_all_{stat}.png')
    plt.close()
    
    # Histogram for each team
    for team in df['Team'].unique():
        team_df = df[df['Team'] == team]
        team_df[stat].hist(bins=20)
        plt.title(f'Distribution of {stat} for {team}')
        plt.xlabel(stat)
        plt.ylabel('Frequency')
        # Sanitize team name for filename
        safe_team = team.replace(" ", "_").replace("/", "_")
        plt.savefig(f'Exercise 2/histograms/hist_{safe_team}_{stat}.png')
        plt.close()

print("Histograms for attacking and defensive statistics have been saved in the 'histograms' directory.")

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Group by Team and compute the mean for each statistic
team_stats = df.groupby('Team')[numeric_cols].mean()
results = []

# For each statistic, find the team with the highest mean value
for stat in numeric_cols:
    max_mean = team_stats[stat].max()
    if pd.notna(max_mean) and max_mean != 0:
        max_team = team_stats[stat].idxmax()
        results.append(f"Statistic: {stat}, Team: {max_team}, Mean Value: {max_mean:.2f}")

output_file = 'Exercise 2/highest_team_stats.txt'
with open(output_file, 'w') as f:
    f.write("Teams with the Highest Mean Scores for Each Statistic\n")
    f.write("================================================\n\n")
    for result in results:
        f.write(result + "\n")

print(f"Results have been saved to highest_team_stats.txt")