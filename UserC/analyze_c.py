
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import koreanfont
import numpy as np

data1 = pd.read_csv('./UserC/팀C_수요건강결과_5년치변화분석.csv', encoding='utf-8')
data2 = pd.read_csv('./UserC/팀C_수요건강결과_시계열.csv', encoding='utf-8')
data3 = pd.read_csv('./UserA/팀A_의료자원공급_5년치변화분석.csv', encoding='utf-8')


# 결측치 확인
print(data1)
print(data1.isnull().sum())

print(data2)
print(data2.isnull().sum())

# 가설1 2019년부터 2023년 사이 분만 건수가 감소한 시군구에서는 분만실 시설 수도 함께 감소했을 것이다.
# 2019~2023년까지 지역별 분만 건수와 , 분만실 시설 수 비교

# 지역별로 


df1= pd.DataFrame(data1)
df2 = pd.DataFrame(data3)

seoul_df1 = df1[df1["시도"] == "서울특별시"]

result = df1[['시군구']]

# 분만건수 변화율
result["분만건수_변화율%"] = (
    (df1["분만건수_2023"] - df1["분만건수_2019"])
    / df1["분만건수_2019"]
    * 100
)

print(result.head())

# 분만실 변화율

result2 = df2[['시군구']]

result2["분만실_변화율%"] = (
    (df2["분만실_2023"] - df2["분만실_2019"])
    / df2["분만실_2019"]
    * 100
)
print(result2)

# NaN값을 0으로 변환
result2['분만실_변화율%'] = result2['분만실_변화율%'].fillna(0)
print(result2)


sns.scatterplot(x=result['분만건수_변화율%'] , y=result2['분만실_변화율%'])
plt.show()



