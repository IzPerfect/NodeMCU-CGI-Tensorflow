#!C:\Python35\python.exe
#-*- coding: utf-8 -*-

# 첫번째에서 경로는 실제 파이썬 인터프리터의 위치를 의미
# 두 번째 줄은 유니코드 명시해준다. 명시해 주는 것이 확실하다.

import cgi
import cgitb
import pymysql # 데이터 베이스를 다루기 위한 모듈
import numpy as np
from pred_xor import *

# CGI 프로그래밍 디버깅 모듈
# 런타임 에러를 웹 브라우저로 전송
# 만약 cgitb.enable()을 실행하지 않으면 웹 서버는 클라이 언트에게 500을 response
cgitb.enable()

# http 규격 뒤에 \n은 반드시 적어야 에러가 나지 않는다.
# 밑의 코드는 HTTP헤더이며 클라이언트에게 어떤 내용을 받게 되는지 미리 알려줘야한다.
print("content-type: text/html; charset=utf-8\n")

# CGI로 GET이나 POST형식으로 받음
# 사전형 key=value로 전해진 데이터들을 FieldStorage를 사용하여 불러온 뒤에 값을 변수에 저장
form= cgi.FieldStorage()
input1 = form['input1'].value
input2 = form['input2'].value
reset_table = form['start_signal'].value
# print(form.values()) # 받은 데이터들을 출력할 수 있다.
# print(form.keys()) # 받은 데이터들의 키를 출력할 수 있다.
# data = curs.fetchall() # 모든 데이터를 client로 가져온다.

# MySQL Connection 연결
conn = pymysql.connect(host='127.0.0.1',port = 3306, user='root', password=???, db='xor_test_db', charset='utf8')

# Cursor 객체를 return, 모든 명령이 이 curs를 통해 이뤄진다.
# Cursor 객체의 execute 메서드를 이용하여 SQL문장을 Database로 전송한다.
curs = conn.cursor()

print('==Database Connection==\n')
print('host : {host}'.format(host='127.0.0.1'))
print('port : {port}'.format(port=3306))
print('DB_name : {db}'.format(db = 'xor_test_db'))

# database 테이블 reset
# TRUNCATE을 사용하여 해당 테이블에 있는 데이터를 비운다.
if int(reset_table)==1:
    print('===reset table===\n\n')
    sql= "TRUNCATE TABLE `xor_input`"
    curs.execute(sql)
    sql= "TRUNCATE TABLE `xor_result`"
    curs.execute(sql)

print('\n===received data===\n')

print('input1 : ', input1)
print('input2 : ', input2,end='\n\n')


# 받은 데이터 들을 데이터테이블에 insert시킨다
# %s : placeholder, 파라미터 값들을 튜플 형태로 넣어주게 된다.
# 숫자, 문자 모두 %s를 사용하여 query를 실행시킨다. 여기서 %s는 MySQL에서 사용되는 %s이다.
sql = "insert into xor_input (input1, input2) values (%s, %s)"
curs.execute(sql, (input1,input2))

# 전송된 input데이터들이 있다면 xor연산을 tensorflow를 이용하여 실행시킨다.
if input1 is not None and input2 is not None:

    print('===xor operation===')
    pred_result = prediction(input1, input2) # tensorflow xor 실행
    pred_result = pred_result.reshape([-1])
    print('output : ',int(pred_result))

    # 결과 값을 xor_test 테이블로 전송
    sql = "insert into xor_result (result) values (%s)"
    curs.execute(sql, (int(pred_result[0])))



# commit으로 실행 결과를 데이터베이스에 반영
conn.commit()

# Connection 닫기
conn.close()
