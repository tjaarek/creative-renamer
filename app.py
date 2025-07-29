import streamlit as st
from datetime import datetime
import zipfile
import io
import os

# Seiteneinstellungen
st.set_page_config(page_title="Creative Renamer", layout="centered")

st.title("Creative Renamer für Asset Library")

# 1. Upload zuerst
st.subheader("📤 1. Bilder hochladen")
uploaded_files = st.file_uploader(
    "Ziehe deine Bilder hier rein oder klicke zum Hochladen",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Wenn Dateien hochgeladen wurden
if uploaded_files:
    st.success(f"{len(uploaded_files)} Datei(en) erfolgreich hochgeladen.")

    # 2. Namensschema definieren
    st.subheader("🔤 2. Namensschema festlegen")
    col1, col2, col3, col4 = st.columns(4)
    feld1 = col1.text_input("Feld 1", placeholder="z.B. Summer")
    feld2 = col2.text_input("Feld 2", placeholder="z.B. Collection")
    feld3 = col3.text_input("Feld 3", placeholder="z.B. Tshirt")
    feld4 = col4.text_input("Feld 4", placeholder="z.B. Print")

    # Nur anzeigen, wenn mindestens ein Feld ausgefüllt wurde
    if any([feld1, feld2, feld3, feld4]):
        prefix = datetime.now().strftime("%Y%m")
        parts = [feld1, feld2, feld3, feld4]
        suffix_base = "_".join([part.strip() for part in parts if part.strip()])

        # ZIP erstellen
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for i, file in enumerate(uploaded_files, start=1):
                ext = os.path.splitext(file.name)[1].lower()
                neuer_name = f"{prefix}_{suffix_base}_{i}{ext}"
                zipf.writestr(neuer_name, file.read())
        zip_buffer.seek(0)

        # 3. Download anbieten
        st.subheader("📦 3. ZIP-Datei herunterladen")
        st.download_button(
            label="📥 ZIP-Datei herunterladen",
            data=zip_buffer,
            file_name=f"{prefix}_{suffix_base}.zip",
            mime="application/zip"
        )
    else:
        st.info("⬇️ Bitte fülle mindestens ein Feld für das Namensschema aus.")
else:
    st.info("⬆️ Bitte lade zuerst Bilder hoch, um fortzufahren.")
