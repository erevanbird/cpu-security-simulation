import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CPU Güvenlik Analiz Portalı",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# SES EFEKTİ
# =========================
def play_sound(success=False):
    freq = 720 if success else 320
    components.html(f"""
    <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime({freq}, audioCtx.currentTime);

    gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.35);
    </script>
    """, height=0)


# =========================
# CSS TASARIM
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1f2937 0%, #0b1120 40%, #020617 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #111827);
    border-right: 1px solid rgba(255,255,255,0.1);
}

h1, h2, h3 {
    color: #e5e7eb;
}

.big-title {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background: rgba(15, 23, 42, 0.85);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.25);
    box-shadow: 0 0 35px rgba(56, 189, 248, 0.08);
    min-height: 180px;
}

.metric-card {
    background: rgba(30, 41, 59, 0.9);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    text-align: center;
}

.stButton>button {
    width: 100%;
    height: 3.4em;
    border-radius: 14px;
    border: none;
    font-weight: 800;
    color: white;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.35);
    transition: 0.25s;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #dc2626, #f97316);
    box-shadow: 0 0 25px rgba(249, 115, 22, 0.45);
}

.info-box {
    background: rgba(2, 132, 199, 0.12);
    border-left: 5px solid #38bdf8;
    padding: 18px;
    border-radius: 12px;
    color: #dbeafe;
    margin-bottom: 20px;
}

.warning-box {
    background: rgba(220, 38, 38, 0.12);
    border-left: 5px solid #ef4444;
    padding: 18px;
    border-radius: 12px;
    color: #fee2e2;
    margin-bottom: 20px;
}

