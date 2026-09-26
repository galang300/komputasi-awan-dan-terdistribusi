# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan: ...
- Kenapa akhirnya pilih [SOA/Pub-Sub]: ...
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26/09/2026 | Gemini | graph LR
	subgraph Publisher
	   P1[Pesanan]
	   P2[Pembayaran]
	subgraph Message Broker [Message Broker - Kafka / RabbitMQ]
	   Kurir{kurir: 'pembayaran berhasil'}
	subgraph Subscribers
	   Q1[modul katalog resto]

P1[Pesanan] --> P2[Pembayaran] |Publish: "pemabayaran berhasil"| Kurir
Kurir --> |Deliver Event| Q1.
apakah kira kira rancangan saya ini sudah sesuai dengan instruksi soal ini
Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan jenis komunikasinya (sinkron/asinkron, request-response/event). | Rancangan Anda sudah memiliki ide dasar yang benar mengenai pemisahan peran, namun belum sepenuhnya tepat dan belum lengkap jika disesuaikan dengan instruksi soal.

Beberapa hal yang perlu diperbaiki dari kode Anda:

Kurir tertukar perannya: Di diagram Anda, Kurir dijadikan nama topik/broker (Kurir{kurir: 'pembayaran berhasil'}). Padahal pada soal, Kurir/Notifikasi adalah modul independen (Subscriber) yang menerima tugas untuk mencari driver atau mengirim peringatan, bukan nama broker/topik.

Katalog Resto sebagai satu-satunya subscriber: Saat pembayaran berhasil, modul yang paling membutuhkan event tersebut adalah Modul Katalog Resto (agar resto menyiapkan makanan) dan Modul Kurir/Notifikasi (mencarikan driver dan mengirim notifikasi ke user).

Sintaks Mermaid belum valid: Ada subgraph yang belum ditutup dengan end, serta baris P1 --> P2 |Publish...| menggabungkan dua relasi sekaligus secara keliru.

Instruksi belum terpenuhi seutuhnya: Soal meminta interaksi penuh end-to-end (mulai dari pemesanan hingga penugasan kurir), menampilkan 4 modul wajib, serta memperjelas jenis komunikasinya (Sinkron/REST vs Asinkron/Event Pub-Sub). | ... |
