# Analisis Studi Kasus: Sistem Data Kependudukan

## Ringkasan Rekomendasi

| Aspek | Pilihan |
|---|---|
| **Deployment Model** | **Hybrid Cloud**, dengan inti **Private Cloud milik pemerintah** (yang dipakai bersama banyak instansi, jadi sifatnya *Government Community Cloud*). Segmen publik hanya menjalankan lapisan yang **tidak menyimpan data pribadi**. |
| **Service Model** | Campuran: IaaS untuk database inti dan biometrik, PaaS untuk API verifikasi, SaaS untuk aplikasi petugas dan portal publik |
| **Alternatif yang ditolak** | Public Cloud murni |

Prinsip utamanya: **data tetap di dalam infrastruktur negara, yang ikut membesar saat lonjakan hanya lalu lintasnya.**

---

## 1. Deployment Model: Hybrid Cloud dengan Inti Private

### Kenapa inti harus Private?

- **Regulasi.** Menurut PP 71/2019, PSE Lingkup Publik wajib mengelola, memproses, dan/atau menyimpan sistem dan data elektroniknya di wilayah Indonesia. PP ini juga membagi data menjadi tiga klasifikasi: data strategis, data berisiko tinggi, dan data berisiko rendah. Data kependudukan dan biometrik jelas masuk kategori strategis. Ditambah lagi UU PDP (UU 27/2022) yang memperlakukan data biometrik sebagai data pribadi spesifik.
- **Kendali penuh.** Studi kasus mensyaratkan data tidak boleh berada di infrastruktur yang tidak dikendalikan penuh oleh negara. Hanya private cloud yang dioperasikan negara yang memenuhinya. Di Indonesia wadahnya adalah Pusat Data Nasional (PDN). Per Januari 2026, PDN I di Cikarang sudah mulai beroperasi secara terbatas setelah menjalani uji keamanan oleh BSSN.

### Kenapa perlu sifat "Hybrid"?

Lonjakan saat pemilu atau PPDB umumnya membebani lapisan depan: portal cek status, halaman informasi, antrean permintaan, dan serangan DDoS. Lapisan ini bisa dilayani oleh segmen publik atau CDN **tanpa menyentuh data pribadi**. Database inti tetap di private.

### Pemetaan ke 5 Karakteristik NIST

| Karakteristik NIST | Kebutuhan sistem | Bagaimana Hybrid memenuhinya | Ketegangan kerahasiaan vs skalabilitas |
|---|---|---|---|
| **On-demand self-service** | Ribuan instansi perlu akses atau kuota API tanpa proses manual | Portal layanan mandiri di private cloud: instansi mengajukan akses API, lalu disetujui otomatis sesuai kebijakan | Self-service tetap **diberi batas** (persetujuan berbasis peran dan tujuan). Tidak boleh bebas seperti di public cloud. |
| **Broad network access** | Diakses dari seluruh daerah, kantor polisi, dan bank | Akses lewat jaringan intra pemerintah atau VPN untuk instansi, dan internet hanya untuk portal publik | Makin luas aksesnya, makin besar permukaan serangan. Karena itu dipakai mTLS, zero-trust, dan segmentasi jaringan. |
| **Resource pooling** | Efisiensi sumber daya untuk banyak instansi | Pooling terjadi **di antara instansi pemerintah saja** (model community), bukan dengan tenant komersial lain | Pooling di public cloud berarti berbagi perangkat keras dengan pihak asing atau komersial. Itu tidak dapat diterima untuk data biometrik. |
| **Rapid elasticity** | Lonjakan saat pemilu dan pendaftaran sekolah | Elastisitas internal (autoscaling dalam pool private) ditambah *cloud bursting* lapisan *stateless* ke segmen publik | Inilah titik lemah private murni. Hybrid menyelesaikannya dengan membesarkan **komputasi tanpa data**, bukan memindahkan data. |
| **Measured service** | Tagihan atau kuota per instansi, serta audit | Metering per instansi (jumlah panggilan verifikasi NIK/KYC) untuk kuota, PNBP dari bank, dan jejak audit | Metering juga berfungsi sebagai alat keamanan: lonjakan akses yang tidak wajar dari satu instansi bisa menandakan penyalahgunaan. |

