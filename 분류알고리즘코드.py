import datetime
import json
import requests
from urllib.parse import quote
import pymysql
import re

REGION = "**********"
endpoint = "**********"
username = "**********"
password = "**********"
database_name = "**********"


def Classification(markets):
    client_id = '**********'
    client_secret = '**********'
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

    category = []

    def etc(store):
        return ['']

    def keyword_compare(naver_keyword_list):
        t = -1
        for p in naver_keyword_list:
            str = p
            # print(str)
            category_str = ['식비', '생활', '교통', '운동', '교육/학습',
                            '배달', '온라인쇼핑', '택시', '의료/건강',
                            '자녀/육아', '카페/디저트', '오프라인쇼핑',
                            '대중교통', '금융', '반려동물', '술/유흥',
                            '자동차', '문화/여가', '꽃', '편의점', '뷰티/미용',
                            '주거/통신', '여행/숙박', '커피생크림빵집과자', '고속시외버스철도',
                            '약국병원한의원', '맛집밥집메뉴', '백화점매장문구', '학원시험', '배송택배', '술집노래방소주맥주', 'PC방서점공방', '스터디',
                            '네일']

            for v in range(len(category_str)):

                if category_str[v].find(str) != -1:
                    if v == 18:
                        category.append('경조/선물')
                    elif v == 23:
                        category.append('카페/디저트')
                    elif v == 24:
                        category.append('교통')
                    elif v == 25:
                        category.append('의료/건강')
                    elif v == 26:
                        category.append('식비')
                    elif v == 27:
                        category.append('오프라인쇼핑')
                    elif v == 28:
                        category.append('교육/학습')
                    elif v == 29:
                        category.append('온라인쇼핑')
                    elif v == 30:
                        category.append('술/유흥')
                    elif v == 31:
                        category.append('문화/여가')
                    elif v == 32:
                        category.append('교육/학습')
                    elif v == 33:
                        category.append('뷰티/미용')
                    else:
                        category.append(category_str[v])
                    t = v
                if t != -1:
                    break

        if t == -1:
            category.append('기타')

    # 엑셀에서 값 받아오기

    for i in range(len(markets)):
        store = markets[i][0]
        store = ''.join(store.split())
        chair = store.find('(주)')
        if chair != -1:
            store = store[:chair] + store[chair + 3:]
        store = re.sub('[/]', '', store)
        url_base = "https://openapi.naver.com/v1/search/local.json?query="
        keyword = quote(store)
        url_last = "&display=5$&start=1&sort=random&item=category"
        url_store = url_base + keyword + url_last
        if store.find('올리브영') != -1 or store.find('이니스프리') != -1:
            category.append('뷰티/미용')
        elif store.find('세븐일레븐') != -1:
            category.append('편의점')
        elif store.find('네이버') != -1:
            category.append('온라인쇼핑')
        elif store.find('한국철도공사') != -1 or store.find('티머니전국시외') != -1 or store.find('코레일') != -1:
            category.append('교통')
        elif store.find('택시') != -1:
            category.append('택시')
        elif store.find('카카오') != -1 or store.find('네이버') != -1 or store.find('Ａｐｐｌｅ') != -1 or store.find(
                '쿠팡') != -1 \
                or store.find('ＳＳＧ．ＣＯＭ') != -1:
            category.append('온라인쇼핑')
        elif store.find('넷플릭스') != -1 or store.find('왓챠') != -1:
            category.append('서비스구독')
        elif store.find('교통-버스') != -1 or store.find('교통-지하철') != -1:
            category.append('대중교통')
        elif store.find('ＧＳ２５') != -1 or store.find('씨유') != -1:
            category.append('편의점')
        elif store.find('이디야') != -1 or store.find('뚜레쥬르') != -1 or store.find('파리바게뜨') != -1:
            category.append('카페/디저트')
        elif store.find('PC') != -1:
            category.append('문화/여가')
        elif store.find('우아한형제들') != -1:
            category.append('배달')
        elif store.find('야놀자') != -1 or store.find('여기어때') != -1:
            category.append('여행/숙박')
        else:
            result = requests.get(url_store, headers=headers).json()
            try:
                res = result['items'][0]['category']
                title = str(result['items'][0]['title'])
                title = str(title.replace('<b>', ''))
                title = str(title.replace('</b>', ''))
                title = str(title.replace(' ', ''))
                res = str(res.replace('>', ''))
                res = str(res.replace(',', ''))
                if title.find(store) != -1 or result['display'] == 1:
                    # 결과가 하나라면 그게 답일 확률이 높습니다
                    # 네이버 지도 api로 긁어온 값이 제대로 도착한 경우에 큰 category 별로 조건문으로 걸러지게 함. 크롤링 하는 것보다 if문으로 걸러서 하는게
                    # 시스템 적으로 시간이 더 적게 걸리니, 큰 category로 if문으로 걸러 보겠습니다.
                    # 우선순위: 적요 > store > res

                    if res.find('슈퍼') != -1 or res.find('마트') != -1 or res.find('종합도소매') != -1:
                        category.append('생활')
                    elif res.find('오락') != -1 or res.find('오락시설') != -1 or res.find('술집') != -1:
                        category.append('술/유흥')
                    elif res.find('가공식품') != -1 or res.find('카페') != -1 or res.find('디저트') != -1:
                        category.append('카페/디저트')
                    elif res.find('편의점') != -1 or store.find('세븐일레븐') != -1:  # 유독 세븐만 잘 안 걸린다
                        category.append('편의점')
                    elif res.find('한식') != -1 or res.find('양식') != -1 or res.find('분식') != -1 or res.find(
                            '중식') != -1 or res.find('음식점') != -1 or res.find('일식') != -1:
                        category.append('식비')
                    elif res.find('공방') != -1 or res.find('PC방') != -1 or res.find('서점') != -1:
                        category.append('문화/여가')
                    elif res.find('꽃집') != -1 or res.find('꽃배달') != -1:
                        category.append('경조/선물')
                    elif res.find('학원') != -1 or res.find('장소대여') != -1 or res.find('출판사') != -1 or res.find(
                            '서점') != -1:
                        category.append('교육/학습')
                    elif res.find('교통') != -1 or res.find('운수') != -1:
                        category.append('교통')
                    elif res.find('여행') != -1 or res.find('명소') != -1 or res.find('숙박') != -1:
                        category.append('여행/숙박')
                    elif res.find('건강') != -1 or res.find('의료') != -1 or res.find('병원') != -1 or res.find(
                            '의원') != -1 or res.find('의약품제조') != -1:
                        category.append('의료/건강')
                    elif res.find('택시회사') != -1 or res.find('택시') != -1:
                        category.append('택시')
                    elif res.find('콘택트렌즈전문') != -1 or res.find('미용실') != -1 or res.find('이발소') != -1:
                        category.append('뷰티/미용')
                    elif res.find('문구') != -1:
                        category.append('오프라인쇼핑')
                    else:
                        category.append('기타')
                else:

                    """# title과 store명이 다른 경우, 즉 네이버지도에서 잘못된 값으로 가져온 경우.
                       # title과 store명이 다를 경우 크롤링 해서 긁어온 text를 가지고 keyword를 뽑아서 예측을 합니다."""
                    if store.find('편의점') != -1:
                        category.append('편의점')
                    elif res.find('한식') != -1 or res.find('양식') != -1 or res.find('분식') != -1 or res.find(
                            '중식') != -1 or res.find('음식점') != -1 or res.find('일식') != -1:
                        category.append('식비')
                    else:
                        naver_keyword_list = etc(store)
                        keyword_compare(naver_keyword_list)
                    # 네이버에서 크롤링 했을 때 검색어를 bold형태로 나오게 하는데 그 bold된 형태들의 주변것들을 가져오기
            except:
                naver_keyword_lists = etc(store)
                keyword_compare(naver_keyword_lists)
    return category


