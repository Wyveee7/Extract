import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO
import openai
import os

# Configurar página
st.set_page_config(page_title="Extrator Inteligente de Tabelas de Aço", layout="wide")
st.title("📐 Extrator de Tabelas de Aço com OpenAI + OCR")

# API Key da OpenAI (escondida)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("📄 Envie o PDF exportado do AutoCAD", type=["pdf"])

# Função para aplicar OCR na primeira página do PDF
def extrair_texto_ocr(pdf_bytes):
    images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
    texto_ocr = pytesseract.image_to_string(images[0], lang="por")
    return texto_ocr

# Função para enviar texto ao GPT e pedir tabela formatada
def formatar_com_gpt(texto):
    prompt = f"""
O texto a seguir foi extraído de um PDF de engenharia com um resumo de aço. Reestruture isso em uma tabela CSV com colunas:
POS, BIT, QUANT, COMPR, TOTAL, PESO, UNIT. 
Apenas retorne a tabela formatada, sem explicações.

Texto:
""" + texto.strip()

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você formata dados técnicos em tabelas CSV."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    return resposta.choices[0].message.content

if uploaded_file:
    st.info("🔍 Processando arquivo...")

    # Tentar OCR na primeira página
    ocr_text = extrair_texto_ocr(uploaded_file.read())
    st.text_area("🧾 Texto extraído via OCR:", ocr_text[:2000], height=200)

    if st.button("🔁 Enviar para GPT e gerar tabela"):
        with st.spinner("Aguarde, formatando com GPT-4..."):
            resposta_gpt = formatar_com_gpt(ocr_text)
            st.success("✅ Tabela formatada com sucesso!")
            st.code(resposta_gpt, language="csv")

            # Opção de download
            st.download_button("📥 Baixar CSV", data=resposta_gpt, file_name="tabela_aco.csv")
