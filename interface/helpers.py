from typing import Dict, Any, Optional
from modules import magento, autcom, ferramentas
import streamlit as st

# ---------------------- Helpers ----------------------
def buscar_produto(sku: str) -> Optional[Dict[str, Any]]:
    if not sku:
        return None
    #Busca produto no ERP
    sku = ferramentas.padronizar_sku(sku)

    #Busca ERP ----------------------------------------
    
    try:
        raw_erp = autcom.get_produto(sku)
    except Exception as e:
        st.error(f"Erro ao consultar ERP: {e}")
        return None
    
    if not raw_erp or (isinstance(raw_erp, dict) and raw_erp.get("erro")):
        msg = ""
        if isinstance(raw_erp, dict) and raw_erp.get("erro"):
            msg = f"ERP: {raw_erp["erro"]}"
        else:
            msg = "Produto não encontrado no ERP."

        st.toast(msg, icon="❌")

        return {
            "exists":False
        }
    
    
    try:
        nome = autcom.filter_nome(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar nome do ERP: {e}")
        nome = ""
    try:
        marca = autcom.filter_marca(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar marca do ERP: {e}")
        marca = ""
    try:
        ean = autcom.filter_codigo_barra(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar EAN do ERP: {e}")
        ean = ""
    try:
        mfg_code = autcom.filter_cod_fab(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Cód. Fab do ERP: {e}")
        mfg_code =""

    try:
        nome_aba14 = autcom.filter_nome_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Nome do ERP: {e}")
        nome_aba14 = ""

    try:
        aplicacao_aba14 = autcom.filter_aplicacao_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Aplicação do ERP: {e}")
        aplicacao_aba14 = ""

    try:
        descricao_aba14 = autcom.filter_descricao_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Descrição do ERP: {e}")
        descricao_aba14 = ""

    try:
        dados_tecnicos_aba14 = autcom.filter_dados_tecnicos_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Dados Técnicos do ERP: {e}")
        dados_tecnicos_aba14 = ""

    try:
        itens_inclusos_aba14 = autcom.filter_itens_inclusos_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Itens Inclusos do ERP: {e}")
        itens_inclusos_aba14 = ""

    try:
        altura_aba14 = autcom.filter_altura_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Altura do ERP: {e}")
        altura_aba14 = ""

    try:
        largura_aba14 = autcom.filter_largura_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Largura do ERP: {e}")
        largura_aba14 = ""

    try:
        profundidade_aba14 = autcom.filter_profundidade_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Profundidade do ERP: {e}")
        profundidade_aba14 = ""

    try:
        peso_aba14 = autcom.filter_peso_aba14(raw_erp)
    except Exception as e:
        st.error(f"Erro ao filtrar Peso do ERP: {e}")
        peso_aba14 = ""


    #Busca Magento ------------------------------------
    try:
        raw_mag = magento.get_produto(sku)
    except Exception as e:
        st.error(f"Erro ao consultar Magento: {e}")
        return None
    

    if not raw_mag or (isinstance(raw_mag, dict) and raw_mag.get("erro")):
        msg = ""
        if isinstance(raw_mag, dict) and raw_mag.get("erro"):
            msg = f"Magento: {raw_mag["erro"]}"
        else:
            msg = "Produto não encontrado no Magento."

        st.toast(msg, icon="❌")

        return {
            "sku": sku,
            "name": nome or "",
            "brand": marca or "",
            "ean": ean or "",
            "mfg_code": mfg_code or "",
            "magento": {
                "exists":False,
                "name": "",
                "brand": "",
                "ean": "",
                "description": "",
                "meta_description": "",
            }
        }
    
    nome_mag = ""
    description_mag = ""
    metadescription_mag = ""

    try:
        nome_mag = magento.filter_nome(raw_mag)
    except Exception as e:
        st.error(f"Erro ao filtrar nome do Magento: {e}")
    try:
        description_mag = magento.filter_descricao(raw_mag)
    except Exception as e:
        st.error(f"Erro ao filtrar descrição do Magento: {e}")
    try:
        metadescription_mag = magento.filter_metaDescription(raw_mag)
    except Exception as e:
        st.error(f"Erro ao filtrar Metadescrição do Magento: {e}")
    

    return{
        "sku": sku,
        "name": nome or "",
        "brand": marca or "",
        "ean": ean or "",
        "mfg_code": mfg_code or "",
        "magento": {
            "exists": True,
            "name":nome_mag or "",
            "brand": marca or "",
            "ean": ean or "",
            "description": description_mag or "",
            "meta_description": metadescription_mag or ""
        },
        "erp_aba_ecom": {
            "nome": nome_aba14 or "",
            "aplicacao": aplicacao_aba14 or "",
            "descricao": descricao_aba14 or "",
            "dados_tecnicos": dados_tecnicos_aba14 or "",
            "itens_inclusos": itens_inclusos_aba14 or "",
            "altura": altura_aba14 or "",
            "largura": largura_aba14 or "",
            "profundidade": profundidade_aba14 or "",
            "peso": peso_aba14 or "",
        }
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
