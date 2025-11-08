import copy
import streamlit as st


def init_state(DEFAULT_PRODUCT):
    if "product" not in st.session_state or not isinstance(st.session_state.product, dict):
        st.session_state.product = copy.deepcopy(DEFAULT_PRODUCT)
    else:
        # Garante que chaves novas do DEFAULT apareçam sem perder o que já existe
        deep_merge(st.session_state.product, copy.deepcopy(DEFAULT_PRODUCT), prefer_left=True)
def deep_merge(left: dict, right: dict, prefer_left: bool = False) -> dict:
    """
    Mescla 'right' em 'left' (in-place). Para chaves que são dict, faz merge recursivo.
    Para valores escalares, mantém 'left' se prefer_left=True; caso contrário sobrescreve com 'right'.
    Retorna 'left'.
    """
    for k, v in right.items():
        if isinstance(v, dict) and isinstance(left.get(k), dict):
            deep_merge(left[k], v, prefer_left=prefer_left)
        else:
            if prefer_left and k in left and left[k] not in (None, ""):
                continue
            if v is not None:
                left[k] = v
    return left
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)