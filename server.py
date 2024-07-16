from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='./file')

def get_mbti_tag(user_mbti, mbti_category):
    for item in mbti_category:
        if item[0] == user_mbti:
            return int(item[1])
    return None

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/mypage', methods=['GET'])
def mypage():
    return render_template('mypage.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        name = request.form['NAME']
        user_mbti = request.form['mbti']
        inst = request.form['inst']
        genre = request.form['genre']
        place = request.form['place']
        print(name, user_mbti, inst, genre, place)
        
        # ファイルパスの設定
        user_csv_path = './user.csv'
        mbti_csv_path = './mbti.csv'

        # CSVファイルの読み込み
        user_df = pd.read_csv(user_csv_path)
        mbti_df = pd.read_csv(mbti_csv_path)
        print(user_df)

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

        # dfをarrayに変換
        mbti_array = mbti_df.values
        print(mbti_category)
        print(mbti_array)
        mbti_array = np.delete(mbti_array, 0, 1)
        print(mbti_array)

        # 新しくscore列に追加。
        compared_mbti_list = np_array[:, 1]
        print(compared_mbti_list)

        # user_mbtiに対応するタグ番号を取得
        user_mbti_tag = get_mbti_tag(user_mbti, mbti_category)
        print(user_mbti_tag)

        # np_arrayのMBTIをタグ番号に変換
        compared_mbti_list = np_array[:, 1]
        compared_mbti_taglist = np.array([get_mbti_tag(user_mbti, mbti_category) for user_mbti in compared_mbti_list])
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

        # htmlに渡す配列
        band = user_df['band'].values.tolist()
        mbti = user_df['mbti'].values.tolist()
        match = user_df['match'].values.tolist()

        print(band, mbti, match)

        return render_template('home.html', band=band, mbti=mbti, match=match)
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
