from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'kahve_keyfi_gizli_anahtar'

# -------------------------------
# GEÇİCİ VERİLER
# -------------------------------

urunler = [
    {
        "UrunID": 1,
        "UrunAd": "Latte",
        "Fiyat": 140,
        "Aciklama": "Yumuşak içimli özel latte",
        "KategoriAd": "İçecekler"
    },
    {
        "UrunID": 2,
        "UrunAd": "Mocha",
        "Fiyat": 160,
        "Aciklama": "Çikolatalı kahve keyfi",
        "KategoriAd": "İçecekler"
    },
    {
        "UrunID": 3,
        "UrunAd": "Cheesecake",
        "Fiyat": 180,
        "Aciklama": "Frambuaz soslu cheesecake",
        "KategoriAd": "Tatlılar"
    },
    {
        "UrunID": 4,
        "UrunAd": "Sufle",
        "Fiyat": 170,
        "Aciklama": "Sıcak çikolatalı sufle",
        "KategoriAd": "Tatlılar"
    },
    {
        "UrunID": 5,
        "UrunAd": "Patates Tabağı",
        "Fiyat": 130,
        "Aciklama": "Özel soslarla servis edilir",
        "KategoriAd": "Ara Sıcaklar"
    }
]

rezervasyonlar = []

# -------------------------------
# ANA SAYFA
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------
# MENÜ
# -------------------------------

@app.route('/menu')
def menu():

    icecekler = [u for u in urunler if u["KategoriAd"] == "İçecekler"]
    tatlilar = [u for u in urunler if u["KategoriAd"] == "Tatlılar"]
    ara_sicaklar = [u for u in urunler if u["KategoriAd"] == "Ara Sıcaklar"]

    return render_template(
        'menu.html',
        icecekler=icecekler,
        tatlilar=tatlilar,
        ara_sicaklar=ara_sicaklar
    )

# -------------------------------
# REZERVASYON
# -------------------------------

@app.route('/rezervasyon', methods=['GET', 'POST'])
def rezervasyon():

    if request.method == 'POST':

        yeni_rezervasyon = {
            "AdSoyad": request.form['ad_soyad'],
            "Telefon": request.form['telefon'],
            "Tarih": request.form['tarih'],
            "BaslangicSaati": request.form['baslangic'],
            "BitisSaati": request.form['bitis'],
            "YetiskinSayisi": request.form['yetiskin'],
            "CocukSayisi": request.form.get('cocuk') or 0
        }

        rezervasyonlar.append(yeni_rezervasyon)

        return redirect(url_for('index'))

    return render_template('reservation.html')

# -------------------------------
# LOGIN
# -------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    hata = None

    if request.method == 'POST':

        email = request.form['username']
        sifre = request.form['password']

        # Geçici admin bilgisi
        if email == "osmankaynar@gmail.com" and sifre == "osmankaynar58gamzekaynar":

            session['admin_giris'] = True
            return redirect(url_for('admin'))

        else:
            hata = "Hatalı kullanıcı adı veya şifre!"

    return render_template('login.html', hata=hata)

# -------------------------------
# ADMIN PANEL
# -------------------------------

@app.route('/admin')
def admin():

    if not session.get('admin_giris'):
        return redirect(url_for('login'))

    return render_template(
        'admin.html',
        urunler=urunler,
        rezervasyonlar=rezervasyonlar
    )

# -------------------------------
# ÜRÜN EKLE
# -------------------------------

@app.route('/urun_ekle', methods=['POST'])
def urun_ekle():

    if not session.get('admin_giris'):
        return redirect(url_for('login'))

    yeni_urun = {
        "UrunID": len(urunler) + 1,
        "UrunAd": request.form['urun_ad'],
        "Fiyat": request.form['fiyat'],
        "Aciklama": request.form['aciklama'],
        "KategoriAd": request.form['kategori']
    }

    urunler.append(yeni_urun)

    return redirect(url_for('admin'))

# -------------------------------
# ÜRÜN SİL
# -------------------------------

@app.route('/urun_sil/<int:id>', methods=['POST'])
def urun_sil(id):

    if not session.get('admin_giris'):
        return redirect(url_for('login'))

    global urunler

    urunler = [u for u in urunler if u["UrunID"] != id]

    return redirect(url_for('admin'))


# -------------------------------
# ÇIKIŞ
# -------------------------------

@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('index'))

# -------------------------------
# RUN
# -------------------------------

if __name__ == '__main__':
    app.run(debug=True)