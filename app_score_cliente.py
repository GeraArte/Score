import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from pathlib import Path

# Função de classificação
def classificar(pontuacao):
    if pontuacao >= 85:
        return "A"
    elif 75 <= pontuacao < 85:
        return "B"
    elif 60 <= pontuacao < 75:
        return "C"
    else:
        return "Desclassificado"

st.set_page_config(page_title="Score de Cliente", layout="centered")
st.title("App de Score de Cliente")

st.header("🔹 Etapa 1 - Pré-Qualificação")

formato = st.selectbox("Formato do negócio", ["", "Supermercado e Atacado", "Home Center", "Outros"])
localizacao = st.selectbox("Localização Geográfica", ["", "Até 400km", "De 400km até 800km", "De 900km até 1200km", "Acima de 1200km"])
expansao = st.selectbox("Plano de expansão", ["", "Expansão", "Projeto único", "Outros"])
tamanho = st.selectbox("Tamanho da loja", ["", "Acima de 1800m²", "De 1200m² até 1800m²", "De 800m² até 1200m²", "Até 800m²"])
obra = st.selectbox("Momento da obra", ["", "120 a 80 dias", "60 a 80 dias (questionar diretor)", "180 a 120 dias", "Acima de 180 dias"])
projeto = st.selectbox("Já tem projeto?", ["", "Projeto Gera Arte", "Caderno/Arq.Parceiro", "Caderno", "Corporativo"])

# Verificação obrigatória
if "" in [formato, localizacao, expansao, tamanho, obra, projeto]:
    st.warning("⚠️ Preencha todos os campos da Pré-Qualificação antes de continuar.")
    st.stop()
    
pontuacao_pre = 0
pontuacao_pre += 10 if formato == "Supermercado e Atacado" else 6 if formato == "Home Center" else 0
pontuacao_pre += 30 if localizacao == "Até 400km" else 17.1 if localizacao == "De 400km até 800km" else 21.4 if localizacao == "De 900km até 1200km" else 12.9
pontuacao_pre += 10 if expansao == "Expansão" else 8 if expansao == "Projeto único" else 0
pontuacao_pre += 15 if tamanho == "Acima de 1800m²" else 12 if tamanho == "De 1200m² até 1800m²" else 9 if tamanho == "De 800m² até 1200m²" else 3
pontuacao_pre += 5 if obra in ["120 a 80 dias", "180 a 120 dias", "Acima de 180 dias"] else 0
pontuacao_pre += 30 if projeto == "Projeto Gera Arte" else 24 if projeto == "Caderno/Arq.Parceiro" else 12 if projeto == "Caderno" else 0

categoria_pre = classificar(pontuacao_pre)
st.markdown(f"**Pontuação Pré-Qualificação:** {pontuacao_pre:.1f} ({categoria_pre})")

if categoria_pre == "C":
    st.warning("⚠️ Cliente pode seguir para qualificação somente com **aprovação da diretoria.**")
    aprovado_diretoria = st.checkbox("✅ Aprovado pela diretoria para continuar?")
    if not aprovado_diretoria:
        st.error("❌ Cliente na categoria C na pré-qualificação. É necessário aprovação da diretoria para seguir.")
        st.stop()
else:
    aprovado_diretoria = True

st.header("🔹 Etapa 2 - Qualificação")

concorrencia = st.selectbox("Concorrência", ["","Sem fornecedor ou insatisfeito", "Fornecedor regional mas aberto à mudança", "Satisfeito ou contrato fechado"])
expectativa = st.selectbox("Desejo e Expectativa", ["","Gerar valor, impacto visual, modernização", "Apenas deixar mais bonito", "Foco em menor preço"])
investimento = st.selectbox("Investimento Previsto", ["","Verba definida e compatível", "Verba indefinida mas aceitou ZOPA", "Sem verba ou expectativa incompatível"])
autoridade = st.selectbox("Autoridade de Decisão", ["","Decisão com sócio/dono com bom relacionamento", "Decisão com sócio/dono sem relacionamento", "Decisor indireto com acesso fácil", "Decisor sem influência"])
quantidade = st.selectbox("Quantidade de lojas", ["","5 ou mais", "Entre 3 e 5", "Entre 1 e 2", "1 loja"])
materiais = st.selectbox("Materiais Complementares", ["","Plantas e layout completos", "Apenas layout de equipamentos", "Nenhuma informação"])

