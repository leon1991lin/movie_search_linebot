def KiMoScore_Desc(actor_name,cur):
    import requests,pymysql
    from bs4 import BeautifulSoup

    import pymysql
    conn = pymysql.Connect(host='localhost',
                            port=3306,
                            user='root',
                            passwd='',
                            db='TFB103d_azure',
                            charset='utf8')
    cur = conn.cursor()

    KiMo = []

    #以該演員名稱搜尋奇摩電影
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        "referer": 'https://movies.yahoo.com.tw/'}
    searchUrl = "https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}&type=movie".format(actor_name)
    searchRes = requests.get(searchUrl, headers=headers)
    searchsoup = BeautifulSoup(searchRes.text, 'html.parser')

    #抓取總資料比數
    number =searchsoup.select_one("div.search_num._c span")
    total_num = number.text

    #抓取全部參與電影簡介連結
    page = 1
    movie_links = []
    while len(movie_links) < int(total_num):
        searchUrl = "https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}&type=movie&page={}".format(actor_name, page)
        searchRes = requests.get(searchUrl, headers=headers)
        searchsoup = BeautifulSoup(searchRes.text, 'html.parser')
        # 抓取電影簡介連結
        NameAndLink = searchsoup.select("div.en a")
        for i in NameAndLink:
            movie_links.append(i["href"])
        page += 1
    
    #抓取電影簡介頁面
    for movieUrl in movie_links:
        infoRes = requests.get(movieUrl, headers=headers)
        infosoup = BeautifulSoup(infoRes.text, 'html.parser')

        #抓取電影名稱
        MovieName = infosoup.select_one("div.movie_intro_info_r h3")
        name = MovieName.text

        #抓取電影綜合評分
        MovieScore = infosoup.select_one("div.score_num.count")
        score = float(MovieScore.text)
        
        #抓取電影簡介
        MovieIntro = infosoup.select_one("span#story")
        Intro = MovieIntro.text.split("\n")[1].replace("      "," ")

        # 輸出為 list 物件 [["movie_name","kimo_rating", "movie_desc"],...]
        KiMo.append([name,score,Intro,movieUrl])

        print('Movie_name = ', name)
        print('Yahoo_score = ', score)
        print("=================================")

        #寫入 SQL 的 movie 資料表中
        # INSERT 電影名稱，此段之後整併時請註解掉
        #sql1 = '''INSERT INTO movie(movie_name)
        #        VALUES ('%s'); ''' % (Name)
        #cur.execute(sql1)

        #插入劇情簡介、電影評價到 SQL
        sql2 = '''UPDATE movie
                     SET movie_desc = %s ,
                         kimo_rating = %s ,
                         link = %s
                   WHERE movie_name = %s ;'''
        cur.execute(sql2,(Intro,score,movieUrl,name))
    return KiMo
#Test
# print(KiMoScore_Desc("Tom Hardy"))
# print(KiMoScore_Desc("Leonardo DiCaprio"))

if __name__ == "__main__":
    import pymysql
    conn = pymysql.Connect(host='localhost',
                            port=3306,
                            user='root',
                            passwd='',
                            db='TFB103d_azure',
                            charset='utf8')
    cur = conn.cursor()

    actor_name='Dong-seok Ma'

    KiMoScore_Desc(actor_name,cur)

    conn.commit()



