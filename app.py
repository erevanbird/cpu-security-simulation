import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CPU Güvenlik Analiz Portalı",
    page_icon="🛡️",
    layout="wide"
)

def play_sound(success=False):
    freq = 760 if success else 320
    components.html(f"""
    <script>
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = {freq};
    gain.gain.setValueAtTime(0.14, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.35);
    </script>
    """, height=0)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 45%, #020617 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #111827);
    border-right: 1px solid rgba(255,255,255,0.12);
}

.big-title {
    font-size: 54px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 24px;
    min-height: 180px;
    box-shadow: 0 0 28px rgba(56,189,248,0.09);
}

.info-box {
    background: rgba(2,132,199,0.13);
    border-left: 5px solid #38bdf8;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.success-box {
    background: rgba(22,163,74,0.13);
    border-left: 5px solid #22c55e;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.danger-box {
    background: rgba(220,38,38,0.13);
    border-left: 5px solid #ef4444;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.stButton>button {
    width: 100%;
    height: 3.4em;
    border: none;
    border-radius: 15px;
    color: white;
    font-weight: 900;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    box-shadow: 0 0 24px rgba(124,58,237,0.35);
}

.stButton>button:hover {
    background: linear-gradient(90deg, #dc2626, #f97316);
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)


def visual_box(kind="spectre", shield=False):
    if kind == "meltdown":
        left_label = "KERNEL RAM"
        left_color = "#450a0a"
        border = "#ef4444"
    elif kind == "cache":
        left_label = "SALDIRGAN"
        left_color = "#1f2937"
        border = "#facc15"
    else:
        left_label = "UYGULAMA"
        left_color = "#082f49"
        border = "#38bdf8"

    shield_html = ""
    anim = "move_leak"

    if shield:
        anim = "move_block"
        shield_html = """
        <div style="
            width:18px;
            height:250px;
            background:linear-gradient(180deg,#67e8f9,#22c55e);
            border-radius:15px;
            box-shadow:0 0 30px #22c55e;
        "></div>
        """

    html = f"""
    <html>
    <head>
    <style>
    @keyframes move_leak {{
        0% {{ left: 14%; }}
        100% {{ left: 50%; }}
    }}
    @keyframes move_block {{
        0% {{ left: 14%; }}
        35% {{ left: 32%; opacity: 1; }}
        100% {{ left: 24%; opacity: 0; }}
    }}
    body {{
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
    }}
    .scene {{
        height: 330px;
        background: rgba(15,23,42,0.96);
        border: 1px solid rgba(148,163,184,0.28);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 38px rgba(56,189,248,0.12);
    }}
    .memory {{
        width: 125px;
        height: 150px;
        background: {left_color};
        border: 2px solid {border};
        color: {border};
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-weight: 900;
        box-shadow: 0 0 20px {border};
    }}
    .packet {{
        width: 32px;
        height: 32px;
        background: #ef4444;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        animation: {anim} 2.3s forwards;
        box-shadow: 0 0 30px #ef4444;
        z-index: 10;
    }}
    .cache {{
        width: 155px;
        height: 78px;
        border: 2px dashed #facc15;
        border-radius: 18px;
        color: #facc15;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        box-shadow: 0 0 22px rgba(250,204,21,0.25);
    }}
    .cpu {{
        width: 125px;
        height: 125px;
        background: #0f172a;
        border: 2px solid #22c55e;
        color: #22c55e;
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        box-shadow: 0 0 26px rgba(34,197,94,0.35);
    }}
    </style>
    </head>
    <body>
        <div class="scene">
            <div class="memory">{left_label}</div>
            <div class="packet"></div>
            {shield_html}
            <div class="cache">CACHE</div>
            <div class="cpu">CPU</div>
        </div>
    </body>
    </html>
    """

    components.html(html, height=350)


def run_simulation(kind, shield, steps):
    status = st.empty()

    status.markdown(f"""
    <div class="info-box">
    🔄 <b>ADIM 1:</b> {steps[0]}
    </div>
    """, unsafe_allow_html=True)
    visual_box(kind=kind, shield=shield)
    time.sleep(2)

    status.markdown(f"""
    <div class="danger-box">
    ⚡ <b>ADIM 2:</b> {steps[1]}
    </div>
    """, unsafe_allow_html=True)
    visual_box(kind=kind, shield=shield)
    time.sleep(3)

    if shield:
        play_sound(success=True)
        status.markdown(f"""
        <div class="success-box">
        🛡️ <b>ADIM 3:</b> {steps[2]}
        </div>
        """, unsafe_allow_html=True)
    else:
        play_sound(success=False)
        status.markdown(f"""
        <div class="danger-box">
        ❌ <b>ADIM 3:</b> {steps[2]}
        </div>
        """, unsafe_allow_html=True)


st.sidebar.title("🛡️ Güvenlik Portalı")
st.sidebar.caption("Spectre, Meltdown ve Cache yan kanal saldırılarını interaktif olarak inceleyin.")

page = st.sidebar.radio(
    "Bölüm Seçin:",
    [
        "📖 Ana Sayfa",
        "🔬 Spectre Analizi",
        "🔥 Meltdown Analizi",
        "⏱️ Önbellek Analizi"
    ]
)

if page == "📖 Ana Sayfa":
    st.markdown('<div class="big-title">CPU Güvenlik Analiz Portalı</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Modern işlemcilerde spekülatif yürütme, Meltdown, Spectre ve önbellek yan kanal saldırılarını görsel olarak açıklayan interaktif simülasyon.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔬 Spectre</h3>
        <p>İşlemcinin tahmin mekanizması kötüye kullanılır. Gizli veri doğrudan okunmaz fakat önbellekte iz bırakır.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>🔥 Meltdown</h3>
        <p>Yetki kontrolü tamamlanmadan önce çekirdek bellekteki veri geçici yürütme ile önbelleğe sızdırılabilir.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>⏱️ Cache Analizi</h3>
        <p>Veri doğrudan okunmaz. Bunun yerine erişim süreleri ölçülerek gizli bilgi tahmin edilir.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("Soldaki menüden bir analiz seçin. Her analiz sayfasında saldırı ve savunma senaryosu birlikte gösterilir.")

elif page == "🔬 Spectre Analizi":
    st.title("🔬 Spectre Analizi")

    st.markdown("""
    <div class="info-box">
    Spectre saldırısı, işlemcinin dal tahmini ve spekülatif yürütme davranışını hedef alır.
    Bu sayfada önce saldırının nasıl veri sızdırdığını, ardından Retpoline savunmasının bunu nasıl engellediğini görebilirsiniz.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="danger-box">
        <b>Senaryo 1: Spectre Saldırısı</b><br>
        İşlemci yanlış tahmin yoluna sokulur ve gizli veri Cache üzerinde iz bırakır.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Spectre Saldırısını Başlat"):
            run_simulation(
                "spectre",
                False,
                [
                    "Tahminleme motoru saldırı için hazırlanıyor.",
                    "İşlemci yanlış spekülatif yürütme yoluna yönlendiriliyor.",
                    "VERİ SIZDI: Gizli veri Cache üzerinde iz bıraktı!"
                ]
            )

    with col2:
        st.markdown("""
        <div class="success-box">
        <b>Senaryo 2: Spectre Savunması</b><br>
        Retpoline tekniği dolaylı dallanma tahminlerini kontrol altına alır.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🛡️ Retpoline Savunmasını Başlat"):
            run_simulation(
                "spectre",
                True,
                [
                    "Retpoline bariyeri aktif hale getirildi.",
                    "Saldırganın yönlendirdiği veri yanlış yola girmeye çalışıyor.",
                    "ENGELLENDİ: Spekülatif sızıntı durduruldu!"
                ]
            )

elif page == "🔥 Meltdown Analizi":
    st.title("🔥 Meltdown Analizi")

    st.markdown("""
    <div class="info-box">
    Meltdown, çekirdek belleğe ait verilerin geçici yürütme sırasında erişilebilir hale gelmesini hedefler.
    Bu sayfada saldırı ve KPTI savunması aynı bölümde gösterilir.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="danger-box">
        <b>Senaryo 1: Meltdown Saldırısı</b><br>
        Kullanıcı alanındaki işlem, kernel bellekteki veriyi geçici olarak önbelleğe taşır.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 Meltdown Saldırısını Başlat"):
            run_simulation(
                "meltdown",
                False,
                [
                    "Kernel belleğindeki gizli veriye erişim deneniyor.",
                    "Yetki kontrolü tamamlanmadan veri önbelleğe taşınıyor.",
                    "KRİTİK: Kernel verisi Cache alanına sızdırıldı!"
                ]
            )

    with col2:
        st.markdown("""
        <div class="success-box">
        <b>Senaryo 2: Meltdown Savunması</b><br>
        KPTI, kullanıcı alanı ile çekirdek belleği ayırarak sızıntıyı engeller.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🛡️ KPTI Savunmasını Başlat"):
            run_simulation(
                "meltdown",
                True,
                [
                    "KPTI ile çekirdek bellek tabloları izole edildi.",
                    "Veri çekirdek sınırını geçmeye çalışıyor.",
                    "BAŞARILI: KPTI izolasyonu sızıntıyı durdurdu!"
                ]
            )

elif page == "⏱️ Önbellek Analizi":
    st.title("⏱️ Önbellek Yan Kanal Analizi")

    st.markdown("""
    <div class="info-box">
    Önbellek yan kanal saldırılarında gizli veri doğrudan okunmaz.
    Saldırgan, erişim sürelerini ölçerek hangi verinin önbellekte olduğunu tahmin eder.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="danger-box">
        <b>Senaryo 1: Zaman Analizi</b><br>
        Flush + Reload mantığıyla erişim süresi ölçülür.
        </div>
        """, unsafe_allow_html=True)

        if st.button("⏱️ Zaman Analizini Başlat"):
            run_simulation(
                "cache",
                False,
                [
                    "Saldırgan önbelleği temizliyor.",
                    "Kurbanın veriye erişmesi bekleniyor ve süre ölçülüyor.",
                    "SONUÇ: Erişim süresinden veri tahmin edildi!"
                ]
            )

    with col2:
        st.markdown("""
        <div class="success-box">
        <b>Senaryo 2: Güvenli Tasarım</b><br>
        Zaman farkını azaltan sabit zamanlı işlem mantığı sızıntı riskini düşürür.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🛡️ Güvenli Önbellek Tasarımını Başlat"):
            run_simulation(
                "cache",
                True,
                [
                    "Sabit zamanlı erişim mantığı aktif edildi.",
                    "Saldırgan süre farkını ölçmeye çalışıyor.",
                    "ENGELLENDİ: Belirgin zaman farkı oluşmadı!"
                ]
            )
