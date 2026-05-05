from flask import Flask, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

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
        markah INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS rekod (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pelajar_id INTEGER,
        jenis TEXT,
        keterangan TEXT,
        markah INTEGER,
        tarikh TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('disiplin.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:

    conn.execute("""
    CREATE TABLE IF NOT EXISTS pelajar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        ic TEXT,
        kelas TEXT,
        asrama TEXT,
        markah INTEGER DEFAULT 100
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS rekod (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        pelajar_id INTEGER,
        tarikh TEXT,
        jenis TEXT,
        keterangan TEXT,
        markah INTEGER
    )
    """)
    conn.execute('''CREATE TABLE IF NOT EXISTS rekod (id INTEGER PRIMARY KEY, pelajar_id INTEGER, tarikh TEXT, jenis TEXT, keterangan TEXT, markah_ubah INTEGER)''')

@app.route('/')
def home():
    with get_db() as conn:
        pelajar = conn.execute("SELECT * FROM pelajar").fetchall()

    lelaki = [p for p in pelajar if p['jantina'] == 'L']
    perempuan = [p for p in pelajar if p['jantina'] == 'P']

    html = f"""
    <html>
    <head>
    <title>Sistem Disiplin Asrama</title>

    <style>
    body {{
        font-family: 'Segoe UI', sans-serif;
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

    .header img {{
        height:70px;
    }}

    .title {{
        text-align:center;
        flex:1;
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
        font-size:14px;
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

    .top-btn {{
        margin-bottom:10px;
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

    <div class="top-btn">
    <a href="/tambah_lelaki" style="background:green;color:white;padding:8px 12px;border-radius:6px;text-decoration:none;">
    + Tambah Lelaki
    </a>

    <a href="/tambah_perempuan" style="background:#e83e8c;color:white;padding:8px 12px;border-radius:6px;text-decoration:none;margin-left:5px;">
    + Tambah Perempuan
    </a>
    </div>
    """

    # LELAKI
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

    # PEREMPUAN
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

@app.route("/tambah_lelaki", methods=["GET", "POST"])
def tambah_lelaki():
    if request.method == "POST":
        nama = request.form.get("nama")
        ic = request.form.get("ic")
        kelas = request.form.get("kelas")
        asrama = request.form.get("asrama")

        conn = get_db()
        conn.execute(
            "INSERT INTO pelajar (nama, ic, kelas, asrama, jantina, markah) VALUES (?, ?, ?, ?, ?, ?)",
            (nama, ic, kelas, asrama, "Lelaki", 100)
            )conn.execute(
            "INSERT INTO pelajar (nama, ic, kelas, asrama, jantina, markah) VALUES (?, ?, ?, ?, ?, ?)",
            (nama, ic, kelas, asrama, "Lelaki", 100)

        )
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Tambah Pelajar Lelaki</h2>
    <form method="POST">
    Nama: <input name="nama"><br>
    IC: <input name="ic"><br>
    Kelas: <input name="kelas"><br>
    Asrama: <input name="asrama"><br>
    <button type="submit">Tambah</button>
    </form>
    <a href="/">Kembali</a>
    """

<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<title>{tajuk}</title>

<style>
body {{
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(to right, #eef2f7, #e6ecf5);
    margin: 0;
}}

.container {{
    max-width: 600px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}}

.header img {{
    width: 70px;
}}

.title {{
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}}

.subtitle {{
    font-size: 12px;
    color: gray;
}}

.badge {{
    background: #007bff;
    color: white;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 12px;
}}

label {{
    font-weight: 600;
    margin-top: 15px;
    display: block;
}}

input {{
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    margin-top: 5px;
}}

button {{
    width: 100%;
    margin-top: 25px;
    padding: 12px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}}

.back {{
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #555;
    text-decoration: none;
}}
</style>
</head>

<body>

<div class="container">

    <div class="header">
        <img src="/static/smknyalas_logo.png">
        
        <div class="title">
            {tajuk}
            <div class="subtitle">Asrama SMK Nyalas</div>
            <div class="badge">{jantina}</div>
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
@app.route("/tambah_perempuan", methods=["GET", "POST"])
def tambah_perempuan():
    if request.method == "POST":
        nama = request.form.get("nama")
        ic = request.form.get("ic")
        kelas = request.form.get("kelas")
        asrama = request.form.get("asrama")

        conn = get_db()
        conn.execute(
            "INSERT INTO pelajar (nama, ic, kelas, asrama, jantina, markah) VALUES (?, ?, ?, ?, ?, ?)",
            (nama, ic, kelas, asrama, "Perempuan", 100)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Tambah Pelajar Perempuan</h2>
    <form method="POST">
        Nama: <input name="nama"><br>
        IC: <input name="ic"><br>
        Kelas: <input name="kelas"><br>
        Asrama: <input name="asrama"><br><br>
        <button type="submit">Tambah</button>
    </form>
    <br><a href="/">Kembali</a>
    """

<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<title>{tajuk}</title>

<style>
body {{
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(to right, #fdf0f5, #f8e4ec);
    margin: 0;
}}

.container {{
    max-width: 600px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}}

.header img {{
    width: 70px;
}}

.title {{
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}}

.subtitle {{
    font-size: 12px;
    color: gray;
}}

.badge {{
    background: #e83e8c;
    color: white;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 12px;
}}

label {{
    font-weight: 600;
    margin-top: 15px;
    display: block;
}}

input {{
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    margin-top: 5px;
}}

button {{
    width: 100%;
    margin-top: 25px;
    padding: 12px;
    background: #e83e8c;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}}

.back {{
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #555;
    text-decoration: none;
}}
</style>
</head>

<body>

<div class="container">

    <div class="header">
        <img src="/static/smknyalas_logo.png">
        
        <div class="title">
            {tajuk}
            <div class="subtitle">Asrama SMK Nyalas</div>
            <div class="badge">{jantina}</div>
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

@app.route('/rekod/<int:pid>', methods=['GET','POST'])
def rekod(pid):

    with get_db() as conn:
        pelajar = conn.execute(
            "SELECT * FROM pelajar WHERE id=?",
            (pid,)
        ).fetchone()

        if request.method == 'POST':
            jenis = request.form['jenis']
            keterangan = request.form['keterangan']
            markah = int(request.form['markah'])

            # LOGIC MARKAH
            if jenis == "Kesalahan":
                markah_ubah = -abs(markah)
            else:
                markah_ubah = abs(markah)

            # SIMPAN REKOD
            conn.execute("""
                INSERT INTO rekod (pelajar_id, tarikh, jenis, keterangan, markah)
                VALUES (?, date('now'), ?, ?, ?)
            """, (pid, jenis, keterangan, markah_ubah))

            # UPDATE MARKAH SEMASA
            conn.execute("""
                UPDATE pelajar SET markah = markah + ?
                WHERE id=?
            """, (markah_ubah, pid))

            conn.commit()

        rekod_list = conn.execute(
            "SELECT * FROM rekod WHERE pelajar_id=? ORDER BY tarikh DESC",
            (pid,)
        ).fetchall()

    html = f"""
    <html>
    <head>
    <title>Rekod Pelajar</title>

    <style>
    body {{
        font-family: 'Segoe UI', sans-serif;
        background:#eef2f7;
        padding:20px;
    }}

    .container {{
        max-width:700px;
        margin:auto;
        background:white;
        padding:25px;
        border-radius:12px;
        box-shadow:0 5px 15px rgba(0,0,0,0.1);
    }}

    h1 {{
        margin-bottom:5px;
    }}

    .markah {{
        font-size:16px;
        color:#555;
        margin-bottom:15px;
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
        background:#007bff;
        color:white;
        border:none;
        padding:10px 20px;
        border-radius:8px;
        cursor:pointer;
    }}

    button:hover {{
        background:#0056b3;
    }}

    .alert {{
        margin-top:15px;
        padding:12px;
        border-radius:8px;
        background:#ffe5e5;
        color:#b30000;
        font-weight:bold;
    }}

    .good {{
        margin-top:15px;
        padding:12px;
        border-radius:8px;
        background:#e6ffea;
        color:#0a7d2c;
        font-weight:bold;
    }}

    .link {{
        display:inline-block;
        margin-top:10px;
        color:#007bff;
        text-decoration:none;
        font-weight:bold;
    }}

    .rekod-box {{
        margin-top:20px;
        padding:15px;
        background:#f9f9f9;
        border-radius:10px;
    }}

    .neg {{ color:red; }}
    .pos {{ color:green; }}

    li {{
        margin-bottom:6px;
    }}
    </style>

    </head>
    <body>

    <div class="container">

    <h1>Rekod: {pelajar['nama']}</h1>
    <div class="markah">Markah Semasa: <b>{pelajar['markah']}</b></div>

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

    <button type="submit">Simpan Rekod</button>

    </form>
    """

    # LOGIC PAPARAN
    if pelajar['markah'] < 80:
        html += f"""
        <div class="alert">⚠️ AMARAN: Markah Disiplin Rendah!</div>
        <a href="/surat/{pid}" class="link">📄 Jana Surat Amaran</a>
        """
    else:
        html += """
        <div class="good">✅ Status: Disiplin Baik</div>
        """

    html += """
    <div class="rekod-box">
    <h3>Rekod Disiplin</h3>
    <ul>
    """

    for r in rekod_list:
        if r['markah'] < 0:
            html += f"<li class='neg'>{r['tarikh']} - {r['keterangan']} ({r['markah']} markah)</li>"
        else:
            html += f"<li class='pos'>{r['tarikh']} - {r['keterangan']} (+{r['markah']} markah)</li>"

    html += """
    </ul>
    </div>

    <a href="/" class="link">⬅ Kembali</a>

    </div>
    </body>
    </html>
    """

    return html

@app.route('/surat/<int:pid>')
def surat(pid):
    import datetime

    with get_db() as conn:
        pelajar = conn.execute(
            "SELECT * FROM pelajar WHERE id=?", (pid,)
        ).fetchone()

        rekod = conn.execute(
            "SELECT * FROM rekod WHERE pelajar_id=?", (pid,)
        ).fetchall()

    senarai_rekod = ""
    jumlah_markah = 0

    for r in rekod:
        markah = r['markah'] if r['markah'] else 0
        jumlah_markah += abs(markah)

        senarai_rekod += f"<li>{r['tarikh']} – {r['keterangan']} ({markah} markah)</li>"

    html = f"""
<html>
<head>
<title>Surat Amaran</title>

<style>
body{{font-family:Arial;padding:40px;line-height:1.6}}

.header{{
    display:flex;
    align-items:center;
    justify-content:space-between;
}}

.header-center{{
    text-align:center;
    flex:1;
}}

.logo{{
    width:80px;
}}

.rujukan{{
    text-align:right;
    margin-top:10px;
}}

.signature{{
    margin-top:80px;
    display:flex;
    justify-content:space-between;
}}
</style>

</head>
<body>

<div class="header">
    <img src="/static/smknyalas_logo.png" class="logo">

    <div class="header-center">
        <h3>ASRAMA SEKOLAH MENENGAH KEBANGSAAN NYALAS</h3>
        <p>77100 ASAHAN<br>MELAKA<br>Email: asramasmknyalas1079@gmail.com</p>
    </div>

    <img src="/static/logo_asramasmknyalas.png" class="logo">
</div>

<div class="rujukan">
    No. Rujukan: SMKN/ASR/DIS/{pid}/{datetime.date.today().strftime('%Y%m%d')}<br>
    Tarikh: {datetime.date.today().strftime('%d/%m/%Y')}
</div>

<h3 style="text-align:center;margin-top:30px;">
SURAT AMARAN DISIPLIN PELAJAR ASRAMA
</h3>

<p>
Adalah dimaklumkan bahawa pelajar berikut telah melakukan kesalahan disiplin asrama seperti yang direkodkan di bawah:
</p>

<p>
Nama Pelajar : {pelajar['nama']}<br>
Kelas : {pelajar['kelas']}<br>
Asrama : {pelajar['asrama']}<br>
Markah Disiplin Semasa : {pelajar['markah']}
</p>

<p><b>Kesalahan direkodkan:</b></p>
<ul>
{senarai_rekod}
</ul>

<p><b>Jumlah potongan markah: {jumlah_markah} markah</b></p>

<p>
Pihak pengurusan asrama memandang serius kesalahan disiplin yang telah dilakukan oleh pelajar. Sehubungan itu, pelajar ini dengan ini diberikan <b style="color:red">AMARAN RASMI</b>. Pelajar diingatkan supaya tidak mengulangi kesalahan yang sama pada masa akan datang.
</p>

<p>Sekian, terima kasih.</p>

<div class="signature">
<div>
_________________________<br>
(MUHAMMAD DZAMIRUL AZIM BIN MAZLAN)<br>
Ketua Warden Asrama<br>
SMK Nyalas
</div>

<div>
_________________________<br>
(ROSLAN BIN YAAKOB)<br>
Penolong Kanan Hal Ehwal Murid (GPK HEM)<br>
SMK Nyalas
</div>
</div>

</body>
</html>
"""

    return html

@app.route('/delete/<int:id>')
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM pelajar WHERE id=?", (id,))
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    with get_db() as conn:

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
            return redirect('/')

        p = conn.execute("SELECT * FROM pelajar WHERE id=?", (id,)).fetchone()

    return f"""
    <h2>Edit Pelajar</h2>
    <form method="post">
    Nama: <input name="nama" value="{p['nama']}" required><br>
    IC: <input name="ic" value="{p['ic']}" required><br>
    Kelas: <input name="kelas" value="{p['kelas']}" required><br>
    Asrama: <input name="asrama" value="{p['asrama']}" required><br><br>
    <button type="submit">Update</button>
    </form>
    """


if __name__ == '__main__':
    print("🚀 Sistem Disiplin SMK Nyalas BERJALAN")
    app.run(host="0.0.0.0", port=10000)
