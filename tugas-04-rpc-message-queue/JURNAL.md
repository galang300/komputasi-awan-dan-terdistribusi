# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: ...

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12 Oktober 2026 | Gemini | "tolong bagaimana jika kode python ini di ubah untuk koneksi ke rabbit mq" | Menyediakan struktur dasar koneksi RabbitMQ via pika, pembuatan channel, deklarasi queue durable=True, dan blok penanganan error. | Menginisialisasi variabel connection dan channel pada file publisher.py dan consumer.py sesuai kebutuhan antrean pembayaran. |
| 12 Oktober 2026 | Gemini | "The token '&&' is not a valid statement separator in this version... PS C:\...>" | Menjelaskan sintaks && dan source tidak valid di PowerShell, serta memberikan alternatif perintah khusus PowerShell dan Git Bash. | Memperbaiki perintah aktivasi virtual environment sesuai shell Windows yang digunakan hingga muncul prompt (venv). |
| 12 Oktober 2026 | Gemini | "def main(): # TODO 3... # TODO 4: panggil channel.start_consuming()... bagaimana kelengkapaan kode" | Menyusun fungsi callback, registrasi basic_consume, konfigurasi basic_qos, serta penanganan graceful shutdown saat keyboard interrupt. | Melengkapi fungsi main() consumer.py dan menghubungkan basic_ack agar pesan antrean diproses tuntas tanpa traceback error. |