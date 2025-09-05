import streamlit as st

def app():
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div class="feature-card">
                <p class="feature-icon">🐾</p>
                <p class="feature-title">Anjing vs Kucing</p>
                <p class="feature-description">
                    Unggah gambar anjing atau kucing, dan biarkan model yang membedakannya.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <p class="feature-icon">🍔</p>
                <p class="feature-title">101 Jenis Makanan</p>
                <p class="feature-description">
                    Punya foto makanan? Unggah foto makanan mu dan model kami akan mengenalinya.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <p class="feature-icon">✍️</p>
                <p class="feature-title">Analisis Sentimen</p>
                <p class="feature-description">
                    Analisis emosi pada teks. Apakah tulisan mu berkonotasi SADNESS, ANGER, SUPPORT, HOPE, atau DISAPPOINTMENT.
                </p>
            </div>
        """, unsafe_allow_html=True)







