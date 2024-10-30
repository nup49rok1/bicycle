#06score.py 

import pandas as pd
import time

path = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'

bicyclesung = pd.read_csv(path,encoding='utf-8')
print('bicyclesung의 정보=>',bicyclesung.info())
print('연령대별 성별 데이터 검색')

print('type(bicyclesung)=>',type(bicyclesung))#type(bicyclesung)=> <class 'pandas.core.frame.DataFrame'>
#bicyclesung = bicycle[ ['대여일자','대여시간','대여소번호','대여소명','대여구분코드','성별','연령대코드','이용건수','이동거리(M)','이용시간(분)']]

print('성별의 m->M,f->F로 변경하기')
print('남자 총수=>',bicyclesung[bicyclesung['성별'] == 'M'].size) 
print('- ' * 70)
print('여자 총수=>',bicyclesung[bicyclesung['성별'] == 'F'].size) 
print('- ' * 70)
print()
print('남자 총수(m)=>',bicyclesung[bicyclesung['성별'] == 'm'].size) 
print('- ' * 70)
print('여자 총수(f)=>',bicyclesung[bicyclesung['성별'] == 'f'].size) 
print('- ' * 70)
print('성별의 데이터값을 수정한 후의 값 출력하기')

# first_set 열의 'Blue' → 'Green' 으로 대체
bicyclesung['성별'] = bicyclesung['성별'].replace(['m'], 'M')
bicyclesung['성별'] = bicyclesung['성별'].replace(['f'], 'F')

print('최종 수정된 남자 총수=>',bicyclesung[bicyclesung['성별'] == 'M'].size) #
print('- ' * 70)
print('최종 수정된 여자 총수=>',bicyclesung[bicyclesung['성별'] == 'F'].size) # 
print('- ' * 70)
print('최종 남자 총수(m)=>',bicyclesung[bicyclesung['성별'] == 'm'].size) #
print('- ' * 70)
print('최종 여자 총수(f)=>',bicyclesung[bicyclesung['성별'] == 'f'].size) #

fname ='./missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2301-2306missing.csv'
bicyclesung.to_csv(fname)

'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12977816 entries, 0 to 12977815
Data columns (total 10 columns):
 #   Column   Dtype  
---  ------   -----  
 0   대여일자     object 
 1   대여시간     int64  
 2   대여구분코드   object 
 3   대여소번호    int64  
 4   대여소명     object 
 5   성별       object 
 6   연령대코드    object 
 7   이용건수     int64  
 8   이동거리(M)  float64
 9   이용시간(분)  int64  
dtypes: float64(1), int64(4), object(5)
memory usage: 990.1+ MB
bicyclesung의 정보=> None
연령대별 성별 데이터 검색
type(bicyclesung)=> <class 'pandas.core.frame.DataFrame'>
성별의 m->M,f->F로 변경하기
남자 총수=> 79416010
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
여자 총수=> 50362150
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

남자 총수(m)=> 0
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
여자 총수(f)=> 0
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
성별의 데이터값을 수정한 후의 값 출력하기
최종 수정된 남자 총수=> 79416010
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
최종 수정된 여자 총수=> 50362150
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
최종 남자 총수(m)=> 0
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
최종 여자 총수(f)=> 0
'''