---

## 2. Service Model per Komponen

| Komponen | Lokasi | Service Model | Alasan |
|---|---|---|---|
| **Database inti kependudukan** (NIK, KK, alamat) | Private (PDN) | **IaaS** | Instansi pemilik data (Dukcapil) perlu mengendalikan OS, enkripsi, kunci (HSM), patching, dan konfigurasi DB secara penuh. Kontrol maksimum, tidak ada abstraksi dari pihak lain. |
| **Data dan mesin pencocokan biometrik** (sidik jari, iris, wajah) | Private (PDN), zona paling terisolasi | **IaaS** (bisa bare-metal atau GPU) | Paling sensitif dan butuh komputasi berat. Isolasi fisik dan logis maksimal. |
| **API verifikasi** untuk polisi dan bank (KYC) | Private | **PaaS** (platform kontainer dan API gateway internal) | Butuh autoscaling, rate limiting, dan deployment cepat. Tim cukup fokus ke logika API. API hanya mengembalikan respons minimal (misalnya "cocok/tidak cocok"), tidak membuka seluruh data. |
| **Aplikasi petugas Dukcapil daerah** (input, perubahan data) | Private atau community | **SaaS** (aplikasi terpusat yang dipakai banyak daerah) | Ratusan kabupaten/kota tidak perlu membangun sistem sendiri. Satu aplikasi seragam lebih mudah diaudit. |
| **Portal publik cek status** (status KTP-el, pindah domisili) | Segmen publik (front-end), back-end tetap private | **SaaS/PaaS** di publik, *stateless* | Lapisan ini yang paling terkena lonjakan. Portal hanya meneruskan permintaan lewat gateway dan menerima status ringkas (tanpa data pribadi lengkap). CDN dan proteksi DDoS bisa memakai layanan publik. |
| **Backup dan DRC** | Private, lokasi kedua | **IaaS** | PP 71/2019 juga mewajibkan data center (DC) dan data recovery center (DRC) berada di Indonesia. Pemerintah merencanakan PDN tambahan di Batam dan IKN yang bisa berfungsi sebagai lokasi kedua. |

---

## 3. Risiko dan Mitigasi

| # | Risiko | Skenario | Mitigasi |
|---|---|---|---|
| **1** | **Kebocoran data lewat segmen publik atau saat sinkronisasi** | Developer meng-cache data pribadi di portal publik untuk mempercepat respons, atau log aplikasi mencatat NIK lengkap. Data pribadi akhirnya berada di infrastruktur publik. | Kebijakan tegas *no PII in public segment*. Tokenisasi atau masking NIK (misalnya hanya 4 digit terakhir). Aliran data satu arah, dari private ke publik hanya berupa status. Koneksi khusus terenkripsi (mTLS) dengan DLP di gateway. Audit konfigurasi rutin. |
| **2** | **Kapasitas private cloud tidak cukup saat lonjakan** | Saat pemilu, KPU dan ribuan TPS memverifikasi pemilih bersamaan dengan bank yang melakukan KYC. API verifikasi down karena bursting hanya bisa untuk lapisan stateless. | Perencanaan kapasitas berbasis kalender (pemilu dan PPDB sudah diketahui jadwalnya). Kuota dan prioritas per instansi (KPU diprioritaskan saat pemilu, bank dibatasi). Antrean asinkron untuk verifikasi massal (*batch*). Cache hasil verifikasi berumur pendek di sisi private. Cadangan kapasitas sekitar 30–50% di atas puncak historis. |
| **3** | **Sentralisasi menjadi target ransomware atau satu titik kegagalan** | Ini pernah terjadi: Pusat Data Nasional Sementara (PDNS) 2 Surabaya diserang ransomware pada 2024, dan layanan seperti KIP Kuliah ikut terdampak. | Backup *immutable* dan *offline* (aturan 3-2-1). DRC aktif di lokasi berbeda dengan uji pemulihan berkala. Segmentasi jaringan agar serangan tidak menyebar. Audit keamanan berkala bersama BSSN. Rencana respons insiden yang sudah dilatih. |
| **4** | **Penyalahgunaan akses oleh orang dalam** dari ribuan instansi | Oknum petugas di salah satu instansi menarik data massal lalu menjualnya. | Akses berbasis peran dan tujuan (ABAC). Respons API minimal. Batas query per pengguna. Log audit yang tidak bisa diubah. Deteksi anomali dari data metering (menyambung ke karakteristik *measured service*). |

