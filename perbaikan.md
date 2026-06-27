Saya sedang mengembangkan aplikasi web Tattoo Studio Management System menggunakan Flask dan Jinja2.

Tugas Anda adalah menjadi Senior Flask Engineer yang melakukan audit dan refactor seluruh project hingga dapat dijalankan tanpa error.

## Context

Project menggunakan:

- Python Flask
- Jinja2
- HTML
- CSS
- JavaScript
- Dummy Data (sementara)
- Nantinya akan menggunakan MongoDB

Saat ini project merupakan hasil generate AI sehingga masih banyak kode yang tidak kompatibel dengan Flask.

======================================================
TARGET
======================================================

Lakukan audit seluruh project dan perbaiki semua permasalahan tanpa mengubah desain UI.

Pastikan project dapat dijalankan menggunakan

python run.py

tanpa muncul exception.

======================================================
HAL YANG HARUS DIPERBAIKI
======================================================

1. Audit seluruh file HTML

Cari seluruh penggunaan seperti:

globals()
globals
window.globals

yang tidak valid pada Jinja2.

Ganti dengan implementasi Flask yang benar.

Contoh:

SALAH

{{ url_for('register') if 'register' in globals() else '/register' }}

BENAR

{{ url_for('register_post') }}

atau endpoint Flask yang sesuai.

======================================================

2. Audit seluruh url_for()

Pastikan semua endpoint benar-benar ada.

Misalnya

url_for("register")

harus diganti apabila endpoint Flask sebenarnya bernama

register_post

Lakukan pengecekan semua:

- login
- register
- logout
- dashboard
- admin
- payment
- booking
- artists
- gallery
- services

======================================================

3. Audit seluruh render_template()

Pastikan semua file template benar-benar ada.

Contoh:

render_template("payment/index.html")

harus sesuai dengan struktur folder.

======================================================

4. Audit Context Processor

Jangan gunakan globals().

Gunakan context_processor Flask dengan benar.

Misalnya:

@app.context_processor
def inject_globals():
    return {
        "session": session,
        "now": datetime.now()
    }

Lalu ubah template agar menggunakan

{{ session }}

{{ now }}

tanpa globals.

======================================================

5. Audit Struktur Folder

Pastikan Flask menggunakan struktur folder project yang benar.

Jika run.py berada di root sedangkan template berada di

app/templates

maka inisialisasi Flask harus menjadi

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

Pastikan seluruh static file dapat diakses.

======================================================

6. Audit Static

Periksa seluruh

url_for('static', filename=...)

Pastikan path benar.

======================================================

7. Audit JavaScript

Cari error JS seperti

showToast is not defined

Bootstrap Modal tidak ditemukan

document.querySelector menghasilkan null

dan perbaiki.

======================================================

8. Audit Form

Pastikan seluruh form

method

action

CSRF (jika ada)

redirect

flash message

berjalan dengan benar.

======================================================

9. Audit Template Inheritance

Pastikan

base.html

memiliki block

title

content

extra_css

extra_js

dan seluruh template child menggunakan block yang benar.

======================================================

10. Audit Routing

Pastikan seluruh route memiliki endpoint yang unik.

Contoh

@app.route("/register")
def register_page():

@app.route("/register", methods=["POST"])
def register_post():

dan seluruh template mengarah ke endpoint yang benar.

======================================================

11. Jangan Mengubah UI

Jangan mengubah layout.

Jangan mengubah styling.

Jangan mengubah warna.

Jangan mengubah tampilan.

Hanya memperbaiki kode.

======================================================

12. Output

Untuk setiap file yang diperbaiki:

- Jelaskan masalahnya
- Jelaskan penyebabnya
- Berikan kode lengkap yang sudah diperbaiki
- Jangan hanya memberikan potongan kode
- Jangan menghilangkan fitur yang sudah ada

======================================================

13. Validasi Akhir

Pastikan project dapat dijalankan tanpa error:

- Jinja2 UndefinedError
- BuildError
- TemplateNotFound
- KeyError
- AttributeError
- url_for BuildError
- globals is undefined
- Static file not found

======================================================

Lakukan audit secara menyeluruh seperti seorang Senior Flask Architect dan jangan berhenti setelah menemukan satu error. Lanjutkan hingga seluruh project konsisten dan siap digunakan sebagai dasar pengembangan berikutnya.