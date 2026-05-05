from flask import Flask, request, redirect, make_response
import sqlite3
import datetime

app = Flask(__name__)

# ================= DB =================
def init_db():
    conn = sqlite3.connect('disiplin.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS pelajar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        ic TEXT,
        kelas TEXT,
        asrama TEXT,
        jantina TEXT,
        markah INTEGER DEFAULT 100
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS rekod (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pelajar_id INTEGER,
        tarikh TEXT,
        jenis TEXT,
        keterangan TEXT,
        markah INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('disiplin.db')
    conn.row_factory = sqlite3.Row
    return conn
    conn.execute("""
    INSERT INTO pelajar (nama, ic, kelas, asrama, jantina, markah)
    VALUES (?, ?, ?, ?, ?, 100)
    """, (nama, ic, kelas, asrama, jantina))

    conn.commit()      # WAJIB
    conn.close()
    return redirect("/")   # WAJIB

# ================= HOME =================
@app.route('/')
def home():
    with get_db() as conn:
       pelajar = conn.execute("SELECT * FROM pelajar").fetchall()

    lelaki = [p for p in pelajar if p["jantina"] == "Lelaki"]
    perempuan = [p for p in pelajar if p["jantina"] == "Perempuan"]
    html = f"""
    <html>
    <head>
    <title>Sistem Disiplin Asrama</title>
    <style>
    body {{
        font-family: 'Segoe UI';
        background:#eef2f7;
        padding:20px;
    }}
    .container {{
        max-width:1100px;
        margin:auto;
        background:white;
        padding:25px;
        border-radius:12px;
        box-shadow:0 5px 15px rgba(0,0,0,0.1);
    }}
    .header {{
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:20px;
    }}
    .header img {{ height:70px; }}
    .title {{
        flex:1;
        text-align:center;
        font-size:22px;
        font-weight:bold;
    }}
    .btn {{
        padding:6px 10px;
        border-radius:6px;
        color:white;
        text-decoration:none;
        font-size:13px;
    }}
    .blue {{ background:#007bff; }}
    .orange {{ background:#f0ad4e; }}
    .red {{ background:#d9534f; }}
    .green {{ background:#28a745; }}
    table {{
        width:100%;
        border-collapse:collapse;
        margin-top:10px;
    }}
    th {{
        background:#2c3e50;
        color:white;
        padding:10px;
    }}
    td {{
        padding:8px;
        border-bottom:1px solid #ddd;
        text-align:center;
    }}
    .section {{
        background:#34495e;
        color:white;
        padding:8px;
        margin-top:20px;
        border-radius:5px;
        font-weight:bold;
    }}
    </style>
    </head>

    <body>
    <div class="container">

    <div class="header">
        <img src="/static/smknyalas_logo.png">
        <div class="title">🏫 Sistem Disiplin Asrama SMK Nyalas</div>
        <img src="/static/logo_asramasmknyalas.png">
    </div>

    <a href="/tambah_lelaki" class="btn green">+ Tambah Lelaki</a>
    <a href="/tambah_perempuan" class="btn orange">+ Tambah Perempuan</a>
    """

    # ===== lelaki =====
    html += """
    <div class="section">LELAKI</div>
    <table>
    <tr>
    <th>ID</th><th>Nama</th><th>IC</th><th>Kelas</th>
    <th>Asrama</th><th>Markah</th><th>Tindakan</th>
    </tr>
    """

    for p in lelaki:
        html += f"""
        <tr>
        <td>{p['id']}</td>
        <td>{p['nama']}</td>
        <td>{p['ic']}</td>
        <td>{p['kelas']}</td>
        <td>{p['asrama']}</td>
        <td>{p['markah']}</td>
        <td>
        <a href="/rekod/{p['id']}" class="btn blue">Rekod</a>
        <a href="/edit/{p['id']}" class="btn orange">Edit</a>
        <a href="/delete/{p['id']}" class="btn red">Delete</a>
        </td>
        </tr>
        """

    html += "</table>"

    # ===== perempuan =====
    html += """
    <div class="section">PEREMPUAN</div>
    <table>
    <tr>
    <th>ID</th><th>Nama</th><th>IC</th><th>Kelas</th>
    <th>Asrama</th><th>Markah</th><th>Tindakan</th>
    </tr>
    """

    for p in perempuan:
        html += f"""
        <tr>
        <td>{p['id']}</td>
        <td>{p['nama']}</td>
        <td>{p['ic']}</td>
        <td>{p['kelas']}</td>
        <td>{p['asrama']}</td>
        <td>{p['markah']}</td>
        <td>
        <a href="/rekod/{p['id']}" class="btn blue">Rekod</a>
        <a href="/edit/{p['id']}" class="btn orange">Edit</a>
        <a href="/delete/{p['id']}" class="btn red">Delete</a>
        </td>
        </tr>
        """

    html += """
    </table>
    </div>
    </body>
    </html>
    """

    return html

# ================= TAMBAH =================
# ================================
# TEMPLATE FORM TAMBAH (UNIVERSAL)
# ================================
def page_tambah(jantina, warna):

    if request.method == "POST":
        nama = request.form["nama"]
        ic = request.form["ic"]
        kelas = request.form["kelas"]
        asrama = request.form["asrama"]

        conn = get_db()
        conn.execute("""
        INSERT INTO pelajar (nama, ic, kelas, asrama, jantina, markah)
        VALUES (?, ?, ?, ?, ?, 100)
        """, (nama, ic, kelas, asrama, jantina))
        conn.commit()
        conn.close()

        return redirect("/")

    return f"""
    <html>
    <head>
    <style>

    body {{
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to right, #eef2f7, #dfe7f1);
        margin:0;
    }}

    .container {{
        max-width: 550px;
        margin: 60px auto;
        background: white;
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }}

    .header {{
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:25px;
    }}

    .header img {{
        width:60px;
    }}

    .title {{
        text-align:center;
        flex:1;
    }}

    .title h2 {{
        margin:0;
        font-size:20px;
    }}

    .subtitle {{
        font-size:12px;
        color:#666;
        margin-top:3px;
    }}

    .badge {{
        display:inline-block;
        margin-top:8px;
        background:{warna};
        color:white;
        padding:5px 14px;
        border-radius:10px;
        font-size:12px;
        font-weight:bold;
    }}

    label {{
        display:block;
        margin-top:15px;
        font-weight:600;
    }}

    input {{
        width:100%;
        padding:11px;
        margin-top:5px;
        border-radius:6px;
        border:1px solid #ccc;
        font-size:14px;
    }}

    button {{
        width:100%;
        margin-top:25px;
        padding:13px;
        background:{warna};
        color:white;
        border:none;
        border-radius:8px;
        font-size:16px;
        font-weight:bold;
        cursor:pointer;
    }}

    .back {{
        display:block;
        text-align:center;
        margin-top:18px;
        color:#555;
        text-decoration:none;
    }}

    </style>
    </head>

    <body>

    <div class="container">

        <div class="header">
            <img src="/static/smknyalas_logo.png">

            <div class="title">
                <h2>Tambah Pelajar {jantina}</h2>
                <div class="subtitle">Asrama SMK Nyalas</div>
                <div class="badge">{jantina.upper()}</div>
            </div>

            <img src="/static/logo_asramasmknyalas.png">
        </div>

        <form method="POST">

            <label>Nama</label>
            <input type="text" name="nama" required>

            <label>No IC</label>
            <input type="text" name="ic" required>

            <label>Kelas</label>
            <input type="text" name="kelas" required>

            <label>Asrama</label>
            <input type="text" name="asrama" required>

            <button type="submit">+ Tambah Pelajar</button>

        </form>

        <a class="back" href="/">← Kembali</a>

    </div>

    </body>
    </html>
    """


# ================================
# ROUTE LELAKI & PEREMPUAN
# ================================
@app.route('/tambah_lelaki', methods=['GET','POST'])
def tambah_lelaki():
    return page_tambah("Lelaki", "#007bff")


@app.route('/tambah_perempuan', methods=['GET','POST'])
def tambah_perempuan():
    return page_tambah("Perempuan", "#e83e8c")

# ================= REKOD =================
@app.route('/rekod/<int:pid>', methods=['GET','POST'])
def rekod(pid):
    import datetime

    with get_db() as conn:

        pelajar = conn.execute(
            "SELECT * FROM pelajar WHERE id=?",
            (pid,)
        ).fetchone()

        # ================= SIMPAN REKOD =================
        if request.method == 'POST':
            jenis = request.form['jenis']
            keterangan = request.form['keterangan']
            markah = int(request.form['markah'])

            if jenis == "Kesalahan":
                markah = -abs(markah)
            else:
                markah = abs(markah)

            conn.execute(
                "INSERT INTO rekod (pelajar_id, tarikh, keterangan, markah) VALUES (?,?,?,?)",
                (pid, datetime.date.today(), keterangan, markah)
            )

            # update markah pelajar
            conn.execute(
                "UPDATE pelajar SET markah = markah + ? WHERE id=?",
                (markah, pid)
            )

            conn.commit()
            return redirect(f"/rekod/{pid}")

        # ================= AMBIL REKOD =================
        rekod_list = conn.execute(
            "SELECT * FROM rekod WHERE pelajar_id=?",
            (pid,)
        ).fetchall()

    # ================= STATUS =================
    if pelajar['markah'] <= 75:
        status = '<div class="alert red">❌ Status: Tidak Layak Asrama Tahun Hadapan</div>'
        btn = f'<a href="/surat/{pid}" class="link">📄 Jana Surat Tidak Layak</a>'
    elif pelajar['markah'] <= 79:
        status = '<div class="alert orange">⚠️ Status: Amaran Tegas</div>'
        btn = f'<a href="/surat/{pid}" class="link">📄 Jana Surat Amaran</a>'
    else:
        status = '<div class="alert green">✅ Status: Disiplin Baik</div>'
        btn = f'<a href="/surat/{pid}" class="link">📄 Lihat Surat</a>'

    # ================= SENARAI =================
    senarai = ""
    for r in rekod_list:
        warna = "red" if r['markah'] < 0 else "green"
        senarai += f"""
        <li class="{warna}">
            {r['tarikh']} - {r['keterangan']} ({r['markah']})
            <a href="/delete_rekod/{pid}/{r['id']}" class="delete">✖</a>
        </li>
        """

    # ================= HTML =================
    html = f"""
    <html>
    <head>
    <title>Rekod</title>

    <style>
    body {{
        font-family: Arial;
        background:#eef2f7;
        padding:40px;
    }}

    .container {{
        max-width:600px;
        margin:auto;
        background:white;
        padding:25px;
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.1);
    }}

    h2 {{
        margin-bottom:5px;
    }}

    .form-group {{
        margin-bottom:15px;
    }}

    input, select {{
        width:100%;
        padding:10px;
        border-radius:8px;
        border:1px solid #ccc;
    }}

    button {{
        width:100%;
        padding:12px;
        background:#007bff;
        color:white;
        border:none;
        border-radius:8px;
        font-weight:bold;
        cursor:pointer;
    }}

    .alert {{
        margin-top:15px;
        padding:10px;
        border-radius:8px;
        font-weight:bold;
    }}

    .green {{background:#d4edda;color:#155724;}}
    .red {{background:#f8d7da;color:#721c24;}}
    .orange {{background:#fff3cd;color:#856404;}}

    ul {{
        margin-top:10px;
    }}

    li {{
        margin-bottom:6px;
    }}

    .red {{color:red;}}
    .green {{color:green;}}

    .delete {{
        margin-left:10px;
        color:red;
        text-decoration:none;
        font-weight:bold;
    }}

    .link {{
        display:inline-block;
        margin-top:10px;
        font-weight:bold;
        color:#007bff;
        text-decoration:none;
    }}

    </style>
    </head>

    <body>

    <div class="container">

    <h2>Rekod: {pelajar['nama']}</h2>
    <div>Markah Semasa: {pelajar['markah']}</div>

    <form method="POST">

    <div class="form-group">
    <label>Jenis</label>
    <select name="jenis">
        <option value="Kesalahan">Kesalahan</option>
        <option value="Kebaikan">Kebaikan</option>
    </select>
    </div>

    <div class="form-group">
    <label>Keterangan</label>
    <input type="text" name="keterangan" required>
    </div>

    <div class="form-group">
    <label>Markah</label>
    <input type="number" name="markah" required>
    </div>

    <button type="submit">💾 Simpan Rekod</button>

    </form>

    {status}
    {btn}

    <h3>Rekod Disiplin</h3>
    <ul>
    {senarai}
    </ul>

    <br>
    <a href="/" class="link">← Kembali</a>

    </div>

    </body>
    </html>
    """

    return html

# ======================
# DELETE REKOD (WAJIB ADA)
# ======================
@app.route('/delete_rekod/<int:pid>/<int:rid>')
def delete_rekod(pid, rid):
    with get_db() as conn:
        # ambil markah rekod tu dulu
        rekod = conn.execute(
            "SELECT markah FROM rekod WHERE id=?",
            (rid,)
        ).fetchone()

        if rekod:
            # tambah balik markah (reverse)
            conn.execute(
                "UPDATE pelajar SET markah = markah + ? WHERE id=?",
                (abs(rekod["markah"]), pid)
            )

        # delete rekod
        conn.execute(
            "DELETE FROM rekod WHERE id=?",
            (rid,)
        )

        conn.commit()

    return redirect(f"/rekod/{pid}")

# ================= SURAT =================
@app.route('/surat/<int:pid>')
def surat(pid):
    import datetime

    with get_db() as conn:
        pelajar = conn.execute(
            "SELECT * FROM pelajar WHERE id=?",
            (pid,)
        ).fetchone()

        rekod_list = conn.execute(
            "SELECT * FROM rekod WHERE pelajar_id=?",
            (pid,)
        ).fetchall()

    # ========================
    # BINA SENARAI REKOD
    # ========================
    senarai_rekod = ""
    jumlah_markah = 0

    for r in rekod_list:
        markah = r["markah"] if r["markah"] else 0
        jumlah_markah += abs(markah)

        senarai_rekod += f"""
        <li>{r['tarikh']} - {r['keterangan']} ({markah})</li>
        """

    # ========================
    # LOGIC SURAT IKUT MARKAH
    # ========================
    if pelajar["markah"] <= 75:
        tajuk = "SURAT TIDAK LAYAK MENDUDUKI ASRAMA"
        ayat = f"""
        Adalah dimaklumkan bahawa pelajar berikut telah menunjukkan tahap disiplin yang tidak memuaskan.
        Berdasarkan rekod disiplin yang direkodkan, pelajar telah mencapai tahap markah yang rendah.

        Sehubungan dengan itu, pihak pengurusan asrama dengan ini memutuskan bahawa pelajar ini
        <b>TIDAK LAYAK</b> untuk meneruskan atau memohon kemasukan ke asrama pada sesi akan datang.

        Keputusan ini adalah muktamad bagi memastikan disiplin dan persekitaran asrama sentiasa berada dalam keadaan terkawal.
        """

    elif pelajar["markah"] <= 79:
        tajuk = "SURAT AMARAN DISIPLIN PELAJAR ASRAMA"
        ayat = f"""
        Adalah dimaklumkan bahawa pelajar berikut telah melakukan kesalahan disiplin yang melanggar peraturan asrama.
        Pihak pengurusan memandang serius perkara ini dan dengan ini mengeluarkan
        <span style='color:red;font-weight:bold;'>AMARAN TEGAS</span> kepada pelajar.

        Pelajar dikehendaki segera memperbaiki disiplin serta mematuhi semua peraturan yang telah ditetapkan.
        Sekiranya kesalahan berulang, tindakan yang lebih tegas akan diambil termasuk penarikan kelayakan asrama.
        """

    else:
        tajuk = "SURAT MAKLUMAN DISIPLIN PELAJAR"
        ayat = f"""
        Pelajar berada dalam keadaan disiplin yang baik.
        Namun begitu, pelajar diingatkan supaya terus mengekalkan disiplin dan mematuhi segala peraturan asrama.
        """

    # ========================
    # HTML SURAT
    # ========================
    html = f"""
    <html>
    <head>
    <title>Surat</title>

    <style>
    body {{
        font-family: Arial;
        margin: 40px;
    }}

    h3 {{
        text-align: center;
        margin-top: 40px;
        margin-bottom: 30px;
    }}

    p {{
        text-align: justify;
        margin-bottom: 15px;
    }}

    ul {{
        margin-left: 20px;
    }}

    .signature {{
        margin-top: 100px;
        display: flex;
        justify-content: space-between;
    }}

    .sign-box {{
        width: 45%;
    }}

    .sign-box:last-child {{
        text-align: right;
    }}

    /* ================= PRINT SETTING ================= */
    @media print {{
        button {{
            display: none;
        }}

        body {{
            margin: 40px;
        }}
    }}
    </style>

    </head>

    <body>

    <!-- 🔥 BUTTON PRINT -->
    <button onclick="window.print()" 
    style="position:fixed;top:20px;right:20px;padding:10px 14px;
    background:#007bff;color:white;border:none;border-radius:6px;cursor:pointer;">
    🖨️ Print / Save PDF
    </button>

    <div class="container">

    <div style="display:flex;justify-content:space-between;align-items:center;">
        <img src="/static/logo_asramasmknyalas.png" width="80">
        <div style="text-align:center;">
            <b>ASRAMA SEKOLAH MENENGAH KEBANGSAAN NYALAS</b><br>
            77100 ASAHAN<br>
            MELAKA
        </div>
        <img src="/static/smknyalas_logo.png" width="80">
    </div>

    <div style="text-align:right;margin-top:20px;">
        No. Rujukan: SMKN/ASR/{pid}/{datetime.date.today().strftime('%Y%m%d')}<br>
        Tarikh: {datetime.date.today().strftime('%d/%m/%Y')}
    </div>

    <h3>{tajuk}</h3>

    <p>{ayat}</p>

    <p>
    Nama: {pelajar['nama']}<br>
    Kelas: {pelajar['kelas']}<br>
    Asrama: {pelajar['asrama']}<br>
    Markah Disiplin Semasa: {pelajar['markah']}
    </p>

    <p><b>Rekod kesalahan:</b></p>
    <ul>
    {senarai_rekod}
    </ul>

    <p><b>Jumlah potongan markah: {jumlah_markah} markah</b></p>

    <p>Sekian, terima kasih.</p>

    <div class="signature">
        <div class="sign-box">
            ___________________________<br><br>
            (MUHAMMAD DZAMIRUL AZIM BIN MAZLAN)<br>
            Ketua Warden Asrama<br>
            SMK Nyalas
        </div>

        <div class="sign-box">
            ___________________________<br><br>
            (ROSLAN BIN YAAKOB)<br>
            Penolong Kanan Hal Ehwal Murid (GPK HEM)<br>
            SMK Nyalas
        </div>
    </div>

    </div>

    </body>
    </html>
    """

    return html

# ================= DELETE =================
@app.route('/delete/<int:id>')
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM pelajar WHERE id=?", (id,))
        conn.execute("DELETE FROM rekod WHERE pelajar_id=?", (id,))
    return redirect('/')

# ================= EDIT =================
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    conn = get_db()

    if request.method == 'POST':
        conn.execute("""
        UPDATE pelajar
        SET nama=?, ic=?, kelas=?, asrama=?
        WHERE id=?
        """, (
            request.form['nama'],
            request.form['ic'],
            request.form['kelas'],
            request.form['asrama'],
            id
        ))
        conn.commit()
        return redirect('/')

    p = conn.execute("SELECT * FROM pelajar WHERE id=?", (id,)).fetchone()

    return f"""
    <html>
    <head>
    <title>Edit Pelajar</title>

    <style>
    body {{
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to right, #eef2f7, #dfe7f1);
        margin:0;
    }}

    .container {{
        max-width: 600px;
        margin: 50px auto;
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }}

    .header {{
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:20px;
    }}

    .title {{
        text-align:center;
        flex:1;
        font-size:22px;
        font-weight:bold;
    }}

    .subtitle {{
        font-size:12px;
        color:gray;
    }}

    label {{
        font-weight:600;
        margin top:12px;
        display:block;
    }}

    input {{
        width:100%;
        padding:10px;
        margin-top:5px;
        border-radius:6px;
        border:1px solid #ccc;
    }}

    button {{
        width:100%;
        margin-top:25px;
        padding:12px;
        background:#ff9800;
        color:white;
        border:none;
        border-radius:8px;
        font-size:15px;
        font-weight:bold;
        cursor:pointer;
    }}

    button:hover {{
        background:#e68900;
    }}

    .back {{
        display:block;
        text-align:center;
        margin-top:15px;
        color:#555;
        text-decoration:none;
    }}

    .badge {{
        display:inline-block;
        margin-top:8px;
        background:#28a745;
        color:white;
        padding:5px 10px;
        border-radius:6px;
        font-size:12px;
    }}

    </style>
    </head>

    <body>

    <div class="container">

        <div class="header">
            <img src="/static/smknyalas_logo.png" width="60">
            
            <div class="title">
                ✏️ Edit Pelajar
                <div class="subtitle">Asrama SMK Nyalas</div>
                <div class="badge">{p['jantina']}</div>
            </div>

            <img src="/static/logo_asramasmknyalas.png" width="60">
        </div>

        <form method="POST">

            <label>Nama</label>
            <input name="nama" value="{p['nama']}" required>

            <label>No IC</label>
            <input name="ic" value="{p['ic']}" required>

            <label>Kelas</label>
            <input name="kelas" value="{p['kelas']}" required>

            <label>Asrama</label>
            <input name="asrama" value="{p['asrama']}" required>

            <button type="submit">💾 Update Pelajar</button>

        </form>

        <a href="/" class="back">← Kembali</a>

    </div>

    </body>
    </html>
    """

# ================= RUN =================
if __name__ == '__main__':
    print("🚀 Sistem Disiplin SMK Nyalas BERJALAN")
    app.run(host="0.0.0.0", port=10000)
