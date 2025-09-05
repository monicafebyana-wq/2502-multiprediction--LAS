import streamlit as st
import home
import dog_cat_classifier
import food_classifier
import nlp_transformer

st.set_page_config(
    page_title="Multi-Model Prediction App",
    layout="wide"
)

PAGES = {
    "Home": home,
    "Klasifikasi Anjing vs Kucing": dog_cat_classifier,
    "Klasifikasi 101 Jenis Makanan": food_classifier,
    "Analisis Sentimen": nlp_transformer
}

def apply_custom_css():
    st.markdown("""
        <style>
            div[data-testid="column"] {
                display: flex;
                justify-content: center;
            }
            .st-emotion-cache-13ln4pb {
                display: flex;
                justify-content: center;
                gap: 0.8rem;
            }

            /* Gaya untuk TOMBOL INAKTIF (bisa diklik) */
            .stButton button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: #e0e5ec;
                color: #5a677d;
                padding: 0.75rem 1.5rem;
                border-radius: 2rem;
                margin: 0.75rem 0;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
                font-weight: 600;
                font-size: 1rem;
                border: none;
                box-shadow: 6px 6px 12px #c5c9d2, -6px -6px 12px #fbffff;
                width: 100%;
            }
            
            .stButton button:hover {
                color: #3b82f6;
                transform: translateY(-3px);
                box-shadow: inset 4px 4px 8px #c5c9d2, inset -4px -4px 8px #fbffff;
            }
                
            .stButton button:active {
                color: #ffffff;
                background-color: #4a90e2;
                box-shadow: inset 4px 4px 8px #3b73b5;
            }
                
            .stButton button:onclick {
                color: #ffffff;
                background-color: #4a90e2;
                box-shadow: inset 4px 4px 8px #3b73b5;
            }
                
            .nav-button-active {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin: 0.75rem 0;
                background-color: #4a90e2; 
                color: #ffffff;
                padding: 0.75rem 1.5rem;
                border-radius: 2rem;
                font-weight: 600;
                font-size: 1rem;
                border: none;
                box-shadow: inset 4px 4px 8px #3b73b5, inset -4px -4px 8px #59adff;
                width: 100%; 
                text-align: center;
            }
            .prediction-card {
                background-color: #f8f9fa;
                border-radius: 20px;
                padding: 2rem;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                border: 1px solid #e9ecef;
                margin-top: 2rem;
            }
            .result-text {
                font-size: 2.2rem;
                font-weight: 600;
                margin: 1rem 0;
                color: #2c3e50;
            }
            .confidence-text {
                font-size: 1.1rem;
                color: #5a677d;
                margin-bottom: 0.5rem;
            }
            .progress-bar-container {
                width: 90%;
                background-color: #e0e5ec;
                border-radius: 1rem;
                margin: 1rem auto;
                box-shadow: inset 2px 2px 5px #c5c9d2, inset -2px -2px 5px #fbffff;
            }
            .progress-bar-fill {
                height: 24px;
                background: linear-gradient(90deg, #4CAF50, #81C784);
                border-radius: 1rem;
                text-align: center;
                color: white;
                line-height: 24px;
                font-weight: bold;
                transition: width 0.5s ease-in-out;
            }
            .stTextArea textarea {
                border-radius: 0.75rem;
                border: 1px solid #ced4da;
                padding: 1rem;
                font-size: 1.1rem;
                min-height: 150px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .result-card {
                background-color: #ffffff;
                border-radius: 1rem;
                padding: 2.5rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                margin-top: 2rem;
                border-top: 10px solid;
                text-align: center;
            }
            .result-emoji { 
                font-size: 5rem; 
            }
            .prediction-text {
                font-size: 1.5rem;
                color: #5a677d;
                margin-bottom: 0;
            }
            .prediction-label {
                font-size: 2.8rem;
                font-weight: bold;
                margin-top: 0;
            }
            .dist-title {
                font-weight: bold;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: #2c3e50;
            }
            .dist-bar-container {
                display: flex;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            .title-icon {
                font-size: 2.5rem;
                vertical-align: middle;
            }
            .stFileUploader {
                text-align: center;
                border: 2px dashed #3b82f6;
                border-radius: 1rem;
                padding: 2rem;
                background-color: #f0f8ff; /* AliceBlue */
            }
            .uploaded-image img {
                border-radius: 1rem;
                box-shadow: 0 10px 20px rgba(0,0,0,0.15);
                transition: transform 0.3s ease-in-out;
            }
            .uploaded-image img:hover {
                transform: scale(1.05);
            }
            .result-card {
                background-color: #ffffff;
                border-radius: 1rem;
                padding: 2rem;
                text-align: center;
                box-shadow: 0 10px 20px rgba(0,0,0,0.15);
                border-left: 8px solid #f97316; /* Warm Orange Accent */
            }
            .prediction-text {
                font-size: 2.2rem;
                font-weight: bold;
                color: #4a4a4a;
                margin-bottom: 0.5rem;
            }
            .confidence-text {
                font-size: 1.2rem;
                color: #6c757d;
            }
            .main-container {
                padding: 2rem 1rem;
            }
            .hero-section {
                text-align: center;
                padding: 3rem 1rem;
                background-color: #f8f9fa;
                border-radius: 1rem;
                margin-bottom: 2rem;
            }
            .hero-title {
                font-size: 3.5rem;
                font-weight: bold;
                color: #212529;
            }
            .hero-subtitle {
                font-size: 1.5rem;
                color: #495057;
                margin-top: -1rem;
            }
            .feature-card {
                background-color: #ffffff;
                border-radius: 1rem;
                padding: 2.5rem;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                height: 100%; /* Membuat kartu memiliki tinggi yang sama */
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.15);
            }
            .feature-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
            .feature-title {
                font-size: 1.75rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .feature-description {
                font-size: 1.1rem;
                color: #6c757d;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()

    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Aplikasi Prediksi Multi Model</h1>", unsafe_allow_html=True)

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Home"

    cols = st.columns(len(PAGES))
    for i, (page_name, _) in enumerate(PAGES.items()):
        with cols[i]:
            if st.session_state.active_page == page_name:
                st.markdown(f'<div class="nav-button-active">{page_name}</div>', unsafe_allow_html=True)
            else:
                if st.button(page_name, use_container_width=True):
                    st.session_state.active_page = page_name
                    st.rerun()

    select_page = PAGES[st.session_state.active_page]
    
    with st.spinner(f"Memuat halaman {st.session_state.active_page}..."):
        select_page.app()

if __name__ == "__main__":
    main()