def week_make(date_array):
    week_array = []
    for i in date_array:
        year = i[0][:4]
        month = i[0][4:6]
        date = i[0][6:]
        n = datetime.datetime(int(year), int(month), int(date))

        week_array.append(str(n.isocalendar().week))
    return week_array


def Report():
    report_array = []
    time_array = []
    weekday_array = []
    food_array = []
    delivery_array = []
    shopping_array = []
    life_array = []
    cafe_array = []
    beauty_array = []
    drink_array = []
    culture_array = []
    transport_array = []
    taxi_array = []
    travel_array = []
    etc_array = []


week = []


def lambda_handler():
    conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    curs = conn.cursor()
    # 1. DB에서 category가 null인 애들 찾기 - markets= [TRN_TXT들]로 정의해서 넣어두고
    markets = []
    conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    curs = conn.cursor()
    mysql_query = "Select TRN_TXT from TransData where CATEGORY IS NULL"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    print(rows)

    for row in rows:
        markets.append(row)
    print(len(markets))

    # 2. 그 아이들의 category를 api로 찾기 - categories =[api 결과들]로 찾아서 넣고

    categories = Classification(markets)

    # 3. 다시 DB의 category에 api로 찾은 매장의 분류결과 넣기 - markets[i]의 txt에 있는 category에 categories[i] 값을 넣어주면 될듯!
    for num in range(len(categories)):
        print(categories[num])
        print(markets[num][0])

        mysql_query = "update TransData set CATEGORY = (%s) where TRN_TXT = (%s)"
        curs.execute(mysql_query, (categories[num], markets[num][0]))
    mysql_query = "Select * from TransData"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    arr = []
    for row in rows:
        arr.append(row)
        print(row)
    conn.commit()

    date = []
    mysql_query = "Select TRN_DT from TransData where WEEK IS NULL"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        date.append(row)
    print(len(date))
    print(date)
    week_array = week_make(date)

    for num in range(len(week_array)):
        mysql_query = "update TransData set WEEK = (%s) where TRN_DT = (%s)"
        curs.execute(mysql_query, (week_array[num], date[num][0]))
        # week가 제대로 들어갔는지 확인하는 아래코드

    conn.commit()

    mysql_query = "Select * from TransData"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    arr = []
    for row in rows:
        arr.append(row)
        print(row)


    mysql_query = "Select distinct WEEK from TransData"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        week.append(row[0])
    print(week)

    # 주차별 리포트 구조만들기
    for idx in week:
        print(idx)
        mysql_query = "Insert into Report(RPTID) values(%s)"
        curs.execute(mysql_query, idx)
        rows = curs.fetchall()

    # total sum, avg 채우기
    mysql_query = "select WEEK, sum(PAY_AM), avg(PAY_AM) from TransData group by WEEK"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        mysql_query = "update Report set TTL_AMT = (%s) where RPTID = (%s)"
        curs.execute(mysql_query, (row[1], row[0]))
        rows = curs.fetchall()
        mysql_query = "update Report set AVG_AMT = (%s) where RPTID = (%s)"
        curs.execute(mysql_query, (row[2], row[0]))

    # category별 합계 채우기

    mysql_query = "select WEEK, CATEGORY, sum(PAY_AM) from TransData group by WEEK, CATEGORY"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        if row[1] == '식비':
            mysql_query = "update Report set food = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
            mysql_query = "select food from Report where RPTID = (%s)"
            curs.execute(mysql_query, row[0])
            rows = curs.fetchall()
            print(rows)

        elif row[1] == '기타':
            mysql_query = "update Report set etc = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '온라인쇼핑':
            mysql_query = "update Report set shopping = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '편의점':
            mysql_query = "update Report set life = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '의료/건강':
            mysql_query = "update Report set life = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '대중교통':
            mysql_query = "update Report set transport = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '술/유흥':
            mysql_query = "update Report set drink = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '카페/디저트':
            mysql_query = "update Report set cafe = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '문화/여가':
            mysql_query = "update Report set culture = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '배달':
            mysql_query = "update Report set delivery = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '교육/학습':
            mysql_query = "update Report set life = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '뷰티/미용':
            mysql_query = "update Report set beauty = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '교통':
            mysql_query = "update Report set transport = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '서비스구독':
            mysql_query = "update Report set life = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '택시':
            mysql_query = "update Report set taxi = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '여행/숙박':
            mysql_query = "update Report set travel = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()
        elif row[1] == '생활':
            mysql_query = "update Report set life = (%s) where RPTID = (%s)"
            curs.execute(mysql_query, (row[2], row[0]))
            rows = curs.fetchall()

    mysql_query = "select * from Report"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        print(row)

    # comment 추가

    mysql_query = "select food,food_avg,delivery,delivery_avg,shopping,shopping_avg,life,life_avg,cafe, cafe_avg,beauty, beauty_avg, drink,drink_avg, culture,culture_avg, transport,transport_avg, taxi, taxi_avg, travel, travel_avg, etc, etc_avg, RPTID from Report"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        print("row:", row)
        elements = []
        weeknum = row[24]
        for ele in row:
            minus = []
            print("ele:", ele)
            elements.append(ele)
            print(elements)
        for i in range(len(elements) - 2):
            if elements[i] is not None:
                if i % 2 == 0:
                    print(type(i))
                    print("i:", i)

                    print(elements[i] - elements[i + 1])
                    j = i // 2
                    minus.append(elements[i] - elements[i + 1])
                    print(minus)
                else:
                    continue
            elif i % 2 == 0:
                minus.append(0)
            else:
                continue
        print("minus:", minus)
        max_idx = -1
        min_idx = -1
        if len(minus) > 0:
            for i in range(len(minus)):
                if max(minus) > 0 and max(minus) == minus[i]:
                    max_idx = i
                    print("max_idx:", max_idx)
                if min(minus) < 0 and min(minus) == minus[i]:
                    min_idx = i
                    print("min_idx:", min_idx)
        # mes1 = max에 따른 mes
        mes0 = "20대에 비해 "
        mes1 = ""
        if max_idx == 0:
            mes1 = "식비를 지출이 많았고 "
        elif max_idx == 1:
            mes1 = "배달을 많이 시키셨고 "
        elif max_idx == 2:
            mes1 = "쇼핑에 지출을 많이 하셨고 "
        elif max_idx == 3:
            mes1 = "생활비를 많이 쓰셨고 "
        elif max_idx == 4:
            mes1 = "카페를 많이 가셨고 "
        elif max_idx == 5:
            mes1 = "미용에 지출이 많으셨고 "
        elif max_idx == 6:
            mes1 = "음주를 많이 하셨고 "
        elif max_idx == 7:
            mes1 = "여가에 지출을 많이하셨고 "
        elif max_idx == 8:
            mes1 = "교통비로 많이 쓰셨고 "
        elif max_idx == 9:
            mes1 = "택시비로 많이 쓰셨고 "
        elif max_idx == 10:
            mes1 = "여행비용으로 많이 지출하셨고 "
        elif max_idx == 11:
            mes1 = "기타비용로 많이 쓰셨고 "
        # message2 = min에 따른 mes
        mes2 = ""
        if min_idx == 0:
            mes2 = "식비지출은 적었습니다."
        elif min_idx == 1:
            mes2 = "배달비용지출은 적었습니다."
        elif min_idx == 2:
            mes2 = "쇼핑을 덜 하셨습니다."
        elif min_idx == 3:
            mes2 = "생활비를 덜 쓰셨습니다."
        elif min_idx == 4:
            mes2 = "카페를 덜 갔습니다."
        elif min_idx == 5:
            mes2 = "미용에 지출이 적습니다."
        elif min_idx == 6:
            mes2 = "음주를 덜 하셨습니다."
        elif min_idx == 7:
            mes2 = "여가지출이 적습니다."
        elif min_idx == 8:
            mes2 = "교통비를 덜 쓰셨습니다."
        elif min_idx == 9:
            mes2 = "택시를 덜 탔습니다."
        elif min_idx == 10:
            mes2 = "여행비용이 적습니다."
        elif min_idx == 11:
            mes2 = "기타비용이 적습니다."
        # message = message1 + message2
        message = mes0 + mes1 + mes2
        print(message)
        mysql_query = "update Report set GRP_COMMENT = (%s) where RPTID = (%s)"
        curs.execute(mysql_query, (message, weeknum))
        rows = curs.fetchall()

    # maxTime
    # 1. TransData에서 시간대 분류

    mysql_query = "Select TRN_TM,TRN_SRNO from TransData"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    times = []
    srno = []
    for row in rows:
        time = int(row[0][:2])
        times.append(time)
        srno.append(row[1])
    print(srno)
    print(times)
    for i in range(len(srno)):
        if times[i] < 6:
            mysql_query = "update TransData set Time = (%s) where TRN_SRNO = (%s)"
            curs.execute(mysql_query, ('새벽', srno[i]))
            rows = curs.fetchall()
        elif times[i] < 12:
            mysql_query = "update TransData set Time = (%s) where TRN_SRNO = (%s)"
            curs.execute(mysql_query, ('오전', srno[i]))
            rows = curs.fetchall()
        elif times[i] < 18:
            mysql_query = "update TransData set Time = (%s) where TRN_SRNO = (%s)"
            curs.execute(mysql_query, ('오후', srno[i]))
            rows = curs.fetchall()
        elif times[i] < 24:
            mysql_query = "update TransData set Time = (%s) where TRN_SRNO = (%s)"
            curs.execute(mysql_query, ('저녁', srno[i]))
            rows = curs.fetchall()

    # 2. Report에서 maxTime 구하기

    mysql_query = "select WEEK, TIME, count(*) from TransData group by WEEK, TIME"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    before_count = 0
    before_week = 0
    for row in rows:
        if row[0] != before_week:
            before_count = 0
            before_week = row[0]
            mysql_query = "update Report set MAXTIME = (%s) where RPTID= (%s)"
            curs.execute(mysql_query, (row[1], row[0]))
            rows = curs.fetchall()
            before_count = row[2]
        elif row[0] == before_week:
            if row[2] > before_count:
                mysql_query = "update Report set MAXTIME = (%s) where RPTID= (%s)"
                curs.execute(mysql_query, (row[1], row[0]))
                rows = curs.fetchall()

    # 확인

    mysql_query = "select * from Report"
    curs.execute(mysql_query)
    rows = curs.fetchall()
    for row in rows:
        print(row)

    # conn.commit()
    conn.close()

    # 비어있지 않다면 TRN_DT를 가지고 RPTID로 변환시키고 기존에 DB에 있던 RPTID가 제일 큰 것(ex 202117) 보다 큰 것들을 가지고 데이터를 만들어줍니다.

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


lambda_handler()