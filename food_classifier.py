import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.applications import ResNet50

INPUT_SHAPE = (128, 128, 3)

food_label = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
    'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
    'ceviche', 'cheesecake', 'cheese_plate', 'chicken_curry', 'chicken_quesadilla',
    'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder',
    'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes',
    'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots',
    'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries',
    'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice',
    'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich',
    'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup',
    'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna',
    'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons',
    'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters',
    'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho',
    'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich',
    'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi',
    'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese',
    'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake',
    'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'
]

basic_path = hf_hub_download(
    repo_id="monicafebyana/food101basic",
    filename="model_food101_2502.h5"
)

pretrained_path = hf_hub_download(
    repo_id="monicafebyana/food101pretrained",
    filename="food101_pretrained_2502.h5"
)

def preprocess_image(img):
    img_resized = img.resize(INPUT_SHAPE[:2])
    image_array = tf.keras.preprocessing.image.img_to_array(img_resized)
    image_array = np.expand_dims(image_array, axis=0) / 255.0
    return image_array

def display_pred(image, prediction):
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.image(image, caption='Gambar yang Anda Unggah', use_container_width=True,
                 output_format='PNG')

    with col2:
        with st.spinner('Model sedang menganalisis...'):
            predicted_class_index = np.argmax(prediction)
            confidence = np.max(prediction)
            
            predicted_class_name = food_label[predicted_class_index]
            
            formatted_class_name = predicted_class_name.replace('_', ' ').title()
            
            confidence_percent = confidence * 100

            st.markdown(f"""
                <div class="prediction-card">
                    <h3>🤔 Sepertinya...</h3>
                    <p class="result-text">Ini adalah <strong>{formatted_class_name}</strong>!</p>
                    <p class="confidence-text">Tingkat Keyakinan Model</p>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {confidence_percent:.2f}%;">
                            {confidence_percent:.2f}%
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; color: #6c757d; margin-top: 1rem;">
                        Model ini menebak dari 101 jenis makanan yang berbeda.
                    </p>
                </div>
            """, unsafe_allow_html=True)

@st.cache_resource
def load_basic_model(path):
    
    model = Sequential([
        Conv2D(32, kernel_size=3, activation='relu', input_shape=INPUT_SHAPE),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),

        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D((2, 2), strides=2, padding='valid'),
        BatchNormalization(),
        
        AveragePooling2D(pool_size=(3,3), strides=(1,1)),

        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(101, activation='softmax')
    ])
    
    model.load_weights(path)
    return model

@st.cache_resource
def load_pretrained_model(path):
    base_model = ResNet50(
    weights=None, 
    include_top=False, 
    input_shape=INPUT_SHAPE
    )

    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(101, activation='softmax')
    ])

    model.load_weights(path, by_name=True)
    return model


def app():
    st.title("Klasifikasi 101 Jenis Makanan")
    st.markdown("---")
    st.markdown("### Pilih model", unsafe_allow_html=True)
    option = st.selectbox(
        "Pilihlah model untuk memprediksi gambar mu!",
        options=["Basic Model", "Pretrained Model"],
        placeholder="Pilih model..."
    )
    st.markdown("### <span class='title-icon'>📸</span> Unggah Foto Makanan Anda", unsafe_allow_html=True)
    st.markdown("Penasaran nama hidangan di depan Anda? Biarkan model AI kami menebaknya dari **101 jenis makanan** yang berbeda! 🍔🍕🥗")

    uploaded_file = st.file_uploader(
        "Pilih gambar makanan untuk dianalisis...",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
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
            display_pred(image, prediction)
    else:
        st.info("Menunggu Anda mengunggah foto makanan lezat.", icon="👆")








