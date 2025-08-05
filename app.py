import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

# ข้อมูลลูกเต๋า
dice_faces = [
    {"name": "หุ้นเทรนสัตว์เลี้ยง", "color": "green", "faces": [-1, -1, 0, 0, 1, 1]},
    {"name": "หุ้นอสังหาริมทรัพย์", "color": "gold", "faces": [-2, -1, 0, 0, 1, 2]},
    {"name": "หุ้นคมนาคม", "color": "orange", "faces": [-3, -2, -1, 1, 2, 3]},
    {"name": "หุ้นเทคโนโลยี", "color": "red", "faces": [-7, -3, -2, 2, 3, 7]},
]

# Session state เริ่มต้น
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "history" not in st.session_state:
    st.session_state.history = []

# แปลงแต้มให้มีเครื่องหมาย +
def format_face(face):
    return f"+{face}" if face > 0 else str(face)

# วาดลูกเต๋าและส่งเป็นภาพ
def draw_dice(face, color):
    fig, ax = plt.subplots(figsize=(1.2, 1.2), dpi=100)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8,
                                   boxstyle="round,pad=0.1",
                                   edgecolor="black",
                                   facecolor=color,
                                   linewidth=1.5)
    ax.add_patch(rect)
    ax.text(0.5, 0.5, format_face(face),
            fontsize=14, ha="center", va="center", color="black", fontweight='bold')

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", transparent=False)
    buf.seek(0)
    plt.close(fig)
    return buf

# UI
st.set_page_config(page_title="ทอยลูกเต๋า", layout="centered")
st.title("🎲 ความผันผวนตลาด")
st.markdown("🎯 ราคาหุ้นปัจจุบัน: **แทงเสียๆๆๆเด้อ**")

# ปุ่มทอยลูกเต๋า
with st.form(key="roll_form"):
    submit_button = st.form_submit_button(label="🎲 ทอยลูกเต๋า!")
    if submit_button:
        i = st.session_state.current_index
        dice = dice_faces[i]
        face = random.choice(dice["faces"])
        st.session_state.history.append((dice["name"], face, dice["color"]))
        st.session_state.current_index = (i + 1) % len(dice_faces)

# แสดงผลลูกเต๋า
if st.session_state.history:
    name, face, color = st.session_state.history[-1]
    st.subheader(f"🎯 {name} 🎯")
    st.image(draw_dice(face, color), width=120)

    with st.expander("📜 ประวัติการทอยทั้งหมด", expanded=True):
        for idx, (n, f, c) in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"{idx}. **{n}**: `{format_face(f)}`")
else:
    st.info("กดปุ่มด้านบนเพื่อเริ่มทอยลูกเต๋า")




