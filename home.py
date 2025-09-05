import streamlit as st

def app():
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div class="feature-card">
                <p class="feature-icon">🐾</p>
                <p class="feature-title">Anjing vs Kucing</p>
                <p class="feature-description">
                    Unggah gambar anjing atau kucing, dan biarkan model Computer Vision kami yang membedakannya.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <h4>🍔</h4>
                <p class="feature-title">101 Jenis Makanan</p>
                <p class="feature-description">
                    Punya foto makanan? Model kami dapat mengenali 101 hidangan berbeda dari seluruh dunia.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <p class="feature-icon">✍️</p>
                <p class="feature-title">Analisis Sentimen</p>
                <p class="feature-description">
                    Analisis emosi di balik teks. Model NLP berbasis Transformer kami akan menentukan apakah sentimennya positif, negatif, atau netral.
                </p>
            </div>
        """, unsafe_allow_html=True)




