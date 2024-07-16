import pandas as pd
import numpy as np

#まずは、楽器とジャンル・活動場所で絞る。
# ファイルパスの設定
user_csv_path = './user.csv'
mbti_csv_path = './mbti.csv'

# CSVファイルの読み込み
user_df = pd.read_csv(user_csv_path)
mbti_df = pd.read_csv(mbti_csv_path)
print(user_df)

inst =  input() 
genre =  input() 
place =  input() 

# 1:instが一致しない場合、出力候補から除外する。
user_df = user_df[user_df['inst'] == inst]
# 2:genreが一致しない場合、出力候補から除外する。
user_df = user_df[user_df['genre'] == genre]
# 3:placeが一致しない場合、出力候補から除外する。
user_df = user_df[user_df['place'] == place]
np_array = user_df.values
print(np_array)

mbti_category = np.array([
    ['entp', 0],
    ['intp', 1],
    ['entj', 2],
    ['intj', 3],
    ['enfp', 4],
    ['infp', 5],
    ['enfj', 6],
    ['infj', 7],
    ['estj', 8],
    ['istj', 9],
    ['esfj', 10],
    ['isfj', 11],
    ['estp', 12],
    ['esfp', 13],
    ['istp', 14],
    ['isfp', 15]
])

#dfをarrayに変換
mbti_array = mbti_df.values
print(mbti_category)
print(mbti_array)
mbti_array = np.delete(mbti_array, 0, 1)
print(mbti_array)

#新しくscore列に追加。
user_mbti =  input() 
compared_mbti_list = np_array[:, 1]
print(compared_mbti_list)


# user_mbtiをタグ番号に変換する関数を定義
def get_mbti_tag(mbti, mbti_category):
    for item in mbti_category:
        if item[0] == mbti:
            return int(item[1])
    return None

# user_mbtiに対応するタグ番号を取得
user_mbti_tag = get_mbti_tag(user_mbti, mbti_category)
print(user_mbti_tag)

# np_arrayのMBTIをタグ番号に変換
compared_mbti_list = np_array[:, 1]
compared_mbti_taglist = np.array([get_mbti_tag(mbti, mbti_category) for mbti in compared_mbti_list])
print(compared_mbti_taglist)


# 相性度を格納するリスト(match_listを作成)
match_list = []
for i in compared_mbti_taglist:
    match_list.append(mbti_array[user_mbti_tag][i])
print(match_list)

# user_dfに'match'列を追加
user_df['match'] = match_list

# mbtiスコア順にソート
user_df = user_df.sort_values('match', ascending=False)
print(user_df)

user_df = user_df[user_df['match'] > 40]

#htmlに渡す配列
band = user_df['band'].values
mbti = user_df['mbti'].values
match = user_df['match'].values

print(band, mbti, match)

