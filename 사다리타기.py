import streamlit as st
import matplotlib
import random

st.title("🎯 진짜 사다리타기 시뮬레이션")

# 사용자 설정: 참가자 수
num_people = st.slider("참가자 수 선택", min_value=2, max_value=30, value=23)

# 사용자 설정: 결과 숫자 입력
default_numbers = list(range(47, 68)) + [97, 98]
result_input = st.text_input("배정할 숫자들 입력 (쉼표로 구분)", value=','.join(map(str, default_numbers)))

try:
    results = [int(x.strip()) for x in result_input.split(',') if x.strip().isdigit()]
    if len(results) != num_people:
        st.error(f"❌ 숫자의 개수({len(results)})가 참가자 수({num_people})와 다릅니다!")
        st.stop()
except ValueError:
    st.error("❌ 숫자 형식이 잘못되었습니다. 숫자만 쉼표로 구분해서 입력해주세요.")
    st.stop()

# 참가자 이름 자동 생성
participants = [f"{i+1}번" for i in range(num_people)]
random.shuffle(results)

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

# 사다리 타기 경로 추적
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

# 참가자별 결과 매핑 및 경로 저장
final_mapping = {}
all_paths = []
for i in range(num_people):
    end_col, path = simulate_path(i)
    final_mapping[participants[i]] = results[end_col]
    all_paths.append(path)

# 시각화
fig, ax = plt.subplots(figsize=(12, 16))

# 세로줄
for c in range(columns):
    ax.plot([c, c], [0, rows], color='black', linewidth=1)

# 가로줄
for r in range(rows):
    for c in range(columns - 1):
        if ladder[r][c] == 1:
            ax.plot([c, c+1], [r, r], color='gray', linewidth=1.5)

# 강조: 경로 시뮬레이션 (굵은 파란선)
for path in all_paths:
    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        ax.plot([x0, x1], [y0, y1], color='blue', alpha=0.3, linewidth=2)

# 참가자/결과 텍스트
for i, name in enumerate(participants):
    ax.text(i, rows + 1, name, ha='center', va='bottom', fontsize=9, rotation=90)

for i, res in enumerate(results):
    ax.text(i, -1, str(res), ha='center', va='top', fontsize=9, rotation=90)

ax.set_xlim(-1, columns)
ax.set_ylim(-2, rows + 2)
ax.axis('off')
st.pyplot(fig)

# 결과 출력
st.subheader("🔢 사다리타기 결과")
for name in sorted(final_mapping):
    st.write(f"{name} → {final_mapping[name]}")
