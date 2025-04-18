import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")
st.title("🎯 진짜 사다리타기 시뮬레이션")

# 사용자 설정: 학생 수만 입력
num_people = st.slider("학생 수 선택", min_value=2, max_value=30, value=5)
participants = [str(i+1) for i in range(num_people)]  # 단순 번호 목록

# 사용자 설정: 결과 항목 입력
result_input = st.text_input("결과 숫자 또는 항목 입력 (쉼표로 구분)", value=','.join([str(i+1) for i in range(num_people)]))
results = [r.strip() for r in result_input.split(',') if r.strip()]

if len(results) != num_people:
    st.error(f"결과 항목 수({len(results)})가 학생 수({num_people})와 일치하지 않습니다.")
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

# 경로 계산
all_paths = []
final_mapping = {}
random.shuffle(results)

for i in range(num_people):
    end_col, path = simulate_path(i)
    final_mapping[participants[i]] = results[end_col]
    all_paths.append(path)

# 학생별 경로 색상
color_palette = plt.cm.get_cmap('tab20', num_people)

# 슬라이더로 몇 번째 학생까지 보여줄지 제어
selected_index = st.slider("몇 번째 학생까지 내려가볼까요?", min_value=1, max_value=num_people, value=1)

# 시각화
fig, ax = plt.subplots(figsize=(num_people, 15))

for c in range(columns):
    ax.plot([c, c], [0, rows], color='black', linewidth=1)

for r in range(rows):
    for c in range(columns - 1):
        if ladder[r][c] == 1:
            ax.plot([c, c+1], [r, r], color='gray', linewidth=1.5)

# 강조 경로 (선택된 학생까지만, 각자 다른 색으로)
for idx in range(selected_index):
    path = all_paths[idx]
    color = color_palette(idx)
    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        ax.plot([x0, x1], [y0, y1], color=color, alpha=0.7, linewidth=2.5)

# 사다리 윗쪽 학생 번호 표시
for i in range(num_people):
    ax.text(i, rows + 1.5, str(i + 1), ha='center', va='bottom', fontsize=14, fontweight='bold')

# 결과 숫자 크게 표시 (아래쪽)
for i, res in enumerate(results):
    ax.text(i, -1.5, str(res), ha='center', va='top', fontsize=16, fontweight='bold')

ax.set_xlim(-1, columns)
ax.set_ylim(-2, rows + 3)
ax.axis('off')
st.pyplot(fig)

# 선택된 학생까지만 결과 표시
st.subheader("🔢 사다리타기 결과")
for i in range(selected_index):
    st.write(f"학생 {participants[i]} → **{final_mapping[participants[i]]}**")
