# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 02

| Nama | NIM | Kontribusi |
|---|---|---|
| Giriputra Galang Samudra | 1030724001311 | network is reliable, latency is zero, single point of failure |
| Muhammad Faiz | [nim] | [pitfall/bagian yang dikerjakan] |
| Rizky Yusuf Maulana | 103072400054 | Single point of failure |

## Pitfall 1: the network is reliable — ditulis oleh Giriputra Galang Samudra

**Bukti di skenario:** network is always reliable, no need for retry

**Kenapa ini keliru:**  karena tidak ada jaringan yang 100 persen aman, di dalam suatu jaringan pasti ada yang namanya celah atau kerusakan pada jaringan

**Dampak ke FoodGo:** sistem akan otomatis bisa mati, yang bisa menggagu jalannya suatu aplikasi, karena jaringan yang seharusnya menjadi tulang punggung aplikasi atau system akan rusak

**Solusi desain awal:** jangan pernah biarkan socket request menggantung, kita harus menentukan batas waktu nya agar tidak terjadi crash semisal connect timeout 500ms, rad timeout 2-3s.

**Trade-off:** request sebenarnya sedang diproses payment gateway. tetapi modul order menganggapnya gagal karena network log melebihi threshold

---

## Pitfall 2: latency is zero — ditulis oleh Giriputra Galang Samudra

**Bukti di skenario:** tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** banyak orang mengira suatu jaringan latensi itu nol atau orang bisa mengirim data tanpa loading sama sekali

**Dampak ke FoodGo:** socket tcp ke sistem pembayaran habis dikarenakan koneksi yang lambat karean tidak pernah ditutup atau dilepas kembali ke pool

**Solusi desain awal:** yaitu dengan menghilangkan ketergantungan blocking synchronous antar-service

**Trade-off:** alur transaksi tidak lagi linier. pengguna tidak langsung mendapat konfirmasi sukses seketika.

---

## Pitfall 3: single point of failure — ditulis oleh Rizky Yusuf Maulana

**Bukti di skenario:** Skenario FoodGo menunjukkan kalau mereka menggunakan satu server untuk menangani semua modul dalam satu proses monolitik. Skenario FoodGo juga menunjukkan kalau server backend kadang crash total dan perlu di restart manual.

**Kenapa ini keliru:** Kondisi ini membuat banyaknya bagian sistem yang bergantung pada satu server. Jika server tersebut mengalami masalah, maka modul lain yang terdapat pada server tersebut ikut terganggu.

**Dampak ke FoodGo:** Saat traffic meningkat, satu server harus menangani banyak proses sehingga beban semakin besar. Jika server menjadi crash, proses modul menjadi ikut terganggu yang berakibat pengguna dapat mengalami gangguan seperti lemot, request timeout bahkan bisa gagal melakukan pemesanan.

**Solusi desain awal:** Memisahkan modul agar tidak bergantung pada satu server. Lalu dapat disediakan server cadangan sehingga jika salah satu server mengalami masalah, layanan dapat berjalan dari server cadangan.

**Trade-off:** Menambah server membutuhkan biaya dan resource yang besar. Kompleksitas sistem juga meningkat untuk dikelola karena tim harus mengelola beberapa service terpisah dan alur komunikasi antar sistemnya. 

---

## Kesimpulan Kelompok

Galang: dari setiap problem diatas solusi arsitektur yang bisa saya tawarkan adalah
1. Load Balancing & Stateless Web Tier (Penyelesaian Pitfall 3: SPOF)
2. Event-Driven & Asynchronous Decoupling (Penyelesaian Pitfall 2: Latency is Non-Zero)
3. Resilient HTTP Client & Idempotency Layer (Penyelesaian Pitfall 1: The Network is Reliable)
4. Webhooks & Polling untuk Feedback Status ke Pengguna
