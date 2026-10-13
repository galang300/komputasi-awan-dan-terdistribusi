# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- Keduanya, alasan: Kami ingin mengimplementasikan dua pola arsitektur secara bersamaan. RPC digunakan untuk fitur inti seperti pengecekan saldo dan proses pembayaran agar client mendapatkan respons hasil transaksi secara langsung. Sementara itu, pola Message Queue digunakan untuk menangani notifikasi atau event pasca pembayaran agar proses pengiriman event tidak memblokir alur utama transaksi.

## Kendala teknis
- Integrasi Pika ke RabbitMQ: Saat awal setup, server RabbitMQ sudah berhasil berjalan (dibuktikan dengan bisa diaksesnya halaman RabbitMQ Management UI pada port 15672). Namun, tantangannya adalah mengubah dummy print bertuliskan [TODO] pada file publisher.py dan consumer.py menjadi kode implementasi yang benar-benar melakukan koneksi ke RabbitMQ menggunakan library pika. Sebelum library diterapkan, dashboard RabbitMQ masih menunjukkan 0 connections dan 0 queues.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: Matikan script consumer.py (menggunakan Ctrl+C) → jalankan publisher.py untuk mengirim beberapa event → periksa dashboard RabbitMQ untuk memastikan pesan masuk dan tertahan di antrean → nyalakan kembali script consumer.py.
- Hasil yang diamati: Pesan terbukti tidak hilang. Ketika consumer dalam keadaan mati, RabbitMQ secara otomatis menyimpan event/pesan dari publisher di dalam queue. Begitu consumer.py kembali dijalankan, semua pesan yang tertunda di antrean langsung masuk, diterima, dan diproses satu per satu oleh consumer tanpa ada yang terlewat.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 13 Okt 2026 | Gemini | "Saya mengimplementasikan RPC untuk transaksi utama dan RabbitMQ untuk notifikasi asinkron. Mari brainstorming poin-poin yang tepat untuk menjelaskan skenario 'uji pesan tidak hilang' saat consumer dimatikan sementara publisher tetap jalan, serta cara merangkum kendala teknis saat setup library pika." | AI menyarankan alur narasi pengujian: mematikan consumer, memverifikasi penumpukan pesan di antrean RabbitMQ, lalu menghidupkan kembali consumer. AI juga menyarankan untuk memfokuskan kendala teknis pada proses transisi dari kode dummy ke koneksi real menggunakan pika. | Saya menggunakan poin-poin brainstorming dari AI sebagai kerangka dasar tulisan (outline). Setelah itu, saya merangkai dan menulis ulang penjelasannya menggunakan gaya bahasa saya sendiri, memastikan detailnya sesuai dengan log terminal dan kondisi dasbor RabbitMQ riil di perangkat saya. |
