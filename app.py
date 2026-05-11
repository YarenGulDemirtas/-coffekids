from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "coffeekids_secret_key"


# =========================
# DATABASE OLUŞTUR
# =========================

def veritabani_olustur():

    baglanti = sqlite3.connect("coffeekids.db")

    cursor = baglanti.cursor()

    # ÜRÜNLER

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS urunler(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        urun_ad TEXT,
        fiyat TEXT,
        aciklama TEXT,
        kategori TEXT

    )

    """)

    # REZERVASYONLAR

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS rezervasyonlar(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ad_soyad TEXT,
        telefon TEXT,
        tarih TEXT,
        baslangic TEXT,
        bitis TEXT,
        yetiskin TEXT,
        cocuk TEXT

    )

    """)

    baglanti.commit()

    baglanti.close()


# =========================
# ANA SAYFA
# =========================

@app.route('/')
def index():

    return render_template('index.html')


# =========================
# MENÜ
# =========================

@app.route('/menu')
def menu():

    baglanti = sqlite3.connect("coffeekids.db")

    baglanti.row_factory = sqlite3.Row

    cursor = baglanti.cursor()

    cursor.execute("SELECT * FROM urunler ORDER BY id DESC")

    urunler = cursor.fetchall()

    baglanti.close()

    icecekler = []
    tatlilar = []
    ara_sicaklar = []

    for urun in urunler:

        kategori = urun["kategori"]

        if kategori == "İçecekler":

            icecekler.append(urun)

        elif kategori == "Tatlılar":

            tatlilar.append(urun)

        elif kategori == "Ara Sıcaklar":

            ara_sicaklar.append(urun)

    return render_template(
        'menu.html',
        icecekler=icecekler,
        tatlilar=tatlilar,
        ara_sicaklar=ara_sicaklar
    )


# =========================
# REZERVASYON
# =========================

@app.route('/rezervasyon', methods=['GET', 'POST'])
def rezervasyon():

    if request.method == 'POST':

        baglanti = sqlite3.connect("coffeekids.db")

        cursor = baglanti.cursor()

        cursor.execute("""

        INSERT INTO rezervasyonlar(

            ad_soyad,
            telefon,
            tarih,
            baslangic,
            bitis,
            yetiskin,
            cocuk

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            request.form.get('ad_soyad'),
            request.form.get('telefon'),
            request.form.get('tarih'),
            request.form.get('baslangic'),
            request.form.get('bitis'),
            request.form.get('yetiskin'),
            request.form.get('cocuk') or 0

        ))

        baglanti.commit()

        baglanti.close()

        print("\nYENİ REZERVASYON GELDİ\n")

        return redirect('/rezervasyon?basarili=1')

    return render_template('reservation.html')


# =========================
# GİRİŞ
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    hata = None

    if request.method == 'POST':

        email = request.form.get('username')

        sifre = request.form.get('password')

        if (
            email == "osmankaynar@gmail.com"
            and
            sifre == "osmankaynar58gamzekaynar"
        ):

            session['admin_giris'] = True

            return redirect('/admin')

        else:

            hata = "Hatalı kullanıcı adı veya şifre"

    return render_template(
        'login.html',
        hata=hata
    )


# =========================
# ADMİN PANELİ
# =========================

@app.route('/admin')
def admin():

    if not session.get('admin_giris'):

        return redirect('/login')

    baglanti = sqlite3.connect("coffeekids.db")

    baglanti.row_factory = sqlite3.Row

    cursor = baglanti.cursor()

    # ÜRÜNLER

    cursor.execute("""

    SELECT * FROM urunler
    ORDER BY id DESC

    """)

    urunler = cursor.fetchall()

    # REZERVASYONLAR

    cursor.execute("""

    SELECT * FROM rezervasyonlar
    ORDER BY id DESC

    """)

    rezervasyonlar = cursor.fetchall()

    baglanti.close()

    return render_template(
        'admin.html',
        urunler=urunler,
        rezervasyonlar=rezervasyonlar
    )


# =========================
# ÜRÜN EKLE
# =========================

@app.route('/urun_ekle', methods=['POST'])
def urun_ekle():

    if not session.get('admin_giris'):

        return redirect('/login')

    baglanti = sqlite3.connect("coffeekids.db")

    cursor = baglanti.cursor()

    cursor.execute("""

    INSERT INTO urunler(

        urun_ad,
        fiyat,
        aciklama,
        kategori

    )

    VALUES (?, ?, ?, ?)

    """, (

        request.form.get('urun_ad'),
        request.form.get('fiyat'),
        request.form.get('aciklama'),
        request.form.get('kategori')

    ))

    baglanti.commit()

    baglanti.close()

    print("\nYENİ ÜRÜN EKLENDİ\n")

    return redirect('/admin')


# =========================
# ÜRÜN SİL
# =========================

@app.route('/urun_sil/<int:id>', methods=['POST'])
def urun_sil(id):

    if not session.get('admin_giris'):

        return redirect('/login')

    baglanti = sqlite3.connect("coffeekids.db")

    cursor = baglanti.cursor()

    cursor.execute("""

    DELETE FROM urunler
    WHERE id = ?

    """, (id,))

    baglanti.commit()

    baglanti.close()

    print("\nÜRÜN SİLİNDİ\n")

    return redirect('/admin')


# =========================
# ÇIKIŞ
# =========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# =========================
# DATABASE BAŞLAT
# =========================

veritabani_olustur()


# =========================
# ÇALIŞTIR
# =========================

if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5050
    )