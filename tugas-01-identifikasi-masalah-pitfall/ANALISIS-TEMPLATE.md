# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Giriputra Galang Samudra | 1030724001311 | network is reliable,single point of failure |
| Mohammad Faiz | 103072400108 | latency is zero |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

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
---

## Pitfall 3: single point of failure — ditulis oleh Giriputra Galang Samudra

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

**Kenapa ini keliru:** kerena tidak ada fault isolation. dalam satu proses monolitik, bug memory atau lonjakan thread pemrosesan pesanan akan langsung menyedot alokasi cpu, memori, dan I/O dari modul lain.
**Dampak ke FoodGo:** yaitu terjadi total service outage yaitu ketika server kewalahan dan proses mati atau crash

**Solusi desain awal:** Deploy minimal dua atau lebih instance server yang identik di belakang load balancer.
**Trade-off:** aplikasi harus diubah menjadi stateless (tidak boleh simpan state/session di memori lokal server)

---


## Kesimpulan Kelompok

dari setiap problem diatas solusi arsitektur yang bisa saya tawarkan adalah
1. Load Balancing & Stateless Web Tier (Penyelesaian Pitfall 3: SPOF)
2. Event-Driven & Asynchronous Decoupling (Penyelesaian Pitfall 2: Latency is Non-Zero)
3. Resilient HTTP Client & Idempotency Layer (Penyelesaian Pitfall 1: The Network is Reliable)
4. Webhooks & Polling untuk Feedback Status ke Pengguna
