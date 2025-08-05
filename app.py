import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# กำหนดข้อมูลลูกเต๋า
dice_faces = [
    {"name": "หุ้นเทรนสัตว์เลี้ยง", "color": "green", "faces": [-1, -1, 0, 0, 1, 1]},
    {"name": "หุ้นอสังหาริมทรัพย์", "color": "gold", "faces": [-2, -1, 0, 0, 1, 2]},
    {"name": "หุ้นคมนาคม", "color": "orange", "faces": [-3, -2, -1, 1, 2, 3]},
    {"name": "หุ้นเทคโนโลยี", "color": "red", "faces": [-7, -3, -2, 2, 3, 7]},
]

# ตั้งค่าเริ่มต้นเมื่อเปิดเว็บ
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "history" not in st.session_state:
    st.session_state.history = []

# แปลงตัวเลขเป็น string พร้อมเครื่องหมาย + ถ้าเป็นบวก
def format_face(face):
    if face > 0:
        return f"+{face}"
    else:
        return str(face)

# ฟังก์ชันวาดลูกเต๋า
def draw_dice(face, color):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8,
                                   boxstyle="round,pad=0.1",
                                   edgecolor="black",
                                   facecolor=color,
                                   linewidth=2)
    ax.add_patch(rect)
    ax.text(0.5, 0.5, format_face(face),
            fontsize=24, ha="center", va="center", color="black")
    
    return fig

# UI
st.set_page_config(page_title="ทอยลูกเต๋าทีละลูก", layout="centered")
st.title("🎲  ความผันผวนของหุ้น")

# แสดงสถานะลูกเต๋าล่าสุด
if st.button("🎲 ทอยลูกเต๋า!"):
    i = st.session_state.current_index
    dice = dice_faces[i]
    face = random.choice(dice["faces"])
    
    st.session_state.history.append((dice["name"], face, dice["color"]))
    
    st.session_state.current_index = (i + 1) % len(dice_faces)

# แสดงลูกเต๋าและประวัติ
if st.session_state.history:
    name, face, color = st.session_state.history[-1]
    st.subheader(f"🎯 ราคาหุ้นปัจจุบัน: {name}")
    st.pyplot(draw_dice(face, color))

    with st.expander("📜 ประวัติความผันผวนทั้งหมด", expanded=True):
        for idx, (n, f, c) in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"{idx}. **{n}**: `{format_face(f)}`")

else:
    st.info("ทอยลูกเต๋า")

