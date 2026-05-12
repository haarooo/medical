
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import koreanfont
import numpy as np

data1 = pd.read_csv('./UserC/팀C_수요건강결과_5년치변화분석.csv', encoding='utf-8')
data2 = pd.read_csv('./UserA/팀A_의료자원공급_5년치변화분석.csv', encoding='utf-8')


# 결측치 확인
print(data1)
print(data1.isnull().sum())

print(data2)
print(data2.isnull().sum())


df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 2019년부터 2023년 사이 분만 건수가 감소한 시군구에서는 분만실 밀집도가 함께 감소했을 것이다.


# 연도별 분만실 , 분만건수 평균 추이
years = [2019, 2020, 2021, 2022, 2023]

birth_means = []
room_means = []

for y in years:
    birth_means.append(df1[f'분만건수_{y}'].mean())
    room_means.append(df2[f'분만실_{y}'].mean())

print(birth_means , room_means)

plt.figure(figsize=(10, 5))
plt.plot(years, birth_means, marker='o', label='분만건수 평균')
plt.plot(years, room_means, marker='o', label='분만실 평균')
plt.title('2019~2023년 분만건수와 분만실 평균 변화')
plt.xlabel('연도')
plt.ylabel('평균값')
plt.legend()
plt.grid(True)
plt.show()


# 분만건수 변화와 분만실밀집도 변화 상관관계 분석
df1 = df1[['sd_cd', '시군구', '분만건수_2019', '분만건수_2023']]
df2 = df2[['sd_cd', '분만실_2019', '분만실_2023']]
df = pd.merge(df1, df2, on='sd_cd', how='inner')
 
# 0 제거
df = df[(df['분만건수_2019'] > 0) & (df['분만건수_2023'] > 0) & (df['분만실_2019'] > 0) & (df['분만실_2023'] > 0)]
 
# 변화율 계산
# 분만건수 연평균 변화율
df['분만건수_변화율'] = (  (df['분만건수_2023'] / df['분만건수_2019']) ** (1/4) - 1) * 100
# 분만실 연평균 변화율
df['분만실_변화율'] = ( (df['분만실_2023'] / df['분만실_2019']) ** (1/4) - 1) * 100
 
# 상관계수
r = df['분만건수_변화율'].corr(df['분만실_변화율'])

# 산점도
plt.figure(figsize=(9, 7))
sns.scatterplot(data=df, x='분만건수_변화율', y='분만실_변화율', alpha=0.6)

# 0 기준선 (사분면 구분)
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
 
plt.title(f'분만건수 변화율 vs 분만실 밀집도 변화율 (r = {r:.3f})')
plt.xlabel('분만건수 변화율(%)')
plt.ylabel('분만실 밀집도 변화율(%)')
plt.legend()
plt.grid()
plt.show()



# 가설 2
# 노인인구비율이 높은 지역일수록 인구 대비 의사 수가 감소할 것이다

df1 = df1[['sd_cd', '시군구', '노인인구비율_2023']]
df2 = df2[['sd_cd', '전체의사_2019', '전체의사_2023']]
df = pd.merge(df1, df2, on='sd_cd', how='inner')
 
 
# 의사수 변화율
df['의사_변화율'] = ( (df['전체의사_2023'] / df['전체의사_2019']) ** (1/4) - 1) * 100
 

r = df['노인인구비율_2023'].corr(df['의사_변화율'])
print('상관계수:', r)
 
# 산점도
sns.scatterplot(data=df, x='노인인구비율_2023', y='의사_변화율', alpha=0.6)
 
# 0 기준선
plt.axhline(0, color='gray', linestyle='--')
 
plt.title('노인인구비율 vs 의사수 변화율')
plt.xlabel('노인인구비율(%)')
plt.ylabel('의사수 변화율(%)')
plt.legend()
plt.grid()
plt.show()

#------------------------------------------------------------

# 워스트 베스트 10개
df1 = df1[['sd_cd', '시도', '시군구', '노인인구비율_2023']]
df2 = df2[['sd_cd', '전체의사_2019', '전체의사_2023']]
df = pd.merge(df1, df2, on='sd_cd', how='inner')
 
 
# 의사수 변화율
df['의사_변화율'] = ( (df['전체의사_2023'] / df['전체의사_2019']) ** (1/4) - 1) * 100


df['지역명'] = df['시도'] + ' ' + df['시군구']
 
# Top10 
worst = df.sort_values(by='의사_변화율').head(10).reset_index(drop=True)
best = df.sort_values(by='의사_변화율', ascending=False).head(10).reset_index(drop=True)
 
fig, axs = plt.subplots(1, 2, figsize=(15, 6))
 
# 워스트
sns.barplot(data=worst, x='의사_변화율', y='지역명', color='red', ax=axs[0])
axs[0].set_title('의사수 감소율 워스트 Top 10')
axs[0].set_xlabel('의사수 변화율(%)')
axs[0].set_ylabel('지역')
 
# 워스트 노인비율 표시
for i in range(len(worst)):
    axs[0].text(1,                              
                i,                             
                f"노인 {worst['노인인구비율_2023'][i]:.1f}%",
                va='center', ha='left', color='black', fontweight='bold')
 
# 베스트
sns.barplot(data=best, x='의사_변화율', y='지역명', color='blue', ax=axs[1])
axs[1].set_title('의사수 증가율 베스트 Top 10')
axs[1].set_xlabel('의사수 변화율(%)')
axs[1].set_ylabel('지역')
 
# 베스트 노인비율 표시
for i in range(len(best)):
    axs[1].text(best['의사_변화율'][i] - 1,     
                i,
                f"노인 {best['노인인구비율_2023'][i]:.1f}%",
                va='center', ha='right', color='white', fontweight='bold')
 
plt.tight_layout()
plt.show()



# 시계열 격차 그래프
df1 = df1[['sd_cd', '시군구', '노인인구비율_2023']]
df2 = df2[['sd_cd', '전체의사_2019', '전체의사_2020', '전체의사_2021','전체의사_2022', '전체의사_2023']]
df = pd.merge(df1, df2, on='sd_cd', how='inner')
 
# 노인비율 사분위 기준
q1 = df['노인인구비율_2023'].quantile(0.25)
q3 = df['노인인구비율_2023'].quantile(0.75)


high = df[df['노인인구비율_2023'] >= q3]   # 노인비율 높은 그룹
low = df[df['노인인구비율_2023'] <= q1]    # 노인비율 낮은 그룹
 
# 연도별 평균 계산
years = [2019, 2020, 2021, 2022, 2023]
high_means = []
low_means = []
for y in years:
    high_means.append(high[f'전체의사_{y}'].mean())
    low_means.append(low[f'전체의사_{y}'].mean())
 

# 시계열 데이터프레임 만들기
df_plot = pd.DataFrame({
    '연도': years + years,
    '평균 의사수': low_means + high_means,
    '그룹': ['노인비율 낮은 그룹'] * 5 + ['노인비율 높은 그룹'] * 5
})
print(df_plot)

 
# 선 그래프
sns.lineplot(data=df_plot, x='연도', y='평균 의사수', hue='그룹',
             marker='o', markersize=10)
plt.title('노인비율 그룹별 의사수 추이 (2019-2023)')
plt.xlabel('연도')
plt.ylabel('인구 10만명당 의사수')
plt.xticks(years)
plt.grid()
plt.show()
 

