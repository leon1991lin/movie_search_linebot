def rotten_tomato_score(actor_name,cur):
    import pymysql, json, requests
    from bs4 import BeautifulSoup

    import pymysql
    conn = pymysql.Connect(host='localhost',
                            port=3306,
                            user='root',
                            passwd='ian1991',
                            db='TFB103d_azure',
                            charset='utf8')
    cur = conn.cursor()

    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    headers = {
        'User-Agent':userAgent
    }
	
    #傳入的人名處理成網頁需要格式
    names = actor_name.split(' ')
    name=''
    for i in names:
        if i != names[0]:
            name += "-"
        name += i

    #各十筆的五個網頁地址
    urls = ['https://www.rottentomatoes.com/napi/search/all?type=movie&searchQuery=',
           'https://www.rottentomatoes.com/napi/search/all?after=MQ%3D%3D&type=movie&searchQuery=',
           'https://www.rottentomatoes.com/napi/search/all?after=Mg%3D%3D&type=movie&searchQuery=',
           'https://www.rottentomatoes.com/napi/search/all?after=Mw%3D%3D&type=movie&searchQuery=',
           'https://www.rottentomatoes.com/napi/search/all?after=NA%3D%3D&type=movie&searchQuery=']

    #電影id，可將此註解
    num = 0

    #跑各網址資料
    for url in urls:
        res = requests.get(url+name, headers=headers)
        movies = res.json()
        for movie in movies['movie']['items']:

            #去除無爛番茄分數的電影
            if movie['tomatometerScore']!={}:

                #電影id逐加，可將此註解
                num += 1

                #檢視爬蟲結果
                #print(movie['name']+" "+movie['tomatometerScore']['score'])

                #sql填入電影分數
                sql = '''UPDATE movie
                        SET tomato_rating = %s
                        WHERE movie_name = %s;
                        '''
                tomatoRating =float(movie['tomatometerScore']['score']) / 10
                cur.execute(sql,(tomatoRating, movie['name']))

if __name__ == "__main__":
    import pymysql
    conn = pymysql.Connect(host='localhost',
                            port=3306,
                            user='root',
                            passwd='ian1991',
                            db='TFB103d_azure',
                            charset='utf8')
    cur = conn.cursor()

    actor_name='Richard Madden'

    rotten_tomato_score(actor_name,cur)

    conn.commit()