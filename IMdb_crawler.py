import requests, uuid, pymysql
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.Connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='ian1991',
                       db='TFB103d_azure',
                       charset='utf8')
cur = conn.cursor()

#連接本地端 SQL 資料庫
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36','Accept-Language':'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4'
           }
ss = requests.session()

#抓取 IMDB 電影評分
def Filmography_score(Filmography_link):
    try:
        url = Filmography_link
        res = ss.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        rating_score = soup.select('div[class="ipc-button__text"] span')[0].text
        score_number =rating_score
        return score_number
    except:
        return 0

#抓取電影劇照
def Filmography_image(Filmography_id,uuid1):
    url = f'https://www.imdb.com/title/{Filmography_id}'
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    image_link = 'https://www.imdb.com' + soup.select('a[class="ipc-lockup-overlay ipc-focusable"]')[0]['href']
    image_res = requests.get(image_link, headers=headers)
    image_soup = BeautifulSoup(image_res.text, "html.parser")
    try:
        image_url = image_soup.select('div[class="MediaViewerImagestyles__PortraitContainer-sc-1qk433p-2 iUyzNI"] img')[0]['src']
        image_content = requests.get(image_url)
        img = image_content.content
        with open(r'%s/%s.jpg' % (r'./static/images', uuid1), 'wb') as f: #requests download
            f.write(img)  #requests download
    except:
        pass

#爬蟲主程序
def IMDb_crawler_by_python(searching_name,cur): # can change searching name by yourself
    url = "https://www.imdb.com/find?q={}"
    res = ss.get(url.format(searching_name), headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    link_url = 'https://www.imdb.com' + soup.select('tr[class="findResult odd"]')[0].a['href']
    link_res = ss.get(link_url, headers=headers)
    link_soup = BeautifulSoup(link_res.text, 'html.parser')
    # print(link_soup)

    for i in range(len(link_soup.select('div[class="filmo-category-section"]')[0].select("div[id]"))):
        Filmography_title_id_list = link_soup.select('div[class="filmo-category-section"]')[0].select("div[id]")[i]
        Filmography_type = link_soup.select('div[class="filmo-category-section"]')[0].select("div[id]")[i].text
        #只抓取 電影 透過 Filmography_type 排除影集等
        if 'TV Series' in Filmography_type:
            pass
        elif 'Video Game' in Filmography_type:
            pass
        elif 'TV Mini Series' in Filmography_type:
            pass
        else:
            Filmography_title_id = Filmography_title_id_list['id']
            if len(Filmography_title_id) > 20:
                pass
            else:
                #電影 ID
                Filmography_id = Filmography_title_id.split('-')[1]
                Filmography_link = 'https://www.imdb.com' + link_soup.select(f'div[id={Filmography_title_id}]')[0].a['href']

                #電影標題
                Filmography_title = link_soup.select(f'div[id={Filmography_title_id}]')[0].a.text
                Filmography_title = Filmography_title.replace(":","").replace("-","").replace("&","and").replace(','," ")

                #新增電影年分
                Filmography_year = link_soup.select(f'div[id={Filmography_title_id}]')[0].span.text.strip()
                if len(Filmography_year) == 4:
                    Filmography_time = str(Filmography_year)+"/01/01"
                else:
                    Filmography_time = None

                #電影評分
                score = Filmography_score(Filmography_link)

                print('Filmography_id = ',Filmography_id)
                print('Filmography_title = ', Filmography_title)
                print('score = ', score)
                print('Filmography_time = ', Filmography_time)
                print('Filmography_link = ', Filmography_link)

                #確認不重複 insert 電影
                selectSql='''select movie_id from movie where movie_name = %s ;'''
                cur.execute(selectSql,Filmography_title)
                movie_data = cur.fetchall()
                isMovieExist = False
                for row in movie_data:
                    uuid12 = uuid.uuid1()
                    sql2 = '''INSERT INTO movie_actor_ref VALUES (%s,%s,%s,%s); '''
                    cur.execute(sql2,(uuid12,searching_name,str(row[0]),Filmography_title))
                    isMovieExist= True
                    
                if(isMovieExist):
                    continue

                # 將電影資料寫入 SQL 的 movie 資料表中
                uuid1 = uuid.uuid1()
                sql1 = '''INSERT INTO movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s); '''
                cur.execute(sql1,(uuid1,Filmography_title,None,score,None,None,Filmography_time,None,0))

                # 將演員對照表 寫入 SQL 的 movie_actor_ref 資料表中
                uuid12 = uuid.uuid1()
                sql2 = '''INSERT INTO movie_actor_ref VALUES (%s,%s,%s,%s); '''
                cur.execute(sql2,(uuid12,searching_name,uuid1,Filmography_title))

                #電影劇照
                Filmography_image(Filmography_id,uuid1)

                print('=======================')
                conn.commit()

if __name__ == "__main__":
    import pymysql
    conn = pymysql.Connect(host='localhost',
                            port=3306,
                            user='root',
                            passwd='ian1991',
                            db='TFB103d_azure',
                            charset='utf8')
    cur = conn.cursor()

    actor_name='Dong-seok Ma'
    IMDb_crawler_by_python(actor_name,cur)

    conn.commit()


