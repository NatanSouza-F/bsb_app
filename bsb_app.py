"""
BSB Contabilidade — Plataforma de Cadastro Inteligente v2.0
Visual: Dark Premium Navy + Blue Pulse
"""

import streamlit as st
import requests
import re
import time
from datetime import datetime, date
from typing import Dict, Any, Optional

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="BSB Contabilidade | Cadastro",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CSS — DARK PREMIUM + ANIMAÇÃO DE ENTRADA
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ─── RESET & BASE ───────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
* { font-family: 'DM Sans', sans-serif !important; }

/* ─── APP BACKGROUND ────────────────────────────────────────────────── */
.stApp {
    background: #080f1a;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -40%;
    left: -20%;
    width: 80%;
    height: 80%;
    background: radial-gradient(ellipse, rgba(37,99,235,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: breathe 8s ease-in-out infinite;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -30%;
    right: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(6,182,212,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: breathe 10s ease-in-out infinite reverse;
}
@keyframes breathe {
    0%, 100% { transform: scale(1) translate(0,0); opacity: 0.7; }
    50% { transform: scale(1.15) translate(2%, 2%); opacity: 1; }
}

/* ─── BLOCK CONTAINER ───────────────────────────────────────────────── */
.block-container {
    max-width: 600px !important;
    padding: 1.5rem 1.2rem 3rem 1.2rem !important;
    position: relative;
    z-index: 1;
}

/* ─── HERO / SPLASH ─────────────────────────────────────────────────── */
.hero-wrapper {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    animation: fadeSlideDown 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-32px); }
    to   { opacity: 1; transform: translateY(0); }
}
.bsb-wordmark {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.4rem, 7vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 45%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.05;
    filter: drop-shadow(0 0 28px rgba(59,130,246,0.35));
}
.bsb-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #60a5fa;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 8px auto 0 auto;
    width: fit-content;
}
.bsb-badge::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #3b82f6;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.6); }
    50% { box-shadow: 0 0 0 5px rgba(59,130,246,0); }
}
.bsb-slogan {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 400;
    margin-top: 0.5rem;
    letter-spacing: 0.01em;
}

