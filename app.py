# app.py
import copy
import streamlit as st
import interface
import streamlit.components.v1 as components
from config import settings

from modules import magento, autcom, ferramentas

DEFAULT_PRODUCT = {
    "sku": "",
    "name": "",
    "brand": "",
    "ean": "",
    "mfg_code": "",
    "magento": {
        "name":"",
        "brand":"",
        "ean":"",
        "description": "",
        "meta_description": "",
        "package_content":""
    },
    "erp_aba_ecom": {
        "nome": "",
        "aplicacao": "",
        "descricao": "",
        "dados_tecnicos": "",
        "itens_inclusos": "",
        "altura": "",
        "largura": "",
        "profundidade": "",
        "peso": "",
    },
    "meli": {
        "description": "",
        "price": 0.0,
        "stock": 0,
        "status": "Disabled",
    },
}

st.set_page_config(page_title="Gestor de Produtos", layout="wide")
interface.init(DEFAULT_PRODUCT)
interface.load_css(".streamlit/style.css")
# # ---------------------- Estado ----------------------
# if "product" not in st.session_state:
#     st.session_state.product = None

# ---------------------- Sidebar ----------------------
st.sidebar.header("Painel")
nav = st.sidebar.radio("Menu", ["Product Editor", "Logs / Insights"], index=0)
st.sidebar.markdown("---")
# st.sidebar.button("Logout")

if nav == "Logs / Insights":
    st.title("Logs / Insights")
    st.info("Espaço reservado para auditoria e métricas.")
    st.stop()


left, main, right = st.columns([1, 3, 1])

