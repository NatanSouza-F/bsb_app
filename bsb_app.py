"""
BSB Contabilidade — Plataforma de Cadastro Inteligente v4.0
"""

import streamlit as st
import requests
import re
import io
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
# CSS v4.0 — WORDMARK PULSE-STYLE + UNIFORMIDADE + REFINAMENTO GERAL
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ─── BASE ──────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ─── BACKGROUND ────────────────────────────────────────────────────── */
.stApp {
    background: #070e1a;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -25%; left: -10%;
    width: 65%; height: 65%;
    background: radial-gradient(ellipse, rgba(26,75,216,0.11) 0%, transparent 68%);
    pointer-events: none; z-index: 0;
    animation: breathe 9s ease-in-out infinite;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -15%; right: -5%;
    width: 45%; height: 45%;
    background: radial-gradient(ellipse, rgba(5,155,195,0.06) 0%, transparent 68%);
    pointer-events: none; z-index: 0;
    animation: breathe 13s ease-in-out infinite reverse;
}
@keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.55; }
    50%       { transform: scale(1.1); opacity: 1; }
}

/* ─── CONTAINER ─────────────────────────────────────────────────────── */
.block-container {
    max-width: 572px !important;
    padding: 1.2rem 1.1rem 3rem !important;
    position: relative; z-index: 1;
}

/* ─── HERO ──────────────────────────────────────────────────────────── */
.hero-wrapper {
    text-align: center;
    padding: 2rem 0 0.4rem;
    animation: fadeDown 0.75s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/*
  WORDMARK — estilo Pulse:
  • Plus Jakarta Sans Bold
  • Gradiente azul horizontal com leve drop-shadow luminoso
  • Sem serifa, sem itálico — limpo e forte
*/
.bsb-wordmark {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: clamp(2.1rem, 7.5vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -0.025em;
    background: linear-gradient(90deg, #3a7bd5 0%, #5ba3f5 40%, #40c8e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 18px rgba(58,123,213,0.38));
    display: block;
    line-height: 1.05;
}
.bsb-sub {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #2d3f58;
    display: block;
    margin-top: 4px;
}
.bsb-slogan {
    font-size: 0.8rem;
    font-weight: 400;
    color: #2d3f58;
    margin-top: 0.45rem;
    letter-spacing: 0.01em;
}

/* ─── SERVICE CARDS STRIP ───────────────────────────────────────────── */
.srv-strip {
    display: flex;
    gap: 9px;
    margin: 1.5rem 0 0.1rem;
    overflow-x: auto;
    padding-bottom: 3px;
    scrollbar-width: none;
}
.srv-strip::-webkit-scrollbar { display: none; }
.srv-card {
    flex: 1; min-width: 106px;
    background: rgba(255,255,255,0.022);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 13px;
    padding: 13px 8px 11px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: cardIn 0.55s cubic-bezier(0.16,1,0.3,1) both;
}
.srv-card:nth-child(1) { animation-delay: 0.07s; }
.srv-card:nth-child(2) { animation-delay: 0.14s; }
.srv-card:nth-child(3) { animation-delay: 0.21s; }
.srv-card:nth-child(4) { animation-delay: 0.28s; }
@keyframes cardIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.srv-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1.5px;
    background: linear-gradient(90deg, transparent 0%, rgba(58,123,213,0.55) 50%, transparent 100%);
    animation: shimLine 3.5s ease-in-out infinite;
}
@keyframes shimLine {
    0%,100% { opacity: 0; transform: scaleX(0.35); }
    50%      { opacity: 1; transform: scaleX(1); }
}
.srv-icon {
    font-size: 1.35rem;
    display: block; margin-bottom: 5px;
    animation: floatY 4s ease-in-out infinite;
}
.srv-card:nth-child(2) .srv-icon { animation-delay: 0.5s; }
.srv-card:nth-child(3) .srv-icon { animation-delay: 1.0s; }
.srv-card:nth-child(4) .srv-icon { animation-delay: 1.5s; }
@keyframes floatY {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-2.5px); }
}
.srv-title {
    font-size: 0.65rem;
    font-weight: 700;
    color: #8faac8;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    line-height: 1.3;
}
.srv-desc {
    font-size: 0.6rem;
    color: #3d5069;
    margin-top: 2px;
    line-height: 1.3;
}