/* ─── STEP INDICATOR ────────────────────────────────────────────────── */
.step-track {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 1.6rem auto 2rem auto;
    width: 100%;
    max-width: 360px;
    animation: fadeIn 0.6s ease both;
    animation-delay: 0.3s;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    flex: 1;
    position: relative;
    z-index: 2;
}
.step-circle {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700;
    font-size: 0.85rem;
    transition: all 0.35s ease;
}
.step-circle.done {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    box-shadow: 0 0 16px rgba(59,130,246,0.45);
}
.step-circle.active {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    box-shadow: 0 0 0 4px rgba(59,130,246,0.2), 0 0 20px rgba(59,130,246,0.5);
    animation: ring-pulse 2s ease-in-out infinite;
}
@keyframes ring-pulse {
    0%, 100% { box-shadow: 0 0 0 4px rgba(59,130,246,0.2), 0 0 20px rgba(59,130,246,0.4); }
    50% { box-shadow: 0 0 0 8px rgba(59,130,246,0.1), 0 0 28px rgba(59,130,246,0.6); }
}
.step-circle.pending {
    background: rgba(30,41,59,0.8);
    color: #475569;
    border: 1px solid #1e293b;
}
.step-label {
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #475569;
    text-align: center;
    white-space: nowrap;
}
.step-label.active { color: #60a5fa; }
.step-connector {
    flex: 1;
    height: 2px;
    background: #1e293b;
    margin-top: -20px;
    position: relative;
    z-index: 1;
    max-width: 40px;
}
.step-connector.done { background: linear-gradient(90deg, #2563eb, #3b82f6); }

/* ─── SECTION CARD ──────────────────────────────────────────────────── */
.section-card {
    background: linear-gradient(145deg, rgba(15,23,42,0.9) 0%, rgba(20,32,54,0.85) 100%);
    border: 1px solid rgba(51,65,85,0.6);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    animation: cardEnter 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes cardEnter {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.card-title .icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(37,99,235,0.25), rgba(6,182,212,0.15));
    border: 1px solid rgba(59,130,246,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}

/* ─── TIPO SELECTOR (CARDS PJ/PF) ──────────────────────────────────── */
.tipo-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin: 1.2rem 0;
}
.tipo-card {
    background: rgba(15,23,42,0.7);
    border: 1.5px solid rgba(51,65,85,0.5);
    border-radius: 16px;
    padding: 1.6rem 1rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.tipo-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(6,182,212,0.06));
    opacity: 0;
    transition: opacity 0.25s ease;
    border-radius: 16px;
}
.tipo-card:hover { border-color: rgba(59,130,246,0.5); transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,0.3); }
.tipo-card:hover::before { opacity: 1; }
.tipo-card .tipo-icon { font-size: 2.2rem; margin-bottom: 0.5rem; display: block; }
.tipo-card .tipo-title {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700;
    font-size: 0.9rem;
    color: #e2e8f0;
    margin-bottom: 0.3rem;
}
.tipo-card .tipo-desc { font-size: 0.72rem; color: #64748b; line-height: 1.4; }

/* ─── LGPD BOX ──────────────────────────────────────────────────────── */
.lgpd-box {
    display: flex;
    gap: 12px;
    background: rgba(37,99,235,0.06);
    border: 1px solid rgba(59,130,246,0.18);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 1.4rem;
    animation: fadeIn 0.8s ease both;
    animation-delay: 0.5s;
}
.lgpd-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 1px; }
.lgpd-text { font-size: 0.8rem; color: #64748b; line-height: 1.55; }
.lgpd-text strong { color: #94a3b8; font-weight: 600; }

/* ─── CNPJ / CEP AUTO-FETCH BADGE ──────────────────────────────────── */
.auto-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #34d399;
    margin-bottom: 6px;
}

/* ─── DIVIDERS ──────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid rgba(51,65,85,0.4);
    margin: 1.2rem 0;
}

/* ─── STREAMLIT OVERRIDES ───────────────────────────────────────────── */
h1, h2, h3 { color: #e2e8f0 !important; font-family: 'Syne', sans-serif !important; }
.stMarkdown p { color: #94a3b8; }

label, .stTextInput label, .stNumberInput label,
.stSelectbox label, .stRadio label, .stCheckbox label,
.stDateInput label, .stTextArea label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

input, textarea, .stNumberInput input,
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(8,15,26,0.8) !important;
    border: 1px solid rgba(51,65,85,0.6) !important;
    color: #f1f5f9 !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus, textarea:focus {
    border-color: rgba(59,130,246,0.7) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    outline: none !important;
}
div[data-baseweb="select"] div[role="option"] {
    background: #0f1a2b !important;
    color: #e2e8f0 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 1.2rem !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(59,130,246,0.35) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(59,130,246,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button[kind="secondary"] {
    background: rgba(15,26,43,0.8) !important;
    border: 1px solid rgba(71,85,105,0.6) !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: rgba(59,130,246,0.5) !important;
    color: #60a5fa !important;
    transform: translateY(-1px) !important;
}

/* Radio */
.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(51,65,85,0.5) !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    color: #94a3b8 !important;
    transition: all 0.2s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: rgba(59,130,246,0.6) !important;
    background: rgba(37,99,235,0.12) !important;
    color: #60a5fa !important;
}

/* Checkbox */
.stCheckbox > label { color: #94a3b8 !important; font-size: 0.85rem !important; }
input[type="checkbox"] { accent-color: #3b82f6 !important; }

/* Select box options */
div[data-baseweb="menu"] { background: #0d1829 !important; border: 1px solid #1e293b !important; }
div[data-baseweb="option"]:hover { background: rgba(37,99,235,0.2) !important; }

/* Success / Info / Error */
.stSuccess { background: rgba(16,185,129,0.1) !important; border: 1px solid rgba(16,185,129,0.25) !important; border-radius: 10px !important; }
.stError { background: rgba(239,68,68,0.1) !important; border: 1px solid rgba(239,68,68,0.25) !important; border-radius: 10px !important; }
.stInfo { background: rgba(59,130,246,0.08) !important; border: 1px solid rgba(59,130,246,0.2) !important; border-radius: 10px !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border: 1px solid rgba(245,158,11,0.25) !important; border-radius: 10px !important; }

/* Upload */
div[data-testid="stFileUploader"] {
    background: rgba(8,15,26,0.6) !important;
    border: 1.5px dashed rgba(51,65,85,0.6) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stFileUploader"]:hover { border-color: rgba(59,130,246,0.5) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080f1a; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3b82f6; }

/* Mobile adjustments */
@media (max-width: 640px) {
    .block-container { padding: 1rem 0.8rem 2rem 0.8rem !important; }
    .section-card { padding: 1.2rem; }
    .tipo-grid { gap: 10px; }
    .tipo-card { padding: 1.2rem 0.7rem; }
    .step-label { font-size: 0.56rem; }
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# INICIALIZAÇÃO DO ESTADO
# =============================================================================
def init_session_state():
    defaults = {
        'step': 0,
        'perfil': None,
        'dados_cadastrais': {},
        'dados_operacionais': {},
        'dados_socio': {},
        'documentos': [],
        'honorario_interno': 0.0,
        'cnpj_consultado': False,
        'cep_consultado': False,
        'submitted': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# =============================================================================
# APIs AUXILIARES
# =============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def consulta_cnpj(cnpj: str) -> Optional[Dict]:
    cnpj_clean = re.sub(r'\D', '', cnpj)
    if len(cnpj_clean) != 14:
        return None
    try:
        resp = requests.get(
            f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}",
            timeout=12,
            headers={"User-Agent": "BSB-Contabilidade/2.0"}
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)
def consulta_cep(cep: str) -> Optional[Dict]:
    cep_clean = re.sub(r'\D', '', cep)
    if len(cep_clean) != 8:
        return None
    try:
        resp = requests.get(
            f"https://brasilapi.com.br/api/cep/v2/{cep_clean}",
            timeout=10,
            headers={"User-Agent": "BSB-Contabilidade/2.0"}
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def consulta_cnae(codigo: str) -> str:
    if not codigo:
        return ""
    codigo_clean = re.sub(r'\D', '', str(codigo))
    try:
        resp = requests.get(
            f"https://brasilapi.com.br/api/cnae/v1/{codigo_clean}",
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get('descricao', 'CNAE não encontrado')
    except Exception:
        return "Descrição não disponível"


@st.cache_data(ttl=3600, show_spinner=False)
def lista_estados() -> list:
    return [
        "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
        "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
        "RS","RO","RR","SC","SP","SE","TO"
    ]


# =============================================================================
# VALIDAÇÕES
# =============================================================================
def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    def calc_digito(cnpj, peso):
        soma = sum(int(cnpj[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    peso1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    peso2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    d1 = calc_digito(cnpj, peso1)
    d2 = calc_digito(cnpj, peso2)
    return cnpj[-2:] == f"{d1}{d2}"


def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def calc_digito(cpf, peso):
        soma = sum(int(cpf[i]) * (peso - i) for i in range(peso - 1))
        resto = (soma * 10) % 11
        return 0 if resto >= 10 else resto
    return int(cpf[9]) == calc_digito(cpf, 10) and int(cpf[10]) == calc_digito(cpf, 11)


def validar_email(email: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))


def validar_telefone(tel: str) -> bool:
    tel_clean = re.sub(r'\D', '', tel)
    return len(tel_clean) in [10, 11]


def formatar_cnpj(cnpj: str) -> str:
    c = re.sub(r'\D', '', cnpj)
    if len(c) == 14:
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
    return cnpj


def formatar_cpf(cpf: str) -> str:
    c = re.sub(r'\D', '', cpf)
    if len(c) == 11:
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
    return cpf


def formatar_cep(cep: str) -> str:
    c = re.sub(r'\D', '', cep)
    if len(c) == 8:
        return f"{c[:5]}-{c[5:]}"
    return cep


def formatar_telefone(tel: str) -> str:
    t = re.sub(r'\D', '', tel)
    if len(t) == 11:
        return f"({t[:2]}) {t[2:7]}-{t[7:]}"
    elif len(t) == 10:
        return f"({t[:2]}) {t[2:6]}-{t[6:]}"
    return tel


# =============================================================================
# CÁLCULO DE HONORÁRIOS (INTERNO — NÃO EXIBIDO AO CLIENTE)
# =============================================================================
def calcular_honorario_pj(dados: Dict) -> float:
    regime = dados.get('regime', 'Simples Nacional')
    fat = float(dados.get('faturamento_mensal', 0))
    notas = int(dados.get('num_notas', 0))
    func = int(dados.get('num_funcionarios', 0))
    est = dados.get('tem_estoque', False)
    sit = dados.get('situacao_fiscal', 'regular')
    filiais = int(dados.get('num_filiais', 0))
    imp_ext = dados.get('importa_exporta', False)

    base_map = {
        'MEI': 180,
        'Simples Nacional': 650,
        'Lucro Presumido': 1400,
        'Lucro Real': 2600
    }
    base = base_map.get(regime, 650)

    # Fator faturamento
    if fat <= 10000: ff = 0.8
    elif fat <= 30000: ff = 1.0
    elif fat <= 100000: ff = 1.35
    elif fat <= 300000: ff = 1.7
    elif fat <= 1000000: ff = 2.2
    else: ff = 3.0

    # Adicionais
    add_notas = (notas // 20) * 90
    add_func = min(func * 55, 1500)
    add_est = 250 if est else 0
    add_fil = filiais * 400
    add_imp = 500 if imp_ext else 0

    # Multiplicador irregularidade
    irreg = 1.35 if sit == 'irregular' else 1.0

    total = (base * ff + add_notas + add_func + add_est + add_fil + add_imp) * irreg
    return round(total, 2)


def calcular_honorario_pf(dados: Dict) -> float:
    renda = float(dados.get('renda_mensal', 0))
    bens = dados.get('possui_bens', False)
    invest = dados.get('possui_investimentos', False)
    exterior = dados.get('renda_exterior', False)
    autonomo = dados.get('autonomo', False)

    base = 250
    if renda <= 5000: ff = 1.0
    elif renda <= 15000: ff = 1.5
    elif renda <= 50000: ff = 2.0
    else: ff = 2.8

    extras = (120 if bens else 0) + (180 if invest else 0) + (300 if exterior else 0) + (150 if autonomo else 0)
    return round(base * ff + extras, 2)


# =============================================================================
# COMPONENTE: STEP INDICATOR
# =============================================================================
def render_step_indicator(current_step: int):
    steps = [
        ("perfil", "Perfil"),
        ("cadastro", "Cadastro"),
        ("fiscal", "Fiscal"),
        ("docs", "Docs"),
    ]
    html = '<div class="step-track">'
    for i, (icon_key, label) in enumerate(steps):
        step_num = i + 1
        if step_num < current_step:
            css = "done"
            label_css = ""
            icon = "✓"
        elif step_num == current_step:
            css = "active"
            label_css = "active"
            icon = str(step_num)
        else:
            css = "pending"
            label_css = ""
            icon = str(step_num)

        html += f'''
        <div class="step-node">
            <div class="step-circle {css}">{icon}</div>
            <span class="step-label {label_css}">{label}</span>
        </div>'''

        if i < len(steps) - 1:
            conn_css = "done" if step_num < current_step else ""
            html += f'<div class="step-connector {conn_css}"></div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# =============================================================================
# COMPONENTE: HERO
# =============================================================================
def render_hero():
    st.markdown("""
    <div class="hero-wrapper">
        <div class="bsb-wordmark">BSB Contabilidade</div>
        <div class="bsb-badge">Plataforma de Cadastro Inteligente</div>
        <div class="bsb-slogan">Inteligência fiscal para acelerar seu futuro.</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# COMPONENTE: LGPD
# =============================================================================
def render_lgpd():
    st.markdown("""
    <div class="lgpd-box">
        <div class="lgpd-icon">🔒</div>
        <div class="lgpd-text">
            <strong>Segurança & Privacidade (LGPD)</strong><br>
            Seus dados estão protegidos pela Lei Geral de Proteção de Dados (Lei 13.709/2018).
            Todas as informações fornecidas são <strong>confidenciais</strong> e serão utilizadas
            exclusivamente para elaboração de proposta de serviços contábeis personalizados.
            Não compartilhamos seus dados com terceiros.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN
# =============================================================================
def main():
    render_hero()
    render_lgpd()

    current_step = st.session_state.step
    render_step_indicator(max(current_step, 1))

    if current_step == 0:
        etapa_selecao_perfil()
    elif current_step == 1:
        etapa_dados_cadastrais()
    elif current_step == 2:
        etapa_dados_operacionais()
    elif current_step == 3:
        etapa_upload()
    elif current_step == 4:
        etapa_sucesso()


# =============================================================================
# ETAPA 0 — SELEÇÃO DE PERFIL
# =============================================================================
def etapa_selecao_perfil():
    st.markdown("""
    <div class="section-card">
        <div class="card-title"><div class="icon">🚀</div>Nova Proposta</div>
        <p style="color:#64748b;font-size:0.85rem;margin-bottom:1rem;">
            Para começarmos, nos diga como você gostaria de ser atendido:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tipo-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢  PESSOA JURÍDICA\n\nEmpresas, MEI, startups e negócios", use_container_width=True):
            st.session_state.perfil = 'PJ'
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("👤  PESSOA FÍSICA\n\nAutônomos, profissionais liberais e IR", use_container_width=True):
            st.session_state.perfil = 'PF'
            st.session_state.step = 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem; padding:1rem; background:rgba(37,99,235,0.06); border-radius:12px; border:1px solid rgba(59,130,246,0.12);">
        <p style="font-size:0.8rem; color:#64748b; margin:0; text-align:center; line-height:1.6;">
            💡 O preenchimento leva em média <strong style="color:#60a5fa">3 a 5 minutos</strong>.
            Após o envio, nossa equipe analisará seu perfil e enviará uma proposta personalizada
            em até <strong style="color:#60a5fa">24 horas úteis</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ETAPA 1 — DADOS CADASTRAIS
# =============================================================================
def etapa_dados_cadastrais():
    perfil = st.session_state.perfil
    dados = st.session_state.dados_cadastrais

    if perfil == 'PJ':
        _etapa_cadastral_pj(dados)
    else:
        _etapa_cadastral_pf(dados)


def _etapa_cadastral_pj(dados: Dict):
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">🏢</div>Dados da Empresa</div>', unsafe_allow_html=True)

    # — CNPJ com consulta automática —
    col1, col2 = st.columns([3, 1])
    with col1:
        cnpj_input = st.text_input(
            "CNPJ *",
            value=dados.get('cnpj', ''),
            placeholder="00.000.000/0000-00",
            key='cnpj_input'
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        consultar = st.button("🔍 Buscar", use_container_width=True, type="secondary")

    if consultar:
        cnpj_clean = re.sub(r'\D', '', cnpj_input)
        if not validar_cnpj(cnpj_clean):
            st.error("❌ CNPJ inválido. Verifique os dígitos e tente novamente.")
        else:
            with st.spinner("Consultando Receita Federal..."):
                resultado = consulta_cnpj(cnpj_clean)
            if resultado:
                # Extrai CNAE — tenta descrição direta, senão consulta
                cnae_desc = resultado.get('cnae_fiscal_descricao', '')
                cnae_cod = str(resultado.get('cnae_fiscal', ''))
                if not cnae_desc and cnae_cod:
                    cnae_desc = consulta_cnae(cnae_cod)

                # CNAEs secundários
                cnaes_sec = resultado.get('cnaes_secundarios', [])
                cnaes_sec_lista = [
                    f"{c.get('codigo','')}: {c.get('descricao','')}"
                    for c in cnaes_sec[:5]
                ] if cnaes_sec else []

                # Quadro societário
                socios = resultado.get('qsa', [])
                socios_lista = [
                    {
                        'nome': s.get('nome_socio', ''),
                        'qualificacao': s.get('qualificacao_socio', ''),
                        'cpf_cnpj': s.get('cnpj_cpf_do_socio', ''),
                        'faixa_etaria': s.get('faixa_etaria', '')
                    }
                    for s in socios
                ]

                st.session_state.dados_cadastrais.update({
                    'cnpj': formatar_cnpj(cnpj_clean),
                    'razao_social': resultado.get('razao_social', ''),
                    'nome_fantasia': resultado.get('nome_fantasia', '') or resultado.get('razao_social', ''),
                    'natureza_juridica': resultado.get('descricao_natureza_juridica', '') or
                                        resultado.get('natureza_juridica', {}).get('descricao', '') if isinstance(resultado.get('natureza_juridica'), dict) else resultado.get('natureza_juridica', ''),
                    'situacao': resultado.get('descricao_situacao_cadastral', '') or resultado.get('situacao_cadastral', ''),
                    'data_abertura': resultado.get('data_inicio_atividade', '') or resultado.get('data_abertura', ''),
                    'porte': resultado.get('descricao_porte', '') or resultado.get('porte', ''),
                    'capital_social': resultado.get('capital_social', 0),
                    'cnae_principal_cod': cnae_cod,
                    'cnae_principal_desc': cnae_desc,
                    'cnaes_secundarios': cnaes_sec_lista,
                    'socios': socios_lista,
                    'email_receita': resultado.get('email', ''),
                    'telefone_receita': resultado.get('ddd_telefone_1', '') + resultado.get('telefone', '') if resultado.get('ddd_telefone_1') else '',
                    'cep': resultado.get('cep', ''),
                    'logradouro': resultado.get('logradouro', ''),
                    'numero': resultado.get('numero', ''),
                    'complemento': resultado.get('complemento', ''),
                    'bairro': resultado.get('bairro', ''),
                    'municipio': resultado.get('municipio', ''),
                    'uf': resultado.get('uf', ''),
                })
                st.session_state.cnpj_consultado = True
                st.success("✅ Empresa localizada! Dados preenchidos automaticamente.")
                st.rerun()
            else:
                st.error("❌ CNPJ não encontrado ou serviço indisponível. Preencha manualmente.")

    # — Badge de consulta automática —
    if st.session_state.get('cnpj_consultado'):
        st.markdown('<div class="auto-badge">⚡ Dados preenchidos via Receita Federal</div>', unsafe_allow_html=True)

    dados = st.session_state.dados_cadastrais

    col1, col2 = st.columns(2)
    with col1:
        razao_social = st.text_input("Razão Social *", value=dados.get('razao_social', ''))
        nome_fantasia = st.text_input("Nome Fantasia", value=dados.get('nome_fantasia', ''))
        natureza_juridica = st.text_input("Natureza Jurídica", value=dados.get('natureza_juridica', ''))
        situacao = st.text_input("Situação Cadastral", value=dados.get('situacao', ''))
    with col2:
        data_abertura = st.text_input("Data de Abertura", value=dados.get('data_abertura', ''))
        porte = st.text_input("Porte da Empresa", value=dados.get('porte', ''))
        capital_social = st.number_input(
            "Capital Social (R$)",
            value=float(dados.get('capital_social', 0)),
            min_value=0.0,
            step=1000.0,
            format="%.2f"
        )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cnae_desc = st.text_input("CNAE Principal", value=dados.get('cnae_principal_desc', ''))
    with col2:
        cnae_cod = st.text_input("Código CNAE", value=dados.get('cnae_principal_cod', ''))

    if dados.get('cnaes_secundarios'):
        with st.expander("📋 CNAEs Secundários"):
            for c in dados['cnaes_secundarios']:
                st.markdown(f"<div style='color:#94a3b8;font-size:0.82rem;padding:3px 0;'>• {c}</div>", unsafe_allow_html=True)

    # Sócios
    if dados.get('socios'):
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-top:0;"><div class="icon">👥</div>Quadro Societário</div>', unsafe_allow_html=True)
        for s in dados['socios']:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='font-size:0.82rem;color:#e2e8f0;font-weight:600;'>{s.get('nome','')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.74rem;color:#64748b;'>{s.get('qualificacao','')}</div>", unsafe_allow_html=True)
            with col2:
                if s.get('faixa_etaria'):
                    st.markdown(f"<div style='font-size:0.74rem;color:#64748b;'>Faixa etária: {s.get('faixa_etaria','')}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close section-card

    # — Endereço —
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📍</div>Endereço</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        cep_input = st.text_input("CEP *", value=dados.get('cep', ''), placeholder="00000-000", key='cep_pj')
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_cep = st.button("📍 Buscar", use_container_width=True, type="secondary", key='btn_cep_pj')

    if buscar_cep:
        cep_clean = re.sub(r'\D', '', cep_input)
        if len(cep_clean) != 8:
            st.error("CEP deve ter 8 dígitos.")
        else:
            with st.spinner("Buscando endereço..."):
                ender = consulta_cep(cep_clean)
            if ender:
                st.session_state.dados_cadastrais.update({
                    'cep': formatar_cep(cep_clean),
                    'logradouro': ender.get('street', '') or ender.get('logradouro', ''),
                    'bairro': ender.get('neighborhood', '') or ender.get('bairro', ''),
                    'municipio': ender.get('city', '') or ender.get('localidade', ''),
                    'uf': ender.get('state', '') or ender.get('uf', ''),
                })
                st.session_state.cep_consultado = True
                st.success("✅ Endereço encontrado!")
                st.rerun()
            else:
                st.error("CEP não encontrado.")

    dados = st.session_state.dados_cadastrais
    col1, col2 = st.columns(2)
    with col1:
        logradouro = st.text_input("Logradouro", value=dados.get('logradouro', ''))
        bairro = st.text_input("Bairro", value=dados.get('bairro', ''))
        municipio = st.text_input("Município", value=dados.get('municipio', ''))
    with col2:
        numero = st.text_input("Número", value=dados.get('numero', ''))
        complemento = st.text_input("Complemento", value=dados.get('complemento', ''))
        uf = st.selectbox("UF", lista_estados(), index=lista_estados().index(dados.get('uf', 'DF')) if dados.get('uf', 'DF') in lista_estados() else 6)

    st.session_state.dados_cadastrais.update({
        'cnpj': dados.get('cnpj', ''),
        'razao_social': razao_social,
        'nome_fantasia': nome_fantasia,
        'natureza_juridica': natureza_juridica,
        'situacao': situacao,
        'data_abertura': data_abertura,
        'porte': porte,
        'capital_social': capital_social,
        'cnae_principal_cod': cnae_cod,
        'cnae_principal_desc': cnae_desc,
        'cep': cep_input,
        'logradouro': logradouro,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'municipio': municipio,
        'uf': uf,
    })
    st.markdown('</div>', unsafe_allow_html=True)  # close endereço card

    _botoes_navegacao(voltar_step=0, proximo_step=2, validar_pj=True)


def _etapa_cadastral_pf(dados: Dict):
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">👤</div>Dados Pessoais</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cpf = st.text_input("CPF *", value=dados.get('cpf', ''), placeholder="000.000.000-00")
        nome = st.text_input("Nome Completo *", value=dados.get('nome', ''))
        data_nasc = st.date_input(
            "Data de Nascimento *",
            value=datetime.strptime(dados['data_nascimento'], '%d/%m/%Y').date()
                if dados.get('data_nascimento') else date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
    with col2:
        nacionalidade = st.text_input("Nacionalidade", value=dados.get('nacionalidade', 'Brasileira'))
        estado_civil = st.selectbox(
            "Estado Civil",
            ["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
            index=["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"].index(dados.get('estado_civil', 'Solteiro(a)')) if dados.get('estado_civil') in ["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"] else 0
        )
        profissao = st.text_input("Profissão / Ocupação", value=dados.get('profissao', ''))

    st.markdown('</div>', unsafe_allow_html=True)

    # — Endereço PF —
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📍</div>Endereço</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        cep_pf = st.text_input("CEP *", value=dados.get('cep', ''), placeholder="00000-000", key='cep_pf_input')
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_cep_pf = st.button("📍 Buscar", use_container_width=True, type="secondary", key='btn_cep_pf')

    if buscar_cep_pf:
        cep_clean = re.sub(r'\D', '', cep_pf)
        if len(cep_clean) != 8:
            st.error("CEP deve ter 8 dígitos.")
        else:
            with st.spinner("Buscando endereço..."):
                ender = consulta_cep(cep_clean)
            if ender:
                st.session_state.dados_cadastrais.update({
                    'cep': formatar_cep(cep_clean),
                    'logradouro': ender.get('street', '') or ender.get('logradouro', ''),
                    'bairro': ender.get('neighborhood', '') or ender.get('bairro', ''),
                    'municipio': ender.get('city', '') or ender.get('localidade', ''),
                    'uf': ender.get('state', '') or ender.get('uf', ''),
                })
                st.rerun()

    dados = st.session_state.dados_cadastrais
    col1, col2 = st.columns(2)
    with col1:
        logradouro = st.text_input("Logradouro", value=dados.get('logradouro', ''), key='log_pf')
        bairro = st.text_input("Bairro", value=dados.get('bairro', ''), key='bairro_pf')
        municipio = st.text_input("Município", value=dados.get('municipio', ''), key='mun_pf')
    with col2:
        numero = st.text_input("Número", value=dados.get('numero', ''), key='num_pf')
        complemento = st.text_input("Complemento", value=dados.get('complemento', ''), key='comp_pf')
        uf = st.selectbox("UF", lista_estados(), index=lista_estados().index(dados.get('uf', 'DF')) if dados.get('uf', 'DF') in lista_estados() else 6, key='uf_pf')

    st.session_state.dados_cadastrais.update({
        'cpf': cpf, 'nome': nome,
        'data_nascimento': data_nasc.strftime('%d/%m/%Y'),
        'nacionalidade': nacionalidade,
        'estado_civil': estado_civil,
        'profissao': profissao,
        'cep': cep_pf,
        'logradouro': logradouro,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'municipio': municipio,
        'uf': uf,
    })
    st.markdown('</div>', unsafe_allow_html=True)

    _botoes_navegacao(voltar_step=0, proximo_step=2, validar_pf=True)


def _botoes_navegacao(voltar_step: int, proximo_step: int,
                       validar_pj: bool = False, validar_pf: bool = False):
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = voltar_step
            st.rerun()
    with col2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            d = st.session_state.dados_cadastrais

            if validar_pj:
                cnpj_val = re.sub(r'\D', '', d.get('cnpj', ''))
                if not validar_cnpj(cnpj_val):
                    erros.append("CNPJ inválido ou não preenchido.")
                if not d.get('razao_social', '').strip():
                    erros.append("Razão Social é obrigatória.")

            if validar_pf:
                cpf_val = re.sub(r'\D', '', d.get('cpf', ''))
                if not validar_cpf(cpf_val):
                    erros.append("CPF inválido.")
                if not d.get('nome', '').strip():
                    erros.append("Nome completo é obrigatório.")

            if erros:
                for e in erros:
                    st.error(f"❌ {e}")
            else:
                st.session_state.step = proximo_step
                st.rerun()


# =============================================================================
# ETAPA 2 — DADOS OPERACIONAIS / FISCAIS
# =============================================================================
def etapa_dados_operacionais():
    perfil = st.session_state.perfil

    if perfil == 'PJ':
        _etapa_fiscal_pj()
    else:
        _etapa_fiscal_pf()


def _etapa_fiscal_pj():
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📊</div>Configuração Fiscal</div>', unsafe_allow_html=True)
    op = st.session_state.dados_operacionais

    col1, col2 = st.columns(2)
    with col1:
        regime = st.selectbox(
            "Regime Tributário *",
            ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"],
            index=["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"].index(op.get('regime', 'Simples Nacional')) if op.get('regime') else 0
        )
        faturamento = st.number_input(
            "Faturamento médio mensal (R$) *",
            min_value=0.0, step=1000.0, format="%.2f",
            value=float(op.get('faturamento_mensal', 0))
        )
        num_notas = st.number_input(
            "Notas fiscais/mês *",
            min_value=0, step=1,
            value=int(op.get('num_notas', 0))
        )
        num_filiais = st.number_input(
            "Número de filiais",
            min_value=0, step=1,
            value=int(op.get('num_filiais', 0)),
            help="Informe 0 caso seja apenas matriz."
        )
    with col2:
        num_funcionarios = st.number_input(
            "Número de funcionários",
            min_value=0, step=1,
            value=int(op.get('num_funcionarios', 0))
        )
        tem_estoque = st.checkbox("Possui controle de estoque?", value=op.get('tem_estoque', False))
        importa_exporta = st.checkbox("Realiza importação/exportação?", value=op.get('importa_exporta', False))
        tem_simples_ativo = st.checkbox("Optante pelo Simples Nacional?", value=op.get('tem_simples_ativo', False))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        situacao_fiscal = st.radio(
            "Situação fiscal atual *",
            ["Em dia", "Com pendências / irregularidades"],
            index=0 if op.get('situacao_fiscal', 'regular') == 'regular' else 1
        )
        contabilidade_atual = st.radio(
            "Possui contador atualmente?",
            ["Não", "Sim, quero trocar", "Sim, consultoria adicional"],
            index=["Não", "Sim, quero trocar", "Sim, consultoria adicional"].index(op.get('contabilidade_atual', 'Não')) if op.get('contabilidade_atual') in ["Não", "Sim, quero trocar", "Sim, consultoria adicional"] else 0
        )
    with col2:
        tipo_servico = st.multiselect(
            "Serviços de interesse",
            [
                "Contabilidade Geral",
                "Abertura de Empresa",
                "Encerramento de Empresa",
                "BPO Financeiro",
                "Folha de Pagamento",
                "Planejamento Tributário",
                "Consultoria Fiscal",
                "Regularização Fiscal",
                "Certidões e Declarações",
            ],
            default=op.get('tipo_servico', [])
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # — Contato —
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📞</div>Dados de Contato</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        contato_nome = st.text_input("Nome do responsável *", value=op.get('contato_nome', ''))
        contato_email = st.text_input("E-mail *", value=op.get('contato_email', ''))
    with col2:
        contato_telefone = st.text_input(
            "Telefone / WhatsApp *",
            value=op.get('contato_telefone', ''),
            placeholder="(00) 00000-0000"
        )
        expectativa = st.selectbox(
            "Início desejado dos serviços",
            ["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"],
            index=["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"].index(op.get('expectativa', 'Imediato (o mais rápido possível)')) if op.get('expectativa') in ["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"] else 0
        )

    observacoes = st.text_area(
        "Observações ou necessidades específicas",
        value=op.get('observacoes', ''),
        placeholder="Descreva qualquer informação adicional relevante...",
        height=90
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # — Salvar e navegar —
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            if not contato_nome.strip():
                erros.append("Nome do responsável é obrigatório.")
            if not validar_email(contato_email):
                erros.append("E-mail inválido.")
            if not validar_telefone(contato_telefone):
                erros.append("Telefone inválido (10 ou 11 dígitos).")
            if faturamento <= 0:
                erros.append("Informe o faturamento médio mensal.")
            if erros:
                for e in erros:
                    st.error(f"❌ {e}")
            else:
                st.session_state.dados_operacionais = {
                    'regime': regime,
                    'faturamento_mensal': faturamento,
                    'num_notas': num_notas,
                    'num_filiais': num_filiais,
                    'num_funcionarios': num_funcionarios,
                    'tem_estoque': tem_estoque,
                    'importa_exporta': importa_exporta,
                    'tem_simples_ativo': tem_simples_ativo,
                    'situacao_fiscal': 'irregular' if 'pendências' in situacao_fiscal else 'regular',
                    'contabilidade_atual': contabilidade_atual,
                    'tipo_servico': tipo_servico,
                    'contato_nome': contato_nome,
                    'contato_email': contato_email,
                    'contato_telefone': formatar_telefone(contato_telefone),
                    'expectativa': expectativa,
                    'observacoes': observacoes,
                }
                st.session_state.step = 3
                st.rerun()


def _etapa_fiscal_pf():
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📊</div>Perfil Financeiro</div>', unsafe_allow_html=True)
    op = st.session_state.dados_operacionais

    col1, col2 = st.columns(2)
    with col1:
        renda_mensal = st.number_input(
            "Renda mensal aproximada (R$) *",
            min_value=0.0, step=500.0, format="%.2f",
            value=float(op.get('renda_mensal', 0))
        )
        possui_bens = st.checkbox("Possui bens imóveis?", value=op.get('possui_bens', False))
        possui_investimentos = st.checkbox("Possui investimentos / aplicações?", value=op.get('possui_investimentos', False))
        renda_exterior = st.checkbox("Possui renda no exterior?", value=op.get('renda_exterior', False))
    with col2:
        autonomo = st.checkbox("É autônomo / prestador de serviços?", value=op.get('autonomo', False))
        pensao = st.checkbox("Recebe pensão alimentícia?", value=op.get('pensao', False))
        socio_empresa = st.checkbox("É sócio de alguma empresa?", value=op.get('socio_empresa', False))
        heranca = st.checkbox("Recebeu herança ou doação no ano?", value=op.get('heranca', False))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        tipo_declaracao = st.radio(
            "Tipo preferido de declaração",
            ["Simplificada", "Completa (deduções)", "Não sei — quero orientação"],
            index=["Simplificada", "Completa (deduções)", "Não sei — quero orientação"].index(op.get('tipo_declaracao', 'Simplificada')) if op.get('tipo_declaracao') in ["Simplificada", "Completa (deduções)", "Não sei — quero orientação"] else 0
        )
    with col2:
        tipo_servico_pf = st.multiselect(
            "Serviços de interesse",
            [
                "Imposto de Renda (IRPF)",
                "Planejamento Patrimonial",
                "Consultoria Tributária",
                "Regularização junto à Receita",
                "Declaração em Atraso",
                "Herança / Doação / Inventário",
            ],
            default=op.get('tipo_servico', [])
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # — Contato PF —
    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📞</div>Dados de Contato</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        contato_email = st.text_input("E-mail *", value=op.get('contato_email', ''), key='email_pf')
    with col2:
        contato_telefone = st.text_input(
            "Telefone / WhatsApp *",
            value=op.get('contato_telefone', ''),
            placeholder="(00) 00000-0000",
            key='tel_pf'
        )
    expectativa_pf = st.selectbox(
        "Inicio desejado",
        ["Imediato", "Próximo mês", "Apenas cotação"],
        index=["Imediato", "Próximo mês", "Apenas cotação"].index(op.get('expectativa', 'Imediato')) if op.get('expectativa') in ["Imediato", "Próximo mês", "Apenas cotação"] else 0
    )
    observacoes_pf = st.text_area(
        "Observações",
        value=op.get('observacoes', ''),
        placeholder="Informações adicionais...",
        height=80
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            if not validar_email(contato_email):
                erros.append("E-mail inválido.")
            if not validar_telefone(contato_telefone):
                erros.append("Telefone inválido.")
            if renda_mensal <= 0:
                erros.append("Informe a renda mensal aproximada.")
            if erros:
                for e in erros:
                    st.error(f"❌ {e}")
            else:
                st.session_state.dados_operacionais = {
                    'renda_mensal': renda_mensal,
                    'possui_bens': possui_bens,
                    'possui_investimentos': possui_investimentos,
                    'renda_exterior': renda_exterior,
                    'autonomo': autonomo,
                    'pensao': pensao,
                    'socio_empresa': socio_empresa,
                    'heranca': heranca,
                    'tipo_declaracao': tipo_declaracao,
                    'tipo_servico': tipo_servico_pf,
                    'contato_email': contato_email,
                    'contato_telefone': formatar_telefone(contato_telefone),
                    'expectativa': expectativa_pf,
                    'observacoes': observacoes_pf,
                }
                st.session_state.step = 3
                st.rerun()


# =============================================================================
# ETAPA 3 — UPLOAD DE DOCUMENTOS
# =============================================================================
def etapa_upload():
    perfil = st.session_state.perfil

    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📎</div>Documentação para Análise</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.83rem;color:#64748b;margin-bottom:1rem;">
        O envio de documentos é <strong style="color:#94a3b8">opcional</strong> neste momento — nossa equipe
        poderá solicitá-los posteriormente se necessário. Mas enviar agora acelera a elaboração da sua proposta.
    </p>
    """, unsafe_allow_html=True)

    docs_salvos = []

    if perfil == 'PJ':
        cartao_cnpj = st.file_uploader("📄 Cartão CNPJ", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_cnpj')
        contrato_social = st.file_uploader("📝 Contrato / Estatuto Social", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_contrato')
        ultimas_guias = st.file_uploader("📋 Últimas guias pagas (DAS, GPS, etc.)", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_guias')
        balanco = st.file_uploader("📊 Último Balanço / DRE (se disponível)", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_balanco')
        docs_salvos = [d for d in [cartao_cnpj, contrato_social, ultimas_guias, balanco] if d]
    else:
        doc_id = st.file_uploader("🪪 RG, CNH ou passaporte", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_id')
        comp_res = st.file_uploader("🏠 Comprovante de Residência", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_res')
        declaracao_ant = st.file_uploader("📋 Última declaração de IR (se tiver)", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_ir')
        informe_rend = st.file_uploader("💼 Informe de Rendimentos", type=['pdf', 'png', 'jpg', 'jpeg'], key='up_informe')
        docs_salvos = [d for d in [doc_id, comp_res, declaracao_ant, informe_rend] if d]

    if docs_salvos:
        st.markdown(f'<div class="auto-badge">📎 {len(docs_salvos)} arquivo(s) anexado(s)</div>', unsafe_allow_html=True)

    st.session_state.documentos = docs_salvos
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("✅  Finalizar Cadastro", use_container_width=True, type="primary"):
            # Calcular honorário (interno)
            if perfil == 'PJ':
                st.session_state.honorario_interno = calcular_honorario_pj(st.session_state.dados_operacionais)
            else:
                st.session_state.honorario_interno = calcular_honorario_pf(st.session_state.dados_operacionais)
            st.session_state.step = 4
            st.rerun()


# =============================================================================
# ETAPA 4 — SUCESSO
# =============================================================================
def etapa_sucesso():
    st.balloons()
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0; animation: fadeSlideDown 0.8s ease both;">
        <div style="font-size:4rem; margin-bottom:1rem;">🎉</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:1.8rem; font-weight:800; color:#e2e8f0; margin-bottom:0.5rem;">
            Cadastro Recebido!
        </h2>
        <p style="color:#64748b; font-size:0.9rem; max-width:380px; margin:0 auto; line-height:1.6;">
            Obrigado pela confiança na <strong style="color:#60a5fa">BSB Contabilidade</strong>.<br>
            Nossa equipe analisará seu perfil e enviará uma <strong style="color:#60a5fa">proposta personalizada</strong>
            em até <strong style="color:#60a5fa">24 horas úteis</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Resumo
    perfil = st.session_state.perfil
    dados_cad = st.session_state.dados_cadastrais
    dados_op = st.session_state.dados_operacionais

    st.markdown('<div class="section-card"><div class="card-title"><div class="icon">📋</div>Resumo do Cadastro</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if perfil == 'PJ':
            st.markdown(f"**Empresa:** {dados_cad.get('razao_social','—')}")
            st.markdown(f"**CNPJ:** {dados_cad.get('cnpj','—')}")
            st.markdown(f"**Regime:** {dados_op.get('regime','—')}")
        else:
            st.markdown(f"**Nome:** {dados_cad.get('nome','—')}")
            st.markdown(f"**CPF:** {dados_cad.get('cpf','—')}")
    with col2:
        st.markdown(f"**E-mail:** {dados_op.get('contato_email','—')}")
        st.markdown(f"**Telefone:** {dados_op.get('contato_telefone','—')}")
        if dados_op.get('expectativa'):
            st.markdown(f"**Início desejado:** {dados_op.get('expectativa')}")

    if dados_op.get('tipo_servico'):
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("**Serviços solicitados:**")
        for s in dados_op['tipo_servico']:
            st.markdown(f"<div style='font-size:0.82rem;color:#60a5fa;padding:2px 0;'>✓ {s}</div>", unsafe_allow_html=True)

    docs_count = len(st.session_state.documentos)
    if docs_count > 0:
        st.markdown(f"<div style='margin-top:0.8rem;font-size:0.82rem;color:#34d399;'>📎 {docs_count} documento(s) anexado(s)</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Novo Cadastro", use_container_width=True, type="secondary"):
        for key in ['step','perfil','dados_cadastrais','dados_operacionais','dados_socio',
                    'documentos','honorario_interno','cnpj_consultado','cep_consultado','submitted']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
