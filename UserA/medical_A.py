import pandas as pd
import matplotlib.pyplot as plt
import koreanfont
import csv
import seaborn as sns
import numpy as np

data1=pd.read_csv( './UserA/팀A_의료자원공급_5년치변화분석.csv',encoding='utf-8' )
data2=pd.read_csv( './UserA/팀A_의료자원공급_시계열.csv',encoding='utf-8' )
data3=pd.read_excel( './UserA/팀A_의료자원공급.xlsx' )
data4=pd.read_csv( './UserC/팀C_수요건강결과_5년치변화분석.csv', encoding='utf-8')

data4['인구밀도'] = data4['인구수_2023'] / data4['면적_2023']

df = pd.merge(data1, data4[['sd_cd', '인구밀도']], on='sd_cd')

grp = df.groupby('시도')[['인구밀도', '전체의사_2023', '종합병원병상_2023']].agg({
    '인구밀도': 'mean',
    '전체의사_2023': 'sum',
    '종합병원병상_2023': 'sum'
})

grp = grp.sort_values('인구밀도')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.bar(grp.index, grp['전체의사_2023'], color='blue', alpha=0.85)
ax1.set_xlabel('지역')
ax1.set_ylabel('평균 전체의사 수')
ax1.set_title('시도별 평균 전체의사 수 (인구밀도 낮은 순)')

ax2.bar(grp.index, grp['종합병원병상_2023'], color='red', alpha=0.85)
ax2.set_xlabel('지역')
ax2.set_ylabel('평균 종합병원 병상 수')
ax2.set_title('인구밀도 구간별 평균 종합병원 병상 수')

ax1.set_xticks(range(len(grp.index)))
ax1.set_xticklabels(grp.index, rotation=45, ha='right')
ax2.set_xticks(range(len(grp.index)))
ax2.set_xticklabels(grp.index, rotation=45, ha='right')

plt.suptitle('인구밀도 구간별 의료자원 비교', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./UserA/fig1_bar.png')
plt.show()

# 수도권과 비수도권 간 인구 10만 명당 전체전문의·산부인과전문의 수 격차는
# 2019년 이후 뚜렷하게 줄어들지 않았을 것이다.
# → 필수의료 인력의 지역 격차가 지속되는지 확인한다.
capital_area=['서울특별시','경기도','인천광역시']

def 지역분류(x):
    if x in capital_area:
        return '수도권'
    else:
        return '비수도권'

data2['권역']=data2['명칭'].apply(지역분류)

전문의=data2.groupby(['기준연도','권역'])['rs04_전체전문의'].mean().reset_index()
산부인과=data2.groupby(['기준연도','권역'])['rs10_산부인과전문의'].mean().reset_index()

print(전문의)
print(산부인과)