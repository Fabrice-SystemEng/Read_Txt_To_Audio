import streamlit as st
from gtts import gTTS
import io

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Convertisseur Texte en Audio",
    page_icon="🎵",
    layout="centered"
)

# --- Titre de l'application ---
st.title("🎵 Convertisseur Texte vers MP3")
st.write("Collez votre texte ci-dessous pour l'écouter ou générer un fichier MP3.")

# --- Zone de saisie du texte ---
# Parfait pour le copier-coller depuis un smartphone Android
text_to_speak = st.text_area(
    label="Entrez ou collez votre texte ici :",
    placeholder="Écrivez quelque chose...",
    height=250
)

# --- Sélections des options ---
LANGUAGE = 'fr'

# --- Traitement ---
if st.button("▶️ Convertir et Écouter", use_container_width=True):
    if not text_to_speak.strip():
        st.warning("⚠️ Le contenu texte est vide. Veuillez coller du texte avant de lancer la conversion.")
    else:
        with st.spinner("⏳ Conversion du texte en audio en cours..."):
            try:
                # Utilisation d'un buffer en mémoire (BytesIO) au lieu d'écrire sur le disque (d:/Download/...)
                # C'est indispensable pour que cela fonctionne à distance sur ton téléphone !
                mp3_fp = io.BytesIO()
                
                # Génération du TTS via gTTS
                tts = gTTS(text=text_to_speak, lang=LANGUAGE, slow=False)
                tts.write_to_fp(mp3_fp)
                
                # Revenir au début du fichier en mémoire pour la lecture
                mp3_fp.seek(0)
                
                st.success("✅ Conversion réussie !")
                
                # --- Lecteur Audio Intégré ---
                # Le widget natif HTML5 s'adapte parfaitement aux navigateurs mobiles (Chrome/Firefox sur Android)
                st.audio(mp3_fp, format="audio/mp3")
                
                # --- Option de téléchargement ---
                # Permet de sauvegarder le fichier directement sur ton stockage Android si besoin
                st.download_button(
                    label="📥 Télécharger le fichier MP3",
                    data=mp3_fp,
                    file_name="texte_audio.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:
                st.error(True, f"❌ Une erreur s'est produite lors de la conversion : {e}")
