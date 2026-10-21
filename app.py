import io
import colorsys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Ruang Statistik",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

brand_col, mode_col = st.columns([.78, .22], vertical_alignment="center")
with brand_col:
    st.markdown('<div class="brand"><span class="brand-mark">◌</span> Ruang Statistik <span class="brand-class">· 1B</span></div>', unsafe_allow_html=True)
with mode_col:
    st.toggle("Mode malam", key="dark_mode")

is_dark = st.session_state.dark_mode

light_css = """
.stApp { background:radial-gradient(ellipse at 12% 2%,rgba(195,187,255,.32),transparent 34%),radial-gradient(ellipse at 94% 20%,rgba(175,230,238,.34),transparent 30%),linear-gradient(145deg,#f8f8fc,#f1f3f9 58%,#f7f8fc); color:#202536; }
.hero { background:linear-gradient(125deg,rgba(255,255,255,.82),rgba(247,247,255,.68)); border-color:rgba(255,255,255,.9); box-shadow:0 18px 48px rgba(67,72,112,.09),inset 0 1px 0 #fff; }
.hero h1,.section-title { color:#25283a; }
.hero p,.section-sub,.stCaption { color:#7b8192 !important; }
.glass { background:rgba(255,255,255,.72); border-color:rgba(255,255,255,.94); box-shadow:0 12px 36px rgba(64,69,106,.07),inset 0 1px 0 #fff; }
.app-table th { background:#f0edff; color:#554b86; }
.app-table td { background:rgba(255,255,255,.72); color:#34394b; border-color:#e7e8ef; }
[data-baseweb="select"] > div, [data-testid="stTextInput"] input { background:rgba(255,255,255,.94) !important; color:#35394c !important; }
"""

