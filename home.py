import streamlit as st

def app():
    st.markdown("""
        <style>
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
                <p class="feature-icon">🍔</p>
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


