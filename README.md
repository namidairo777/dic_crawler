##Problem
1. NEologd にまだ含まれていない単語を収集するプログラムおよびデータを作成してください。
 
要件：
・単語、読みのペアを10万組以上を収集すること
・インターネット上から（各サービス規約に違反しない形で）収集可能であること
・データの所在が明らかにできること（市販の辞書のコピーなどは不可）
 
2. NEologd に含まれる単語に関するメタ情報を収集するプログラムおよびデータを作成してください。
 
要件：
・単語、メタ情報のペアを1万個以上作成すること
・どのようなメタ情報でも構いません
　例：単語のカテゴリ情報（品詞、意味的分類カテゴリなど）
　　　位置情報（東京タワー →  〒105-0011 東京都港区芝公園４丁目２−８など）
　　　学習された単語ベクトル
 
3. NEologdを用いたオリジナルのWebサービスを作成してください。
 
要件：
・NEologdを使っていること
・ブラウザからアクセスできるWebサービスであること
・どこかのサーバでサービスとして稼働してあること

##dic_crawler
1と2の問題両方を対応させるプログラムを作りました。

#問題制限
名詞に対する

#アイデア
情報収集なら、クローラの作成です。今回は初めてです。

#情報源簡単に解析できる情報なら、RSS情報です。
		新聞のニュースのタイトルなら、新語や固有名詞のほうが多い。
		日本でYahooニュースが人気で、YahooニュースのRSSを選びました

#rss源：http://headlines.yahoo.co.jp/rss/list

#理由
1. RSSの解析が容易で、処理時間が早くなれます。
　　　2. YahooニュースのRSSデータが大量で、最新です。
　　　3. YahooニュースのRSSの収集が可能です。
　　　4. データの所在が明らかにできます。

#単語のメタ情報と読みのデータ源：Wikipedia


#理由
1. WikipediaのHtmlの<div id=”mw-content-text”>のタグに、検索する単語の読みが書いてあります。それで、ここの一段落が検索単語の定義（紹介か？）を見られて、メタ情報として考えられます。
     2. 収集可能。
　　　3.　データの所在が明らかにできます。
	　4.　大量で、最近なデータ。

#保存形式：CSV
