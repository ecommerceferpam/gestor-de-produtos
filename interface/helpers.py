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
        raw = autcom.get_produto(sku)
    except Exception as e:
        st.error(f"Erro ao consultar ERP: {e}")
        return None
    #Filtra campos necessários
    try:
        nome = autcom.filter_nome(raw)
    except Exception as e:
        st.error(f"Erro ao filtrar nome do ERP: {e}")
    try:
        marca = autcom.filter_marca(raw)
    except Exception as e:
        st.error(f"Erro ao filtrar marca do ERP: {e}")
    try:
        ean = autcom.filter_codigo_barra(raw)
    except Exception as e:
        st.error(f"Erro ao filtrar EAN do ERP: {e}")
    try:
        mfg_code = autcom.filter_cod_fab(raw)
    except Exception as e:
        st.error(f"Erro ao filtrar Cód. Fab do ERP: {e}")

    #Busca Magento ------------------------------------
    try:
        raw_mag = magento.get_produto(sku)
    except Exception as e:
        st.error(f"Erro ao consultar Magento: {e}")
        return None
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
            "name":nome_mag or "",
            "brand": marca or "",
            "ean": ean or "",
            "description": description_mag or "",
            "meta_description": metadescription_mag or ""
        }
    }

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
