import streamlit as st
import time

# Sayfa Ayarları
st.set_page_config(page_title="CPU Güvenlik Analiz Portalı", layout="wide")

# CSS - Genel Görünüm
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; border: 1px solid #444; }
    .stButton>button:hover { background-color: #ff4b4b; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- ANİMASYON MOTORU (GARANTİLİ VERSİYON) ---
def run_visual(type="meltdown", is_shielded=False, descriptions=[]):
    placeholder = st.empty()
    desc_placeholder = st.empty()
    
    zırh_html = '<div style="width: 15px; height: 250px; background: #64ffda; box-shadow: 0 0 20px #64ffda; border-radius: 10px;"></div>' if is_shielded else ""
    
    if type == "meltdown":
        ram_label, ram_color, ram_border, duration = "KERNEL RAM", "#3d0000", "#f44336", "1.2s"
    elif type == "spectre":
        ram_label, ram_color, ram_border, duration = "UYGULAMA", "#001a3d", "#2196F3", "2.8s"
    else:
        ram_label, ram_color, ram_border, duration = "SALDIRGAN", "#222", "#777", "1.5s"

    desc_placeholder.info("🔄 *ADIM 1:* " + descriptions[0])
    s1 = '<div style="display: flex; justify-content: space-around; align-items: center; background: #1a1a1a; padding: 50px; border-radius: 15px; border: 2px solid #444; height: 300px; position: relative;">'
    s1 += '<div style="width: 80px; height: 120px; background: ' + ram_color + '; border: 2px solid ' + ram_border + '; display: flex; align-items: center; justify-content: center; color: ' + ram_border + '; font-weight: bold; text-align: center; font-size: 10px;">' + ram_label + '</div>'
    s1 += zırh_html
    s1 += '<div style="width: 120px; height: 60px; border: 2px dashed #ffeb3b; display: flex; align-items: center; justify-content: center; color: #ffeb3b; font-weight: bold;">CACHE</div>'
    s1 += '<div style="width: 100px; height: 100px; background: #112240; border: 2px solid #00ff00; display: flex; align-items: center; justify-content: center; color: #00ff00;">CPU</div></div>'
    placeholder.markdown(s1, unsafe_allow_html=True)
    time.sleep(2)

    desc_placeholder.warning("⚡ *ADIM 2:* " + descriptions[1])
    anim_type = "move_leak" if not is_shielded else "move_block"
    
    s2 = '<style>@keyframes move_leak { 0% { left: 15%; } 100% { left: 50%; } } '
    s2 += '@keyframes move_block { 0% { left: 15%; } 30% { left: 24%; opacity: 1; } 100% { left: 18%; opacity: 0; } }</style>'
    s2 += '<div style="display: flex; justify-content: space-around; align-items: center; background: #1a1a1a; padding: 50px; border-radius: 15px; border: 2px solid #444; height: 300px; position: relative;">'
    s2 += '<div style="width: 80px; height: 120px; background: ' + ram_color + '; border: 2px solid ' + ram_border + '; display: flex; align-items: center; justify-content: center; color: ' + ram_border + '; font-weight: bold; text-align: center; font-size: 10px;">' + ram_label + '</div>'
    s2 += '<div style="width: 25px; height: 25px; border-radius: 50%; background: #f44336; position: absolute; top: 50%; transform: translateY(-50%); animation: ' + anim_type + ' ' + duration + ' forwards; z-index: 10; box-shadow: 0 0 10px red;"></div>'
    s2 += zırh_html
    s2 += '<div style="width: 120px; height: 60px; border: 2px dashed #ffeb3b; display: flex; align-items: center; justify-content: center; color: #ffeb3b; font-weight: bold;">CACHE</div>'
    s2 += '<div style="width: 100px; height: 100px; background: #112240; border: 2px solid #00ff00; display: flex; align-items: center; justify-content: center; color: #00ff00;">CPU</div></div>'
    placeholder.markdown(s2, unsafe_allow_html=True)
    time.sleep(3)

    if is_shielded:
        desc_placeholder.success("🛡️ *ADIM 3:* " + descriptions[2])
    else:
        desc_placeholder.error("❌ *ADIM 3:* " + descriptions[2])

# --- YAN MENÜ ---
st.sidebar.title("🛡️ Güvenlik Portalı")
page = st.sidebar.radio("Bölüm Seçin:", [
    "📖 Ana Sayfa",
    "🔬 Spectre Saldırısı",
    "🛡️ Spectre Savunması",
    "🔬 Meltdown Saldırısı",
    "🛡️ Meltdown Savunması",
    "⏱️ Önbellek Analizi"
])

# --- SAYFALAR ---
if page == "📖 Ana Sayfa":
    st.title("🛡️ İşlemci Seviyesinde Güvenlik Analizi")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Instruction_Pipeline.svg/1200px-Instruction_Pipeline.svg.png", caption="İşlem Hattı (Pipeline)")
    st.info("Spekülatif yürütme mekanizmalarını incelemek için soldaki sekmeleri kullanın.")

elif page == "🔬 Spectre Saldırısı":
    st.title("🔬 Spectre Saldırı Simülasyonu")
    if st.button("Saldırıyı Başlat"):
        run_visual(type="spectre", is_shielded=False, descriptions=["Tahminleme motoru bir sonraki komutu bekliyor.", "İşlemci yanlış yola sapıp gizli veriyi yürütüyor.", "VERİ SIZDI: Gizli veri Cache (Önbellek) alanına ulaştı!"])

elif page == "🛡️ Spectre Savunması":
    st.title("🛡️ Spectre Savunması (Retpoline)")
    if st.button("Savunmayı Başlat"):
        run_visual(type="spectre", is_shielded=True, descriptions=["Retpoline bariyerleri aktif edildi.", "Veri paketi yanlış yola girmeye çalışıyor...", "ENGELLENDİ: Veri zırha çarptı ve sızıntı önlendi!"])

elif page == "🔬 Meltdown Saldırısı":
    st.title("🔬 Meltdown Saldırı Simülasyonu")
    if st.button("Meltdown Başlat"):
        run_visual(type="meltdown", is_shielded=False, descriptions=["Kernel belleğindeki gizli veriye erişim isteniyor.", "Yetki kontrolü atlanarak veri hızla çekiliyor.", "KRİTİK: Kernel verisi Cache alanına sızdırıldı!"])

elif page == "🛡️ Meltdown Savunması":
    st.title("🛡️ Meltdown Savunması (KPTI)")
    if st.button("KPTI Aktif Et"):
        run_visual(type="meltdown", is_shielded=True, descriptions=["KPTI ile çekirdek bellek tabloları izole edildi.", "Veri çekirdek sınırını geçmeye çalışıyor...", "BAŞARILI: KPTI zırhı sızıntıyı fiziksel olarak durdurdu!"])

elif page == "⏱️ Önbellek Analizi":
    st.title("⏱️ Önbellek Yan Kanal Analizi")
    if st.button("Zaman Analizini Başlat"):
        run_visual(type="cache", is_shielded=False, descriptions=["Saldırgan önbelleği sıfırladı (Flush).", "Kurbanın veriyi getirmesi bekleniyor...", "SONUÇ: Erişim süresi ölçüldü ve veri çalındı!"])
