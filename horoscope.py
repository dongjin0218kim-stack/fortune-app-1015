import datetime
import hashlib
import random

import streamlit as st

# ---------------------------------------------
# 기본 데이터
# ---------------------------------------------
ZODIACS = {
    "쥐띠": "🐭", "소띠": "🐮", "호랑이띠": "🐯", "토끼띠": "🐰",
    "용띠": "🐲", "뱀띠": "🐍", "말띠": "🐴", "양띠": "🐑",
    "원숭이띠": "🐵", "닭띠": "🐔", "개띠": "🐶", "돼지띠": "🐷",
}
ZODIAC_LIST = list(ZODIACS.keys())

GENERAL = [
    "막혔던 일이 술술 풀리는 하루입니다. 미뤄둔 일을 처리해 보세요.",
    "작은 오해가 생길 수 있으니 말 한마디에 신경 쓰세요.",
    "주변의 도움으로 뜻밖의 성과를 얻게 됩니다.",
    "서두르면 일을 그르칠 수 있습니다. 한 박자 쉬어 가세요.",
    "새로운 시작에 좋은 기운이 들어옵니다. 망설이지 말고 도전하세요.",
    "평범하지만 안정적인 하루. 기본에 충실하면 좋은 결과가 따릅니다.",
    "오랜만에 반가운 소식을 듣게 됩니다.",
    "생각이 많아지는 날입니다. 중요한 결정은 내일로 미루는 것이 좋습니다.",
    "노력한 만큼 인정받는 날입니다. 자신감을 가지세요.",
    "예상치 못한 변수가 생기지만 침착하게 대응하면 전화위복이 됩니다.",
]
MONEY = [
    "작은 지출이 모여 큰돈이 됩니다. 충동구매를 조심하세요.",
    "뜻밖의 수입이 생길 수 있습니다.",
    "투자보다는 저축이 유리한 날입니다.",
    "금전 거래는 신중하게. 빌려주는 돈은 돌아오기 어렵습니다.",
    "재물운이 상승하는 날입니다. 계획했던 일을 추진해 보세요.",
    "큰 변동은 없지만 꾸준함이 이득이 됩니다.",
]
LOVE = [
    "솔직한 표현이 관계를 더욱 깊게 만듭니다.",
    "새로운 인연을 만날 가능성이 높은 날입니다.",
    "사소한 일로 다툴 수 있으니 한 번 더 양보하세요.",
    "오래된 인연과 다시 연락이 닿을 수 있습니다.",
    "함께하는 시간이 소중하게 느껴지는 하루입니다.",
    "혼자만의 시간이 필요한 날. 무리하게 약속을 잡지 마세요.",
]
HEALTH = [
    "가벼운 산책이 컨디션 회복에 큰 도움이 됩니다.",
    "과식을 피하고 물을 충분히 드세요.",
    "눈과 어깨의 피로에 신경 쓰세요. 틈틈이 스트레칭을!",
    "활력이 넘치는 날입니다. 운동을 시작하기 좋습니다.",
    "충분한 수면이 최고의 보약입니다.",
    "환절기 감기를 조심하세요.",
]
COLORS = ["빨강", "주황", "노랑", "초록", "파랑", "남색", "보라", "흰색", "검정", "금색", "은색", "분홍"]
DIRECTIONS = ["동쪽", "서쪽", "남쪽", "북쪽", "동남쪽", "동북쪽", "서남쪽", "서북쪽"]


# ---------------------------------------------
# 함수
# ---------------------------------------------
def zodiac_from_year(year: int) -> str:
    """출생연도로 띠 계산 (양력 기준, 1900년 = 쥐띠)"""
    return ZODIAC_LIST[(year - 1900) % 12]


def get_fortune(zodiac: str, date: datetime.date) -> dict:
    """날짜 + 띠를 시드로 사용 → 같은 날, 같은 띠는 항상 같은 운세"""
    seed_text = f"{date.isoformat()}-{zodiac}"
    seed = int(hashlib.md5(seed_text.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    return {
        "score": rng.randint(50, 100),
        "general": rng.choice(GENERAL),
        "money": rng.choice(MONEY),
        "love": rng.choice(LOVE),
        "health": rng.choice(HEALTH),
        "color": rng.choice(COLORS),
        "number": rng.randint(1, 45),
        "direction": rng.choice(DIRECTIONS),
        "stars": {k: rng.randint(1, 5) for k in ["금전운", "애정운", "건강운"]},
    }


def stars(n: int) -> str:
    return "★" * n + "☆" * (5 - n)


# ---------------------------------------------
# 화면 구성
# ---------------------------------------------
st.set_page_config(page_title="오늘의 운세", page_icon="🔮")
st.title("🔮 오늘의 띠별 운세")

# 서버 위치와 상관없이 한국 시간 기준 날짜 사용
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(KST).date()
st.caption(f"{today.year}년 {today.month}월 {today.day}일")

# 띠 선택 방식
mode = st.radio("띠 선택 방법", ["띠 직접 선택", "출생연도로 찾기"], horizontal=True)

if mode == "띠 직접 선택":
    zodiac = st.selectbox(
        "띠를 선택하세요",
        ZODIAC_LIST,
        format_func=lambda z: f"{ZODIACS[z]} {z}",
    )
else:
    year = st.number_input("출생연도 (양력)", min_value=1920, max_value=today.year, value=1985, step=1)
    zodiac = zodiac_from_year(int(year))
    st.info(f"{int(year)}년생은 **{ZODIACS[zodiac]} {zodiac}** 입니다. (음력 설 이전 출생자는 앞 띠일 수 있어요)")

if st.button("운세 보기 ✨", type="primary", use_container_width=True):
    f = get_fortune(zodiac, today)

    st.divider()
    st.header(f"{ZODIACS[zodiac]} {zodiac}의 오늘 운세")

    st.metric("오늘의 운세 점수", f"{f['score']}점")
    st.progress(f["score"] / 100)

    st.subheader("🌟 총운")
    st.write(f["general"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**💰 금전운**  \n{stars(f['stars']['금전운'])}")
        st.write(f["money"])
    with col2:
        st.markdown(f"**💕 애정운**  \n{stars(f['stars']['애정운'])}")
        st.write(f["love"])
    with col3:
        st.markdown(f"**💪 건강운**  \n{stars(f['stars']['건강운'])}")
        st.write(f["health"])

    st.subheader("🍀 행운 아이템")
    c1, c2, c3 = st.columns(3)
    c1.metric("행운의 색", f["color"])
    c2.metric("행운의 숫자", f["number"])
    c3.metric("행운의 방향", f["direction"])

    if f["score"] >= 90:
        st.balloons()

st.divider()
st.caption("※ 재미로 보는 운세입니다. 같은 날 같은 띠는 항상 같은 결과가 나옵니다.")