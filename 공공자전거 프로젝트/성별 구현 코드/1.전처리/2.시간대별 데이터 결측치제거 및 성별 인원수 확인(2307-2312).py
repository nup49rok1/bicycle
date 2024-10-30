#06score.py 

import pandas as pd
import time

path = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'

bicycle = pd.read_csv(path,encoding='utf-8')
# print(bicycle)
print(bicycle.info())
# print()
time.sleep(1)

print('bicycle.dropna() 테스트중')
print('결측치 처리전=>',bicycle.count()) #각 columns별로 데이터 갯수를 확인할 수 있다.
print(bicycle.isna()) #NaN인지 아닌지 체크

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

fname ='./missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2307-2312missing.csv'
bicycle.to_csv(fname)

print()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 14380971 entries, 0 to 14380970
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
 7   이용건수     float64
 8   이동거리(M)  float64
 9   이용시간(분)  float64
dtypes: float64(3), int64(2), object(5)
memory usage: 1.1+ GB
None
bicycle.dropna() 테스트중
결측치 처리전=> 대여일자       14380971
대여시간       14380971
대여구분코드     14380971
대여소번호      14380971
대여소명       14380971
성별         14380971
연령대코드      14380971
이용건수       14380971
이동거리(M)    14380971
이용시간(분)    14380971
dtype: int64
           대여일자   대여시간  대여구분코드  대여소번호   대여소명     성별  연령대코드   이용건수  이동거리(M)  이용시간(분)
0         False  False   False  False  False  False  False  False    False    False
1         False  False   False  False  False  False  False  False    False    False
2         False  False   False  False  False  False  False  False    False    False
3         False  False   False  False  False  False  False  False    False    False
4         False  False   False  False  False  False  False  False    False    False
...         ...    ...     ...    ...    ...    ...    ...    ...      ...      ...
14380966  False  False   False  False  False  False  False  False    False    False
14380967  False  False   False  False  False  False  False  False    False    False
14380968  False  False   False  False  False  False  False  False    False    False
14380969  False  False   False  False  False  False  False  False    False    False
14380970  False  False   False  False  False  False  False  False    False    False

[14380971 rows x 10 columns]
bicycle[성별]=> 14380971
bicycle[성별].size=> 14380971

bicycle.isna()=>            대여일자   대여시간  대여구분코드  대여소번호   대여소명     성별  연령대코드   이용건수  이동거리(M)  이용시간(분)
0         False  False   False  False  False  False  False  False    False    False
1         False  False   False  False  False  False  False  False    False    False
2         False  False   False  False  False  False  False  False    False    False
3         False  False   False  False  False  False  False  False    False    False
4         False  False   False  False  False  False  False  False    False    False
...         ...    ...     ...    ...    ...    ...    ...    ...      ...      ...
14380966  False  False   False  False  False  False  False  False    False    False
14380967  False  False   False  False  False  False  False  False    False    False
14380968  False  False   False  False  False  False  False  False    False    False
14380969  False  False   False  False  False  False  False  False    False    False
14380970  False  False   False  False  False  False  False  False    False    False

[14380971 rows x 10 columns]
최종 성별 결측치 수정한 결과 및 파일로 저장하기
결측후 처리전=> 대여일자       14380971
대여시간       14380971
대여구분코드     14380971
대여소번호      14380971
대여소명       14380971
성별         14380971
연령대코드      14380971
이용건수       14380971
이동거리(M)    14380971
이용시간(분)    14380971
dtype: int64
bicycle[성별]=> 14380971
'''