#06score.py 

import pandas as pd

# Load the dataset
path = './missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2301-2306missing.csv'
bicyclesung = pd.read_csv(path, encoding='utf-8')
print('bicyclesung의 정보=>',bicyclesung.info())

# Handle missing values by dropping rows with missing '성별', '연령대코드', '이용건수'
bicyclesung = bicyclesung.dropna(subset=['성별', '연령대코드', '이용건수'])

# Convert '이용건수' to numeric in case there are any non-numeric values
bicyclesung['이용건수'] = pd.to_numeric(bicyclesung['이용건수'], errors='coerce')

# Group by '성별' and '연령대코드', then calculate count, mean, max, and min for '이용건수'
stats = bicyclesung.groupby(['성별', '연령대코드'])['이용건수'].agg(['count', 'mean', 'max', 'min']).reset_index()

# Print the result
print(stats)
'''
성별  연령대코드    count      mean  max  min
0   F    20대  1673908  1.176599   32    1
1   F    30대  1280938  1.117512   24    1
2   F    40대   742090  1.071225    9    1
3   F    50대   520200  1.045202    5    1
4   F    60대   122300  1.017375    5    1
5   F  70대이상    20885  1.010917    4    1
6   F   ~10대   270342  1.152348   23    1
7   F     기타   482061  1.045017    6    1
8   M    20대  2097648  1.165931   28    1
9   M    30대  1931477  1.153193   31    1
10  M    40대  1351631  1.107664   22    1
11  M    50대   934570  1.062640   12    1
12  M    60대   370561  1.027356    5    1
13  M  70대이상    57057  1.010078    5    1
14  M   ~10대   651230  1.231866   28    1
15  M     기타   701933  1.053328    9    1
PS C:\Mnet\miniproject>
'''
#성별의 연령대별로 이동거리의 합,최대값,최소값,평균값을 구하기

# Handle missing values by dropping rows with missing '성별', '연령대코드', and '이동거리(M)'
bicyclesung = bicyclesung.dropna(subset=['성별', '연령대코드', '이동거리(M)'])

# Convert '이동거리(M)' to numeric in case there are any non-numeric values
bicyclesung['이동거리(M)'] = pd.to_numeric(bicyclesung['이동거리(M)'], errors='coerce')

# Group by '성별' and '연령대코드', then calculate sum, mean, max, and min for '이동거리(M)'
distance_stats = bicyclesung.groupby(['성별', '연령대코드'])['이동거리(M)'].agg(['sum', 'mean', 'max', 'min']).reset_index()

# Print the result
print(distance_stats)
'''
성별  연령대코드           sum         mean        max  min
0   F    20대  4.898448e+09  2926.354319  183372.72  0.0
1   F    30대  3.635140e+09  2837.873455  105927.85  0.0
2   F    40대  2.123979e+09  2862.157959  144196.74  0.0
3   F    50대  1.512360e+09  2907.265665  109176.84  0.0
4   F    60대  3.671970e+08  3002.428376   50576.49  0.0
5   F  70대이상  5.020589e+07  2403.921098   54120.00  0.0
6   F   ~10대  6.853158e+08  2534.995618   98585.78  0.0
7   F     기타  1.243502e+09  2579.553070  134006.27  0.0
8   M    20대  5.702326e+09  2718.438113  166482.21  0.0
9   M    30대  5.385887e+09  2788.480923  693418.03  0.0
10  M    40대  4.046038e+09  2993.448489  179803.02  0.0
11  M    50대  2.817685e+09  3014.953440  138651.05  0.0
12  M    60대  1.064033e+09  2871.410683  117400.00  0.0
13  M  70대이상  1.618657e+08  2836.912944   42110.00  0.0
14  M   ~10대  1.685757e+09  2588.573759  307412.44  0.0
15  M     기타  1.810498e+09  2579.303444   95263.26  0.0
'''
