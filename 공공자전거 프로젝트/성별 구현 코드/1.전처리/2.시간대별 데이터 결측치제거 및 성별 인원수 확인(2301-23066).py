#06score.py 

import pandas as pd
import time

path = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
# score = pd.read_csv(path,encoding='utf-8')
# bicycle = pd.read_csv(path,encoding='cp949') #한글깨지면 cp949
bicycle = pd.read_csv(path,encoding='utf-8')
# print(bicycle)
print(bicycle.info())
# print()
time.sleep(1)

#1.남자,여자 인원수 구하기
#추가 코딩
print('bicycle.dropna() 테스트중')
print('결측치 처리전=>',bicycle.count()) #각 columns별로 데이터 갯수를 확인할 수 있다.
print(bicycle.isna()) #NaN인지 아닌지 체크
# df = df.dropna() #지우고
# print(df)

print('bicycle[성별]=>',bicycle['성별'].count()) #bicycle[성별]=> 13208831
print('bicycle[성별].size=>',bicycle['성별'].size)#null값까지 계산된 데이터수  bicycle[성별].size=> 19223555
print()
time.sleep(1)
# print()

print('bicycle.isna()=>',bicycle.isna()) #NaN인지 아닌지 체크 =>확인됨.

bicycle = bicycle.dropna()
print('최종 성별 결측치 수정한 결과 및 파일로 저장하기')
print('결측후 처리전=>',bicycle.count()) 
print('bicycle[성별]=>',bicycle['성별'].count())

#다른 파일로 저장하는 경우 예) 선택적
fname ='./missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2301-2306missing.csv'
bicycle.to_csv(fname)

print()
'''
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
None
bicycle.dropna() 테스트중
결측치 처리전=> 대여일자       12977816
대여시간       12977816
대여구분코드     12977816
대여소번호      12977816
대여소명       12977816
성별         12977816
연령대코드      12977816
이용건수       12977816
이동거리(M)    12977816
이용시간(분)    12977816
dtype: int64
           대여일자   대여시간  대여구분코드  대여소번호   대여소명     성별  연령대코드   이용건수  이동거리(M)  이용시간(분)
0         False  False   False  False  False  False  False  False    False    False
1         False  False   False  False  False  False  False  False    False    False
2         False  False   False  False  False  False  False  False    False    False
3         False  False   False  False  False  False  False  False    False    False
4         False  False   False  False  False  False  False  False    False    False
...         ...    ...     ...    ...    ...    ...    ...    ...      ...      ...
12977811  False  False   False  False  False  False  False  False    False    False
12977812  False  False   False  False  False  False  False  False    False    False
12977813  False  False   False  False  False  False  False  False    False    False
12977814  False  False   False  False  False  False  False  False    False    False
12977815  False  False   False  False  False  False  False  False    False    False

[12977816 rows x 10 columns]
bicycle[성별]=> 12977816
bicycle[성별].size=> 12977816

bicycle.isna()=>            대여일자   대여시간  대여구분코드  대여소번호   대여소명     성별  연령대코드   이용건수  이동거리(M)  이용시간(분)
0         False  False   False  False  False  False  False  False    False    False
1         False  False   False  False  False  False  False  False    False    False
2         False  False   False  False  False  False  False  False    False    False
3         False  False   False  False  False  False  False  False    False    False
4         False  False   False  False  False  False  False  False    False    False
...         ...    ...     ...    ...    ...    ...    ...    ...      ...      ...
12977811  False  False   False  False  False  False  False  False    False    False
12977812  False  False   False  False  False  False  False  False    False    False
12977813  False  False   False  False  False  False  False  False    False    False
12977814  False  False   False  False  False  False  False  False    False    False
12977815  False  False   False  False  False  False  False  False    False    False

[12977816 rows x 10 columns]
최종 성별 결측치 수정한 결과 및 파일로 저장하기
결측후 처리전=> 대여일자       12977816
대여시간       12977816
대여구분코드     12977816
대여소번호      12977816
대여소명       12977816
성별         12977816
연령대코드      12977816
이용건수       12977816
이동거리(M)    12977816
이용시간(분)    12977816
dtype: int64
bicycle[성별]=> 12977816

'''