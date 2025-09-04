import streamlit as st
import tensorflow as tf
from tensorflow import keras
import re
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer
from transformers import TFBertModel

tokenizer = AutoTokenizer.from_pretrained("indolem/indobertweet-base-uncased")

model_path = hf_hub_download(
    repo_id="monicafebyana/transformernlp2502",
    filename="transformer_sentiment_2502.h5"
)

@st.cache_resource
def load_model_cached(path):
    custom_objects = {'TFBertModel': TFBertModel}

    model = keras.models.load_model(
        model_path,
        custom_objects=custom_objects
    )
    
    return model

label_mapping = {
    0 : "SADNESS",
    1 : "ANGER",
    2 : "SUPPORT",
    3 : "HOPE",
    4 : "DISAPPOINTMENT"
}

emoji_mapping = {
    "SADNESS": "😢", 
    "ANGER": "😠", 
    "SUPPORT": "🤗", 
    "HOPE": "✨", 
    "DISAPPOINTMENT": "😞"
}

warna_mapping = {
    "SADNESS": "#3498db", 
    "ANGER": "#e74c3c", 
    "SUPPORT": "#2ecc71", 
    "HOPE": "#f1c40f", 
    "DISAPPOINTMENT": "#9b59b6"
}

def tokenize_function(examples):
    return tokenizer(
        examples,
        padding="max_length",
        truncation=True,
        max_length=64,
        return_tensors='tf'
        )


slang_dict = {
    "gk": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "tdk": "tidak",
    "bgt": "banget",
    "wkwk": "ketawa",
    "btw": "ngomong-ngomong",
    "cmn": "cuman",
    "yg": "yang",
    "mmg": "memang",
    "trus": "terus",
    "moga": "semoga",
    "ya": " ",
    "negri": "negara",
    "org": "orang",
    "aja": " ",
    "sih": " ",
    "blm": "belum",
    "lg": "lagi",
    "tp": "tapi",
    "sy": "saya",
    "utbk": " ",
    "unk": " ",
    "httpurl": " ",
    "nih": " "
}

def slang_replace(text):
    for k, v in slang_dict.items():
        text = re.sub(r"\b{}\b".format(k), v, text)
    return text

def user_preprocess(text):
    nouser = []

    for t in text.split(" "):
        t = '' if t.startswith('@') and len(t) > 1 else t
        nouser.append(t)

    return " ".join(nouser).strip().replace("  ", " ")


def text_preprocessing(text):
    text = text.lower() # text jadi kecil
    text = user_preprocess(text) # hapus username
    text = re.sub(r"https?://\S+|www\.\S+", " ", text) # hapus link
    text = re.sub(r"[-+]?[0-9]+", " ", text) # hapus angka
    text = re.sub(r"[^\w\s]", " ", text) # hapus tanda baca
    text = re.sub(r"[^a-z\s]", " ", text) # selain huruf dihapus
    text = re.sub('rt',' ',text) # hapus retweet
    text = re.sub(r'(.)\1{2,}', r'\1', text) # hapus hruf berulang
    text = slang_replace(text) # hapus slang
    text = text.strip() # hapus spasi awal dan akhir

    return text

def display_result_card(probabilities):
    pred_label = label_mapping[probabilities]
    pred_color = warna_mapping[pred_label]
    pred_emoji = emoji_mapping[pred_label]

    st.markdown(f"""
        <div class="prediction-card">
            <p class="result-emoji">{pred_emoji}</p>
            <p class="prediction-text">Sentimen yang terdeteksi adalah</p>
            <p class="prediction-label" style="color: {pred_color};">{pred_label}</p>
        </div>
    """, unsafe_allow_html=True)


def app():
    st.markdown("""
        <style>
            .title-icon {
                font-size: 2.5rem;
                vertical-align: middle;
            }
            .stTextArea textarea {
                border-radius: 0.75rem;
                border: 2px solid #ced4da;
                padding: 1rem;
                font-size: 1.1rem;
                min-height: 200px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            .result-card {
                background-color: #ffffff;
                border-radius: 1rem;
                padding: 2rem;
                text-align: center;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                margin-top: 2rem;
                border-top: 10px solid;
            }
            
            .result-card.positive { border-top-color: #198754; } /* Green */
            .result-card.negative { border-top-color: #dc3545; } /* Red */
            .result-card.neutral  { border-top-color: #6c757d; } /* Gray */
            
            .prediction-text {
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .confidence-text {
                font-size: 1.2rem;
                color: #6c757d;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Analisis Sentimen Teks dengan Transformer")
    st.markdown("---")
    st.markdown("### <span class='title-icon'>✍️</span> Masukkan Teks Anda di Bawah", unsafe_allow_html=True)
    st.markdown("Model kami akan menganalisis sentimen dari teks Anda dan mengklasifikasikannya sebagai **SADNESS**, **ANGER**, **HOPE**, **SUPPORT**, atau **DISSAPOINTMERNT**.")

    model = load_model_cached(model_path)

    user_text = st.text_area(
        "Ketik atau tempel teks Anda di sini...",
        placeholder="Contoh: Kenapa peraturan yg dibuat seperti ini?",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("Analisis Sentimen Sekarang"):
        if user_text.strip() != "":
            tokens = tokenizer(
                user_text,
                return_tensors="tf",
                truncation=True,
                padding=True,
                max_length=50
            )

            input = text_preprocessing(user_text)

            encoding = tokenize_function([input])

            preds = model({
                "input_ids": encoding["input_ids"],
                "attention_mask": encoding["attention_mask"]
            })
            pred_class = tf.argmax(preds, axis=1).numpy()[0]
            display_result_card(pred_class)
        else:
            st.error("Harap masukkan teks terlebih dahulu untuk dianalisis.", icon="🚨")


