# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [18 - 9 - 2026]
- Peserta: galang, faiz, rizky
- Poin diskusi: membahas tentang pembagian pitfall

## [19 - 9 - 2026]
- Peserta: galang, faiz, rizky
- Poin diskusi: membahas tentang pitfall pertama, yaitu network is always reliable

## [22 - 9 - 2026]
- Peserta: galang, faiz, rizky
- Poin diskusi: membahas tentang pitfall kedua dan ketiga, yaitu latency is zero dan single point of failure. dan membahas tentang rangkuman untuk ketiga pitfall

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19/09/2026 | Gemini | **Peran:** Berperanlah seperti seorang software engineer yang sudah memiliki pengalaman 10 tahun. <br><br> **Objektif:** Sebuah sistem bernama FoodGo terdampak masalah kegagalan sistem saat terjadi lonjakan beban. Salah satu tim menemukan bahwa kode mereka menulis `# network is always reliable, no need for retry` dan tidak memiliki timeout pada pemanggilan antar-service. Modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu. Apa solusi dan trade-off dari kejadian ini? <br><br> **Konteks:** Terdapat kesalahan asumsi yang merujuk pada literatur *Fallacies of Distributed Computing* (pitfall klasik), yaitu **"the network is reliable"**. <br><br> **Batasan:** Pembahasan hanya berfokus pada *Fallacies of Distributed Computing* (pitfall klasik). | AI menyarankan beberapa ide atau perspektif mengenai solusi dan trade-off berdasarkan perspektif *Fallacies of Distributed Computing*. | Ide AI digunakan sebagai bahan brainstorming, kemudian dipilih dan dikembangkan kembali menggunakan pemahaman sendiri. |
| 22/09/2026 | Gemini | Bertindaklah sebagai Senior Software Engineer berpengalaman 10 tahun yang ahli di bidang arsitektur sistem terdistribusi. Analisis kegagalan sistem pada aplikasi FoodGo saat peak traffic, yang disebabkan oleh asumsi keliru 'Latency is Zero' (salah satu Fallacies of Distributed Computing). Fokus utama masalah terletak pada pemanggilan antar-service yang tidak menggunakan batas waktu (no timeout), di mana modul pesanan menunggu modul pembayaran secara tak terbatas. Berdasarkan skenario tersebut, uraikan mekanisme dampak teknisnya terhadap aplikasi, usulkan solusi arsitektur yang tepat, serta bedah trade-off dari solusi tersebut. Pembahasan wajib dibatasi hanya pada koridor Fallacies of Distributed Computing. | AI memaparkan dampak teknis (thread/connection pool exhaustion, cascading failure), opsi solusi seperti asynchronous/event-driven, SLA timeout, serta trade-off terkait konsistensi data. | Mengidentifikasi dampak penumpukan socket TCP dan blocking synchronous, lalu menyusun analisis arsitektur berbasis asynchronous/eventual consistency dengan kata-kata sendiri. |
| 22/09/2026 | Gemini | **Peran:** Berperanlah seperti Anda adalah software engineer yang sudah memiliki pengalaman 10 tahun. <br><br> **Objektif:** Sebuah sistem bernama FoodGo terdampak masalah kegagalan sistem saat melonjak. Salah satu tim menemukan saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama. Apa solusi, trade-off, dampaknya pada aplikasi, dan kenapa asumsi ini keliru? <br><br> **Konteks:** Terdapat kesalahan asumsi yang merujuk pada konsep **"single point of failure"**. <br><br> **Batasan:** Pembahasan hanya berfokus pada *Single Point of Failure* (SPOF). | Single Point of Failure (SPOF) adalah kondisi ketika satu komponen menjadi titik yang sangat bergantung bagi beberapa bagian sistem, sehingga jika komponen tersebut gagal, bagian lain juga dapat ikut terganggu.Pada kasus FoodGo, satu server menangani semua modul seperti orders, payments, dan courier notifications dalam satu proses monolitik. Ketika traffic tinggi, server tersebut dapat kewalahan atau mengalami crash. Karena semua modul bergantung pada server yang sama, gangguan pada server dapat menyebabkan beberapa layanan FoodGo ikut terganggu. Salah satu solusi awal adalah memisahkan layanan ke beberapa service/server dan menyediakan cadangan agar tidak semua layanan bergantung pada satu titik. Trade-off-nya, sistem menjadi lebih kompleks dan membutuhkan resource serta biaya tambahan. | Saat traffic meningkat, satu server harus menangani banyak proses sehingga beban semakin besar. Jika server menjadi crash, proses modul menjadi ikut terganggu yang berakibat pengguna dapat mengalami gangguan seperti lemot, request timeout bahkan bisa gagal melakukan pemesanan. |
| 22/09/2026 | Gemini | Merangkum 3 temuan pitfall pada sistem FoodGo (*The network is reliable*, *Latency is zero*, dan *Single point of failure*) beserta analisis dampak, solusi awal, dan trade-off-nya, kemudian menanyakan rekomendasi perancangan arsitektur sistem yang komprehensif untuk FoodGo. | AI menyarankan rancangan arsitektur target berupa Stateless Multi-Instance Modular Architecture dengan Event-Driven Communication, mencakup Load Balancer, pemisahan worker/broker, resilient HTTP client, serta mekanisme webhook/polling status. | Menyimpulkan dan merumuskan 4 pilar solusi arsitektur utama: <br> 1. Load Balancing & Stateless Web Tier (SPOF) <br> 2. Event-Driven & Asynchronous Decoupling (Latency non-zero) <br> 3. Resilient HTTP Client & Idempotency Layer (Network reliability) <br> 4. Webhook/Polling untuk update status pengguna. |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
