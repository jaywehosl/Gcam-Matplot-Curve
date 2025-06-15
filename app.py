import streamlit as st
import struct
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="HEX ↔ Double Tone Curve Editor")

st.title("🎚 HEX ↔ Double Tone Curve Editor (ARM64, little-endian)")

# ===== Functions =====

def hex_to_doubles(hex_string):
    hex_string = hex_string.replace(" ", "").replace("\n", "")
    if len(hex_string) % 16 != 0:
        raise ValueError("Hex length must be multiple of 16.")
    values = []
    for i in range(0, len(hex_string), 16):
        chunk = hex_string[i:i+16]
        b = bytes.fromhex(chunk)
        val = struct.unpack("<d", b)[0]
        values.append(val)
    return values

def doubles_to_hex(doubles):
    return ''.join(struct.pack('<d', val).hex() for val in doubles).upper()

# ===== Input Area =====

hex_input = st.text_area(
    "🔢 Вставь HEX строку (по 16 символов на значение, можно с пробелами/переносами):",
    placeholder="0000000000000000732F622CD40BA63F...",
    height=200
)

if hex_input:
    try:
        doubles = hex_to_doubles(hex_input)

        st.success("✅ HEX успешно преобразован в double значения.")

        # Editable Table
        st.subheader("📋 Значения (редактируемые)")
        cols = st.columns(len(doubles))
        new_values = []
        for i, (col, val) in enumerate(zip(cols, doubles)):
            new_val = col.number_input(f"{i}", value=val, key=f"val_{i}", format="%.10f")
            new_values.append(new_val)

        # Plot
        st.subheader("📈 График")
        fig, ax = plt.subplots()
        x = [i / (len(new_values) - 1) for i in range(len(new_values))]
        ax.plot(x, new_values, marker='o')
        for xi, yi in zip(x, new_values):
            ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)
        ax.set_xlabel("Input (Normalized)")
        ax.set_ylabel("Output (Double)")
        ax.set_title("Tone Curve")
        ax.grid(True)
        st.pyplot(fig)

        # HEX Output
        st.subheader("📦 HEX обратно")
        st.code(doubles_to_hex(new_values), language="text")

    except Exception as e:
        st.error(f"❌ Ошибка: {e}")