dark_css = """
.stApp { background:radial-gradient(ellipse at 12% 2%,rgba(93,75,153,.24),transparent 34%),radial-gradient(ellipse at 94% 20%,rgba(40,104,119,.20),transparent 30%),linear-gradient(145deg,#171923,#12151f 58%,#181923); color:#e9eaf2; }
.hero { background:linear-gradient(125deg,rgba(37,39,56,.90),rgba(29,32,46,.82)); border-color:rgba(255,255,255,.12); box-shadow:0 18px 48px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.10); }
.hero h1,.section-title { color:#f0eff8; }
.hero p,.section-sub,.stCaption { color:#a9adbd !important; }
.glass { background:rgba(31,34,49,.82); border-color:rgba(255,255,255,.11); box-shadow:0 12px 36px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.08); }
.pill { background:#302b4b; color:#c4b8ff; }
.brand,.brand-class { color:#b8bbca !important; }
.app-table th { background:#302b4b; color:#ded7ff; }
.app-table td { background:rgba(30,33,47,.84); color:#e2e4ed; border-color:#3a3d4d; }
[data-baseweb="select"] > div, [data-testid="stTextInput"] input { background:#242737 !important; border-color:#414458 !important; color:#e8e9f1 !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] > div { background:#242737 !important; border-color:#414458 !important; color:#e8e9f1 !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] div { background:#242737 !important; color:#e8e9f1 !important; border-color:#414458 !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] { background:#242737 !important; color:#e8e9f1 !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"] { background:#242737 !important; color:#e8e9f1 !important; }
[data-testid="stSelectbox"] * { background-color:#242737 !important; color:#e8e9f1 !important; border-color:#414458 !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] { background:#393253 !important; color:#ded7ff !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] * { color:#ded7ff !important; }
[data-testid="stDownloadButton"] button { background:#393253 !important; border-color:#5e547f !important; color:#f0eff8 !important; }
[data-baseweb="tag"] { background:#393253 !important; color:#ded7ff !important; }
[data-testid="stFileUploader"] section { background:rgba(31,34,49,.62) !important; border-color:#55506e !important; }
[data-testid="stFileUploader"] small, [data-testid="stFileUploader"] section * { color:#a9adbd !important; }
[data-testid="stFileUploader"] label { color:#c4c6d2 !important; }
[data-testid="stFileUploader"] small { color:#c4c6d2 !important; }
[data-testid="stAlert"] { background:#292c40 !important; border-color:#49435f !important; }
[data-testid="stAlert"] * { color:#e0e1eb !important; }
[data-testid="stExpander"] { background:rgba(31,34,49,.50); border-color:rgba(255,255,255,.13); }
[data-testid="stExpander"] summary { color:#e8e9f1; }
[data-testid="stPlotlyChart"] .js-plotly-plot { filter:drop-shadow(0 10px 18px rgba(0,0,0,.24)); }
[data-testid="stCheckbox"] label,[data-testid="stRadio"] label,[data-testid="stSelectbox"] label,[data-testid="stSlider"] label,[data-testid="stColorPicker"] label { color:#d8dae5 !important; }
.stButton button { background:#393253 !important; border-color:#5e547f !important; color:#f0eff8 !important; }
.stButton button:hover { background:#494064 !important; border-color:#8071b4 !important; color:#ffffff !important; }
div[data-testid="stMetric"] { background:rgba(31,34,49,.7); border-color:#393c4e; }
"""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family:'DM Sans',sans-serif; }}
.block-container {{ max-width:1120px; padding:1.2rem 2.2rem 4rem; }}
#MainMenu, footer, header {{ visibility:hidden; }}
[data-testid="stAppViewContainer"] {{ background:transparent; }}
.brand {{ display:flex; align-items:center; gap:10px; color:#656b7c; font-size:13px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin:0; min-height:38px; }}
.brand-class {{ color:#c0c2cc; font-weight:500; letter-spacing:0; margin-left:2px; }}
.brand-mark {{ display:grid; place-items:center; width:30px;height:30px;border-radius:11px; color:#fff; font-size:17px; background:linear-gradient(145deg,#a88cf5,#7059da); box-shadow:0 5px 14px #8066e83d; }}
.hero {{ position:relative; overflow:hidden; padding:32px 38px; border:1px solid; border-radius:28px; backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); }}
.hero:after {{ content:""; position:absolute; width:260px;height:260px;right:-95px;top:-150px;border-radius:50%;background:radial-gradient(circle,rgba(184,167,255,.28),rgba(181,230,235,.08) 60%,transparent 70%); pointer-events:none; }}
.kicker {{ color:#8274c6; text-transform:uppercase; letter-spacing:.13em; font-size:11px; font-weight:700; margin-bottom:10px; }}
.hero h1 {{ font-family:Manrope,sans-serif; font-size:clamp(30px,4.4vw,48px); line-height:1.08; letter-spacing:-.045em; margin:0; }}
.hero p {{ font-size:15px; margin:12px 0 0; max-width:580px; line-height:1.55; }}
.glass {{ border:1px solid; border-radius:20px; backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); padding:18px 22px; }}
.section-title {{ font-family:Manrope,sans-serif; font-size:18px; font-weight:750; letter-spacing:-.025em; margin:0 0 5px; }}
.section-sub {{ font-size:13px; margin:0 0 8px; }}
.pill {{ display:inline-block; color:#7462c6; background:#f0edff; border-radius:999px; padding:6px 11px; font-size:11px; font-weight:700; letter-spacing:.04em; }}
.stButton button {{ border-radius:12px; border:1px solid #e7e5f0; background:rgba(255,255,255,.82); color:#575d70; font-weight:600; min-height:40px; }}
.stFileUploader section {{ border:1px dashed #c9c4e1; border-radius:16px; }}
[data-testid="stFileUploader"] button {{ background:linear-gradient(145deg,#8c76e8,#7059d8) !important; border:0 !important; color:white !important; }}
[data-testid="stDataFrame"] {{ border:1px solid rgba(227,228,237,.9); border-radius:14px; overflow:hidden; }}
[data-baseweb="tag"] {{ background:#eeeaff !important; color:#5f50b3 !important; border:0 !important; }}
[data-baseweb="select"] > div {{ border-color:#e6e4ef !important; }}
[data-testid="stExpander"] {{ border-radius:18px; }}
.app-table-wrap {{ overflow-x:auto; border-radius:14px; border:1px solid rgba(130,135,157,.2); }}
.app-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
.dataset-table-wrap {{ max-height:290px; overflow:auto; }}
.app-table th,.app-table td {{ padding:10px 12px; border-bottom:1px solid; text-align:left; white-space:nowrap; }}
.app-table th {{ font-weight:700; }}
.app-table tr:last-child td {{ border-bottom:0; }}
[data-testid="stPlotlyChart"] .js-plotly-plot {{ filter:drop-shadow(0 10px 18px rgba(63,69,105,.11)); }}
[data-testid="stColorPicker"] [data-baseweb="input"] {{ border-radius:10px; }}
{dark_css if is_dark else light_css}
@media(max-width:700px) {{ .block-container {{ padding:1rem .9rem 2.5rem; }} .hero {{ padding:24px 21px; border-radius:22px; }} .glass {{ padding:16px 16px; border-radius:17px; }} .brand {{ font-size:11px; }} }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="kicker">Statistika deskriptif</div><h1>Baca data.<br>Temukan ceritanya.</h1><p>Unggah dataset, pilih variabel yang ingin dilihat, lalu biarkan ringkasan statistik menyusunnya dengan jelas.</p></div>', unsafe_allow_html=True)
st.write("")

st.markdown('<div class="glass"><div class="pill">01 &nbsp; DATA</div><div style="height:9px"></div><div class="section-title">Mulai dari dataset</div><div class="section-sub">Unggah file yang ingin dianalisis.</div></div>', unsafe_allow_html=True)
upload = st.file_uploader("Pilih file Excel atau CSV", type=["xlsx", "xls", "csv"])
if upload is None:
    st.info("Unggah dataset sendiri, atau unduh salah satu file contoh untuk mencoba aplikasi.")
    sample_dir = Path(__file__).parent / "data"
    sample_files = [
        ("Contoh CSV", "data_contoh_statistika.csv", "text/csv"),
        ("Contoh XLSX", "data_contoh_statistika.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        ("Contoh XLS", "data_contoh_statistika.xls", "application/vnd.ms-excel"),
    ]
    sample_columns = st.columns(3)
    for column, (label, filename, mime) in zip(sample_columns, sample_files):
        with column:
            st.download_button(label, (sample_dir / filename).read_bytes(), file_name=filename, mime=mime, width="stretch")
    st.stop()
try:
    if upload.name.lower().endswith(".csv"):
        df = pd.read_csv(upload)
    else:
        df = pd.read_excel(upload)
    source_label = upload.name
except Exception as exc:
    st.error(f"File belum bisa dibaca. Periksa formatnya lalu coba lagi. ({exc})")
    st.stop()

missing_total = int(df.isna().sum().sum())
st.caption(f"{source_label} · {len(df)} baris · {len(df.columns)} kolom · {missing_total} nilai kosong")
missing_method = st.radio(
    "Penanganan nilai kosong",
    ["Abaikan nilai kosong", "Isi dengan median kolom"],
    horizontal=True,
    help="Pilihan ini berlaku pada kolom numerik yang dianalisis.",
)
df_calc = df.copy()
numeric_cols_all = list(df.select_dtypes(include="number").columns)
if missing_method == "Isi dengan median kolom":
    for col in numeric_cols_all:
        if df_calc[col].notna().any():
            df_calc[col] = df_calc[col].fillna(df_calc[col].median())

st.write("")
left, right = st.columns([1.15, .85], gap="medium")
with left:
    st.markdown('<div class="glass"><div class="pill">02 &nbsp; PILIH VARIABEL</div><div style="height:9px"></div><div class="section-title">Apa yang ingin kamu lihat?</div><div class="section-sub">Pilih satu atau beberapa kolom numerik.</div></div>', unsafe_allow_html=True)
    numeric_cols = numeric_cols_all
    if numeric_cols:
        default_cols = numeric_cols[:min(2, len(numeric_cols))]
        selected_cols = st.multiselect("Variabel", numeric_cols, default=default_cols, label_visibility="collapsed", placeholder="Pilih variabel numerik")
    else:
        selected_cols = []
        st.info("Dataset ini belum memiliki kolom numerik yang bisa dianalisis.")
with right:
    st.markdown('<div class="glass"><div class="pill">03 &nbsp; UKURAN</div><div style="height:9px"></div><div class="section-title">Ringkasan statistik</div><div class="section-sub">Ukuran yang dihitung otomatis.</div></div>', unsafe_allow_html=True)
    measures = ["Jumlah data (N)", "Minimum", "Maksimum", "Mean", "Median", "Modus", "Varians sampel", "Standar deviasi", "Kuartil (Q1, Q2, Q3)"]
    default_measures = ["Jumlah data (N)", "Minimum", "Maksimum", "Mean", "Median", "Standar deviasi"]
    selected_measures = st.multiselect("Ukuran", measures, default=default_measures, label_visibility="collapsed", placeholder="Pilih ukuran statistik")

st.write("")
st.markdown('<div class="glass"><div class="pill">DATASET</div><div style="height:9px"></div><div class="section-title">Tinjau data</div></div>', unsafe_allow_html=True)
dataset_html = df.to_html(index=False, escape=True, classes="app-table", border=0)
st.markdown(f'<div class="app-table-wrap dataset-table-wrap">{dataset_html}</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="glass"><div class="pill">HASIL ANALISIS</div><div style="height:9px"></div><div class="section-title">Ringkasan deskriptif</div><div class="section-sub">Nilai kosong '+("diisi dengan median" if missing_method == "Isi dengan median kolom" else "diabaikan")+' dalam perhitungan.</div></div>', unsafe_allow_html=True)

def mode_text(values):
    values = values.dropna()
    if values.empty:
        return "—"
    counts = values.value_counts()
    modes = counts[counts == counts.max()].index.tolist()
    if counts.max() == 1 and len(counts) > 1:
        return "Tidak ada"
    return ", ".join(f"{v:g}" if isinstance(v, (int, float)) else str(v) for v in modes[:4])

def show_html_table(table):
    html = table.to_html(index=False, escape=True, classes="app-table", border=0)
    st.markdown(f'<div class="app-table-wrap">{html}</div>', unsafe_allow_html=True)

result = pd.DataFrame()
analysis_series = {}
if selected_cols and selected_measures:
    rows = []
    for col in selected_cols:
        x = pd.to_numeric(df_calc[col], errors="coerce").dropna()
        analysis_series[col] = x
        values = {
            "Jumlah data (N)": len(x),
            "Minimum": x.min() if len(x) else None,
            "Maksimum": x.max() if len(x) else None,
            "Mean": x.mean() if len(x) else None,
            "Median": x.median() if len(x) else None,
            "Modus": mode_text(x),
            "Varians sampel": x.var(ddof=1) if len(x) > 1 else None,
            "Standar deviasi": x.std(ddof=1) if len(x) > 1 else None,
        }
        if "Kuartil (Q1, Q2, Q3)" in selected_measures and len(x):
            q = x.quantile([.25, .5, .75])
            values.update({"Q1": q.loc[.25], "Q2": q.loc[.5], "Q3": q.loc[.75]})
        row = {"Variabel": col}
        row.update({m: values[m] for m in selected_measures if m != "Kuartil (Q1, Q2, Q3)"})
        if "Kuartil (Q1, Q2, Q3)" in selected_measures:
            row.update({k: values[k] for k in ["Q1", "Q2", "Q3"] if k in values})
        rows.append(row)
    result = pd.DataFrame(rows)
    display_result = result.copy()
    for col in display_result.columns[1:]:
        display_result[col] = display_result[col].map(lambda v: f"{v:.2f}" if isinstance(v, (int, float)) and not pd.isna(v) else v)
    show_html_table(display_result)
    st.caption("Varians dan standar deviasi memakai rumus sampel (n−1).")
    csv_bytes = result.to_csv(index=False).encode("utf-8-sig")
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        result.to_excel(writer, index=False, sheet_name="Ringkasan")
    download_csv, download_excel = st.columns(2)
    with download_csv:
        st.download_button("Unduh CSV", csv_bytes, file_name="ringkasan_statistik.csv", mime="text/csv", width="stretch")
    with download_excel:
        st.download_button("Unduh Excel", excel_buffer.getvalue(), file_name="ringkasan_statistik.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width="stretch")
elif not selected_cols:
    st.info("Pilih kolom numerik untuk melihat ringkasan statistik.")
else:
    st.info("Pilih setidaknya satu ukuran statistik.")

with st.expander("Eksplorasi data · grafik, frekuensi, dan interpretasi", expanded=False):
    st.markdown("#### Visualisasi")
    chart_types = ["Histogram", "Boxplot", "Diagram batang", "Diagram lingkaran"]
    chart_type = st.selectbox("Jenis grafik", chart_types)
    chart_color = st.color_picker("Warna grafik", "#8066E8")
    is_numeric_chart = chart_type in ["Histogram", "Boxplot"]
    chart_columns = numeric_cols if is_numeric_chart else list(df.select_dtypes(exclude="number").columns)
    if chart_columns:
        default_chart_col = chart_columns[0]
        if not is_numeric_chart and "Kelompok" in chart_columns:
            default_chart_col = "Kelompok"
        chart_col = st.selectbox("Variabel grafik", chart_columns, index=chart_columns.index(default_chart_col))
        if is_numeric_chart:
            chart_values = pd.to_numeric(df_calc[chart_col], errors="coerce").dropna()
            chart_df = pd.DataFrame({chart_col: chart_values})
            if chart_type == "Histogram":
                bin_count = st.slider("Jumlah interval histogram", 5, 30, 12)
                fig = px.histogram(chart_df, x=chart_col, nbins=bin_count, color_discrete_sequence=[chart_color])
                fig.update_traces(marker_line_color="rgba(255,255,255,.35)", marker_line_width=1)
            else:
                fig = px.box(chart_df, y=chart_col, points="all", color_discrete_sequence=[chart_color])
        else:
            category_values = df[chart_col].fillna("(Kosong)").astype(str).value_counts().head(12)
            chart_df = category_values.rename_axis(chart_col).reset_index(name="Frekuensi")
            def coordinated_palette(base_color, count=12):
                red = int(base_color[1:3], 16) / 255
                green = int(base_color[3:5], 16) / 255
                blue = int(base_color[5:7], 16) / 255
                hue, _, saturation = colorsys.rgb_to_hls(red, green, blue)
                saturation = max(.42, min(.78, saturation))
                lightnesses = [.40 + (.38 * i / max(1, count - 1)) for i in range(count)]
                return ["#%02x%02x%02x" % tuple(round(channel * 255) for channel in colorsys.hls_to_rgb(hue, lightness, saturation)) for lightness in lightnesses]

            palette = coordinated_palette(chart_color, max(8, len(chart_df)))
            if chart_type == "Diagram batang":
                fig = px.bar(chart_df, x=chart_col, y="Frekuensi", color=chart_col, color_discrete_sequence=palette)
                fig.update_layout(showlegend=False)
            else:
                fig = px.pie(chart_df, names=chart_col, values="Frekuensi", color_discrete_sequence=palette, hole=.42)
                fig.update_traces(marker_line_color="#242638" if is_dark else "rgba(255,255,255,.92)", marker_line_width=2, textposition="inside", textinfo="label+percent")
        fig.update_traces(marker_line_color="#242638" if is_dark else "rgba(255,255,255,.92)", marker_line_width=1.5)
        chart_text_color = "#e7e8f0" if is_dark else "#42475a"
        fig.update_layout(
            template="plotly_dark" if is_dark else "plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=chart_text_color, family="DM Sans"),
            legend=dict(font=dict(color=chart_text_color), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=20, b=10),
            legend_title_text="",
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Grafik ini memerlukan setidaknya satu kolom yang sesuai: numerik untuk histogram/boxplot, atau kategori untuk diagram batang/lingkaran.")

    st.markdown("#### Tabel distribusi frekuensi")
    if len(df.columns):
        frequency_columns = list(df.columns)
        default_frequency_col = selected_cols[0] if selected_cols else frequency_columns[0]
        if not selected_cols and "Kelompok" in frequency_columns:
            default_frequency_col = "Kelompok"
        freq_col = st.selectbox("Variabel frekuensi", frequency_columns, index=frequency_columns.index(default_frequency_col), key="frequency_column")
        if freq_col in numeric_cols_all:
            freq_values = pd.to_numeric(df_calc[freq_col], errors="coerce")
            bins = st.slider("Jumlah kelas", 3, 15, 6, key="frequency_bins")
            non_missing = freq_values.dropna()
            if len(non_missing):
                grouped = pd.cut(non_missing, bins=bins, include_lowest=True)
                frequency = grouped.value_counts(sort=False)
                frequency.index = frequency.index.astype(str)
                freq_table = pd.DataFrame({"Kelas": frequency.index, "Frekuensi": frequency.values})
            else:
                freq_table = pd.DataFrame(columns=["Kelas", "Frekuensi"])
            missing_n = int(freq_values.isna().sum())
            if missing_n:
                freq_table.loc[len(freq_table)] = ["(Kosong)", missing_n]
        else:
            frequency = df[freq_col].fillna("(Kosong)").astype(str).value_counts()
            freq_table = pd.DataFrame({"Kategori": frequency.index.astype(str), "Frekuensi": frequency.values})
        if not freq_table.empty:
            freq_table["Persentase"] = (freq_table["Frekuensi"] / max(1, len(df)) * 100).map(lambda v: f"{v:.1f}%")
            freq_table["Frekuensi kumulatif"] = freq_table["Frekuensi"].cumsum()
            show_html_table(freq_table)

    st.markdown("#### Interpretasi sederhana")
    if analysis_series:
        for col, x in analysis_series.items():
            if x.empty:
                st.write(f"**{col}:** belum ada nilai numerik yang dapat diringkas.")
                continue
            missing_n = int(df[col].isna().sum())
            mean, median = x.mean(), x.median()
            tendency = "rata-rata lebih tinggi daripada median" if mean > median else "rata-rata lebih rendah daripada median" if mean < median else "rata-rata sama dengan median"
            st.write(f"**{col}:** terdapat {len(x)} nilai yang dianalisis; nilainya berkisar dari {x.min():g} sampai {x.max():g}, dan {tendency}. Nilai kosong pada kolom: {missing_n}.")
        st.caption("Interpretasi ini hanya gambaran awal; pertimbangkan konteks data sebelum menarik kesimpulan.")
    else:
        st.info("Pilih minimal satu variabel numerik untuk menampilkan interpretasi.")

st.markdown('<div style="text-align:center;color:#a0a4b1;font-size:12px;padding:28px 0 4px">Ruang Statistik &nbsp;·&nbsp; dibuat untuk memahami data, satu langkah sederhana pada satu waktu.</div>', unsafe_allow_html=True)
