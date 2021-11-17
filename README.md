# movie_search_linebot
透過 Azure 人臉辨識服務識別演員照片\劇照，並搜尋所參與的電影資料，以 Line Bot 呈現。

<h3>Demo 影片連結: https://youtu.be/gjcFkgjGA38 </h3>
<h3>說明簡報資料: https://docs.google.com/presentation/d/1IrjX65JhsEgBwCKarR_w8e_foP4pfwimgF-cPO_GPSc/edit?usp=sharing</h3>

<h3>功能說明:</h3>

1.以圖搜影: 於 Line Bot 上傳演員照片/含演員的劇照，透過 Azure 中電腦視覺功能，識別照片中演員，再以演員名稱搜尋資料庫中近期參演的電影資訊，並回傳 Line Bot 使用者。

2.圖文選單-熱門電影(熱搜): 每筆電影查詢接會計入資料庫中，透過圖文選單-熱門電影功能可回傳被搜尋次數最高之五部電影。

3.圖文選單-最新電影: 透過圖文選單-最新電影功能可回傳近期熱映或即將上映的5部電影。

4.圖文選單-訂票去:透過圖文選單-訂票去，可取得威秀影城、國賓影城與 EZ訂訂票平台之連結。
