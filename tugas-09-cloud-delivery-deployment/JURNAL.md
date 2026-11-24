# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan: Public Cloud murni, Private Cloud murni, Community Cloud (khusus instansi pemerintah/PDN), dan Hybrid Cloud (menggabungkan inti Private/Government Community Cloud dengan lapisan depan/publik yang stateless).
- **Alasan memilih Hybrid Cloud (inti Private/Community + segmen publik *stateless*):**
  - Data kependudukan dan biometrik termasuk data strategis dan data pribadi spesifik (UU No. 27 Tahun 2022 dan PP No. 71 Tahun 2019) sehingga wajib berada di bawah kendali penuh negara (wadahnya PDN) dan tidak boleh diserahkan ke infrastruktur publik komersial yang tidak dikendalikan negara penuh.
  - Sifat berbagi pakai (*resource pooling*) antar ribuan instansi (Dukcapil, kepolisian, bank, KPU) menjadikan inti sistem juga berkarakter *Government Community Cloud* dengan batasan akses/otorisasi (*on-demand self-service* terkendali) serta *measured service* untuk kuota, audit, dan PNBP.
  - Private Cloud murni cenderung boros jika harus menyediakan kapasitas puncak musiman (pemilu atau PPDB) yang menganggur di luar periode puncak, sedangkan Public Cloud murni berisiko pada kendali infrastruktur, kunci enkripsi, dan yurisdiksi hukum. Dengan Hybrid Cloud, data inti tetap di Private/PDN, sementara lonjakan trafik depan (*stateless*) dan proteksi DDoS/CDN dapat memanfaatkan segmen publik tanpa menyimpan PII.

## Diskusi service model per komponen
- **Database inti kependudukan & data/mesin biometrik (IaaS / bare-metal atau GPU di zona paling terisolasi PDN):** Membutuhkan kontrol penuh atas OS, enkripsi, manajemen kunci (HSM), *patching*, isolasi fisik/logis, serta komputasi berat pencocokan biometrik tanpa abstraksi pihak ketiga.
- **Backup dan Disaster Recovery Center / DRC (IaaS di lokasi terpisah di Indonesia):** Memenuhi kewajiban lokasi DC/DRC di dalam negeri sesuai PP No. 71 Tahun 2019 serta kesiapan pemulihan pasca-insiden/ransomware.
- **API verifikasi untuk instansi seperti kepolisian dan perbankan/KYC (PaaS di lingkungan private):** Memudahkan *autoscaling*, *rate limiting*, dan *deployment* layanan verifikasi dengan respons minimal (misalnya kecocokan status) tanpa mengekspos data mentah secara penuh.
- **Aplikasi petugas Dukcapil daerah (SaaS terpusat di jaringan private/community):** Menyeragamkan alur input dan pembaruan data lintas kabupaten/kota, mengurangi duplikasi pengembangan, serta memudahkan audit dan pemeliharaan terpusat.
- **Portal publik cek status (SaaS/PaaS *stateless* di segmen publik, terhubung ke *back-end* private):** Menangani lonjakan trafik publik dan DDoS/CDN dengan aman karena bersifat *stateless* dan tidak menyimpan data pribadi di sisi publik.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-20 | Gemini | Jelaskan gambaran umum 5 karakteristik esensial NIST SP 800-145 dan perbedaan antara Private, Community, serta Hybrid Cloud. | Menjelaskan definisi ringkas *on-demand self-service*, *broad network access*, *resource pooling*, *rapid elasticity*, dan *measured service*, serta konsep pemisahan komponen *stateless* dan data sensitif pada Hybrid Cloud. | Menggunakan penjelasan konsep dasar tersebut untuk memetakan kebutuhan akses ribuan instansi, lonjakan pemilu/PPDB, dan kerahasiaan data kependudukan ke dalam tabel karakteristik NIST di `README.md`. |
| 2026-11-22 | Gemini | Apa saja contoh pembagian service model (IaaS, PaaS, SaaS) pada sistem berskala nasional yang punya database sensitif dan portal publik? | Memberikan ide pembagian lapisan: IaaS untuk kontrol penuh infrastruktur/database inti, PaaS untuk lapisan API dan integrasi, serta SaaS untuk aplikasi pengguna akhir dan portal layanan. | Mengadaptasi ide pembagian lapisan tersebut secara spesifik ke komponen Dukcapil (DB inti & biometrik ke IaaS, API verifikasi KYC ke PaaS, aplikasi petugas daerah & portal cek status ke SaaS/PaaS *stateless*). |
| 2026-11-24 | Gemini | Berikan brainstorming poin-poin risiko arsitektur Hybrid Cloud dan ide skenario tandingan untuk diskusi sistem pemerintahan. | Menyarankan fokus pada risiko sinkronisasi data PII ke segmen publik, kapasitas *bursting* yang terbatas pada lapisan *stateless*, risiko serangan siber terpusat, serta skenario kesiapan infrastruktur daerah. | Mengembangkan poin-poin brainstorming tersebut dengan mengaitkannya pada regulasi PP No. 71 Tahun 2019, UU PDP No. 27 Tahun 2022, operasional PDN, serta merumuskan skenario tandingan dan mitigasinya dengan bahasa kelompok sendiri. |
