import streamlit as st
import openai
import os

st.set_page_config("Bot de Tabela de Aço", layout="wide")
st.title("📐 GPT Extrator de Tabelas de Aço")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

texto_bruto = st.text_area("📋 Cole aqui o texto extraído do PDF ou OCR:", height=300)

if st.button("🔍 Gerar tabela"):
    if texto_bruto.strip():
        with st.spinner("Enviando para GPT..."):
            prompt = f"""
O texto a seguir foi extraído de um PDF técnico de engenharia. Ele contém informações sobre barras de aço, incluindo posição, bitola, quantidade, comprimento e peso.

Sua tarefa é:
1. Identificar e organizar os dados em formato de tabela CSV.
2. Utilizar colunas: POS, BIT, QUANT, COMPR, TOTAL, PESO, UNIT
3. Corrigir espaçamentos ou quebras se necessário.

Texto:
{texto_bruto}
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
    else:
        st.warning("Cole algum texto primeiro.")
