import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2

INPUT_SHAPE = (128, 128, 3)

basic_path = hf_hub_download(
    repo_id="monicafebyana/catvsdogbasic",
    filename="model_catvsdog_2502.h5"
)

pretrained_path = hf_hub_download(
    repo_id="monicafebyana/catvsdogpretrained",
    filename="catvsdog_pretrained_2502.h5"
)

@st.cache_resource
def load_basic_model(path):
    
    model = Sequential([
        Conv2D(32, kernel_size=3, activation='relu', input_shape=INPUT_SHAPE),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),
        Conv2D(64, kernel_size=3, activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),
        Conv2D(128, kernel_size=3, activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),
        Conv2D(256, kernel_size=3, activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.1),
        Dense(64, activation='relu'),
        Dropout(0.1),
        Dense(1, activation='sigmoid')
    ])
    
    model.load_weights(path)
    return model

@st.cache_resource
def load_pretrained_model(path):
    base = MobileNetV2(
        weights=None,
        include_top=False,
        input_shape=INPUT_SHAPE
    )
    base.trainable = False

    model = Sequential([
        base,
        GlobalAveragePooling2D(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.load_weights(path, by_name=True)
    return model

def preprocess_image(img):
    img_resized = img.resize(INPUT_SHAPE[:2])
    image_array = tf.keras.preprocessing.image.img_to_array(img_resized)
    image_array = np.expand_dims(image_array, axis=0) / 255.0
    return image_array

def display_pred(image, confidence):
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(image, caption='Gambar yang Anda Unggah', use container_width=True)

    with col2:
        with st.spinner('Model sedang memprediksi...'):
            is_dog = confidence > 0.5
            label = "Anjing" if is_dog else "Kucing"
            emoji = "🐕" if is_dog else "🐈"
            
            if is_dog:
                confidence_percent = confidence * 100
            else:
                confidence_percent = (1 - confidence) * 100

            st.markdown(f"""
                <div class="prediction-card">
                    <h3>🤔 Sepertinya...</h3>
                    <p class="result-text">{emoji} Ini adalah <strong>{label}</strong>!</p>
                    <p class="confidence-text">Tingkat Keyakinan Model</p>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {confidence_percent:.2f}%;">
                            {confidence_percent:.2f}%
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; color: #6c757d; margin-top: 1rem;">
                        Model ini menebak foto anda kucing atau kucing.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
def app():
    st.title("Klasifikasi Anjing vs Kucing")
    st.markdown("---")
    
    st.markdown("### Pilih model", unsafe_allow_html=True)
    option = st.selectbox(
        "Pilihlah model untuk memprediksi hewan peliharaanmu!",
        options=["Basic Model", "Pretrained Model"],
        placeholder="Pilih model..."
    )


    st.markdown("### <span class='title-icon'>📸</span> Unggah Gambar Anda", unsafe_allow_html=True)
    st.markdown("Sebenarnya hewan peliharaanmu **kucing** atau **anjing** ya?🐕🐈")
    uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        processed_image = preprocess_image(image)
        model = None

        if option == "Basic Model":
            model = load_basic_model(basic_path)
        elif option == "Pretrained Model":
            model = load_pretrained_model(pretrained_path)
        elif option == "Pilih model...":
            st.warning("Silakan pilih model terlebih dahulu!", icon="⚠️")
            st.stop()
        
        if model:
            prediction = model.predict(processed_image)
            confidence = prediction[0][0]
            display_pred(image, confidence)
    else:
        st.info("Menunggu Anda untuk mengunggah gambar.", icon="👆")


