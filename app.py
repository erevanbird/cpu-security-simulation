import streamlit as st
import time
import streamlit.components.v1 as components

# =========================
# SAYFA AYARI
# =========================
st.set_page_config(
    page_title="CPU Güvenlik Analiz Portalı",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# SES EFEKTİ
# =========================
def play_sound(success=False):
    freq = 700 if success else 300

    components.html(f"""
    <script>
    const audioCtx = new(window.AudioContext || window.webkitAudioContext)();

    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime({freq}, audioCtx.currentTime);

    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.3);
    </script>
    """, height=0)

# =========================
# CSS TASARIM
# =========================
st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top left,#1e293b 0%,#0f172a 45%,#020617 100%);
    color:white;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#020617,#111827);
}

.big-title{
    font-size:55px;
    font-weight:900;
    background:linear-gradient(90deg,#38bdf8,#818cf8,#f472b6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    color:#cbd5e1;
    font-size:18px;
    margin-top:-10px;
}

.card{
    background:rgba(15,23,42,0.9);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:18px;
    padding:25px;
    min-height:180px;
    box-shadow:0 0 25px rgba(59,130,246,0.1);
}

.metric{
    background:rgba(30,41,59,0.85);
    border-radius:16px;
    padding:20px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.1);
}

.stButton>button{
    width:100%;
    height:3.4em;
    border:none;
    border-radius:14px;
    font-weight:800;
    color:white;
    background:linear-gradient(90deg,#2563eb,#7c3aed);
    box-shadow:0 0 25px rgba(124,58,237,0.35);
}

.stButton>button:hover{
    background:linear-gradient(90deg,#dc2626,#ea580c);
    transform:scale(1.02);
}

.info-box{
    background:rgba(2,132,199,0.12);
    border-left:5px solid #38bdf8;
    padding:18px;
    border-radius:12px;
    margin-bottom:20px;
}

.success-box{
    background:rgba(22,163,74,0.12);
    border-left:5px solid #22c55e;
    padding:18px;
    border-radius:12px;
    margin-bottom:20px;
}

.warning-box{
    background:rgba(220,38,38,0.12);
    border-left:5px solid #ef4444;
    padding:18px;
    border-radius:12px;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# ANİMASYON MOTORU
# =========================
def run_visual(type="spectre", is_shielded=False, descriptions=None):

    if descriptions is None:
        descriptions = ["Hazırlık", "İşlem", "Sonuç"]

    placeholder = st.empty()
    desc_placeholder = st.empty()

    shield_html = ""

    if is_shielded:
        shield_html = """
        <div style="
        width:18px;
        height:260px;
        background:linear-gradient(180deg,#67e8f9,#22c55e);
        border-radius:15px;
        box-shadow:0 0 25px #22c55e;
        "></div>
        """

    if type == "meltdown":
        ram_label = "KERNEL RAM"
        ram_color = "#450a0a"
        ram_border = "#ef4444"
        duration = "1.2s"

    elif type == "spectre":
        ram_label = "UYGULAMA"
        ram_color = "#082f49"
        ram_border = "#38bdf8"
        duration = "2.8s"

    else:
        ram_label = "CACHE"
        ram_color = "#1f2937"
        ram_border = "#facc15"
        duration = "1.8s"

    # STEP 1
    desc_placeholder.markdown(f"""
    <div class="info-box">
    🔄 <b>ADIM 1:</b> {descriptions[0]}
    </div>
    """, unsafe_allow_html=True)

    s1 = f"""
    <div style="
    display:flex;
    justify-content:space-around;
    align-items:center;
    background:rgba(15,23,42,0.95);
    padding:50px;
    border-radius:22px;
    height:330px;
    position:relative;
    overflow:hidden;
    ">

    <div style="
    width:120px;
    height:145px;
    background:{ram_color};
    border:2px solid {ram_border};
    border-radius:18px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:{ram_border};
    font-weight:900;
    text-align:center;
    ">
    {ram_label}
    </div>

    {shield_html}

    <div style="
    width:150px;
    height:75px;
    border:2px dashed #facc15;
    border-radius:16px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:#facc15;
    font-weight:900;
    ">
    CACHE
    </div>

    <div style="
    width:120px;
    height:120px;
    background:#0f172a;
    border:2px solid #22c55e;
    border-radius:22px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:#22c55e;
    font-weight:900;
    ">
    CPU
    </div>

    </div>
    """

    placeholder.markdown(s1, unsafe_allow_html=True)

    time.sleep(2)

    # STEP 2
    desc_placeholder.markdown(f"""
    <div class="warning-box">
    ⚡ <b>ADIM 2:</b> {descriptions[1]}
    </div>
    """, unsafe_allow_html=True)

    animation_name = "move_leak"

    if is_shielded:
        animation_name = "move_block"

    s2 = f"""
    <style>

    @keyframes move_leak {{
        0% {{ left:15%; }}
        100% {{ left:50%; }}
    }}

    @keyframes move_block {{
        0% {{ left:15%; }}
        35% {{ left:31%; opacity:1; }}
        100% {{ left:24%; opacity:0; }}
    }}

    </style>

    <div style="
    display:flex;
    justify-content:space-around;
    align-items:center;
    background:rgba(15,23,42,0.95);
    padding:50px;
    border-radius:22px;
    height:330px;
    position:relative;
    overflow:hidden;
    ">

    <div style="
    width:120px;
    height:145px;
    background:{ram_color};
    border:2px solid {ram_border};
    border-radius:18px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:{ram_border};
    font-weight:900;
    text-align:center;
    ">
    {ram_label}
    </div>

    <div style="
    width:30px;
    height:30px;
    border-radius:50%;
    background:#ef4444;
    position:absolute;
    top:50%;
    transform:translateY(-50%);
    animation:{animation_name} {duration} forwards;
    box-shadow:0 0 25px #ef4444;
    ">
    </div>

    {shield_html}

    <div style="
    width:150px;
    height:75px;
    border:2px dashed #facc15;
    border-radius:16px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:#facc15;
    font-weight:900;
    ">
    CACHE
    </div>

    <div style="
    width:120px;
    height:120px;
    background:#0f172a;
    border:2px solid #22c55e;
    border-radius:22px;
    display:flex;
    justify-content:center;
    align-items:center;
    color:#22c55e;
    font-weight:900;
    ">
    CPU
    </div>

    </div>
    """

    placeholder.markdown(s2, unsafe_allow_html=True)

    time.sleep(3)

    # STEP 3
    if is_shielded:

        play_sound(success=True)

        desc_placeholder.markdown(f"""
        <div class="success-box">
        🛡️ <b>ADIM 3:</b> {descriptions[2]}
        </div>
        """, unsafe_allow_html=True)

    else:

        play_sound(success=False)

        desc_placeholder.markdown(f"""
        <div class="warning-box">
        ❌ <b>ADIM 3:</b> {descriptions[2]}
        </div>
        """, unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🛡️ Güvenlik Portalı")

st.sidebar.caption(
"Spectre, Meltdown ve Cache saldırılarını interaktif şekilde inceleyin."
)

page = st.sidebar.radio(
    "Bölüm Seçin:",
    [
        "📖 Ana Sayfa",
        "🔬 Spectre Saldırısı",
        "🛡️ Spectre Savunması",
        "🔬 Meltdown Saldırısı",
        "🛡️ Meltdown Savunması",
        "⏱️ Önbellek Analizi"
    ]
)

# =========================
# SAYFALAR
# =========================

if page == "📖 Ana Sayfa":

    st.markdown(
        '<div class="big-title">CPU Güvenlik Analiz Portalı</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Modern işlemcilerde spekülatif yürütme ve yan kanal saldırılarını görselleştiren interaktif analiz sistemi.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔬 Spectre</h3>
        <p>Dal tahmini mekanizmasını manipüle ederek gizli verilerin önbelleğe sızdırılmasını simüle eder.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>🔥 Meltdown</h3>
        <p>Çekirdek bellekteki kritik verilerin geçici yürütme sırasında okunmasını gösterir.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>⏱️ Cache Analizi</h3>
        <p>Erişim süreleri üzerinden gizli bilgilerin tahmin edilmesini görselleştirir.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "🔬 Spectre Saldırısı":

    st.title("🔬 Spectre Saldırı Simülasyonu")

    st.markdown("""
    <div class="info-box">
    Spectre saldırısı işlemcinin tahmin motorunu kandırır ve veri önbelleğe sızar.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Spectre Saldırısını Başlat"):

        run_visual(
            type="spectre",
            is_shielded=False,
            descriptions=[
                "Tahmin sistemi hazırlanıyor.",
                "Yanlış yürütme başlatıldı.",
                "VERİ ÖNBELLEĞE SIZDI!"
            ]
        )

elif page == "🛡️ Spectre Savunması":

    st.title("🛡️ Spectre Savunması")

    st.markdown("""
    <div class="success-box">
    Retpoline koruması aktif edilerek saldırı yolu engellenir.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛡️ Retpoline Savunmasını Başlat"):

        run_visual(
            type="spectre",
            is_shielded=True,
            descriptions=[
                "Koruma sistemi etkinleştirildi.",
                "Veri saldırı yoluna girmeye çalışıyor.",
                "SALDIRI ENGELLENDİ!"
            ]
        )

elif page == "🔬 Meltdown Saldırısı":

    st.title("🔬 Meltdown Saldırısı")

    st.markdown("""
    <div class="info-box">
    Meltdown saldırısı çekirdek bellekteki verilere erişmeye çalışır.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔥 Meltdown Saldırısını Başlat"):

        run_visual(
            type="meltdown",
            is_shielded=False,
            descriptions=[
                "Kernel belleğine erişim hazırlanıyor.",
                "Yetki kontrolü atlandı.",
                "KERNEL VERİSİ SIZDIRILDI!"
            ]
        )

elif page == "🛡️ Meltdown Savunması":

    st.title("🛡️ Meltdown Savunması")

    st.markdown("""
    <div class="success-box">
    KPTI sistemi çekirdek belleği kullanıcı alanından ayırır.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛡️ KPTI Savunmasını Başlat"):

        run_visual(
            type="meltdown",
            is_shielded=True,
            descriptions=[
                "KPTI izolasyonu aktif edildi.",
                "Veri sınırı geçmeye çalışıyor.",
                "SIZINTI ENGELLENDİ!"
            ]
        )

elif page == "⏱️ Önbellek Analizi":

    st.title("⏱️ Önbellek Analizi")

    st.markdown("""
    <div class="info-box">
    Cache erişim süreleri analiz edilerek veri tahmini yapılır.
    </div>
    """, unsafe_allow_html=True)

    if st.button("⏱️ Analizi Başlat"):

        run_visual(
            type="cache",
            is_shielded=False,
            descriptions=[
                "Önbellek temizlendi.",
                "Erişim süreleri ölçülüyor.",
                "VERİ TAHMİN EDİLDİ!"
            ]
        )
