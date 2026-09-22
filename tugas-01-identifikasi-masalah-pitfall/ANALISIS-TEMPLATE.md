# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 02

| Nama | NIM | Kontribusi |
|---|---|---|
| Giriputra Galang Samudra | 1030724001311 | network is reliable |
| Mohammad Faiz | 103072400108 | latency is zero |
| Rizky Yusuf Maulana | 103072400054 | Single point of failure |


## Pitfall 1: the network is reliable — ditulis oleh Giriputra Galang Samudra

**Bukti di skenario:** network is always reliable, no need for retry

**Kenapa ini keliru:**  karena tidak ada jaringan yang 100 persen aman, di dalam suatu jaringan pasti ada yang namanya celah atau kerusakan pada jaringan

**Dampak ke FoodGo:** sistem akan otomatis bisa mati, yang bisa menggagu jalannya suatu aplikasi, karena jaringan yang seharusnya menjadi tulang punggung aplikasi atau system akan rusak

**Solusi desain awal:** jangan pernah biarkan socket request menggantung, kita harus menentukan batas waktu nya agar tidak terjadi crash semisal connect timeout 500ms, rad timeout 2-3s.

**Trade-off:** request sebenarnya sedang diproses payment gateway. tetapi modul order menganggapnya gagal karena network log melebihi threshold

---

## Pitfall 2: Latency is Zero — Mohammad Faiz

**Bukti pada Skenario:**  
Tidak ditemukannya konfigurasi *timeout* pada komunikasi antarlayanan, di mana modul pesanan memanggil modul pembayaran secara *synchronous* dan tertahan (*blocked*) tanpa batas waktu.

**Akar Masalah:**  
Kekeliruan mendasar dalam mengasumsikan latensi jaringan bernilai nol (transfer data terjadi secara instan tanpa jeda).

**Dampak pada Sistem FoodGo:**  
Mengakibatkan *socket leak* dan *connection exhaustion* pada layer TCP menuju gateway pembayaran. Koneksi tertahan akibat respons yang lambat dan *pool* tidak melepaskan (*release*) *resource* kembali ke sistem.

**Solusi Desain:**  
Mengubah pola komunikasi *blocking synchronous* antarlayanan menjadi *asynchronous* untuk menghilangkan ketergantungan langsung saat pemrosesan.
**Trade-off:**  
Sifat transaksi berubah menjadi *non-linear*, sehingga sistem tidak lagi memberikan konfirmasi status sukses secara instan (*real-time*) kepada pengguna.
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

dari setiap problem diatas solusi arsitektur yang bisa saya tawarkan adalah
1. Load Balancing & Stateless Web Tier (Penyelesaian Pitfall 3: SPOF)
2. Event-Driven & Asynchronous Decoupling (Penyelesaian Pitfall 2: Latency is Non-Zero)
3. Resilient HTTP Client & Idempotency Layer (Penyelesaian Pitfall 1: The Network is Reliable)
4. Webhooks & Polling untuk Feedback Status ke Pengguna
