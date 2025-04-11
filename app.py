import streamlit as st
import openai
import os
import fitz  # PyMuPDF

st.set_page_config("Bot de Tabela de Aço com PDF", layout="wide")
st.title("📐 GPT Extrator de Tabelas de Aço (PDF AutoCAD)")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("📄 Envie o PDF exportado do AutoCAD", type=["pdf"])

def extrair_texto_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        texto_total = "\n".join([page.get_text() for page in doc])
    return texto_total

if uploaded_file:
    texto_extraido = extrair_texto_pdf(uploaded_file)
    st.text_area("🧾 Texto extraído do PDF:", texto_extraido[:3000], height=300)

    if st.button("🔁 Enviar para GPT e gerar tabela"):
        with st.spinner("Formatando com GPT-4..."):
            prompt = f"""
O texto a seguir foi extraído de um PDF técnico de engenharia. Ele contém informações sobre barras de aço, incluindo posição, bitola, quantidade, comprimento e peso.

Sua tarefa é:
1. Identificar e organizar os dados em formato de tabela CSV.
2. Utilizar colunas: POS, BIT, QUANT, COMPR, TOTAL, PESO, UNIT
3. Corrigir espaçamentos ou quebras se necessário.

Texto:
{texto_extraido}
"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você organiza textos técnicos em tabelas estruturadas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            tabela_csv = response.choices[0].message.content
            st.success("✅ Tabela gerada com sucesso!")
            st.code(tabela_csv, language="csv")
            st.download_button("📥 Baixar CSV", data=tabela_csv, file_name="tabela_aco.csv")
