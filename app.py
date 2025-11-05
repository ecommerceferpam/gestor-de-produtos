# app.py
import time
from typing import Dict, Any, Optional
import streamlit as st

# >>> CONEXÃO COM O MAGENTO
from modules import magento  # magento.get_produto(sku) retorna JSON e existem os filters citados

st.set_page_config(page_title="Product Editor", layout="wide")

# ------- CSS (tema claro fiel) -------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
:root{
  --bg: #F5F7FB; --card: #FFFFFF; --border: #E5E7EB; --text: #0F172A; --muted: #6B7280;
  --brand: #004ac2; --brand-600:#4287f5; --sidebar:#111827; --sidebar-text:#E5E7EB; --sidebar-active:#1F2937;
}
html, body, .stApp { background: var(--bg) !important; color: var(--text) !important; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }
[data-testid="stSidebar"]{ background: var(--sidebar) !important; color: var(--sidebar-text) !important; border-right: 1px solid #0B1220; }
[data-testid="stSidebar"] * { color: var(--sidebar-text) !important; }
[data-testid="stSidebar"] .stButton>button{ background: var(--sidebar-active) !important; color: #fff !important; border: 1px solid #00000033; }
header[data-testid="stHeader"]{ background: #fff !important; border-bottom: 1px solid var(--border); }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
.section { border: 1px solid var(--border); border-radius: 12px; padding: 16px; background: var(--card); }
.section + .section { margin-top: 16px; }
.section-title { font-weight: 600; color: var(--text); margin-bottom: 8px; }
.subtle { color: var(--muted); font-size: 0.875rem; }
textarea, .stTextInput>div>div>input, .stNumberInput input, .stSelectbox div[data-baseweb="select"]{
  border-radius: 10px !important; border: 1px solid var(--border) !important; background: #fff !important; color:#000 !important;
}
.stTextInput:focus-within input, .stNumberInput:focus-within input, .stSelectbox:focus-within div[data-baseweb="select"], textarea:focus{
  outline: none !important; border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(91,91,214,.15) !important;
}
.stButton>button{ background: var(--brand) !important; color: #fff !important; border: 1px solid var(--brand) !important; border-radius: 10px; font-weight: 600; }
.stButton>button:hover{ background: var(--brand-600) !important; border-color: var(--brand-600) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 16px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"]{ padding: 8px 14px; border-radius: 10px 10px 0 0; background: #F8FAFC; color:#1F2937; }
.stTabs [data-baseweb="tab"][aria-selected="true"]{ background: #fff; color: var(--text); box-shadow: inset 0 -2px 0 0 var(--brand); }
.stAlert { border-radius: 12px; }
            
.stFormSubmitButton>button{ background: var(--brand) !important; color: #fff !important; border: 1px solid var(--brand) !important; border-radius: 10px; font-weight: 600; }

            .st-emotion-cache-qcpnpn{padding:0px !important; color: #000 !important;}
            .st-emotion-cache-1weic72{color:#000 !important;}
</style>
""", unsafe_allow_html=True)

# ---------------------- Helpers ----------------------
def load_from_magento(sku: str) -> Optional[Dict[str, Any]]:
    """
    Busca no Magento e aplica filtros para campos principais.
    magento.get_produto(sku) -> JSON
    magento.filter_nome(json) -> str
    magento.filter_marca(json) -> str
    magento.filter_descricao(json) -> str
    magento.filter_ean(json) -> str
    """
    if not sku:
        return None
    try:
        raw = magento.get_produto(sku)
    except Exception as e:
        st.error(f"Erro ao consultar Magento: {e}")
        return None

    # Aplica filtros solicitados
    try:
        name = getattr(magento, "filter_nome")(raw)
    except Exception:
        name = ""
    try:
        brand = getattr(magento, "filter_marca")(raw)
    except Exception:
        brand = ""
    try:
        descricao = getattr(magento, "filter_descricao")(raw)
    except Exception:
        descricao = ""
    try:
        ean = getattr(magento, "filter_ean")(raw)
    except Exception:
        ean = ""
    try:
        meta_desc = getattr(magento, "filter_metaDescription")(raw)
    except Exception:
        meta_desc = ""


    return {
        "sku": sku,
        "name": name or "",
        "brand": brand or "",
        "ean": ean or "",
        "magento": {
            "description": descricao or "",
            "meta_description": meta_desc or "",
        },
        # Mantemos ERP/MELI intactos por enquanto
        "erp": {},
        "meli": {},
    }

def try_salvar_no_magento(sku: str, descricao: str, meta_descricao: str) -> bool:
    """
    Placeholder de salvamento. Se você tiver um método oficial (ex.: magento.update_produto),
    troque aqui para a chamada real.
    """
    try:
        if hasattr(magento, "salvar_descricao"):
            magento.salvar_descricao(sku, descricao, meta_descricao)
            return True
        # Fallback: se não existir, apenas sinaliza que precisa implementar
        st.info("Implemente `magento.salvar_descricao(sku, descricao, meta_descricao)` no módulo.")
        return False
    except Exception as e:
        st.error(f"Erro ao salvar no Magento: {e}")
        return False

def try_gerar_com_gemini(sku: str, descricao_atual: str) -> str:
    """
    Placeholder para geração com Gemini. Substitua por sua integração real.
    """
    # Exemplo simples: devolve um texto simulado a partir do SKU
    return f"[Gemini] Descrição otimizada para SKU {sku} baseada no conteúdo atual."

# ---------------------- Estado ----------------------
if "product" not in st.session_state:
    st.session_state.product = None

# ---------------------- Sidebar ----------------------
st.sidebar.header("Painel")
nav = st.sidebar.radio("Menu", ["Product Editor", "Logs / Insights"], index=0)
st.sidebar.markdown("---")
# st.sidebar.button("Logout")

if nav == "Logs / Insights":
    st.title("Logs / Insights")
    st.info("Espaço reservado para auditoria e métricas.")
    st.stop()

# ---------------------- Topo ----------------------
st.title("Editor de Produtos")

# ---------------------- Buscar por SKU ----------------------
with st.container():
    st.markdown('<div class="section-title">Busque um produto por SKU</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 1.3])
    with c1:
        sku_input = st.text_input("SKU", key="sku_input", label_visibility="collapsed", placeholder="Digite o SKU no formato 7 dígitos…")
    with c2:
        if st.button("Buscar", use_container_width=True):
            data = load_from_magento(sku_input.strip())
            if data:
                st.session_state.product = data
                st.toast(f"Produto '{data['sku']}' carregado do Magento.")
            else:
                st.toast("SKU inválido ou não encontrado.")

product = st.session_state.product

# ---------------------- Header Card ----------------------
if product:
    st.subheader(product.get("name") or "—")
    st.caption(product.get("sku") or "")

    # ---------------------- Main Informations ----------------------
    st.markdown('<div class="section-title">Dados Gerais</div>', unsafe_allow_html=True)

    with st.form("main_info"):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            name = st.text_input("Nome", value=product.get("name", ""))
        with col2:
            brand = st.text_input("Marca", value=product.get("brand", ""))
        with col3:
            ean = st.text_input("EAN", value=product.get("ean", ""))

        # Mantive "Cod. Fab." se você usa; senão remova
        mfg_code = st.text_input("Código de Fáb.", value=product.get("mfg_code", ""))

        submitted = st.form_submit_button("Salvar Dados Gerais (Localmente)")
        if submitted:
            product.update({
                "name": name,
                "brand": brand,
                "ean": ean,
                "mfg_code": mfg_code
            })
            st.success("Informações principais salvas localmente.")

    # ---------------------- Tabs ----------------------
    tabs = st.tabs(["🛒 Magento", "📦 ERP", "🚀 MELI"])

    # -------- Magento TAB (apenas Descrição e Meta-Descrição + botões solicitados) --------
    with tabs[0]:
        mag_data = product.get("magento", {}) if product else {}
        with st.form("magento_form"):
            descricao = st.text_area("Descrição", value=mag_data.get("description", ""), height=180, key="magento_desc")
            meta_descricao = st.text_area("Meta-Descrição", value=mag_data.get("meta_description", ""), height=100, key="magento_meta")

            col_a, col_b = st.columns([1, 1])
            gemini_clicked = col_a.form_submit_button("Gerar com Gemini")
            salvar_clicked = col_a.form_submit_button("Salvar no Magento")

            if salvar_clicked:
                ok = try_salvar_no_magento(product["sku"], descricao, meta_descricao)
                if ok:
                    product["magento"] = {"description": descricao, "meta_description": meta_descricao}
                    st.success("Descrição atualizada no Magento.")
            if gemini_clicked:
                novo_texto = try_gerar_com_gemini(product["sku"], descricao)
                if novo_texto:
                    # Atualiza apenas no UI; usuário decide salvar
                    product.setdefault("magento", {})
                    product["magento"]["description"] = novo_texto
                    st.experimental_rerun()

    # -------- ERP TAB (mantido) --------
    with tabs[1]:
        erp = product.get("erp", {})
        with st.form("erp_form"):
            desc = st.text_area("Description", value=erp.get("description", ""), height=140)
            c1, c2, c3 = st.columns(3)
            with c1:
                price = st.number_input("Price", value=float(erp.get("price") or 0.0), step=0.01, min_value=0.0)
            with c2:
                stock = st.number_input("Stock", value=int(erp.get("stock") or 0), step=1, min_value=0)
            with c3:
                status = st.selectbox("Status", ["Active", "Disabled"], index=0 if erp.get("status")=="Active" else 1)
            if st.form_submit_button("Save ERP"):
                product["erp"] = {"description": desc, "price": float(price), "stock": int(stock), "status": status}
                st.success("ERP atualizado (local).")

    # -------- MELI TAB (mantido) --------
    with tabs[2]:
        meli = product.get("meli", {})
        with st.form("meli_form"):
            desc = st.text_area("Description", value=meli.get("description", ""), height=140)
            c1, c2, c3 = st.columns(3)
            with c1:
                price = st.number_input("Price", value=float(meli.get("price") or 0.0), step=0.01, min_value=0.0)
            with c2:
                stock = st.number_input("Stock", value=int(meli.get("stock") or 0), step=1, min_value=0)
            with c3:
                status = st.selectbox("Status", ["Active", "Disabled"], index=0 if meli.get("status")=="Active" else 1)
            if st.form_submit_button("Save MELI"):
                product["meli"] = {"description": desc, "price": float(price), "stock": int(stock), "status": status}
                st.success("MELI atualizado (local).")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Carregue um SKU para começar.")