with main:
    st.title("Editor de Produtos")
    # ---------------------- Buscar por SKU ----------------------
    with st.container():
        c1, c2 = st.columns([6, 1.3])
        with c1:
            sku_input = st.text_input("SKU", key="sku_input", label_visibility="collapsed", placeholder="Digite o SKU no formato 7 dígitos…")
        with c2:
            if st.button("Editar", use_container_width=True):
                data = interface.buscar_produto(sku_input.strip())
                if data:
                    # Começa do DEFAULT para garantir todas as chaves
                    new_product = copy.deepcopy(DEFAULT_PRODUCT)
                    # Mescla o que veio do Magento
                    interface.deep_merge(new_product, data)
                    # Mantém valores locais que você não quer perder? (opcional)
                    # deep_merge(new_product, st.session_state.product, prefer_left=False)
                    st.session_state.product = new_product
                else:
                    st.toast("SKU inválido ou não encontrado.")

    product = st.session_state.product

    # ---------------------- Header Card ----------------------
    if product.get("name"):


        # Linha 1: Nome
        st.subheader("Nome")
        st.write(product.get("name", ""))


        # Linha 2: Marca | EAN | Cód. Fabricante
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Marca")
            st.write(product.get("brand", ""))

        with col2:
            st.subheader("EAN")
            st.write(product.get("ean", ""))

        with col3:
            st.subheader("Cód. Fabricante")
            st.write(product.get("mfg_code", ""))

        st.divider()



        # ---------------------- Tabs ----------------------
        tabs = st.tabs(["🛒 Magento", "📦 ERP (Aba 14)", "🚀 MELI"])

        # -------- Magento TAB (apenas Descrição e Meta-Descrição + botões solicitados) --------
        with tabs[0]:
            mag_data = product.get("magento", {}) if product else {}
            with st.form("magento_form"):
                
                disable_mag = False
                if(mag_data.get("exists")==False):
                    st.error("Produto não encontrado no Magento. Realize a liberação no painel para poder editá-lo.")
                    disable_mag = True
                else:
                    nome = st.text_input("Nome", value=mag_data.get("name", ""), key="mag_nome")

                    st.session_state.tiny_html = mag_data.get("description", "") or ""
                    tiny_value = st.session_state.get("tiny_value", "")

                    editor_html = f"""
                    <!DOCTYPE html>
                    <html lang="pt-BR">
                    <head>
                        <meta charset="utf-8"/>
                        <script src="https://cdn.tiny.cloud/1/{settings.TINY_API_KEY}/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
                        <script src="https://cdn.jsdelivr.net/npm/tinymce-i18n/langs/pt_BR.js"></script>
                        <style>
                            body{{margin:0;}}
                        </style>
                    </head>
                    <body>
                        <!-- Campo editor -->
                        <textarea id="editor">{st.session_state.tiny_html}</textarea>

                        <script>
                        tinymce.init({{
                            selector: '#editor',
                            readonly: false,
                            height: 560,
                            plugins: [
                            'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                            'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                            'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
                            ],
                            toolbar:
                            'undo redo | bold italic underline | forecolor backcolor | ' +
                            'alignleft aligncenter alignright alignjustify | ' +
                            'bullist numlist outdent indent | table | link image media | code preview',
                            menubar: 'file edit view insert format tools table help',
                            promotion: false,
                            branding: false,
                            automatic_uploads: true,
                            content_style: 'body {{ font-family:Arial,Helvetica,sans-serif; font-size:16px }}',
                            language: "pt_BR",
                            language_url: "https://cdn.jsdelivr.net/npm/tinymce-i18n/langs/pt_BR.js",

                            // 🚨 IMPORTANTE: quando o conteúdo mudar, envia para o Streamlit
                            setup: function(editor) {{
                                editor.on('keyup change input', function() {{
                                    const html = editor.getContent();
                                    window.parent.postMessage({{ tiny_value: html }}, "*");
                                }});
                            }}
                        }});
                        </script>
                    </body>
                    </html>
                    """  
                    components.html(editor_html, height=560, scrolling=True)
                    components.html("""
                    <script>
                    window.addEventListener("message", (event) => {
                        if (event.data.tiny_value !== undefined) {
                            const streamlitMsg = {
                                type: "streamlit:setComponentValue",
                                value: event.data.tiny_value
                            };
                            window.parent.postMessage(streamlitMsg, "*");
                        }
                    });
                    </script>
                    """)

                    # Meta-descrição
                    meta_descricao = st.text_area(
                        "Meta-Descrição",
                        value=mag_data.get("meta_description", ""),
                        height=120,
                        key="magento_meta", 
                
                    )

                    # Conteúdo da embalagem
                    conteudo_embalagem = st.text_area(
                        "Conteúdo da Embalagem",
                        value=mag_data.get("package_content", ""),
                        height=70,
                        key="mag_conteudo_embalagem",
                
                    )

                    # Linha 2 — Peso | Largura | Altura | Comprimento
                    ca, cb, cc, cd = st.columns(4)
                    with ca:
                        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.01, value=float(mag_data.get("weight", 0.0)), key="mag_peso")
                    with cb:
                        largura = st.number_input("Largura (cm)", min_value=0.0, step=0.1, value=float(mag_data.get("width", 0.0)), key="mag_largura")
                    with cc:
                        altura = st.number_input("Altura (cm)", min_value=0.0, step=0.1, value=float(mag_data.get("height", 0.0)), key="mag_altura")
                    with cd:
                        comprimento = st.number_input("Comprimento (cm)", min_value=0.0, step=0.1, value=float(mag_data.get("length", 0.0)), key="mag_comprimento")

                    # Linha 3 — Google Merchant | Preço Boleto no Feed (toggles)
                    t1, t2 = st.columns(2)
                    with t1:
                        google_merchant = st.toggle("Google Merchant", value=bool(mag_data.get("google_merchant", False)), key="mag_google_merchant")
                    with t2:
                        preco_boleto_feed = st.toggle("Preço Boleto no Feed", value=bool(mag_data.get("preco_boleto_feed", False)), key="mag_preco_boleto_feed")

                    st.divider()

                # Ações
                col_a, col_b= st.columns([1, 1])
                with col_a:
                    gemini_clicked = st.form_submit_button("Gerar com Gemini", disabled=disable_mag)
                with col_b:
                    salvar_clicked = st.form_submit_button("Salvar no Magento", disabled=disable_mag)

                if salvar_clicked:
                    html_do_editor = st.session_state.get("tiny_value", "")
                    st.write("HTML capturado do TinyMCE:", html_do_editor)

        # -------- ERP TAB (mantido) --------
        with tabs[1]:
            erp_data = product.get("erp_aba_ecom", {}) if product else {}
            with st.form("erp_form"):
                nome_aba14 = st.text_input("Nome", value=erp_data.get("nome", ""))
                aplicacao_aba14 = st.text_area("Aplicação", value=erp_data.get("aplicacao", ""), height=140)
                descricao_aba14 = st.text_area("Descricão do Produto", value=erp_data.get("descricao", ""), height=240)
                dados_tecnicos_aba14 = st.text_area("Dados Técnicos", value=erp_data.get("dados_tecnicos", ""), height=120)
                itens_inclusos_14 = st.text_area("Itens Inclusos", value=erp_data.get("itens_inclusos", ""), height=120)
                

                c1, c2, c3, c4 = st.columns([1,1,1,1])
                with c1:
                    altura_aba14 = st.number_input("Altura", value=float(erp_data.get("altura") or 0.0), step=0.01, min_value=0.0)
                with c2:
                    largura_aba14 = st.number_input("Largura", value=float(erp_data.get("largura") or 0.0), step=0.01, min_value=0.0)
                with c3:
                    profundidade_aba14 = st.number_input("Profundidade", value=float(erp_data.get("profundidade") or 0.0), step=0.01, min_value=0.0)
                with c4:
                    peso_aba14 = st.number_input("Peso", value=float(erp_data.get("peso") or 0.0), step=0.01, min_value=0.0)

                if st.form_submit_button("Save ERP"):
                    # product["erp"] = {"description": desc, "price": float(price), "stock": int(stock), "status": status}
                    st.success("ERP atualizado (local).")


        with tabs[2]:
            st.warning("Disponível em breve.")
    else:
        st.info("Carregue um SKU para começar.")