.success-box {
    background: rgba(22, 163, 74, 0.12);
    border-left: 5px solid #22c55e;
    padding: 18px;
    border-radius: 12px;
    color: #dcfce7;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# ANİMASYON MOTORU
# =========================
def run_visual(type="meltdown", is_shielded=False, descriptions=None):
    if descriptions is None:
        descriptions = ["Hazırlık yapılıyor.", "İşlem başlatılıyor.", "Sonuç gösteriliyor."]

    placeholder = st.empty()
    desc_placeholder = st.empty()

    shield_html = """
    <div style="
        width: 18px;
        height: 260px;
        background: linear-gradient(180deg, #67e8f9, #22c55e);
        box-shadow: 0 0 30px #22c55e;
        border-radius: 15px;
    "></div>
    """ if is_shielded else ""

    if type == "meltdown":
        ram_label = "KERNEL RAM"
        ram_color = "#450a0a"
        ram_border = "#ef4444"
        duration = "1.2s"
    elif type == "spectre":
        ram_label = "UYGULAMA ALANI"
        ram_color = "#082f49"
        ram_border = "#38bdf8"
        duration = "2.8s"
    else:
        ram_label = "SALDIRGAN"
        ram_color = "#1f2937"
        ram_border = "#facc15"
        duration = "1.8s"

    # ADIM 1
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
        border:1px solid rgba(148,163,184,0.3);
        height:330px;
        position:relative;
        box-shadow:0 0 35px rgba(56,189,248,0.12);
    ">
        <div style="
            width:120px;
            height:145px;
            background:{ram_color};
            border:2px solid {ram_border};
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:{ram_border};
            font-weight:900;
            text-align:center;
            font-size:14px;
            box-shadow:0 0 18px {ram_border};
        ">{ram_label}</div>

        {shield_html}

        <div style="
            width:150px;
            height:75px;
            border:2px dashed #facc15;
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:#facc15;
            font-weight:900;
            box-shadow:0 0 20px rgba(250,204,21,0.2);
        ">CACHE</div>

        <div style="
            width:120px;
            height:120px;
            background:#0f172a;
            border:2px solid #22c55e;
            border-radius:22px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:#22c55e;
            font-weight:900;
            box-shadow:0 0 24px rgba(34,197,94,0.35);
        ">CPU</div>
    </div>
    """

    placeholder.markdown(s1, unsafe_allow_html=True)
    time.sleep(2)

    # ADIM 2
    desc_placeholder.markdown(f"""
    <div class="warning-box">
    ⚡ <b>ADIM 2:</b> {descriptions[1]}
    </div>
    """, unsafe_allow_html=True)

    anim_type = "move_leak" if not is_shielded else "move_block"

    s2 = f"""
    <style>
    @keyframes move_leak {{
        0% {{ left: 15%; }}
        100% {{ left: 50%; }}
    }}
    @keyframes move_block {{
        0% {{ left: 15%; }}
        35% {{ left: 31%; opacity: 1; }}
        100% {{ left: 24%; opacity: 0; }}
    }}
    </style>

    <div style="
        display:flex;
        justify-content:space-around;
        align-items:center;
        background:rgba(15,23,42,0.95);
        padding:50px;
        border-radius:22px;
        border:1px solid rgba(148,163,184,0.3);
        height:330px;
        position:relative;
        box-shadow:0 0 35px rgba(56,189,248,0.12);
        overflow:hidden;
    ">
        <div style="
            width:120px;
            height:145px;
            background:{ram_color};
            border:2px solid {ram_border};
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:{ram_border};
            font-weight:900;
            text-align:center;
            font-size:14px;
            box-shadow:0 0 18px {ram_border};
        ">{ram_label}</div>

        <div style="
            width:30px;
            height:30px;
            border-radius:50%;
            background:#ef4444;
            position:absolute;
            top:50%;
            transform:translateY(-50%);
            animation:{anim_type} {duration} forwards;
            z-index:10;
            box-shadow:0 0 25px #ef4444;
        "></div>

        {shield_html}

        <div style="
            width:150px;
            height:75px;
            border:2px dashed #facc15;
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:#facc15;
            font-weight:900;
            box-shadow:0 0 20px rgba(250,204,21,0.2);
        ">CACHE</div>

        <div style="
            width:120px;
            height:120px;
            background:#0f172a;
            border:2px solid #22c55e;
            border-radius:22px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:#22c55e;
            font-weight:900;
            box-shadow:0 0 24px rgba(34,197,94,0.35);
        ">CPU</div>
    </div>
    """

    placeholder.markdown(s2, unsafe_allow_html=True)
    time.sleep(3)

    # ADIM 3
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
# YAN MENÜ
# =========================
st.sidebar.title("🛡️ Güvenlik Portalı")
st.sidebar.caption("Spectre, Meltdown ve Cache yan kanal saldırılarını görsel olarak inceleyin.")

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
    st.markdown('<div class="big-title">CPU Güvenlik Analiz Portalı</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Modern işlemcilerde spekülatif yürütme, önbellek yan kanalları ve güvenlik savunmalarını görsel olarak inceleyen interaktif simülasyon.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔬 Spectre</h3>
        <p>İşlemcinin tahmin mekanizmasını kötüye kullanarak gizli verilerin önbellek izleri üzerinden sızdırılmasını simüle eder.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>🔥 Meltdown</h3>
        <p>Kullanıcı alanındaki bir işlemin çekirdek belleğe ait verilere geçici yürütme sırasında erişmesini gösterir.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>⏱️ Cache Analizi</h3>
        <p>Önbelleğe erişim süreleri ölçülerek gizli bilgilerin nasıl çıkarılabileceğini görselleştirir.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><h2>3</h2><p>Saldırı Senaryosu</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><h2>2</h2><p>Savunma Mekanizması</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h2>1</h2><p>Yan Kanal Analizi</p></div>', unsafe_allow_html=True)

elif page == "🔬 Spectre Saldırısı":
    st.title("🔬 Spectre Saldırı Simülasyonu")
    st.markdown("""
    <div class="info-box">
    Spectre saldırısı, işlemcinin dal tahmini ve spekülatif yürütme mekanizmasını hedef alır.
    İşlemci yanlış bir tahmin yoluna sokulur ve gizli veri doğrudan okunmasa bile önbellekte iz bırakır.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Spectre Saldırısını Başlat"):
        run_visual(
            type="spectre",
            is_shielded=False,
            descriptions=[
                "Tahminleme motoru bir sonraki komutu bekliyor.",
                "İşlemci yanlış yola sapıp gizli veriyi yürütüyor.",
                "VERİ SIZDI: Gizli veri Cache alanına ulaştı!"
            ]
        )

elif page == "🛡️ Spectre Savunması":
    st.title("🛡️ Spectre Savunması - Retpoline")
    st.markdown("""
    <div class="success-box">
    Retpoline tekniği, işlemcinin tehlikeli dolaylı dallanma tahminlerini kontrol altına alır.
    Böylece saldırganın spekülatif yürütme yolunu manipüle etmesi engellenir.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛡️ Retpoline Savunmasını Başlat"):
        run_visual(
            type="spectre",
            is_shielded=True,
            descriptions=[
                "Retpoline bariyerleri aktif edildi.",
                "Veri paketi yanlış yola girmeye çalışıyor.",
                "ENGELLENDİ: Veri zırha çarptı ve sızıntı önlendi!"
            ]
        )

elif page == "🔬 Meltdown Saldırısı":
    st.title("🔬 Meltdown Saldırı Simülasyonu")
    st.markdown("""
    <div class="info-box">
    Meltdown saldırısı, kullanıcı alanındaki bir programın çekirdek belleğe ait verileri geçici yürütme sırasında
    erişilebilir hale getirmesini gösterir. Veri daha sonra önbellek zamanlaması ile çıkarılabilir.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔥 Meltdown Saldırısını Başlat"):
        run_visual(
            type="meltdown",
            is_shielded=False,
            descriptions=[
                "Kernel belleğindeki gizli veriye erişim isteniyor.",
                "Yetki kontrolü atlanarak veri hızla çekiliyor.",
                "KRİTİK: Kernel verisi Cache alanına sızdırıldı!"
            ]
        )

elif page == "🛡️ Meltdown Savunması":
    st.title("🛡️ Meltdown Savunması - KPTI")
    st.markdown("""
    <div class="success-box">
    KPTI, kullanıcı alanı ile çekirdek belleği birbirinden ayırır.
    Bu izolasyon sayesinde Meltdown saldırısının çekirdek belleğe ulaşması engellenir.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛡️ KPTI Savunmasını Başlat"):
        run_visual(
            type="meltdown",
            is_shielded=True,
            descriptions=[
                "KPTI ile çekirdek bellek tabloları izole edildi.",
                "Veri çekirdek sınırını geçmeye çalışıyor.",
                "BAŞARILI: KPTI zırhı sızıntıyı fiziksel olarak durdurdu!"
            ]
        )

elif page == "⏱️ Önbellek Analizi":
    st.title("⏱️ Önbellek Yan Kanal Analizi")
    st.markdown("""
    <div class="info-box">
    Önbellek yan kanal saldırılarında veri doğrudan okunmaz.
    Bunun yerine, belleğe erişim süreleri ölçülerek hangi verinin önbellekte olduğu anlaşılmaya çalışılır.
    </div>
    """, unsafe_allow_html=True)

    if st.button("⏱️ Zaman Analizini Başlat"):
        run_visual(
            type="cache",
            is_shielded=False,
            descriptions=[
                "Saldırgan önbelleği sıfırladı.",
                "Kurbanın veriyi getirmesi bekleniyor.",
                "SONUÇ: Erişim süresi ölçüldü ve veri tahmin edildi!"
            ]
        )
