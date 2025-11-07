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
    "mfg_code": "",          # padronize este nome na UI
    "magento": {
        "name":"",
        "brand":"",
        "ean":"",
        "description": "",
        "meta_description": "",
        "package_content":"Esse não é para apagar"
    },
    "erp": {
        "description": "",
        "price": 0.0,
        "stock": 0,
        "status": "Disabled",
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
        tabs = st.tabs(["🛒 Magento", "📦 ERP", "🚀 MELI"])

        # -------- Magento TAB (apenas Descrição e Meta-Descrição + botões solicitados) --------
        with tabs[0]:
            mag_data = product.get("magento", {}) if product else {}
            with st.form("magento_form"):
                # descricao = st.text_area("Descrição", value=mag_data.get("description", ""), height=180, key="magento_desc")
                # meta_descricao = st.text_area("Meta-Descrição", value=mag_data.get("meta_description", ""), height=100, key="magento_meta")

                # col_a, col_b = st.columns([1, 1])
                # gemini_clicked = col_a.form_submit_button("Gerar com Gemini")
                # salvar_clicked = col_a.form_submit_button("Salvar no Magento")

                # if salvar_clicked:
                #     ok = try_salvar_no_magento(product["sku"], descricao, meta_descricao)
                #     if ok:
                #         product["magento"] = {"description": descricao, "meta_description": meta_descricao}
                #         st.success("Descrição atualizada no Magento.")
                # if gemini_clicked:
                #     novo_texto = try_gerar_com_gemini(product["sku"], descricao)
                #     if novo_texto:
                #         # Atualiza apenas no UI; usuário decide salvar
                #         product.setdefault("magento", {})
                #         product["magento"]["description"] = novo_texto
                #         st.experimental_rerun()
                    # Linha 1 — Nome | Status (toggle Ativo/Inativo)
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    nome = st.text_input("Nome", value=mag_data.get("name", ""), key="mag_nome")
                with c2:
                    status = st.toggle("Status", value=bool(product.get("active", True)), key="mag_status")
                    st.caption("Ativo" if status else "Inativo")

                # Descrição
                descricao = st.text_area(
                    "Descrição",
                    value=mag_data.get("description", ""),
                    height=480,
                    key="magento_desc",
                )

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
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    gemini_clicked = st.form_submit_button("Gerar com Gemini")
                with col_b:
                    salvar_clicked = st.form_submit_button("Salvar no Magento")

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
                meta_descricao = st.text_area(
                    "Meta-Descrição",
                    value=mag_data.get("meta_description", ""),
                    height=100,
                    key="meli_meta",
                )

                # ----- EDITOR TINYMCE (Descrição) + botões "Buscar" (GET) e "Enviar" (POST) -----
                # Conteúdo inicial do editor = descrição vinda do Magento (ou última editada)
                if "tiny_html" not in st.session_state:
                    st.session_state.tiny_html = mag_data.get("description", "") or "<p>Comece a editar…</p>"

                # Render do editor + botões (tudo no mesmo iframe p/ poder acessar tinymce.activeEditor)
                import streamlit.components.v1 as components
                editor_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <script src="https://cdn.tiny.cloud/1/{settings.TINY_API_KEY}/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
            <style>
            body {{ font-family: Arial, Helvetica, sans-serif; }}
            .row {{ display:flex; gap:8px; margin:12px 0; }}
            .btn {{
                background:#004ac2; color:#fff; border:none; padding:10px 14px; border-radius:8px;
                cursor:pointer; font-weight:600;
            }}
            .btn.secondary {{ background:#4287f5; }}
            .msg {{ margin-top:8px; font-size:13px; }}
            .input-inline input {{
                width: 280px; padding:8px 10px; border:1px solid #E5E7EB; border-radius:8px; margin-right:8px;
            }}
            </style>
        </head>
        <body>
            <!-- Campo editor -->
            <textarea id="editor">{st.session_state.tiny_html}</textarea>

            <!-- Barra de ações (dentro do mesmo iframe) -->
            <div class="row">
            <div class="input-inline">
                <input id="skuField" placeholder="SKU (opcional)" value="{product.get("sku","")}"/>
            </div>
            <button class="btn" onclick="buscarHtmlExterno()">🔎 Buscar HTML externo</button>
            <button class="btn secondary" onclick="enviarHtml()">📤 Enviar HTML para API</button>
            </div>
            <div id="status" class="msg"></div>

            <script>
            const API_GET_URL  = "";
            const API_POST_URL = "";

            tinymce.init({{
                selector: '#editor',
                height: 420,
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
            }});

            function setStatus(msg, ok=true) {{
                const el = document.getElementById('status');
                el.textContent = msg;
                el.style.color = ok ? '#0f766e' : '#b91c1c';
            }}

            async function buscarHtmlExterno() {{
                try {{
                const sku = document.getElementById('skuField').value || '';
                const url = sku ? (API_GET_URL + encodeURIComponent(sku)) : API_GET_URL;

                setStatus('Buscando conteúdo…');
                const res = await fetch(url, {{ method: 'GET' }});
                if (!res.ok) throw new Error('GET falhou: ' + res.status);
                const contentType = res.headers.get('content-type') || '';
                let html = '';
                if (contentType.includes('application/json')) {{
                    const data = await res.json();
                    // tenta campos comuns
                    html = data.html || data.descricao || data.description || '';
                }} else {{
                    html = await res.text();
                }}
                if (!html) throw new Error('Resposta sem HTML');
                tinymce.activeEditor.setContent(html);
                setStatus('Conteúdo inserido no editor ✔');
                }} catch (e) {{
                console.error(e);
                setStatus('Erro ao buscar HTML: ' + e.message, false);
                }}
            }}

            async function enviarHtml() {{
                try {{
                const sku = document.getElementById('skuField').value || '';
                const html = tinymce.activeEditor.getContent();

                setStatus('Enviando conteúdo…');
                const res = await fetch(API_POST_URL, {{
                    method: 'POST',
                    headers: {{
                    'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ sku, html }})
                }});
                if (!res.ok) throw new Error('POST falhou: ' + res.status);
                setStatus('HTML enviado com sucesso ✔');
                }} catch (e) {{
                console.error(e);
                setStatus('Erro ao enviar HTML: ' + e.message, false);
                }}
            }}
            </script>
        </body>
        </html>
        """
                components.html(editor_html, height=560, scrolling=True)

                # Botão de submit do form (apenas para meta-descrição aqui no backend)
                # A descrição (HTML) fica no TinyMCE; salve-a no Magento via seu endpoint JS (Enviar HTML) acima.
                col_inline = st.container()
                with col_inline:
                    st.write("")  # apenas para espaçar um pouco
                salvar_clicked = st.form_submit_button("Salvar Meta-Descrição no Magento")
                if salvar_clicked:
                    # Se você também quiser salvar a meta_descrição no mesmo endpoint do Magento:
                    # try_salvar_no_magento(product["sku"], descricao_html, meta_descricao)
                    st.toast("Meta-Descrição pronta para envio (implemente a chamada no seu módulo).", icon="🧩")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Carregue um SKU para começar.")
