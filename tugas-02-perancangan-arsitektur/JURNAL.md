# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan: ...
- Kenapa akhirnya pilih [SOA/Pub-Sub]: ...
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26/09/2026 | Gemini | Saya membuat rancangan diagram untuk menggambarkan interaksi modul Pesanan, Pembayaran, Kurir/Notifikasi, Katalog Resto, dan Message Broker. Rancangan awal saya menggunakan Mermaid dan memiliki alur Pesanan → Pembayaran → Message Broker → Katalog Resto. Apakah rancangan tersebut sudah sesuai dengan instruksi soal: menggambarkan minimal 4 komponen, yaitu modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto, serta menjelaskan satu skenario penuh secara end-to-end dan jenis komunikasi yang digunakan (sinkron/asinkron, request-response/event)? | AI menyarankan bahwa rancangan awal sudah memiliki konsep dasar yang benar, tetapi masih perlu diperbaiki. Modul Kurir/Notifikasi seharusnya menjadi komponen tersendiri dan bukan nama topic pada message broker. Modul Katalog Resto dan Modul Kurir/Notifikasi perlu menerima event `payment-success`. Diagram juga perlu menunjukkan alur end-to-end dan membedakan komunikasi sinkron seperti HTTP dengan komunikasi asinkron melalui message broker. | Saya menggunakan saran tersebut sebagai bahan brainstorming. Saya kemudian memperbaiki rancangan dengan menambahkan Pelanggan/Mobile App, API Gateway, Modul Pesanan, Modul Pembayaran, Message Broker, Modul Katalog Resto, dan Modul Kurir/Notifikasi. Saya juga menambahkan topic `order-created` dan `payment-success` serta memberikan keterangan jenis komunikasi pada setiap interaksi. |r), menampilkan 4 modul wajib, serta memperjelas jenis komunikasinya (Sinkron/REST vs Asinkron/Event Pub-Sub). | ... |
