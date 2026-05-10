-- 1. TERTEMİZ YENİ VERİTABANI
CREATE DATABASE KafeWebDB;
GO
USE KafeWebDB;
GO

-- 2. TABLOLARI OLUŞTURMA
CREATE TABLE Kategoriler (
    KategoriID INT PRIMARY KEY IDENTITY(1,1),
    KategoriAd NVARCHAR(50) NOT NULL
);

CREATE TABLE Urunler (
    UrunID INT PRIMARY KEY IDENTITY(1,1),
    KategoriID INT FOREIGN KEY REFERENCES Kategoriler(KategoriID),
    UrunAd NVARCHAR(100) NOT NULL,
    Fiyat DECIMAL(18,2) NOT NULL,
    StokDurumu BIT DEFAULT 1, 
    Aciklama NVARCHAR(500)
);

CREATE TABLE Kullanicilar (
    KullaniciID INT PRIMARY KEY IDENTITY(1,1),
    AdSoyad NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    SifreHash NVARCHAR(MAX) NOT NULL,
    Rol NVARCHAR(20) DEFAULT 'Admin'
);

CREATE TABLE Rezervasyonlar (
    RezervasyonID INT PRIMARY KEY IDENTITY(1,1),
    AdSoyad NVARCHAR(100) NOT NULL, 
    Telefon NVARCHAR(20) NOT NULL, 
    Email NVARCHAR(100) NULL, 
    Tarih DATE NOT NULL,           
    BaslangicSaati TIME NOT NULL,  
    BitisSaati TIME NOT NULL,      
    YetiskinSayisi INT NOT NULL, 
    CocukSayisi INT NOT NULL DEFAULT 0, 
    Durum NVARCHAR(20) DEFAULT 'Beklemede'
);
GO

-- 3. BAŞLANGIÇ VERİLERİNİ EKLEME
INSERT INTO Kategoriler (KategoriAd) VALUES ('İçecekler'), ('Tatlılar'), ('Ara Sıcaklar');

INSERT INTO Urunler (KategoriID, UrunAd, Fiyat, Aciklama) VALUES 
(1, 'Türk Kahvesi', 45.00, 'Geleneksel Türk kahvesi, lokum ile'),
(1, 'Iced Latte', 75.00, 'Buzlu süt ve espresso'),
(2, 'San Sebastian Cheesecake', 110.00, 'Akışkan Belçika çikolatası sosu ile'),
(3, 'Patates Tabağı', 70.00, 'Baharatlı anne patatesi');

INSERT INTO Kullanicilar (AdSoyad, Email, SifreHash, Rol) 
VALUES ('admin', 'admin@cafe.com', '1234', 'Admin');
GO