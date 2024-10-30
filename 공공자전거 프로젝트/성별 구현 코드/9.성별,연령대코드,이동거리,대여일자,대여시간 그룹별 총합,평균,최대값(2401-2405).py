import pandas as pd

# Load the dataset
path = './missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2401-2405missing.csv'
bicyclesung = pd.read_csv(path, encoding='utf-8')
print('bicyclesung의 정보=>',bicyclesung.info())

# Handle missing values by dropping rows with missing '성별', '연령대코드', '이동거리(M)', '대여일자', and '대여시간'
bicyclesung = bicyclesung.dropna(subset=['성별', '연령대코드', '이동거리(M)', '대여일자', '대여시간'])

# Convert '이동거리(M)' to numeric in case there are any non-numeric values
bicyclesung['이동거리(M)'] = pd.to_numeric(bicyclesung['이동거리(M)'], errors='coerce')

# Group by '대여일자', '대여시간', '성별', and '연령대코드', then calculate sum, mean, max, and min for '이동거리(M)'
distance_stats = bicyclesung.groupby(['대여일자', '대여시간', '성별', '연령대코드'])['이동거리(M)'].agg(['sum', 'mean', 'max', 'min']).reset_index()

# Round the values to 2 decimal places
distance_stats = distance_stats.round({'sum': 2, 'mean': 2, 'max': 2, 'min': 2})

# Print the result
print(distance_stats)

'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
             대여일자  대여시간 성별  연령대코드        sum     mean       max     min
0      2023-01-01     0  F    20대  235020.59  2238.29   8744.87  333.59
1      2023-01-01     0  F    30대   80532.74  1750.71   7034.41  440.00
2      2023-01-01     0  F    40대   34215.66  2443.98   6750.00  410.00
3      2023-01-01     0  F    50대   14334.32  1194.53   3039.01  370.86
4      2023-01-01     0  F    60대    5350.43  1070.09   1732.53  691.40
...           ...   ... ..    ...        ...      ...       ...     ...
68715  2023-06-30    23  M    50대  395434.97  2017.53  23850.00    0.00
68716  2023-06-30    23  M    60대  149408.44  1915.49  11950.00   10.00
68717  2023-06-30    23  M  70대이상   15855.56  1585.56   4508.27  473.07
68718  2023-06-30    23  M   ~10대  800528.40  2879.60  25732.99    0.00
68719  2023-06-30    23  M     기타  676616.50  2842.93  20722.60    0.00
'''

