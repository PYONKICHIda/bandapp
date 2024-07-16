import pandas as pd

# Load the CSV file
file_path = './mbti.csv'
mbti_df = pd.read_csv(file_path)

def find_best_and_worst_match(mbti_type):
    # Extract the row corresponding to the user's MBTI type
    user_row = mbti_df[mbti_df['Unnamed: 0'] == mbti_type]
    
    # Remove the first column which contains the MBTI type itself
    user_row = user_row.drop(columns=['Unnamed: 0'])
    # Find the highest score
    best_score = user_row.max(axis=1).values[0]
    # Find all MBTI types with the highest score
    best_matches = user_row.loc[:, user_row.iloc[0] == best_score].columns.tolist()
    # Find the lowest score
    worst_score = user_row.min(axis=1).values[0]
    # Find all MBTI types with the lowest score
    worst_matches = user_row.loc[:, user_row.iloc[0] == worst_score].columns.tolist()
    
    return best_matches, best_score, worst_matches, worst_score

# Get MBTI type from user input
name = input("あなたのMBTIタイプを入力してください: ")

# Find the best and worst match
result = find_best_and_worst_match(name)

# Print the result
if isinstance(result, str):
    print(result)
else:
    best_matches, best_score, worst_matches, worst_score = result
    print(f"あなたのMBTIタイプ: {name}")
    print(f"最も相性の良いMBTIタイプ: {', '.join(best_matches)}（スコア: {best_score}）")
    print(f"最も相性の悪いMBTIタイプ: {', '.join(worst_matches)}（スコア: {worst_score}）")
