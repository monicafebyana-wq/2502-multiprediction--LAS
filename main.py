import streamlit as st
import home
import dog_cat_classifier
import food_classifier
import nlp_transformer

st.set_page_config(
    page_title="Multi Model Prediction App",
    layout="wide"
)

PAGES = {
    "Home": home,
    "Klasifikasi Anjing vs Kucing": dog_cat_classifier,
    "Klasifikasi 101 Jenis Makanan": food_classifier,
    "Analisis Sentimen": nlp_transformer
}

def main():
    local_css("style.css")
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem; color: #4a90e2'>Aplikasi Prediksi Multi Model</h1>", unsafe_allow_html=True)

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