> Tugas meminta minimal 2 risiko. Risiko 1 dan 2 paling relevan langsung dengan pilihan Hybrid. Risiko 3 menambah bobot karena ada contoh kasus nyata di Indonesia.

---

## 4. Alternatif yang Ditolak: Public Cloud Murni

| Kriteria | Public Cloud murni | Hybrid (pilihan kami) |
|---|---|---|
| Skalabilitas | ✅ Sangat baik, praktis tanpa batas | ✅ Baik untuk lapisan depan, terbatas tapi terencana untuk inti |
| Kendali negara atas infrastruktur | ❌ Dikendalikan penyedia, umumnya perusahaan asing | ✅ Inti dikendalikan penuh oleh negara |
| Yurisdiksi hukum | ❌ Penyedia asing bisa tunduk pada hukum negara asalnya (misalnya US CLOUD Act) | ✅ Sepenuhnya hukum Indonesia |
| Resource pooling | ❌ Berbagi perangkat keras dengan tenant lain | ✅ Hanya antarinstansi pemerintah |
| Kesesuaian dengan syarat kasus | ❌ Melanggar syarat "terkendali penuh oleh negara" | ✅ Memenuhi |

**Catatan penting:** penyedia public cloud dengan region di Jakarta bisa memenuhi syarat **lokasi** data di Indonesia. Tetapi lokasi tidak sama dengan **kendali**. Akses fisik, kunci enkripsi utama, staf operasional, dan keputusan teknis tetap ada di tangan penyedia. Untuk data biometrik yang tidak bisa diganti seperti kata sandi saat bocor, risiko itu tidak sebanding dengan keuntungan elastisitasnya.

**Sebagai pembanding, Private Cloud murni** memang paling aman. Kelemahannya, untuk menghadapi puncak beban sesekali (pemilu 5 tahunan, PPDB tahunan), negara harus membeli kapasitas berlebih yang menganggur hampir sepanjang tahun. Proteksi DDoS skala besar juga sulit dibangun sendiri. Hybrid mengambil keamanan private dan menambahkan elastisitas publik hanya di bagian yang tidak berisiko.

---

## Catatan untuk Diskusi

Inti private ini sebenarnya bisa disebut juga **Community Cloud**, karena dipakai bersama banyak instansi dengan kebutuhan keamanan yang sama. Kalau dosen menanyakannya, jawabannya: *inti = private/community pemerintah, ditambah segmen publik untuk lapisan stateless, sehingga secara keseluruhan disebut Hybrid*.

---

## Referensi

- [PP No. 71 Tahun 2019 tentang Penyelenggaraan Sistem dan Transaksi Elektronik](https://jdih.komdigi.go.id/produk_hukum/view/id/695/t/peraturan+pemerintah+nomor+71+tahun+2019)
- [Hukumonline: Mengenal Pokok-Pokok Aturan Baru PP PSTE](https://www.hukumonline.com/berita/a/mengenal-pokok-pokok-aturan-baru-pp-pste-lt5de653d86d627/?page=all)
- [Bisnis.com: Komdigi Ungkap PDN I Mulai Beroperasi Secara Terbatas (27 Jan 2026)](https://teknologi.bisnis.com/read/20260127/84/1947403/komdigi-ungkap-pdn-i-mulai-beroperasi-secara-terbatas)
- [Bisnis.com: PDN Cikarang Beroperasi 2026, Pemerintah Bakal Bangun 2 Lagi di Batam dan IKN](https://teknologi.bisnis.com/read/20240923/101/1801639/pdn-cikarang-beroperasi-2026-pemerintah-bakal-bangun-2-lagi-di-batam-dan-ikn)
- [Tirto: Pemerintah Bangun 3 Pusat Data Nasional (konteks serangan ransomware PDNS)](https://tirto.id/pemerintah-bangun-3-pusat-data-nasional-1-beroperasi-di-2026-g31K)
- NIST SP 800-145, *The NIST Definition of Cloud Computing*
- UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi
