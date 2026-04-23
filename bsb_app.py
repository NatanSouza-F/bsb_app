"""
BSB Contabilidade — Plataforma de Cadastro Inteligente v3.0
Visual: Premium Dark — referência XP Investimentos
"""

import streamlit as st
import requests
import re
from datetime import datetime, date
from typing import Dict, Optional

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
# CSS PREMIUM v3.0 — TIPOGRAFIA REFINADA + CARDS DE SERVIÇOS + CÂMERA
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Instrument+Serif:ital@0;1&display=swap');

/* ─── RESET ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
* {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ─── APP BACKGROUND ────────────────────────────────────────────────── */
.stApp {
    background: #06101c;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -30%;
    left: -15%;
    width: 70%;
    height: 70%;
    background: radial-gradient(ellipse, rgba(30,86,220,0.10) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
    animation: breathe 9s ease-in-out infinite;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -20%;
    right: -5%;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse, rgba(5,160,200,0.06) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
    animation: breathe 12s ease-in-out infinite reverse;
}
@keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(1.12); opacity: 1; }
}

/* ─── BLOCK CONTAINER ───────────────────────────────────────────────── */
.block-container {
    max-width: 580px !important;
    padding: 1.4rem 1.2rem 3rem 1.2rem !important;
    position: relative;
    z-index: 1;
}

/* ─── HERO ──────────────────────────────────────────────────────────── */
.hero-wrapper {
    text-align: center;
    padding: 2.2rem 0 0.6rem 0;
    animation: fadeSlideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Wordmark — serifado elegante para "BSB" + sans para "Contabilidade" */
.bsb-wordmark-line1 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    font-size: clamp(2.6rem, 8vw, 3.6rem);
    font-weight: 400;
    font-style: italic;
    letter-spacing: -0.01em;
    background: linear-gradient(135deg, #4f8ef7 0%, #6cb4fc 50%, #34c3e8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.0;
    filter: drop-shadow(0 0 22px rgba(79,142,247,0.30));
    display: block;
}
.bsb-wordmark-line2 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: clamp(0.9rem, 3vw, 1.05rem);
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #475569;
    display: block;
    margin-top: 2px;
}
.bsb-slogan {
    font-size: 0.82rem;
    font-weight: 400;
    color: #334155;
    margin-top: 0.5rem;
    letter-spacing: 0.015em;
}

/* ─── SERVIÇOS CARDS (hero) ─────────────────────────────────────────── */
.servicos-strip {
    display: flex;
    gap: 10px;
    margin: 1.6rem 0 0.2rem 0;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: none;
}
.servicos-strip::-webkit-scrollbar { display: none; }
.srv-card {
    flex: 1;
    min-width: 110px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 14px 10px 12px 10px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: cardEnter 0.6s cubic-bezier(0.16,1,0.3,1) both;
}
.srv-card:nth-child(1) { animation-delay: 0.08s; }
.srv-card:nth-child(2) { animation-delay: 0.16s; }
.srv-card:nth-child(3) { animation-delay: 0.24s; }
.srv-card:nth-child(4) { animation-delay: 0.32s; }
.srv-card::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(79,142,247,0.5), transparent);
    animation: shimmer-line 3s ease-in-out infinite;
}
@keyframes shimmer-line {
    0%, 100% { opacity: 0; transform: scaleX(0.4); }
    50% { opacity: 1; transform: scaleX(1); }
}
.srv-card .srv-icon {
    font-size: 1.4rem;
    display: block;
    margin-bottom: 6px;
    animation: floatIcon 4s ease-in-out infinite;
}
.srv-card:nth-child(2) .srv-icon { animation-delay: 0.5s; }
.srv-card:nth-child(3) .srv-icon { animation-delay: 1s; }
.srv-card:nth-child(4) .srv-icon { animation-delay: 1.5s; }
@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}
.srv-card .srv-title {
    font-size: 0.68rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    line-height: 1.3;
}
.srv-card .srv-desc {
    font-size: 0.62rem;
    color: #475569;
    margin-top: 3px;
    line-height: 1.35;
    font-weight: 400;
}

/* ─── STEP INDICATOR ────────────────────────────────────────────────── */
.step-track {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    margin: 1.8rem auto 1.6rem auto;
    width: 100%;
    max-width: 340px;
    animation: fadeIn 0.6s ease both;
    animation-delay: 0.4s;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    flex: 1;
    position: relative;
    z-index: 2;
}
.step-circle {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.75rem;
    transition: all 0.3s ease;
}
.step-circle.done {
    background: #1e4bd8;
    color: white;
    box-shadow: 0 0 12px rgba(79,142,247,0.4);
}
.step-circle.active {
    background: #1e4bd8;
    color: white;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.18), 0 0 16px rgba(79,142,247,0.45);
    animation: ring-pulse 2.2s ease-in-out infinite;
}
@keyframes ring-pulse {
    0%, 100% { box-shadow: 0 0 0 3px rgba(79,142,247,0.18), 0 0 16px rgba(79,142,247,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(79,142,247,0.08), 0 0 22px rgba(79,142,247,0.55); }
}
.step-circle.pending {
    background: rgba(20,30,48,0.9);
    color: #334155;
    border: 1px solid rgba(51,65,85,0.4);
}
.step-label {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #334155;
    text-align: center;
    white-space: nowrap;
}
.step-label.active { color: #4f8ef7; }
.step-connector {
    flex: 1;
    height: 1px;
    background: rgba(51,65,85,0.5);
    margin-top: 15px;
    position: relative;
    z-index: 1;
    max-width: 36px;
}
.step-connector.done { background: #1e4bd8; }

/* ─── SECTION CARD ──────────────────────────────────────────────────── */
.section-card {
    background: rgba(10,18,32,0.92);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03);
    animation: cardEnter 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes cardEnter {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-title-icon {
    width: 26px; height: 26px;
    border-radius: 7px;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.18);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
}

/* ─── LGPD BOX ──────────────────────────────────────────────────────── */
.lgpd-box {
    display: flex;
    gap: 10px;
    background: rgba(79,142,247,0.04);
    border: 1px solid rgba(79,142,247,0.12);
    border-radius: 10px;
    padding: 11px 14px;
    margin-bottom: 1.2rem;
    animation: fadeIn 0.9s ease both;
    animation-delay: 0.6s;
}
.lgpd-icon { font-size: 0.9rem; flex-shrink: 0; margin-top: 1px; }
.lgpd-text { font-size: 0.74rem; color: #334155; line-height: 1.5; }
.lgpd-text strong { color: #64748b; font-weight: 600; }

/* ─── AUTO-FILL BADGE ───────────────────────────────────────────────── */
.auto-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #34d399;
    margin-bottom: 8px;
    letter-spacing: 0.03em;
}

/* ─── DIVIDER ───────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 1.1rem 0;
}

/* ─── STREAMLIT LABEL OVERRIDES ─────────────────────────────────────── */
label,
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stRadio label, .stCheckbox label,
.stDateInput label, .stTextArea label {
    color: #64748b !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.035em !important;
    text-transform: uppercase !important;
}

/* ─── INPUTS ────────────────────────────────────────────────────────── */
input, textarea,
.stNumberInput input,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(6,14,26,0.85) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
    border-radius: 9px !important;
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}
input:focus, textarea:focus {
    border-color: rgba(79,142,247,0.55) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.08) !important;
    outline: none !important;
}
input::placeholder, textarea::placeholder { color: #1e293b !important; }

/* Select */
div[data-baseweb="select"] > div {
    background: rgba(6,14,26,0.85) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 9px !important;
    font-size: 0.875rem !important;
    color: #e2e8f0 !important;
}
div[data-baseweb="menu"] {
    background: #0a1220 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
div[data-baseweb="option"] { color: #cbd5e1 !important; font-size: 0.85rem !important; }
div[data-baseweb="option"]:hover { background: rgba(79,142,247,0.12) !important; }

/* ─── BUTTONS ───────────────────────────────────────────────────────── */
.stButton > button {
    background: #1a43cc !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.68rem 1.1rem !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4), 0 4px 14px rgba(26,67,204,0.28) !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #1e4bd8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4), 0 6px 20px rgba(26,67,204,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0) scale(0.99) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(10,18,32,0.9) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #64748b !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: rgba(79,142,247,0.3) !important;
    color: #94a3b8 !important;
    background: rgba(79,142,247,0.05) !important;
}

/* ─── RADIO ─────────────────────────────────────────────────────────── */
.stRadio > div { gap: 6px !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: rgba(6,14,26,0.8) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    padding: 7px 12px !important;
    color: #64748b !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    transition: all 0.18s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: rgba(79,142,247,0.45) !important;
    background: rgba(26,67,204,0.1) !important;
    color: #93b4fb !important;
}

/* ─── CHECKBOX ──────────────────────────────────────────────────────── */
.stCheckbox > label {
    color: #64748b !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0.01em !important;
}
input[type="checkbox"] { accent-color: #1e4bd8 !important; }

/* ─── MULTISELECT ───────────────────────────────────────────────────── */
span[data-baseweb="tag"] {
    background: rgba(26,67,204,0.2) !important;
    border: 1px solid rgba(79,142,247,0.3) !important;
    border-radius: 6px !important;
    color: #93b4fb !important;
    font-size: 0.75rem !important;
}

/* ─── ALERTS ────────────────────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 9px !important;
    font-size: 0.82rem !important;
}
.stSuccess { background: rgba(16,185,129,0.07) !important; border: 1px solid rgba(16,185,129,0.2) !important; }
.stError { background: rgba(239,68,68,0.07) !important; border: 1px solid rgba(239,68,68,0.2) !important; }
.stInfo { background: rgba(79,142,247,0.06) !important; border: 1px solid rgba(79,142,247,0.18) !important; }
.stWarning { background: rgba(245,158,11,0.07) !important; border: 1px solid rgba(245,158,11,0.2) !important; }

/* ─── FILE UPLOADER ─────────────────────────────────────────────────── */
div[data-testid="stFileUploader"] {
    background: rgba(6,14,26,0.7) !important;
    border: 1.5px dashed rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(79,142,247,0.35) !important;
}
div[data-testid="stFileUploader"] label {
    text-transform: none !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.01em !important;
    color: #94a3b8 !important;
}

/* ─── SPINNER ───────────────────────────────────────────────────────── */
div[data-testid="stSpinner"] { color: #4f8ef7 !important; }

/* ─── EXPANDER ──────────────────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: rgba(6,14,26,0.7) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
}

/* ─── SCROLLBAR ─────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #06101c; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #1e4bd8; }

/* ─── CAMERA CAPTURE SECTION ────────────────────────────────────────── */
.camera-card {
    background: rgba(6,14,26,0.7);
    border: 1.5px dashed rgba(79,142,247,0.2);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 0.5rem;
    text-align: center;
}
.camera-card-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.5rem;
}

/* ─── MOBILE ────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .block-container { padding: 1rem 0.85rem 2.5rem !important; }
    .section-card { padding: 1.1rem 1rem; }
    .servicos-strip { flex-wrap: nowrap; }
    .bsb-wordmark-line1 { font-size: clamp(2.2rem, 10vw, 3rem); }
    .step-label { font-size: 0.52rem; }
}

/* ─── HIDE STREAMLIT CHROME ─────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
.stApp > div:first-child [data-testid="stToolbar"] { display: none; }
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
# LISTAS DE OPÇÕES — CAMPOS COM SUGESTÕES
# =============================================================================
PROFISSOES = [
    "Administrador(a)", "Advogado(a)", "Agente de Saúde", "Analista de Sistemas",
    "Arquiteto(a)", "Autônomo(a) / Prestador(a) de Serviços", "Bancário(a)",
    "Comerciante / Lojista", "Contador(a)", "Dentista", "Designer",
    "Economista", "Enfermeiro(a)", "Engenheiro(a)", "Estudante",
    "Farmacêutico(a)", "Funcionário Público", "Gestor(a) Financeiro(a)",
    "Investidor(a)", "Jornalista", "Médico(a)", "Motorista / Transportador(a)",
    "Nutricionista", "Pedagogo(a)", "Policial / Militar", "Professor(a)",
    "Psicólogo(a)", "Servidor Público", "Técnico(a)", "Vendedor(a)", "Outro"
]

SEGMENTOS_PJ = [
    "Agropecuária / Agricultura",
    "Alimentação / Restaurante / Delivery",
    "Comércio Varejista",
    "Comércio Atacadista",
    "Construção Civil / Incorporação",
    "Consultoria / Assessoria",
    "Educação / Treinamento",
    "Estética / Saúde / Bem-estar",
    "Indústria / Manufatura",
    "Logística / Transporte",
    "Saúde / Clínica / Laboratório",
    "Serviços em Geral",
    "Tecnologia / Software / SaaS",
    "Turismo / Hotelaria",
    "Outro"
]

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
            headers={"User-Agent": "BSB-Contabilidade/3.0"}
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
            headers={"User-Agent": "BSB-Contabilidade/3.0"}
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
        return resp.json().get('descricao', '')
    except Exception:
        return ""


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
    def calc(cnpj, p):
        s = sum(int(cnpj[i]) * p[i] for i in range(len(p)))
        r = s % 11
        return 0 if r < 2 else 11 - r
    d1 = calc(cnpj, [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = calc(cnpj, [6,5,4,3,2,9,8,7,6,5,4,3,2])
    return cnpj[-2:] == f"{d1}{d2}"


def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def calc(cpf, p):
        s = sum(int(cpf[i]) * (p - i) for i in range(p - 1))
        r = (s * 10) % 11
        return 0 if r >= 10 else r
    return int(cpf[9]) == calc(cpf, 10) and int(cpf[10]) == calc(cpf, 11)


def validar_email(e: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', e))


def validar_telefone(t: str) -> bool:
    return len(re.sub(r'\D', '', t)) in [10, 11]


def formatar_cnpj(c: str) -> str:
    c = re.sub(r'\D', '', c)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}" if len(c) == 14 else c


def formatar_cpf(c: str) -> str:
    c = re.sub(r'\D', '', c)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else c


def formatar_cep(c: str) -> str:
    c = re.sub(r'\D', '', c)
    return f"{c[:5]}-{c[5:]}" if len(c) == 8 else c


def formatar_telefone(t: str) -> str:
    t = re.sub(r'\D', '', t)
    if len(t) == 11: return f"({t[:2]}) {t[2:7]}-{t[7:]}"
    if len(t) == 10: return f"({t[:2]}) {t[2:6]}-{t[6:]}"
    return t


# =============================================================================
# CÁLCULO DE HONORÁRIOS — INTERNO
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
    base = {'MEI': 180, 'Simples Nacional': 650, 'Lucro Presumido': 1400, 'Lucro Real': 2600}.get(regime, 650)
    ff = 0.8 if fat <= 10000 else (1.0 if fat <= 30000 else (1.35 if fat <= 100000 else (1.7 if fat <= 300000 else (2.2 if fat <= 1000000 else 3.0))))
    add = (notas // 20) * 90 + min(func * 55, 1500) + (250 if est else 0) + filiais * 400 + (500 if imp_ext else 0)
    return round((base * ff + add) * (1.35 if sit == 'irregular' else 1.0), 2)


def calcular_honorario_pf(dados: Dict) -> float:
    renda = float(dados.get('renda_mensal', 0))
    ff = 1.0 if renda <= 5000 else (1.5 if renda <= 15000 else (2.0 if renda <= 50000 else 2.8))
    extras = (120 if dados.get('possui_bens') else 0) + (180 if dados.get('possui_investimentos') else 0) + (300 if dados.get('renda_exterior') else 0) + (150 if dados.get('autonomo') else 0)
    return round(250 * ff + extras, 2)


# =============================================================================
# COMPONENTES VISUAIS
# =============================================================================
def render_hero():
    """Hero com wordmark tipográfico refinado + cards animados de serviços."""
    st.markdown("""
    <div class="hero-wrapper">
        <span class="bsb-wordmark-line1">BSB Contabilidade</span>
        <span class="bsb-wordmark-line2">Brasília · DF</span>
        <div class="bsb-slogan">Inteligência fiscal para acelerar seu futuro.</div>
    </div>
    <div class="servicos-strip">
        <div class="srv-card">
            <span class="srv-icon">🏛️</span>
            <div class="srv-title">Contabilidade</div>
            <div class="srv-desc">Gestão contábil completa</div>
        </div>
        <div class="srv-card">
            <span class="srv-icon">📊</span>
            <div class="srv-title">Tributário</div>
            <div class="srv-desc">Planejamento e economia fiscal</div>
        </div>
        <div class="srv-card">
            <span class="srv-icon">🧾</span>
            <div class="srv-title">Imposto de Renda</div>
            <div class="srv-desc">IRPJ, IRPF e obrigações</div>
        </div>
        <div class="srv-card">
            <span class="srv-icon">⚖️</span>
            <div class="srv-title">Legalização</div>
            <div class="srv-desc">Abertura e regularização</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_lgpd():
    st.markdown("""
    <div class="lgpd-box">
        <div class="lgpd-icon">🔒</div>
        <div class="lgpd-text">
            <strong>LGPD — Lei 13.709/2018:</strong>
            Seus dados são <strong>confidenciais</strong> e utilizados exclusivamente para elaboração
            de proposta de serviços. Não compartilhamos com terceiros.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_step_indicator(current_step: int):
    steps = [("1", "Perfil"), ("2", "Cadastro"), ("3", "Fiscal"), ("4", "Docs")]
    html = '<div class="step-track">'
    for i, (num, label) in enumerate(steps):
        step_num = i + 1
        if step_num < current_step:
            css, label_css, icon = "done", "", "✓"
        elif step_num == current_step:
            css, label_css, icon = "active", "active", num
        else:
            css, label_css, icon = "pending", "", num
        html += f'<div class="step-node"><div class="step-circle {css}">{icon}</div><span class="step-label {label_css}">{label}</span></div>'
        if i < len(steps) - 1:
            conn = "done" if step_num < current_step else ""
            html += f'<div class="step-connector {conn}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def card_title(icon: str, text: str):
    st.markdown(f'<div class="card-title"><span class="card-title-icon">{icon}</span>{text}</div>', unsafe_allow_html=True)


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
    """, unsafe_allow_html=True)
    card_title("🚀", "Como você deseja ser atendido?")
    st.markdown("""
    <p style="font-size:0.8rem; color:#334155; margin-bottom:1.1rem; line-height:1.5;">
        Selecione o perfil que melhor descreve sua necessidade para que possamos personalizar sua proposta.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢  Pessoa Jurídica\nEmpresas · MEI · Startups", use_container_width=True):
            st.session_state.perfil = 'PJ'
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("👤  Pessoa Física\nAutônomos · Profissionais · IR", use_container_width=True):
            st.session_state.perfil = 'PF'
            st.session_state.step = 1
            st.rerun()

    st.markdown("""
    <div style="margin-top:1rem;padding:10px 14px;background:rgba(79,142,247,0.04);border-radius:9px;border:1px solid rgba(79,142,247,0.10);">
        <p style="font-size:0.76rem;color:#334155;margin:0;text-align:center;line-height:1.55;">
            ⏱ Preenchimento em <strong style="color:#4f8ef7">3 a 5 minutos</strong> ·
            Proposta personalizada em até <strong style="color:#4f8ef7">24 horas úteis</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ETAPA 1 — DADOS CADASTRAIS
# =============================================================================
def etapa_dados_cadastrais():
    if st.session_state.perfil == 'PJ':
        _etapa_cadastral_pj(st.session_state.dados_cadastrais)
    else:
        _etapa_cadastral_pf(st.session_state.dados_cadastrais)


def _etapa_cadastral_pj(dados: Dict):
    # ── Card: Dados da Empresa ──────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("🏢", "Dados da Empresa")

    col1, col2 = st.columns([3, 1])
    with col1:
        cnpj_input = st.text_input("CNPJ *", value=dados.get('cnpj', ''), placeholder="00.000.000/0000-00", key='cnpj_input')
    with col2:
        st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
        consultar = st.button("🔍 Buscar", use_container_width=True, type="secondary", key='btn_cnpj')

    if consultar:
        cnpj_clean = re.sub(r'\D', '', cnpj_input)
        if not validar_cnpj(cnpj_clean):
            st.error("❌ CNPJ inválido. Verifique os dígitos.")
        else:
            with st.spinner("Consultando Receita Federal..."):
                resultado = consulta_cnpj(cnpj_clean)
            if resultado:
                cnae_desc = resultado.get('cnae_fiscal_descricao', '')
                cnae_cod = str(resultado.get('cnae_fiscal', ''))
                if not cnae_desc and cnae_cod:
                    cnae_desc = consulta_cnae(cnae_cod)
                cnaes_sec = resultado.get('cnaes_secundarios', [])
                socios = resultado.get('qsa', [])

                # Natureza jurídica — trata dict ou string
                nj = resultado.get('natureza_juridica', '')
                if isinstance(nj, dict):
                    nj = nj.get('descricao', '')

                st.session_state.dados_cadastrais.update({
                    'cnpj': formatar_cnpj(cnpj_clean),
                    'razao_social': resultado.get('razao_social', ''),
                    'nome_fantasia': resultado.get('nome_fantasia', '') or resultado.get('razao_social', ''),
                    'natureza_juridica': resultado.get('descricao_natureza_juridica', '') or nj,
                    'situacao': resultado.get('descricao_situacao_cadastral', '') or str(resultado.get('situacao_cadastral', '')),
                    'data_abertura': resultado.get('data_inicio_atividade', '') or resultado.get('data_abertura', ''),
                    'porte': resultado.get('descricao_porte', '') or resultado.get('porte', ''),
                    'capital_social': resultado.get('capital_social', 0),
                    'cnae_principal_cod': cnae_cod,
                    'cnae_principal_desc': cnae_desc,
                    'cnaes_secundarios': [f"{c.get('codigo','')}: {c.get('descricao','')}" for c in cnaes_sec[:5]],
                    'socios': [{'nome': s.get('nome_socio',''), 'qualificacao': s.get('qualificacao_socio',''), 'faixa_etaria': s.get('faixa_etaria','')} for s in socios],
                    'email_receita': resultado.get('email', ''),
                    'cep': resultado.get('cep', ''),
                    'logradouro': resultado.get('logradouro', ''),
                    'numero': resultado.get('numero', ''),
                    'complemento': resultado.get('complemento', ''),
                    'bairro': resultado.get('bairro', ''),
                    'municipio': resultado.get('municipio', ''),
                    'uf': resultado.get('uf', ''),
                })
                st.session_state.cnpj_consultado = True
                st.success("✅ Empresa localizada — campos preenchidos automaticamente.")
                st.rerun()
            else:
                st.error("❌ CNPJ não encontrado ou serviço temporariamente indisponível. Preencha manualmente.")

    if st.session_state.get('cnpj_consultado'):
        st.markdown('<div class="auto-badge">⚡ Preenchido via Receita Federal</div>', unsafe_allow_html=True)

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
        capital_social = st.number_input("Capital Social (R$)", value=float(dados.get('capital_social', 0)), min_value=0.0, step=1000.0, format="%.2f")
        segmento = st.selectbox(
            "Segmento / Setor",
            [""] + SEGMENTOS_PJ,
            index=SEGMENTOS_PJ.index(dados.get('segmento', '')) + 1 if dados.get('segmento') in SEGMENTOS_PJ else 0
        )

    col1, col2 = st.columns(2)
    with col1:
        cnae_desc = st.text_input("CNAE Principal", value=dados.get('cnae_principal_desc', ''))
    with col2:
        cnae_cod = st.text_input("Código CNAE", value=dados.get('cnae_principal_cod', ''))

    if dados.get('cnaes_secundarios'):
        with st.expander("📋 CNAEs Secundários"):
            for c in dados['cnaes_secundarios']:
                st.markdown(f"<div style='font-size:0.78rem;color:#64748b;padding:2px 0;'>• {c}</div>", unsafe_allow_html=True)

    if dados.get('socios'):
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-bottom:0.7rem;"><span class="card-title-icon">👥</span>Quadro Societário</div>', unsafe_allow_html=True)
        for s in dados['socios']:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='font-size:0.82rem;color:#cbd5e1;font-weight:600;'>{s.get('nome','')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.72rem;color:#475569;'>{s.get('qualificacao','')}</div>", unsafe_allow_html=True)
            with col2:
                if s.get('faixa_etaria'):
                    st.markdown(f"<div style='font-size:0.72rem;color:#334155;'>Faixa etária: {s.get('faixa_etaria','')}</div>", unsafe_allow_html=True)

    st.session_state.dados_cadastrais.update({
        'cnpj': cnpj_input,
        'razao_social': razao_social,
        'nome_fantasia': nome_fantasia,
        'natureza_juridica': natureza_juridica,
        'situacao': situacao,
        'data_abertura': data_abertura,
        'porte': porte,
        'capital_social': capital_social,
        'segmento': segmento,
        'cnae_principal_cod': cnae_cod,
        'cnae_principal_desc': cnae_desc,
    })
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Card: Endereço ──────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📍", "Endereço")
    _bloco_endereco(dados, sufixo='pj')
    st.markdown('</div>', unsafe_allow_html=True)

    _botoes_navegacao(0, 2, validar_pj=True)


def _etapa_cadastral_pf(dados: Dict):
    # ── Card: Dados Pessoais ────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("👤", "Dados Pessoais")

    col1, col2 = st.columns(2)
    with col1:
        cpf = st.text_input("CPF *", value=dados.get('cpf', ''), placeholder="000.000.000-00")
        nome = st.text_input("Nome Completo *", value=dados.get('nome', ''))
        data_nasc = st.date_input(
            "Data de Nascimento *",
            value=datetime.strptime(dados['data_nascimento'], '%d/%m/%Y').date() if dados.get('data_nascimento') else date(1990, 1, 1),
            min_value=date(1900, 1, 1), max_value=date.today()
        )
    with col2:
        nacionalidade = st.text_input("Nacionalidade", value=dados.get('nacionalidade', 'Brasileira'))
        estado_civil = st.selectbox(
            "Estado Civil",
            ["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
            index=["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"].index(dados.get('estado_civil', 'Solteiro(a)')) if dados.get('estado_civil') in ["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"] else 0
        )
        # Profissão como selectbox com opções
        profissao_idx = PROFISSOES.index(dados.get('profissao', 'Outro')) if dados.get('profissao') in PROFISSOES else len(PROFISSOES) - 1
        profissao = st.selectbox("Profissão / Ocupação", PROFISSOES, index=profissao_idx)

    st.session_state.dados_cadastrais.update({
        'cpf': cpf, 'nome': nome,
        'data_nascimento': data_nasc.strftime('%d/%m/%Y'),
        'nacionalidade': nacionalidade,
        'estado_civil': estado_civil,
        'profissao': profissao,
    })
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Card: Endereço ──────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📍", "Endereço")
    _bloco_endereco(dados, sufixo='pf')
    st.markdown('</div>', unsafe_allow_html=True)

    _botoes_navegacao(0, 2, validar_pf=True)


def _bloco_endereco(dados: Dict, sufixo: str):
    """Bloco de endereço reutilizável com busca automática de CEP."""
    col1, col2 = st.columns([3, 1])
    with col1:
        cep_val = st.text_input("CEP *", value=dados.get('cep', ''), placeholder="00000-000", key=f'cep_{sufixo}')
    with col2:
        st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
        buscar = st.button("📍 Buscar", use_container_width=True, type="secondary", key=f'btn_cep_{sufixo}')

    if buscar:
        cep_clean = re.sub(r'\D', '', cep_val)
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
                st.success("✅ Endereço encontrado!")
                st.rerun()
            else:
                st.error("CEP não encontrado. Preencha manualmente.")

    dados = st.session_state.dados_cadastrais
    col1, col2 = st.columns(2)
    with col1:
        logradouro = st.text_input("Logradouro", value=dados.get('logradouro', ''), key=f'log_{sufixo}')
        bairro = st.text_input("Bairro", value=dados.get('bairro', ''), key=f'bairro_{sufixo}')
        municipio = st.text_input("Município", value=dados.get('municipio', ''), key=f'mun_{sufixo}')
    with col2:
        numero = st.text_input("Número", value=dados.get('numero', ''), key=f'num_{sufixo}')
        complemento = st.text_input("Complemento", value=dados.get('complemento', ''), key=f'comp_{sufixo}')
        estados = lista_estados()
        uf_default = dados.get('uf', 'DF')
        uf_idx = estados.index(uf_default) if uf_default in estados else 6
        uf = st.selectbox("UF", estados, index=uf_idx, key=f'uf_{sufixo}')

    st.session_state.dados_cadastrais.update({
        'cep': cep_val,
        'logradouro': logradouro, 'numero': numero, 'complemento': complemento,
        'bairro': bairro, 'municipio': municipio, 'uf': uf,
    })


def _botoes_navegacao(voltar_step: int, proximo_step: int, validar_pj=False, validar_pf=False):
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
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
                if not validar_cnpj(re.sub(r'\D', '', d.get('cnpj', ''))):
                    erros.append("CNPJ inválido ou não preenchido.")
                if not d.get('razao_social', '').strip():
                    erros.append("Razão Social é obrigatória.")
            if validar_pf:
                if not validar_cpf(re.sub(r'\D', '', d.get('cpf', ''))):
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
# ETAPA 2 — FISCAL / OPERACIONAL
# =============================================================================
def etapa_dados_operacionais():
    if st.session_state.perfil == 'PJ':
        _etapa_fiscal_pj()
    else:
        _etapa_fiscal_pf()


def _etapa_fiscal_pj():
    op = st.session_state.dados_operacionais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📊", "Configuração Fiscal")

    col1, col2 = st.columns(2)
    with col1:
        regime = st.selectbox("Regime Tributário *", ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"],
            index=["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"].index(op.get('regime', 'Simples Nacional')) if op.get('regime') else 0)
        faturamento = st.number_input("Faturamento médio mensal (R$) *", min_value=0.0, step=1000.0, format="%.2f", value=float(op.get('faturamento_mensal', 0)))
        num_notas = st.number_input("Notas fiscais emitidas/mês *", min_value=0, step=1, value=int(op.get('num_notas', 0)))
        num_filiais = st.number_input("Número de filiais", min_value=0, step=1, value=int(op.get('num_filiais', 0)), help="0 = apenas matriz")
    with col2:
        num_funcionarios = st.number_input("Número de funcionários", min_value=0, step=1, value=int(op.get('num_funcionarios', 0)))
        tem_estoque = st.checkbox("Possui controle de estoque?", value=op.get('tem_estoque', False))
        importa_exporta = st.checkbox("Realiza importação/exportação?", value=op.get('importa_exporta', False))
        tem_simples_ativo = st.checkbox("Optante pelo Simples Nacional?", value=op.get('tem_simples_ativo', False))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        situacao_fiscal = st.radio("Situação fiscal *", ["Em dia", "Com pendências / irregularidades"],
            index=1 if op.get('situacao_fiscal') == 'irregular' else 0)
        contabilidade_atual = st.radio("Possui contador atualmente?", ["Não", "Sim, quero trocar", "Sim, consultoria adicional"],
            index=["Não", "Sim, quero trocar", "Sim, consultoria adicional"].index(op.get('contabilidade_atual', 'Não')) if op.get('contabilidade_atual') in ["Não", "Sim, quero trocar", "Sim, consultoria adicional"] else 0)
    with col2:
        tipo_servico = st.multiselect("Serviços de interesse",
            ["Contabilidade Geral", "Abertura de Empresa", "Encerramento de Empresa",
             "BPO Financeiro", "Folha de Pagamento", "Planejamento Tributário",
             "Consultoria Fiscal", "Regularização Fiscal", "Certidões e Declarações"],
            default=op.get('tipo_servico', []))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📞", "Dados de Contato")

    col1, col2 = st.columns(2)
    with col1:
        contato_nome = st.text_input("Nome do responsável *", value=op.get('contato_nome', ''))
        contato_email = st.text_input("E-mail *", value=op.get('contato_email', ''))
    with col2:
        contato_telefone = st.text_input("Telefone / WhatsApp *", value=op.get('contato_telefone', ''), placeholder="(00) 00000-0000")
        expectativa = st.selectbox("Início desejado dos serviços",
            ["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"],
            index=["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"].index(op.get('expectativa', 'Imediato (o mais rápido possível)')) if op.get('expectativa') in ["Imediato (o mais rápido possível)", "Próximo mês", "Em até 3 meses", "Apenas cotação por enquanto"] else 0)

    observacoes = st.text_area("Observações ou necessidades específicas", value=op.get('observacoes', ''), placeholder="Descreva qualquer informação adicional relevante...", height=80)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            if not contato_nome.strip(): erros.append("Nome do responsável é obrigatório.")
            if not validar_email(contato_email): erros.append("E-mail inválido.")
            if not validar_telefone(contato_telefone): erros.append("Telefone inválido (10 ou 11 dígitos).")
            if faturamento <= 0: erros.append("Informe o faturamento médio mensal.")
            if erros:
                for e in erros: st.error(f"❌ {e}")
            else:
                st.session_state.dados_operacionais = {
                    'regime': regime, 'faturamento_mensal': faturamento,
                    'num_notas': num_notas, 'num_filiais': num_filiais,
                    'num_funcionarios': num_funcionarios,
                    'tem_estoque': tem_estoque, 'importa_exporta': importa_exporta,
                    'tem_simples_ativo': tem_simples_ativo,
                    'situacao_fiscal': 'irregular' if 'pendências' in situacao_fiscal else 'regular',
                    'contabilidade_atual': contabilidade_atual,
                    'tipo_servico': tipo_servico,
                    'contato_nome': contato_nome, 'contato_email': contato_email,
                    'contato_telefone': formatar_telefone(contato_telefone),
                    'expectativa': expectativa, 'observacoes': observacoes,
                }
                st.session_state.step = 3
                st.rerun()


def _etapa_fiscal_pf():
    op = st.session_state.dados_operacionais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📊", "Perfil Financeiro")

    col1, col2 = st.columns(2)
    with col1:
        renda_mensal = st.number_input("Renda mensal aproximada (R$) *", min_value=0.0, step=500.0, format="%.2f", value=float(op.get('renda_mensal', 0)))
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
        tipo_declaracao = st.radio("Tipo preferido de declaração",
            ["Simplificada", "Completa (deduções)", "Não sei — quero orientação"],
            index=["Simplificada", "Completa (deduções)", "Não sei — quero orientação"].index(op.get('tipo_declaracao', 'Simplificada')) if op.get('tipo_declaracao') in ["Simplificada", "Completa (deduções)", "Não sei — quero orientação"] else 0)
    with col2:
        tipo_servico_pf = st.multiselect("Serviços de interesse",
            ["Imposto de Renda (IRPF)", "Planejamento Patrimonial",
             "Consultoria Tributária", "Regularização junto à Receita",
             "Declaração em Atraso", "Herança / Doação / Inventário"],
            default=op.get('tipo_servico', []))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📞", "Dados de Contato")

    col1, col2 = st.columns(2)
    with col1:
        contato_email = st.text_input("E-mail *", value=op.get('contato_email', ''), key='email_pf')
    with col2:
        contato_telefone = st.text_input("Telefone / WhatsApp *", value=op.get('contato_telefone', ''), placeholder="(00) 00000-0000", key='tel_pf')

    expectativa_pf = st.selectbox("Início desejado",
        ["Imediato", "Próximo mês", "Apenas cotação"],
        index=["Imediato", "Próximo mês", "Apenas cotação"].index(op.get('expectativa', 'Imediato')) if op.get('expectativa') in ["Imediato", "Próximo mês", "Apenas cotação"] else 0)
    observacoes_pf = st.text_area("Observações", value=op.get('observacoes', ''), placeholder="Informações adicionais...", height=75)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            if not validar_email(contato_email): erros.append("E-mail inválido.")
            if not validar_telefone(contato_telefone): erros.append("Telefone inválido.")
            if renda_mensal <= 0: erros.append("Informe a renda mensal aproximada.")
            if erros:
                for e in erros: st.error(f"❌ {e}")
            else:
                st.session_state.dados_operacionais = {
                    'renda_mensal': renda_mensal, 'possui_bens': possui_bens,
                    'possui_investimentos': possui_investimentos, 'renda_exterior': renda_exterior,
                    'autonomo': autonomo, 'pensao': pensao,
                    'socio_empresa': socio_empresa, 'heranca': heranca,
                    'tipo_declaracao': tipo_declaracao, 'tipo_servico': tipo_servico_pf,
                    'contato_email': contato_email,
                    'contato_telefone': formatar_telefone(contato_telefone),
                    'expectativa': expectativa_pf, 'observacoes': observacoes_pf,
                }
                st.session_state.step = 3
                st.rerun()


# =============================================================================
# ETAPA 3 — DOCUMENTOS + CÂMERA
# =============================================================================
def etapa_upload():
    perfil = st.session_state.perfil

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📎", "Documentação para Análise")

    st.markdown("""
    <p style="font-size:0.78rem;color:#334155;margin-bottom:1rem;line-height:1.5;">
        O envio é <strong style="color:#64748b">opcional</strong> neste momento — nossa equipe poderá solicitar
        posteriormente. Mas enviar agora <strong style="color:#64748b">agiliza sua proposta</strong>.
        Você pode <strong style="color:#64748b">enviar arquivo</strong> ou <strong style="color:#64748b">fotografar com a câmera</strong> do celular.
    </p>
    """, unsafe_allow_html=True)

    docs_salvos = []

    if perfil == 'PJ':
        _doc_upload_com_camera("📄 Cartão CNPJ", "cartao_cnpj", "Frente do cartão CNPJ emitido pela Receita Federal")
        _doc_upload_com_camera("📝 Contrato / Estatuto Social", "contrato_social", "Última versão consolidada")
        _doc_upload_com_camera("📋 Últimas guias pagas (DAS, GPS)", "ultimas_guias", "DAS, GPS, DARF, etc.")
        _doc_upload_com_camera("📊 Balanço / DRE (se disponível)", "balanco_dre", "Último exercício disponível")
        docs_salvos = [st.session_state.get(f'doc_{k}') for k in ['cartao_cnpj', 'contrato_social', 'ultimas_guias', 'balanco_dre'] if st.session_state.get(f'doc_{k}')]
    else:
        _doc_upload_com_camera("🪪 RG, CNH ou Passaporte", "doc_id", "Frente e verso — legível")
        _doc_upload_com_camera("🏠 Comprovante de Residência", "comp_res", "Últimos 90 dias")
        _doc_upload_com_camera("📋 Última declaração de IR", "declaracao_ir", "Recibo de entrega da última declaração")
        _doc_upload_com_camera("💼 Informe de Rendimentos", "informe_rend", "Todos os informes do ano")
        docs_salvos = [st.session_state.get(f'doc_{k}') for k in ['doc_id', 'comp_res', 'declaracao_ir', 'informe_rend'] if st.session_state.get(f'doc_{k}')]

    if docs_salvos:
        st.markdown(f'<div class="auto-badge">📎 {len(docs_salvos)} arquivo(s) anexado(s)</div>', unsafe_allow_html=True)

    st.session_state.documentos = docs_salvos
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("✅  Finalizar Cadastro", use_container_width=True, type="primary"):
            if st.session_state.perfil == 'PJ':
                st.session_state.honorario_interno = calcular_honorario_pj(st.session_state.dados_operacionais)
            else:
                st.session_state.honorario_interno = calcular_honorario_pf(st.session_state.dados_operacionais)
            st.session_state.step = 4
            st.rerun()


def _doc_upload_com_camera(label: str, chave: str, descricao: str):
    """Componente de upload com alternativa de câmera (foto direta no celular)."""
    key_arquivo = f'doc_{chave}'
    key_camera = f'cam_{chave}'
    key_modo = f'modo_{chave}'

    if key_modo not in st.session_state:
        st.session_state[key_modo] = 'arquivo'

    st.markdown(f"""
    <div style="margin-bottom:0.3rem;">
        <div style="font-size:0.73rem;font-weight:700;color:#64748b;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:3px;">{label}</div>
        <div style="font-size:0.68rem;color:#334155;margin-bottom:6px;">{descricao}</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        arquivo = st.file_uploader(
            f"Enviar arquivo — {label}",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            key=f'up_{chave}',
            label_visibility='collapsed'
        )
        if arquivo:
            st.session_state[key_arquivo] = arquivo
    with col_b:
        foto = st.camera_input(
            f"Tirar foto — {label}",
            key=f'cam_{chave}',
            label_visibility='collapsed',
            help="Abra a câmera do dispositivo para fotografar o documento"
        )
        if foto:
            st.session_state[key_arquivo] = foto

    if st.session_state.get(key_arquivo):
        st.markdown(f'<div class="auto-badge" style="margin-bottom:10px;">✓ Documento recebido</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider" style="margin:0.6rem 0;">', unsafe_allow_html=True)


# =============================================================================
# ETAPA 4 — SUCESSO
# =============================================================================
def etapa_sucesso():
    st.balloons()

    dados_cad = st.session_state.dados_cadastrais
    dados_op = st.session_state.dados_operacionais
    perfil = st.session_state.perfil

    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1.4rem 0;animation:fadeSlideDown 0.7s ease both;">
        <div style="font-size:3rem;margin-bottom:0.8rem;">✅</div>
        <div style="font-family:'Instrument Serif',Georgia,serif !important;font-style:italic;font-size:1.9rem;color:#e2e8f0;line-height:1.1;margin-bottom:0.5rem;">
            Cadastro Recebido
        </div>
        <p style="font-size:0.82rem;color:#334155;max-width:360px;margin:0 auto;line-height:1.6;">
            Obrigado pela confiança na <strong style="color:#4f8ef7">BSB Contabilidade</strong>.<br>
            Nossa equipe enviará uma proposta personalizada em até
            <strong style="color:#4f8ef7">24 horas úteis</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    card_title("📋", "Resumo do Cadastro")

    col1, col2 = st.columns(2)
    with col1:
        if perfil == 'PJ':
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;'>Empresa</div><div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;'>{dados_cad.get('razao_social','—')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-top:8px;'>CNPJ</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_cad.get('cnpj','—')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-top:8px;'>Regime</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_op.get('regime','—')}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;'>Nome</div><div style='color:#e2e8f0;font-weight:600;font-size:0.9rem;'>{dados_cad.get('nome','—')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-top:8px;'>CPF</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_cad.get('cpf','—')}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='font-size:0.8rem;color:#64748b;'>E-mail</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_op.get('contato_email','—')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-top:8px;'>Telefone</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_op.get('contato_telefone','—')}</div>", unsafe_allow_html=True)
        if dados_op.get('expectativa'):
            st.markdown(f"<div style='font-size:0.8rem;color:#64748b;margin-top:8px;'>Início desejado</div><div style='color:#e2e8f0;font-size:0.85rem;'>{dados_op.get('expectativa')}</div>", unsafe_allow_html=True)

    if dados_op.get('tipo_servico'):
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#475569;margin-bottom:6px;">Serviços solicitados</div>', unsafe_allow_html=True)
        for s in dados_op['tipo_servico']:
            st.markdown(f"<div style='font-size:0.8rem;color:#93b4fb;padding:2px 0;'>✓ {s}</div>", unsafe_allow_html=True)

    n_docs = len(st.session_state.documentos)
    if n_docs > 0:
        st.markdown(f"<div style='margin-top:10px;font-size:0.78rem;color:#34d399;'>📎 {n_docs} documento(s) anexado(s)</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Novo Cadastro", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