/* ─── LGPD BOX ──────────────────────────────────────────────────────── */
.lgpd-box {
    display: flex; gap: 10px;
    background: rgba(58,123,213,0.045);
    border: 1px solid rgba(58,123,213,0.11);
    border-radius: 9px;
    padding: 10px 13px;
    margin-bottom: 1.1rem;
    animation: fadeIn 1s ease both;
    animation-delay: 0.55s;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.lgpd-icon { font-size: 0.85rem; flex-shrink: 0; margin-top: 1px; }
.lgpd-text { font-size: 0.72rem; color: #2d3f58; line-height: 1.5; }
.lgpd-text strong { color: #536882; font-weight: 600; }

/* ─── STEP TRACK ────────────────────────────────────────────────────── */
.step-track {
    display: flex; align-items: flex-start; justify-content: center;
    margin: 1.6rem auto 1.4rem;
    max-width: 330px; width: 100%;
    animation: fadeIn 0.6s ease both; animation-delay: 0.35s;
}
.step-node {
    display: flex; flex-direction: column; align-items: center;
    gap: 4px; flex: 1; position: relative; z-index: 2;
}
.step-circle {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.72rem;
    transition: all 0.28s ease;
}
.step-circle.done   { background: #1a43cc; color: #fff; box-shadow: 0 0 10px rgba(58,123,213,0.38); }
.step-circle.active {
    background: #1a43cc; color: #fff;
    box-shadow: 0 0 0 3px rgba(58,123,213,0.16), 0 0 14px rgba(58,123,213,0.42);
    animation: ringPulse 2.3s ease-in-out infinite;
}
@keyframes ringPulse {
    0%,100% { box-shadow: 0 0 0 3px rgba(58,123,213,0.16), 0 0 14px rgba(58,123,213,0.38); }
    50%     { box-shadow: 0 0 0 6px rgba(58,123,213,0.07), 0 0 20px rgba(58,123,213,0.52); }
}
.step-circle.pending {
    background: rgba(18,28,44,0.9); color: #2d3f58;
    border: 1px solid rgba(45,63,88,0.5);
}
.step-label {
    font-size: 0.56rem; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase;
    color: #2d3f58; text-align: center; white-space: nowrap;
}
.step-label.active { color: #5ba3f5; }
.step-connector {
    flex: 1; height: 1px; background: rgba(45,63,88,0.5);
    margin-top: 14px; position: relative; z-index: 1; max-width: 34px;
}
.step-connector.done { background: #1a43cc; }

/* ─── SECTION CARD ──────────────────────────────────────────────────── */
.section-card {
    background: rgba(9,16,30,0.93);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 14px;
    padding: 1.35rem 1.3rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.5), 0 6px 20px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.025);
    animation: cardIn 0.42s cubic-bezier(0.16,1,0.3,1) both;
}

/* ─── CARD TITLE ────────────────────────────────────────────────────── */
.card-title {
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: #3d5069; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 7px;
}
.ct-icon {
    width: 24px; height: 24px; border-radius: 6px;
    background: rgba(58,123,213,0.1);
    border: 1px solid rgba(58,123,213,0.15);
    display: inline-flex; align-items: center;
    justify-content: center; font-size: 0.73rem;
}

/* ─── AUTO BADGE ────────────────────────────────────────────────────── */
.auto-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(16,185,129,0.07);
    border: 1px solid rgba(16,185,129,0.18);
    border-radius: 5px; padding: 2px 8px;
    font-size: 0.65rem; font-weight: 600;
    color: #2dd4a0; margin-bottom: 7px;
    letter-spacing: 0.03em;
}

/* ─── DIVIDER ───────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.042);
    margin: 1rem 0;
}

/* ─── LABELS ────────────────────────────────────────────────────────── */
label,
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stRadio label,
.stCheckbox label, .stDateInput label,
.stTextArea label {
    color: #536882 !important;
    font-size: 0.73rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ─── INPUTS ────────────────────────────────────────────────────────── */
input, textarea,
.stNumberInput input,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(5,11,22,0.88) !important;
    border: 1px solid rgba(255,255,255,0.065) !important;
    color: #dde6f0 !important;
    border-radius: 8px !important;
    font-size: 0.865rem !important;
    font-weight: 500 !important;
    transition: border-color 0.16s, box-shadow 0.16s !important;
    min-height: 40px !important;
}
input:focus, textarea:focus {
    border-color: rgba(58,123,213,0.5) !important;
    box-shadow: 0 0 0 3px rgba(58,123,213,0.08) !important;
}
input::placeholder, textarea::placeholder { color: #1c2d42 !important; }

/* Select */
div[data-baseweb="select"] > div {
    background: rgba(5,11,22,0.88) !important;
    border: 1px solid rgba(255,255,255,0.065) !important;
    border-radius: 8px !important;
    font-size: 0.865rem !important;
    font-weight: 500 !important;
    color: #dde6f0 !important;
    min-height: 40px !important;
}
div[data-baseweb="menu"] {
    background: #0a1525 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 9px !important;
}
div[data-baseweb="option"] { color: #b0c4d8 !important; font-size: 0.845rem !important; }
div[data-baseweb="option"]:hover { background: rgba(58,123,213,0.1) !important; }

/* Date input — forçar fundo escuro */
div[data-baseweb="datepicker"] input { color: #dde6f0 !important; }

/* ─── BUTTONS — tamanho único, uniforme ─────────────────────────────── */
.stButton > button {
    background: #1a43cc !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    /* padding uniforme para todos os botões */
    padding: 0 1rem !important;
    height: 40px !important;
    min-height: 40px !important;
    font-weight: 700 !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4), 0 3px 12px rgba(26,67,204,0.25) !important;
    transition: all 0.16s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.stButton > button:hover {
    background: #1e4bd8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4), 0 5px 18px rgba(26,67,204,0.38) !important;
}
.stButton > button:active { transform: scale(0.99) !important; }
.stButton > button[kind="secondary"] {
    background: rgba(9,16,30,0.92) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #536882 !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: rgba(58,123,213,0.3) !important;
    color: #8faac8 !important;
    background: rgba(58,123,213,0.04) !important;
}

/* ─── RADIO ─────────────────────────────────────────────────────────── */
.stRadio > div { gap: 5px !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: rgba(5,11,22,0.82) !important;
    border: 1px solid rgba(255,255,255,0.065) !important;
    border-radius: 7px !important;
    padding: 6px 11px !important;
    color: #536882 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    transition: all 0.16s !important;
    text-transform: none !important;
    letter-spacing: 0.01em !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: rgba(58,123,213,0.4) !important;
    background: rgba(26,67,204,0.09) !important;
    color: #7aaaf5 !important;
}

/* ─── CHECKBOX ──────────────────────────────────────────────────────── */
.stCheckbox > label {
    color: #536882 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0.01em !important;
}
input[type="checkbox"] { accent-color: #1a43cc !important; }

/* ─── MULTISELECT ───────────────────────────────────────────────────── */
span[data-baseweb="tag"] {
    background: rgba(26,67,204,0.18) !important;
    border: 1px solid rgba(58,123,213,0.28) !important;
    border-radius: 5px !important;
    color: #7aaaf5 !important;
    font-size: 0.73rem !important;
}

/* ─── ALERTS ────────────────────────────────────────────────────────── */
div[data-testid="stAlert"] { border-radius: 8px !important; font-size: 0.8rem !important; }
.stSuccess  { background: rgba(16,185,129,0.06) !important; border: 1px solid rgba(16,185,129,0.18) !important; }
.stError    { background: rgba(239,68,68,0.06) !important;  border: 1px solid rgba(239,68,68,0.18) !important; }
.stInfo     { background: rgba(58,123,213,0.06) !important; border: 1px solid rgba(58,123,213,0.16) !important; }
.stWarning  { background: rgba(245,158,11,0.06) !important; border: 1px solid rgba(245,158,11,0.18) !important; }

/* ─── FILE UPLOADER ─────────────────────────────────────────────────── */
div[data-testid="stFileUploader"] {
    background: rgba(5,11,22,0.65) !important;
    border: 1.5px dashed rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    transition: border-color 0.18s !important;
}
div[data-testid="stFileUploader"]:hover { border-color: rgba(58,123,213,0.32) !important; }
div[data-testid="stFileUploader"] label {
    text-transform: none !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.01em !important;
    color: #8faac8 !important;
}

/* ─── EXPANDER ──────────────────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: rgba(5,11,22,0.65) !important;
    border: 1px solid rgba(255,255,255,0.045) !important;
    border-radius: 9px !important;
}

/* ─── SCROLLBAR ─────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #070e1a; }
::-webkit-scrollbar-thumb { background: #1a2a40; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #1a43cc; }

/* ─── MOBILE ────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .block-container { padding: 0.9rem 0.8rem 2.5rem !important; }
    .section-card { padding: 1rem 0.9rem; }
    .bsb-wordmark { font-size: clamp(1.9rem, 9vw, 2.6rem); }
    .step-label { font-size: 0.5rem; }
    .srv-strip { flex-wrap: nowrap; }
}

/* ─── HIDE CHROME ───────────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# ESTADO
# =============================================================================
def init_session_state():
    defaults = {
        'step': 0, 'perfil': None,
        'dados_cadastrais': {}, 'dados_operacionais': {},
        'documentos': [], 'honorario_interno': 0.0,
        'cnpj_consultado': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()


# =============================================================================
# LISTAS
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
    "Agropecuária / Agricultura", "Alimentação / Restaurante / Delivery",
    "Comércio Varejista", "Comércio Atacadista",
    "Construção Civil / Incorporação", "Consultoria / Assessoria",
    "Educação / Treinamento", "Estética / Saúde / Bem-estar",
    "Indústria / Manufatura", "Logística / Transporte",
    "Saúde / Clínica / Laboratório", "Serviços em Geral",
    "Tecnologia / Software / SaaS", "Turismo / Hotelaria", "Outro"
]

ESTADOS = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
]


# =============================================================================
# APIs
# =============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def consulta_cnpj(cnpj: str) -> Optional[Dict]:
    c = re.sub(r'\D', '', cnpj)
    if len(c) != 14: return None
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{c}",
                         timeout=12, headers={"User-Agent": "BSB/4.0"})
        r.raise_for_status(); return r.json()
    except: return None


@st.cache_data(ttl=600, show_spinner=False)
def consulta_cep(cep: str) -> Optional[Dict]:
    c = re.sub(r'\D', '', cep)
    if len(c) != 8: return None
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cep/v2/{c}",
                         timeout=10, headers={"User-Agent": "BSB/4.0"})
        r.raise_for_status(); return r.json()
    except: return None


@st.cache_data(ttl=3600, show_spinner=False)
def consulta_cnae(codigo: str) -> str:
    c = re.sub(r'\D', '', str(codigo))
    if not c: return ""
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cnae/v1/{c}", timeout=10)
        r.raise_for_status(); return r.json().get('descricao', '')
    except: return ""


# =============================================================================
# VALIDAÇÕES E FORMATAÇÕES
# =============================================================================
def validar_cnpj(cnpj: str) -> bool:
    c = re.sub(r'\D', '', cnpj)
    if len(c) != 14 or c == c[0]*14: return False
    def dig(c, p):
        s = sum(int(c[i])*p[i] for i in range(len(p))); r = s%11
        return 0 if r < 2 else 11-r
    return c[-2:] == f"{dig(c,[5,4,3,2,9,8,7,6,5,4,3,2])}{dig(c,[6,5,4,3,2,9,8,7,6,5,4,3,2])}"

def validar_cpf(cpf: str) -> bool:
    c = re.sub(r'\D', '', cpf)
    if len(c) != 11 or c == c[0]*11: return False
    def dig(c, p):
        s = sum(int(c[i])*(p-i) for i in range(p-1)); r=(s*10)%11
        return 0 if r >= 10 else r
    return int(c[9])==dig(c,10) and int(c[10])==dig(c,11)

def validar_email(e: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', e))

def validar_telefone(t: str) -> bool:
    return len(re.sub(r'\D','',t)) in [10,11]

def fmt_cnpj(c: str) -> str:
    c=re.sub(r'\D','',c)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}" if len(c)==14 else c

def fmt_cpf(c: str) -> str:
    c=re.sub(r'\D','',c)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c)==11 else c

def fmt_cep(c: str) -> str:
    c=re.sub(r'\D','',c)
    return f"{c[:5]}-{c[5:]}" if len(c)==8 else c

def fmt_tel(t: str) -> str:
    t=re.sub(r'\D','',t)
    if len(t)==11: return f"({t[:2]}) {t[2:7]}-{t[7:]}"
    if len(t)==10: return f"({t[:2]}) {t[2:6]}-{t[6:]}"
    return t

def fmt_moeda(v: float) -> str:
    return f"R$ {v:,.2f}".replace(',','X').replace('.',',').replace('X','.')

def fmt_data_br(d) -> str:
    """Converte date ou string ISO para DD/MM/AAAA."""
    if isinstance(d, date):
        return d.strftime('%d/%m/%Y')
    if isinstance(d, str):
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'):
            try: return datetime.strptime(d, fmt).strftime('%d/%m/%Y')
            except: pass
    return str(d)


# =============================================================================
# HONORÁRIOS — INTERNO
# =============================================================================
def calcular_honorario_pj(d: Dict) -> float:
    base = {'MEI':180,'Simples Nacional':650,'Lucro Presumido':1400,'Lucro Real':2600}.get(d.get('regime','Simples Nacional'),650)
    fat = float(d.get('faturamento_mensal',0))
    ff = 0.8 if fat<=10000 else (1.0 if fat<=30000 else (1.35 if fat<=100000 else (1.7 if fat<=300000 else (2.2 if fat<=1000000 else 3.0))))
    add = (int(d.get('num_notas',0))//20)*90 + min(int(d.get('num_funcionarios',0))*55,1500) + (250 if d.get('tem_estoque') else 0) + int(d.get('num_filiais',0))*400 + (500 if d.get('importa_exporta') else 0)
    return round((base*ff+add)*(1.35 if d.get('situacao_fiscal')=='irregular' else 1.0), 2)

def calcular_honorario_pf(d: Dict) -> float:
    r=float(d.get('renda_mensal',0))
    ff=1.0 if r<=5000 else (1.5 if r<=15000 else (2.0 if r<=50000 else 2.8))
    ex=(120 if d.get('possui_bens') else 0)+(180 if d.get('possui_investimentos') else 0)+(300 if d.get('renda_exterior') else 0)+(150 if d.get('autonomo') else 0)
    return round(250*ff+ex, 2)


# =============================================================================
# FICHA DE CADASTRO — geração de texto estruturado para download
# =============================================================================
def gerar_ficha_texto() -> str:
    dc = st.session_state.dados_cadastrais
    op = st.session_state.dados_operacionais
    perf = st.session_state.perfil
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')

    linhas = []
    SEP  = "=" * 56
    SEP2 = "-" * 56

    linhas += [
        SEP,
        "  BSB CONTABILIDADE — FICHA DE CADASTRO",
        f"  Gerado em: {agora}",
        SEP, ""
    ]

    if perf == 'PJ':
        linhas += [
            "DADOS DA EMPRESA",
            SEP2,
            f"Razão Social .....: {dc.get('razao_social','—')}",
            f"Nome Fantasia ....: {dc.get('nome_fantasia','—')}",
            f"CNPJ .............: {dc.get('cnpj','—')}",
            f"Natureza Jurídica : {dc.get('natureza_juridica','—')}",
            f"Situação Cadastral: {dc.get('situacao','—')}",
            f"Data de Abertura .: {dc.get('data_abertura','—')}",
            f"Porte ............: {dc.get('porte','—')}",
            f"Capital Social ...: {fmt_moeda(float(dc.get('capital_social',0)))}",
            f"Segmento .........: {dc.get('segmento','—')}",
            f"CNAE Principal ...: {dc.get('cnae_principal_desc','—')} ({dc.get('cnae_principal_cod','—')})",
            "",
        ]
        if dc.get('cnaes_secundarios'):
            linhas.append("CNAEs Secundários.:")
            for c in dc['cnaes_secundarios']:
                linhas.append(f"  • {c}")
            linhas.append("")
        if dc.get('socios'):
            linhas.append("Quadro Societário.:")
            for s in dc['socios']:
                linhas.append(f"  • {s.get('nome','—')} — {s.get('qualificacao','—')}")
            linhas.append("")
    else:
        linhas += [
            "DADOS PESSOAIS",
            SEP2,
            f"Nome Completo ....: {dc.get('nome','—')}",
            f"CPF ..............: {dc.get('cpf','—')}",
            f"Data de Nascimento: {fmt_data_br(dc.get('data_nascimento','—'))}",
            f"Estado Civil .....: {dc.get('estado_civil','—')}",
            f"Profissão ........: {dc.get('profissao','—')}",
            f"Nacionalidade ....: {dc.get('nacionalidade','—')}",
            "",
        ]

    linhas += [
        "ENDEREÇO",
        SEP2,
        f"CEP ..............: {dc.get('cep','—')}",
        f"Logradouro .......: {dc.get('logradouro','—')}, {dc.get('numero','s/n')}",
        f"Complemento ......: {dc.get('complemento','—')}",
        f"Bairro ...........: {dc.get('bairro','—')}",
        f"Município/UF .....: {dc.get('municipio','—')} / {dc.get('uf','—')}",
        "",
    ]

    if perf == 'PJ':
        linhas += [
            "PERFIL FISCAL",
            SEP2,
            f"Regime Tributário : {op.get('regime','—')}",
            f"Faturamento Médio : {fmt_moeda(float(op.get('faturamento_mensal',0)))} / mês",
            f"Notas Fiscais/mês : {op.get('num_notas','—')}",
            f"Funcionários .....: {op.get('num_funcionarios',0)}",
            f"Filiais ..........: {op.get('num_filiais',0)}",
            f"Estoque ..........: {'Sim' if op.get('tem_estoque') else 'Não'}",
            f"Importa/Exporta ..: {'Sim' if op.get('importa_exporta') else 'Não'}",
            f"Situação Fiscal ..: {'Com pendências' if op.get('situacao_fiscal')=='irregular' else 'Em dia'}",
            f"Contador Atual ...: {op.get('contabilidade_atual','—')}",
            "",
        ]
    else:
        linhas += [
            "PERFIL FINANCEIRO",
            SEP2,
            f"Renda Mensal .....: {fmt_moeda(float(op.get('renda_mensal',0)))}",
            f"Bens Imóveis .....: {'Sim' if op.get('possui_bens') else 'Não'}",
            f"Investimentos ....: {'Sim' if op.get('possui_investimentos') else 'Não'}",
            f"Renda Exterior ...: {'Sim' if op.get('renda_exterior') else 'Não'}",
            f"Autônomo .........: {'Sim' if op.get('autonomo') else 'Não'}",
            f"Sócio de Empresa .: {'Sim' if op.get('socio_empresa') else 'Não'}",
            f"Pensão Alimentícia: {'Sim' if op.get('pensao') else 'Não'}",
            f"Herança/Doação ...: {'Sim' if op.get('heranca') else 'Não'}",
            f"Tipo Declaração ..: {op.get('tipo_declaracao','—')}",
            "",
        ]

    servicos = op.get('tipo_servico', [])
    if servicos:
        linhas += ["SERVIÇOS SOLICITADOS", SEP2]
        for s in servicos: linhas.append(f"  ✓ {s}")
        linhas.append("")

    contato_nome = op.get('contato_nome', dc.get('nome', '—'))
    linhas += [
        "CONTATO",
        SEP2,
        f"Responsável ......: {contato_nome}",
        f"E-mail ...........: {op.get('contato_email','—')}",
        f"Telefone/WhatsApp : {op.get('contato_telefone','—')}",
        f"Início Desejado ..: {op.get('expectativa','—')}",
    ]
    if op.get('observacoes','').strip():
        linhas += ["", f"Observações ......: {op.get('observacoes','')}"]

    n_docs = len(st.session_state.documentos)
    linhas += [
        "",
        "DOCUMENTOS",
        SEP2,
        f"Documentos anexados: {n_docs} arquivo(s)",
        "",
        SEP,
        "  BSB Contabilidade — Brasília · DF",
        "  Este documento é de uso exclusivo do escritório.",
        SEP,
    ]
    return "\n".join(linhas)


# =============================================================================
# COMPONENTES DE UI
# =============================================================================
def render_hero():
    st.markdown("""
    <div class="hero-wrapper">
        <span class="bsb-wordmark">BSB Contabilidade</span>
        <span class="bsb-sub">Brasília · DF</span>
        <div class="bsb-slogan">Inteligência fiscal para acelerar seu futuro.</div>
    </div>
    <div class="srv-strip">
        <div class="srv-card">
            <span class="srv-icon">🏛️</span>
            <div class="srv-title">Contabilidade</div>
            <div class="srv-desc">Gestão contábil completa</div>
        </div>
        <div class="srv-card">
            <span class="srv-icon">📊</span>
            <div class="srv-title">Tributário</div>
            <div class="srv-desc">Planejamento e economia</div>
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
            Seus dados são <strong>confidenciais</strong> e utilizados exclusivamente
            para elaboração de proposta de serviços. Não compartilhamos com terceiros.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_steps(current: int):
    steps = [("1","Perfil"),("2","Cadastro"),("3","Fiscal"),("4","Docs")]
    h = '<div class="step-track">'
    for i,(num,lbl) in enumerate(steps):
        n = i+1
        if n < current:   css,lcss,ico = "done","","✓"
        elif n == current: css,lcss,ico = "active","active",num
        else:              css,lcss,ico = "pending","",num
        h += f'<div class="step-node"><div class="step-circle {css}">{ico}</div><span class="step-label {lcss}">{lbl}</span></div>'
        if i < 3:
            h += f'<div class="step-connector {"done" if n < current else ""}"></div>'
    h += '</div>'
    st.markdown(h, unsafe_allow_html=True)


def ctitle(icon: str, text: str):
    st.markdown(f'<div class="card-title"><span class="ct-icon">{icon}</span>{text}</div>', unsafe_allow_html=True)


def badge(text: str):
    st.markdown(f'<div class="auto-badge">{text}</div>', unsafe_allow_html=True)


# =============================================================================
# MAIN
# =============================================================================
def main():
    render_hero()
    render_lgpd()
    step = st.session_state.step
    render_steps(max(step, 1))
    {0: etapa_perfil, 1: etapa_cadastral, 2: etapa_fiscal,
     3: etapa_docs,   4: etapa_sucesso}.get(step, etapa_perfil)()


# =============================================================================
# ETAPA 0 — PERFIL
# =============================================================================
def etapa_perfil():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("🚀", "Como deseja ser atendido?")
    st.markdown('<p style="font-size:0.78rem;color:#2d3f58;margin-bottom:1.2rem;line-height:1.5;">Selecione o perfil para personalizarmos sua proposta.</p>', unsafe_allow_html=True)

    # Cards visuais — puramente decorativos, os botões ficam abaixo
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">
        <div style="background:rgba(5,11,22,0.85);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:18px 14px 14px;text-align:center;">
            <div style="font-size:1.8rem;margin-bottom:6px;">🏢</div>
            <div style="font-size:0.82rem;font-weight:700;color:#c5d4e5;letter-spacing:-0.01em;margin-bottom:3px;">Pessoa Jurídica</div>
            <div style="font-size:0.68rem;color:#3d5069;line-height:1.4;">Empresas · MEI · Startups</div>
        </div>
        <div style="background:rgba(5,11,22,0.85);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:18px 14px 14px;text-align:center;">
            <div style="font-size:1.8rem;margin-bottom:6px;">👤</div>
            <div style="font-size:0.82rem;font-weight:700;color:#c5d4e5;letter-spacing:-0.01em;margin-bottom:3px;">Pessoa Física</div>
            <div style="font-size:0.68rem;color:#3d5069;line-height:1.4;">Autônomos · Profissionais · IR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botões funcionais — limpos, sem \n, tamanho uniforme
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Selecionar  →", use_container_width=True, key="btn_pj"):
            st.session_state.perfil = 'PJ'; st.session_state.step = 1; st.rerun()
    with c2:
        if st.button("Selecionar  →", use_container_width=True, key="btn_pf"):
            st.session_state.perfil = 'PF'; st.session_state.step = 1; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.8rem;padding:9px 12px;background:rgba(58,123,213,0.04);border-radius:8px;border:1px solid rgba(58,123,213,0.09);">
        <p style="font-size:0.74rem;color:#2d3f58;margin:0;text-align:center;line-height:1.55;">
            ⏱ Preenchimento em <strong style="color:#5ba3f5">3 a 5 minutos</strong> ·
            Proposta em até <strong style="color:#5ba3f5">24 horas úteis</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ETAPA 1 — DADOS CADASTRAIS
# =============================================================================
def etapa_cadastral():
    if st.session_state.perfil == 'PJ': _cadastral_pj()
    else: _cadastral_pf()


def _cadastral_pj():
    dc = st.session_state.dados_cadastrais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("🏢", "Dados da Empresa")

    # CNPJ
    c1, c2 = st.columns([3,1])
    with c1: cnpj_v = st.text_input("CNPJ *", value=dc.get('cnpj',''), placeholder="00.000.000/0000-00", key='k_cnpj')
    with c2:
        st.text_input("​", value="", key="_sp_cnpj", label_visibility="visible", disabled=True)
        if st.button("🔍 Buscar", use_container_width=True, type="primary", key='btn_cnpj'):
            limpo = re.sub(r'\D','',cnpj_v)
            if not validar_cnpj(limpo):
                st.error("❌ CNPJ inválido.")
            else:
                with st.spinner("Consultando Receita Federal..."):
                    res = consulta_cnpj(limpo)
                if res:
                    nj = res.get('natureza_juridica','')
                    if isinstance(nj, dict): nj = nj.get('descricao','')
                    desc_cnae = res.get('cnae_fiscal_descricao','')
                    cod_cnae  = str(res.get('cnae_fiscal',''))
                    if not desc_cnae and cod_cnae: desc_cnae = consulta_cnae(cod_cnae)
                    cnaes_s = res.get('cnaes_secundarios',[])
                    socios  = res.get('qsa',[])
                    st.session_state.dados_cadastrais.update({
                        'cnpj': fmt_cnpj(limpo),
                        'razao_social': res.get('razao_social',''),
                        'nome_fantasia': res.get('nome_fantasia','') or res.get('razao_social',''),
                        'natureza_juridica': res.get('descricao_natureza_juridica','') or nj,
                        'situacao': res.get('descricao_situacao_cadastral','') or str(res.get('situacao_cadastral','')),
                        'data_abertura': res.get('data_inicio_atividade','') or res.get('data_abertura',''),
                        'porte': res.get('descricao_porte','') or res.get('porte',''),
                        'capital_social': res.get('capital_social',0),
                        'cnae_principal_cod': cod_cnae, 'cnae_principal_desc': desc_cnae,
                        'cnaes_secundarios': [f"{c.get('codigo','')}: {c.get('descricao','')}" for c in cnaes_s[:5]],
                        'socios': [{'nome':s.get('nome_socio',''),'qualificacao':s.get('qualificacao_socio',''),'faixa_etaria':s.get('faixa_etaria','')} for s in socios],
                        'cep': res.get('cep',''), 'logradouro': res.get('logradouro',''),
                        'numero': res.get('numero',''), 'complemento': res.get('complemento',''),
                        'bairro': res.get('bairro',''), 'municipio': res.get('municipio',''), 'uf': res.get('uf',''),
                    })
                    st.session_state.cnpj_consultado = True
                    st.success("✅ Empresa localizada — campos preenchidos automaticamente.")
                    st.rerun()
                else:
                    st.error("❌ CNPJ não encontrado. Preencha manualmente.")

    if st.session_state.get('cnpj_consultado'): badge("⚡ Dados via Receita Federal")
    dc = st.session_state.dados_cadastrais

    c1, c2 = st.columns(2)
    with c1:
        razao   = st.text_input("Razão Social *",     value=dc.get('razao_social',''))
        fantasia= st.text_input("Nome Fantasia",       value=dc.get('nome_fantasia',''))
        nat_jur = st.text_input("Natureza Jurídica",   value=dc.get('natureza_juridica',''))
        situacao= st.text_input("Situação Cadastral",  value=dc.get('situacao',''))
    with c2:
        abertura= st.text_input("Data de Abertura",    value=dc.get('data_abertura',''))
        porte   = st.text_input("Porte da Empresa",    value=dc.get('porte',''))
        capital = st.number_input("Capital Social (R$)", value=float(dc.get('capital_social',0)), min_value=0.0, step=1000.0, format="%.2f")
        seg_idx = SEGMENTOS_PJ.index(dc.get('segmento','')) if dc.get('segmento') in SEGMENTOS_PJ else 0
        segmento= st.selectbox("Segmento / Setor", [""] + SEGMENTOS_PJ, index=seg_idx if dc.get('segmento') else 0)

    c1, c2 = st.columns(2)
    with c1: cnae_d = st.text_input("CNAE Principal", value=dc.get('cnae_principal_desc',''))
    with c2: cnae_c = st.text_input("Código CNAE",    value=dc.get('cnae_principal_cod',''))

    if dc.get('cnaes_secundarios'):
        with st.expander("📋 CNAEs Secundários"):
            for c in dc['cnaes_secundarios']:
                st.markdown(f"<div style='font-size:0.76rem;color:#536882;padding:2px 0;'>• {c}</div>", unsafe_allow_html=True)

    if dc.get('socios'):
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-bottom:0.6rem;"><span class="ct-icon">👥</span>Quadro Societário</div>', unsafe_allow_html=True)
        for s in dc['socios']:
            st.markdown(f"<div style='font-size:0.8rem;color:#c5d4e5;font-weight:600;'>{s.get('nome','')}</div>"
                        f"<div style='font-size:0.7rem;color:#3d5069;margin-bottom:4px;'>{s.get('qualificacao','')} {'· '+s.get('faixa_etaria','') if s.get('faixa_etaria') else ''}</div>", unsafe_allow_html=True)

    st.session_state.dados_cadastrais.update({
        'cnpj': cnpj_v, 'razao_social': razao, 'nome_fantasia': fantasia,
        'natureza_juridica': nat_jur, 'situacao': situacao, 'data_abertura': abertura,
        'porte': porte, 'capital_social': capital, 'segmento': segmento,
        'cnae_principal_cod': cnae_c, 'cnae_principal_desc': cnae_d,
    })
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📍", "Endereço")
    _bloco_cep('pj')
    st.markdown('</div>', unsafe_allow_html=True)
    _nav(0, 2, pj=True)


def _cadastral_pf():
    dc = st.session_state.dados_cadastrais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("👤", "Dados Pessoais")

    c1, c2 = st.columns(2)
    with c1:
        cpf  = st.text_input("CPF *", value=dc.get('cpf',''), placeholder="000.000.000-00")
        nome = st.text_input("Nome Completo *", value=dc.get('nome',''))
        # Data no formato DD/MM/AAAA usando text_input para total controle
        data_str = st.text_input(
            "Data de Nascimento *",
            value=dc.get('data_nascimento', ''),
            placeholder="DD/MM/AAAA",
            help="Informe no formato DD/MM/AAAA"
        )
    with c2:
        nac   = st.text_input("Nacionalidade", value=dc.get('nacionalidade','Brasileira'))
        ecivil_opts = ["Solteiro(a)","Casado(a)","Separado(a)","Divorciado(a)","Viúvo(a)","União Estável"]
        ecivil= st.selectbox("Estado Civil", ecivil_opts,
                             index=ecivil_opts.index(dc.get('estado_civil','Solteiro(a)')) if dc.get('estado_civil') in ecivil_opts else 0)
        prof_idx = PROFISSOES.index(dc.get('profissao','Outro')) if dc.get('profissao') in PROFISSOES else len(PROFISSOES)-1
        prof  = st.selectbox("Profissão / Ocupação", PROFISSOES, index=prof_idx)

    # Valida formato da data informada
    data_valida = ''
    if data_str.strip():
        try:
            dt = datetime.strptime(data_str.strip(), '%d/%m/%Y')
            data_valida = dt.strftime('%d/%m/%Y')
        except ValueError:
            st.warning("⚠️ Data inválida — use o formato DD/MM/AAAA")

    st.session_state.dados_cadastrais.update({
        'cpf': cpf, 'nome': nome,
        'data_nascimento': data_valida or dc.get('data_nascimento',''),
        'nacionalidade': nac, 'estado_civil': ecivil, 'profissao': prof,
    })
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📍", "Endereço")
    _bloco_cep('pf')
    st.markdown('</div>', unsafe_allow_html=True)
    _nav(0, 2, pf=True)


def _bloco_cep(sufixo: str):
    dc = st.session_state.dados_cadastrais
    c1, c2 = st.columns([3,1])
    with c1: cep_v = st.text_input("CEP *", value=dc.get('cep',''), placeholder="00000-000", key=f'cep_{sufixo}')
    with c2:
        st.text_input("​", value="", key=f"_sp_cep_{sufixo}", label_visibility="visible", disabled=True)
        if st.button("📍 Buscar", use_container_width=True, type="primary", key=f'btn_cep_{sufixo}'):
            c = re.sub(r'\D','',cep_v)
            if len(c) != 8:
                st.error("CEP deve ter 8 dígitos.")
            else:
                with st.spinner("Buscando endereço..."):
                    end = consulta_cep(c)
                if end:
                    st.session_state.dados_cadastrais.update({
                        'cep': fmt_cep(c),
                        'logradouro': end.get('street','')  or end.get('logradouro',''),
                        'bairro':     end.get('neighborhood','') or end.get('bairro',''),
                        'municipio':  end.get('city','')    or end.get('localidade',''),
                        'uf':         end.get('state','')   or end.get('uf',''),
                    })
                    st.success("✅ Endereço preenchido!")
                    st.rerun()
                else:
                    st.error("CEP não encontrado. Preencha manualmente.")

    dc = st.session_state.dados_cadastrais
    c1, c2 = st.columns(2)
    with c1:
        log  = st.text_input("Logradouro",  value=dc.get('logradouro',''), key=f'log_{sufixo}')
        bairro=st.text_input("Bairro",      value=dc.get('bairro',''),     key=f'bairro_{sufixo}')
        mun  = st.text_input("Município",   value=dc.get('municipio',''),  key=f'mun_{sufixo}')
    with c2:
        num  = st.text_input("Número",      value=dc.get('numero',''),     key=f'num_{sufixo}')
        comp = st.text_input("Complemento", value=dc.get('complemento',''),key=f'comp_{sufixo}')
        uf_i = ESTADOS.index(dc.get('uf','DF')) if dc.get('uf','DF') in ESTADOS else 6
        uf   = st.selectbox("UF", ESTADOS, index=uf_i, key=f'uf_{sufixo}')

    st.session_state.dados_cadastrais.update({
        'cep': cep_v, 'logradouro': log, 'numero': num, 'complemento': comp,
        'bairro': bairro, 'municipio': mun, 'uf': uf,
    })


def _nav(voltar: int, proximo: int, pj=False, pf=False):
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"):
            st.session_state.step = voltar; st.rerun()
    with c2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros = []
            d = st.session_state.dados_cadastrais
            if pj:
                if not validar_cnpj(re.sub(r'\D','',d.get('cnpj',''))): erros.append("CNPJ inválido ou não preenchido.")
                if not d.get('razao_social','').strip(): erros.append("Razão Social é obrigatória.")
            if pf:
                if not validar_cpf(re.sub(r'\D','',d.get('cpf',''))): erros.append("CPF inválido.")
                if not d.get('nome','').strip(): erros.append("Nome completo é obrigatório.")
                if not d.get('data_nascimento',''): erros.append("Data de nascimento obrigatória (DD/MM/AAAA).")
            for e in erros: st.error(f"❌ {e}")
            if not erros: st.session_state.step = proximo; st.rerun()


# =============================================================================
# ETAPA 2 — FISCAL
# =============================================================================
def etapa_fiscal():
    if st.session_state.perfil == 'PJ': _fiscal_pj()
    else: _fiscal_pf()


def _fiscal_pj():
    op = st.session_state.dados_operacionais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📊", "Configuração Fiscal")
    c1, c2 = st.columns(2)
    with c1:
        regime  = st.selectbox("Regime Tributário *", ["Simples Nacional","Lucro Presumido","Lucro Real","MEI"],
                    index=["Simples Nacional","Lucro Presumido","Lucro Real","MEI"].index(op.get('regime','Simples Nacional')) if op.get('regime') else 0)
        faturam = st.number_input("Faturamento médio mensal (R$) *", min_value=0.0, step=1000.0, format="%.2f", value=float(op.get('faturamento_mensal',0)))
        n_notas = st.number_input("Notas fiscais / mês *", min_value=0, step=1, value=int(op.get('num_notas',0)))
        n_filiais=st.number_input("Número de filiais", min_value=0, step=1, value=int(op.get('num_filiais',0)), help="0 = apenas matriz")
    with c2:
        n_func  = st.number_input("Número de funcionários", min_value=0, step=1, value=int(op.get('num_funcionarios',0)))
        estoque = st.checkbox("Possui controle de estoque?", value=op.get('tem_estoque',False))
        imp_exp = st.checkbox("Realiza importação/exportação?", value=op.get('importa_exporta',False))
        simples = st.checkbox("Optante pelo Simples Nacional?", value=op.get('tem_simples_ativo',False))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        sit_fisc = st.radio("Situação fiscal *", ["Em dia","Com pendências / irregularidades"],
                    index=1 if op.get('situacao_fiscal')=='irregular' else 0)
        cont_atual=st.radio("Possui contador atualmente?",["Não","Sim, quero trocar","Sim, consultoria adicional"],
                    index=["Não","Sim, quero trocar","Sim, consultoria adicional"].index(op.get('contabilidade_atual','Não')) if op.get('contabilidade_atual') in ["Não","Sim, quero trocar","Sim, consultoria adicional"] else 0)
    with c2:
        servicos = st.multiselect("Serviços de interesse",
            ["Contabilidade Geral","Abertura de Empresa","Encerramento de Empresa",
             "BPO Financeiro","Folha de Pagamento","Planejamento Tributário",
             "Consultoria Fiscal","Regularização Fiscal","Certidões e Declarações"],
            default=op.get('tipo_servico',[]))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📞", "Dados de Contato")
    c1, c2 = st.columns(2)
    with c1:
        c_nome = st.text_input("Nome do responsável *", value=op.get('contato_nome',''))
        c_email= st.text_input("E-mail *",               value=op.get('contato_email',''))
    with c2:
        c_tel  = st.text_input("Telefone / WhatsApp *",  value=op.get('contato_telefone',''), placeholder="(00) 00000-0000")
        expect = st.selectbox("Início desejado",
            ["Imediato (o mais rápido possível)","Próximo mês","Em até 3 meses","Apenas cotação por enquanto"],
            index=["Imediato (o mais rápido possível)","Próximo mês","Em até 3 meses","Apenas cotação por enquanto"].index(op.get('expectativa','Imediato (o mais rápido possível)')) if op.get('expectativa') in ["Imediato (o mais rápido possível)","Próximo mês","Em até 3 meses","Apenas cotação por enquanto"] else 0)
    obs = st.text_area("Observações", value=op.get('observacoes',''), placeholder="Informações adicionais...", height=75)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"): st.session_state.step=1; st.rerun()
    with c2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros=[]
            if not c_nome.strip(): erros.append("Nome do responsável obrigatório.")
            if not validar_email(c_email): erros.append("E-mail inválido.")
            if not validar_telefone(c_tel): erros.append("Telefone inválido.")
            if faturam <= 0: erros.append("Informe o faturamento médio mensal.")
            for e in erros: st.error(f"❌ {e}")
            if not erros:
                st.session_state.dados_operacionais = {
                    'regime':regime,'faturamento_mensal':faturam,'num_notas':n_notas,
                    'num_filiais':n_filiais,'num_funcionarios':n_func,
                    'tem_estoque':estoque,'importa_exporta':imp_exp,'tem_simples_ativo':simples,
                    'situacao_fiscal':'irregular' if 'pendências' in sit_fisc else 'regular',
                    'contabilidade_atual':cont_atual,'tipo_servico':servicos,
                    'contato_nome':c_nome,'contato_email':c_email,
                    'contato_telefone':fmt_tel(c_tel),'expectativa':expect,'observacoes':obs,
                }
                st.session_state.step=3; st.rerun()


def _fiscal_pf():
    op = st.session_state.dados_operacionais

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📊", "Perfil Financeiro")
    c1, c2 = st.columns(2)
    with c1:
        renda  = st.number_input("Renda mensal aproximada (R$) *", min_value=0.0, step=500.0, format="%.2f", value=float(op.get('renda_mensal',0)))
        bens   = st.checkbox("Possui bens imóveis?",        value=op.get('possui_bens',False))
        invest = st.checkbox("Possui investimentos?",        value=op.get('possui_investimentos',False))
        exterior=st.checkbox("Possui renda no exterior?",   value=op.get('renda_exterior',False))
    with c2:
        autono = st.checkbox("É autônomo / prestador?",     value=op.get('autonomo',False))
        pensao = st.checkbox("Recebe pensão alimentícia?",  value=op.get('pensao',False))
        socio  = st.checkbox("É sócio de alguma empresa?",  value=op.get('socio_empresa',False))
        heranca= st.checkbox("Recebeu herança/doação?",     value=op.get('heranca',False))

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        tipo_dec = st.radio("Tipo de declaração",
            ["Simplificada","Completa (deduções)","Não sei — quero orientação"],
            index=["Simplificada","Completa (deduções)","Não sei — quero orientação"].index(op.get('tipo_declaracao','Simplificada')) if op.get('tipo_declaracao') in ["Simplificada","Completa (deduções)","Não sei — quero orientação"] else 0)
    with c2:
        servicos_pf = st.multiselect("Serviços de interesse",
            ["Imposto de Renda (IRPF)","Planejamento Patrimonial","Consultoria Tributária",
             "Regularização junto à Receita","Declaração em Atraso","Herança / Doação / Inventário"],
            default=op.get('tipo_servico',[]))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📞", "Dados de Contato")
    c1, c2 = st.columns(2)
    with c1: c_email= st.text_input("E-mail *",              value=op.get('contato_email',''), key='em_pf')
    with c2: c_tel  = st.text_input("Telefone / WhatsApp *", value=op.get('contato_telefone',''), placeholder="(00) 00000-0000", key='tel_pf')
    expect = st.selectbox("Início desejado", ["Imediato","Próximo mês","Apenas cotação"],
        index=["Imediato","Próximo mês","Apenas cotação"].index(op.get('expectativa','Imediato')) if op.get('expectativa') in ["Imediato","Próximo mês","Apenas cotação"] else 0)
    obs = st.text_area("Observações", value=op.get('observacoes',''), placeholder="Informações adicionais...", height=70)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"): st.session_state.step=1; st.rerun()
    with c2:
        if st.button("Próximo  ➡", use_container_width=True, type="primary"):
            erros=[]
            if not validar_email(c_email): erros.append("E-mail inválido.")
            if not validar_telefone(c_tel): erros.append("Telefone inválido.")
            if renda <= 0: erros.append("Informe a renda mensal aproximada.")
            for e in erros: st.error(f"❌ {e}")
            if not erros:
                st.session_state.dados_operacionais = {
                    'renda_mensal':renda,'possui_bens':bens,'possui_investimentos':invest,
                    'renda_exterior':exterior,'autonomo':autono,'pensao':pensao,
                    'socio_empresa':socio,'heranca':heranca,'tipo_declaracao':tipo_dec,
                    'tipo_servico':servicos_pf,'contato_email':c_email,
                    'contato_telefone':fmt_tel(c_tel),'expectativa':expect,'observacoes':obs,
                }
                st.session_state.step=3; st.rerun()


# =============================================================================
# ETAPA 3 — DOCUMENTOS
# =============================================================================
def etapa_docs():
    perf = st.session_state.perfil

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📎", "Documentação para Análise")
    st.markdown("""
    <p style="font-size:0.76rem;color:#2d3f58;margin-bottom:1rem;line-height:1.5;">
        Envio <strong style="color:#536882">opcional</strong> — nossa equipe pode solicitar depois.
        Enviar agora <strong style="color:#536882">acelera sua proposta</strong>.
        Use <strong style="color:#536882">arquivo</strong> ou <strong style="color:#536882">câmera do celular</strong>.
    </p>
    """, unsafe_allow_html=True)

    if perf == 'PJ':
        _doc_item("📄 Cartão CNPJ",             "d_cnpj",     "Emitido pela Receita Federal")
        _doc_item("📝 Contrato / Estatuto Social","d_contrato", "Última versão consolidada")
        _doc_item("📋 Últimas guias pagas",       "d_guias",    "DAS, GPS, DARF, etc.")
        _doc_item("📊 Balanço / DRE",             "d_balanco",  "Último exercício disponível")
        chaves = ['d_cnpj','d_contrato','d_guias','d_balanco']
    else:
        _doc_item("🪪 RG, CNH ou Passaporte",    "d_id",       "Frente e verso — legível")
        _doc_item("🏠 Comprovante de Residência", "d_res",      "Últimos 90 dias")
        _doc_item("📋 Última declaração de IR",   "d_ir",       "Recibo de entrega")
        _doc_item("💼 Informe de Rendimentos",    "d_informe",  "Todos os informes do ano")
        chaves = ['d_id','d_res','d_ir','d_informe']

    salvos = [st.session_state.get(k) for k in chaves if st.session_state.get(k)]
    if salvos: badge(f"📎 {len(salvos)} arquivo(s) anexado(s)")
    st.session_state.documentos = salvos
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅  Voltar", use_container_width=True, type="secondary"): st.session_state.step=2; st.rerun()
    with c2:
        if st.button("✅  Finalizar Cadastro", use_container_width=True, type="primary"):
            if perf == 'PJ': st.session_state.honorario_interno = calcular_honorario_pj(st.session_state.dados_operacionais)
            else:            st.session_state.honorario_interno = calcular_honorario_pf(st.session_state.dados_operacionais)
            st.session_state.step=4; st.rerun()


def _doc_item(label: str, chave: str, descricao: str):
    st.markdown(f"""
    <div style="margin-bottom:3px;">
        <div style="font-size:0.7rem;font-weight:700;color:#536882;letter-spacing:0.05em;text-transform:uppercase;">{label}</div>
        <div style="font-size:0.65rem;color:#2d3f58;margin-bottom:5px;">{descricao}</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        arq = st.file_uploader(label, type=['pdf','png','jpg','jpeg'],
                               key=f'up_{chave}', label_visibility='collapsed')
        if arq: st.session_state[chave] = arq
    with c2:
        foto = st.camera_input(label, key=f'cam_{chave}', label_visibility='collapsed')
        if foto: st.session_state[chave] = foto
    if st.session_state.get(chave):
        st.markdown('<div class="auto-badge" style="margin:2px 0 6px;">✓ Recebido</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider" style="margin:0.55rem 0;">', unsafe_allow_html=True)


# =============================================================================
# ETAPA 4 — SUCESSO + FICHA PARA DOWNLOAD
# =============================================================================
def etapa_sucesso():
    st.balloons()
    dc  = st.session_state.dados_cadastrais
    op  = st.session_state.dados_operacionais
    perf= st.session_state.perfil

    # Cabeçalho de sucesso
    st.markdown("""
    <div style="text-align:center;padding:1.8rem 0 1.2rem;animation:fadeDown 0.7s ease both;">
        <div style="font-size:2.8rem;margin-bottom:0.7rem;">✅</div>
        <div style="font-size:1.65rem;font-weight:800;color:#dde6f0;letter-spacing:-0.02em;line-height:1.1;margin-bottom:0.4rem;">
            Cadastro Recebido!
        </div>
        <p style="font-size:0.8rem;color:#2d3f58;max-width:340px;margin:0 auto;line-height:1.6;">
            Obrigado pela confiança na <strong style="color:#5ba3f5">BSB Contabilidade</strong>.<br>
            Proposta personalizada em até <strong style="color:#5ba3f5">24 horas úteis</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Resumo
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📋", "Resumo do Cadastro")
    c1, c2 = st.columns(2)
    with c1:
        if perf == 'PJ':
            _info_row("Empresa",  dc.get('razao_social','—'), bold=True)
            _info_row("CNPJ",     dc.get('cnpj','—'))
            _info_row("Regime",   op.get('regime','—'))
        else:
            _info_row("Nome",     dc.get('nome','—'), bold=True)
            _info_row("CPF",      dc.get('cpf','—'))
    with c2:
        _info_row("E-mail",   op.get('contato_email','—'))
        _info_row("Telefone", op.get('contato_telefone','—'))
        if op.get('expectativa'): _info_row("Início", op.get('expectativa'))

    if op.get('tipo_servico'):
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#3d5069;margin-bottom:5px;">Serviços solicitados</div>', unsafe_allow_html=True)
        for s in op['tipo_servico']:
            st.markdown(f"<div style='font-size:0.78rem;color:#7aaaf5;padding:1px 0;'>✓ {s}</div>", unsafe_allow_html=True)

    n = len(st.session_state.documentos)
    if n: st.markdown(f"<div style='margin-top:8px;font-size:0.75rem;color:#2dd4a0;'>📎 {n} documento(s) anexado(s)</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── FICHA ESTRUTURADA PARA DOWNLOAD ────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    ctitle("📄", "Ficha de Cadastro — para o Contador")
    st.markdown("""
    <p style="font-size:0.76rem;color:#2d3f58;margin-bottom:0.9rem;line-height:1.5;">
        Faça o download da ficha estruturada com todas as informações cadastradas.
        Pronta para uso interno do escritório.
    </p>
    """, unsafe_allow_html=True)

    ficha_txt = gerar_ficha_texto()

    # Exibir prévia
    with st.expander("👁️  Visualizar ficha"):
        st.code(ficha_txt, language=None)

    # Download como .txt
    nome_arquivo = (
        f"BSB_Ficha_{re.sub(r'[^a-zA-Z0-9]','_', dc.get('razao_social', dc.get('nome','Cliente')))[:30]}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    )
    st.download_button(
        label="⬇️  Baixar Ficha de Cadastro (.txt)",
        data=ficha_txt.encode('utf-8'),
        file_name=nome_arquivo,
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Novo Cadastro", use_container_width=True, type="secondary"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()


def _info_row(label: str, value: str, bold: bool = False):
    w = "font-weight:700;" if bold else ""
    st.markdown(
        f"<div style='margin-bottom:7px;'>"
        f"<div style='font-size:0.68rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;color:#3d5069;'>{label}</div>"
        f"<div style='font-size:0.84rem;color:#c5d4e5;{w}'>{value}</div>"
        f"</div>", unsafe_allow_html=True)


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
