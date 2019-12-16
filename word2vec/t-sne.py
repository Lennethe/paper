import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from matplotlib.cm import get_cmap
from sklearn.manifold import TSNE
from sklearn.metrics import explained_variance_score
from dataloader import load_visualize_data
from dataloader import load_v

#X, y = load_v(10)
#X /= 255
#X = X.reshape(X.shape[0], -1)

dic = ["日本",'ドイツ','インドネシア','トカラ','京外','ヨーロッパ','イギリス','タイ','スワヒリ','ロシア','アジア','アメリカ','オランダ','東洋','マレーシア','東京','フランス','ヒンディー','オーストラリア','韓','フィリピン','カナダ','ブラジル','ティモール','世界','イディッシュ','インド','ニュージーランド','ギリシャ','一方日本','アフリカーンス',
        "甥",'叔父','弟','曾孫','義弟','長兄','次男','伯父','三男','長男','末弟','外孫','舅','嫡子','次兄','玄孫','嫡孫','四男','兄','五男','庶子','息子','義父','長子','子息','嫡男','伯母','岳父','六男','異母','末子',
        '魔物','エルフ','ゴブリン','怪物','魔女','狩人','ドワーフ','天使','魔法','人魚','イブ','妖怪','チャチャ','アリス','勇者','アラジン','妖魔','テレサ','薔薇','プリンセス','天上','ドラゴン','夢幻','サンタクロース','小人','リリス','子猫','オオカミ','ムヒョ','幻影',
        'チーズ','牛乳','シロップ','アイスクリーム','バター','豆乳','ヨーグルト','トマト','デザート','ブランデー','果汁','ニンニク','コーラ','肉類','ラード','フルーツ','蜂蜜','ソーセージ','レモン','マヨネーズ','豚肉','オリーブオイル','ウイスキー','ナッツ','レタス','野菜','キャベツ','アーモンド','スパイス','豆類',
        "美味",'重苦','淋','忙','欲','逞','珍','貧','嬉','一美','好物','悲','乏','ステーキ','寂','愉','スープ','カレー','カレーライス','デザート','副食','シチュー','鰻','ラーメン','難','マヨネーズ','激','ハンバーガー','惜','豆腐','ハンバーグ',
        "コストパフォーマンス",'性能','クオリティ','精度','品質','音質','スペック','ハンドリング','コスト','燃費','ランニングコスト','レスポンス','剛性','モチベーション','スループット','難度','水準','感度','ブランドイメージ','空力','ゲームバランス','ハードル','初速','彩度','威力','クロック','コントラスト','品位','相性','ビットレート','食味']
X = load_visualize_data(dic)
print(len(dic))

decomp = TSNE(n_components=2)
X_decomp = decomp.fit_transform(X)

cmap = get_cmap("tab10")
for i in range(len(dic)):
    plt.plot(X_decomp[i][0], X_decomp[i][1], ".");
    plt.annotate(dic[i], xy=(X_decomp[i][0], X_decomp[i][1]))
plt.title(f"t-SNE")
plt.show()

#for i in range(len(dic)):
#    plt.plot(X_decomp[i][0], X_decomp[i][1], ".");
#    plt.annotate(i/30, xy=(X_decomp[i][0], X_decomp[i][1]))
#plt.title(f"t-SNE")
#plt.show()

#cmap = get_cmap("tab10")
#for i in range(10):
#    marker = "$" + str(i) + "$"
#    indices = np.arange(i*100, (i+1)*100)
#    plt.scatter(X_decomp[indices, 0], X_decomp[indices, 1], marker=marker, color=cmap(i))
#plt.title(f"t-SNE")
#plt.show()