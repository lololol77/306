import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")
st.title("🎯 진짜 사다리타기 시뮬레이션")

# 사용자 설정: 참가자 수
num_people = st.slider("참가자 수 선택", min_value=2, max_value=30, value=5)

# 사용자 설정: 참가자 이름 입력
participant_input = st.text_area("참가자 이름 입력 (쉼표로 구분)", value=','.join([f"{i+1}번" for i in range(num_people)]))
participants = [name.strip() for name in participant_input.split(',') if name.strip()]

if len(participants) != num_people:
    st.error(f"참가자 수({len(participants)})가 슬라이더에서 선택한 수({num_people})와 일치하지 않습니다.")
    st.stop()

# 사용자 설정: 결과 항목 입력
result_input = st.text_input("결과 숫자 또는 항목 입력 (쉼표로 구분)", value=','.join([str(i+1) for i in range(num_people)]))
results = [r.strip() for r in result_input.split(',') if r.strip()]

if len(results) != num_people:
    st.error(f"결과 항목 수({len(results)})가 참가자 수({num_people})와 일치하지 않습니다.")
    st.stop()

# 사다리 구조 생성
columns = num_people
rows = 30
ladder = [[0 for _ in range(columns)] for _ in range(rows)]

# 랜덤 가로줄 배치
for r in range(rows):
    for c in range(columns - 1):
        if random.random() < 0.2 and ladder[r][c] == 0 and ladder[r][c+1] == 0:
            ladder[r][c] = 1
            ladder[r][c+1] = -1

# 사다리 타기 경로 시뮬레이션
def simulate_path(start_col):
    path = [(start_col, 0)]
    col = start_col
    for r in range(rows):
        if ladder[r][col] == 1:
            col += 1
        elif ladder[r][col] == -1:
            col -= 1
        path.append((col, r + 1))
    return col, path

# 버튼 누를 때 실행
if st.button("🎲 사다리 타기 결과 보기"):
    random.shuffle(results)  # 버튼 누를 때마다 shuffle
    final_mapping = {}
    all_paths = []

    for i in range(num_people):
        end_col, path = simulate_path(i)
        final_mapping[participants[i]] = results[end_col]
        all_paths.append(path)

    # 시각화
    fig, ax = plt.subplots(figsize=(num_people, 15))

    for c in range(columns):
        ax.plot([c, c], [0, rows], color='black', linewidth=1)

    for r in range(rows):
        for c in range(columns - 1):
            if ladder[r][c] == 1:
                ax.plot([c, c+1], [r, r], color='gray', linewidth=1.5)

    # 강조 경로
    for path in all_paths:
        for i in range(len(path) - 1):
            x0, y0 = path[i]
            x1, y1 = path[i + 1]
            ax.plot([x0, x1], [y0, y1], color='blue', alpha=0.3, linewidth=2)

    for i, name in enumerate(participants):
        ax.text(i, rows + 1.5, name, ha='center', va='bottom', fontsize=10, rotation=90)

    for i, res in enumerate(results):
        ax.text(i, -1.5, str(res), ha='center', va='top', fontsize=10, rotation=90)

    ax.set_xlim(-1, columns)
    ax.set_ylim(-2, rows + 3)
    ax.axis('off')
    st.pyplot(fig)

    st.subheader("🔢 사다리타기 결과")
    for name in sorted(final_mapping):
        st.write(f"**{name}** → **{final_mapping[name]}**")
