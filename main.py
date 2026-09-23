import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정

st.set_page_config(
page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

# 데이터 불러오기

@st.cache_data
def load_data():
df = pd.read_csv(DATA_URL)
return df

df = load_data()

# 개봉일 변환

df["openDt"] = pd.to_datetime(
df["openDt"].astype(str),
format="%Y%m%d",
errors="coerce"
)

# 장르가 여러 개 적힌 경우 첫 번째 장르만 사용

df["genre_first"] = (
df["genre"]
.fillna("미상")
.astype(str)
.str.split("|")
.str[0]
.str.strip()
)

# -----------------------------

# 그래프 1. 장르별 영화 편수

# -----------------------------

st.header("그래프 1. 장르별 영화 편수")

genre_counts = (
df["genre_first"]
.value_counts()
.reset_index()
)

genre_counts.columns = ["장르", "영화편수"]

fig = px.pie(
genre_counts,
names="장르",
values="영화편수",
hole=0.45,
title="장르별 영화 편수"
)

fig.update_traces(
textinfo="percent",
hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig.update_layout(
height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.info("여기에 이 그래프로 알 수 있는 사실을 한 문장으로 작성하세요.")

st.divider()