if "" in [concorrencia, expectativa, investimento, autoridade, quantidade, materiais]:
    st.warning("⚠️ Preencha todos os campos da Qualificação antes de continuar.")
    st.stop()

pontuacao_qual = 0
pontuacao_qual += 25 if concorrencia == "Sem fornecedor ou insatisfeito" else 15 if concorrencia == "Fornecedor regional mas aberto à mudança" else 0
pontuacao_qual += 20 if expectativa == "Gerar valor, impacto visual, modernização" else 8 if expectativa == "Apenas deixar mais bonito" else 4
pontuacao_qual += 20 if investimento == "Verba definida e compatível" else 16 if investimento == "Verba indefinida mas aceitou ZOPA" else 4
pontuacao_qual += 20 if autoridade == "Decisão com sócio/dono com bom relacionamento" else 16 if autoridade == "Decisão com sócio/dono sem relacionamento" else 12 if autoridade == "Decisor indireto com acesso fácil" else 4
pontuacao_qual += 10 if quantidade == "5 ou mais" else 8 if quantidade == "Entre 3 e 5" else 6 if quantidade == "Entre 1 e 2" else 4
pontuacao_qual += 5 if materiais == "Plantas e layout completos" else 3 if materiais == "Apenas layout de equipamentos" else 1

categoria_qual = classificar(pontuacao_qual)
pontuacao_final = (pontuacao_pre + pontuacao_qual) / 2
categoria_final = classificar(pontuacao_final)

st.success(f"**Score Final:** {pontuacao_final:.1f} - **Categoria {categoria_final}**")

cor_categoria = (0, 150, 0) if categoria_final == "A" else (255, 165, 0) if categoria_final == "B" else (200, 0, 0)

img = Image.new('RGB', (1000, 1400), color=(255, 255, 255))
d = ImageDraw.Draw(img)

font_path = Path("fonts/DejaVuSans.ttf")
try:
    fonte_titulo = ImageFont.truetype(str(font_path), 24)
    fonte = ImageFont.truetype(str(font_path), 18)
except:
    fonte_titulo = ImageFont.load_default()
    fonte = ImageFont.load_default()

d.text((50, 30), "Relatório de Score do Cliente", fill=(0, 0, 0), font=fonte_titulo)
d.text((50, 100), "🔹 Pré-Qualificação", fill=(0, 0, 0), font=fonte)
texto_pre = f"""Formato do negócio: {formato}
Localização: {localizacao}
Plano de expansão: {expansao}
Tamanho da loja: {tamanho}
Momento da obra: {obra}
Já tem projeto: {projeto}
Pontuação Pré-Qualificação: {pontuacao_pre} ({categoria_pre})
Aprovação da Diretoria: {"Sim" if categoria_pre == "C" else "Não se aplica"}"""
d.multiline_text((70, 130), texto_pre, fill=(0, 0, 0), font=fonte, spacing=5)

d.text((50, 400), "🔹 Qualificação", fill=(0, 0, 0), font=fonte)
texto_qual = f"""Concorrência: {concorrencia}
Desejo e Expectativa: {expectativa}
Investimento Previsto: {investimento}
Autoridade de Decisão: {autoridade}
Quantidade de lojas: {quantidade}
Materiais Complementares: {materiais}
Pontuação Qualificação: {pontuacao_qual} ({categoria_qual})"""
d.multiline_text((70, 430), texto_qual, fill=(0, 0, 0), font=fonte, spacing=5)

d.rectangle([50, 700, 950, 770], fill=(230, 230, 230), outline=(0, 0, 0))
d.text((60, 710), "🔸 Resultado Final", fill=(0, 0, 0), font=fonte)
d.text((80, 740), f"Pontuação Final: {pontuacao_final}", fill=(0, 0, 0), font=fonte)
d.text((500, 740), f"Categoria Final: {categoria_final}", fill=cor_categoria, font=fonte_titulo)

buf = io.BytesIO()
img.save(buf, format="PNG")

st.download_button("📥 Baixar PNG", data=buf.getvalue(), file_name="relatorio_score_cliente.png", mime="image/png")
