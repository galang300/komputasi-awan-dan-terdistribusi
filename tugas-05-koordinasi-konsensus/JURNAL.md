# Jurnal Proses — Tugas 5

## Implementasi Bully
- **Kendala saat mengisi TODO 1-4:** 
  Memahami alur asinkron dari algoritma Bully cukup menantang, terutama untuk memastikan tidak terjadi pemilihan (election) ganda ketika beberapa node mendeteksi kegagalan secara bersamaan. Kendala lainnya adalah memetakan `node_id` ke *port* yang tepat saat mengirim pesan balasan, karena metode pengiriman pesan membutuhkan port, bukan ID. Selain itu, sinkronisasi *thread* saat menunggu pesan `OK` (menggunakan flag atau event) sempat membuat bingung sebelum akhirnya menggunakan `threading.Event()` dan `lock` untuk menghindari kondisi *race* saat mengubah status `leader_id`.

## Skenario 1: Start normal
- **Leader yang terpilih:** Node 5
- **Log/observasi:** 
  Pada saat inisialisasi awal, node dengan ID yang lebih rendah mencoba melakukan inisiasi pemilihan dengan mengirim pesan ELECTION ke node yang lebih tinggi, seperti Node 1 yang memulai pemilihan ke peer [2, 3, 4, 5][cite: 5]. Namun, karena Node 5 memiliki ID tertinggi dan membalas pesan ELECTION, Node 5 pada akhirnya menjadi *coordinator*. Setelah status stabil, Node 5 secara konsisten menerima pesan 'PING' (heartbeat) dari node-node di bawahnya, yaitu node 1, 2, 3, dan 4[cite: 1].

## Skenario 2: Leader dimatikan
- **Leader baru yang terpilih:** Node 4[cite: 2]
- **Berapa lama waktu sampai leader baru terdeteksi:** (Sekitar 3-5 detik, bergantung pada konfigurasi timeout PING dan ELECTION_TIMEOUT di dalam kode). 
  **Observasi:** Ketika Node 5 dimatikan, node lain gagal mengirimkan PING. Node 4 mendeteksi ketiadaan respons ini lalu memulai *election* ke peer yang lebih tinggi, yaitu [5][cite: 2]. Karena Node 5 tidak membalas pesan `OK` dalam batas waktu, Node 4 mendeklarasikan dirinya sebagai LEADER dan langsung melakukan *broadcast* pesan COORDINATOR ke node lain di bawahnya[cite: 2]. Pesan COORDINATOR dari Node 4 ini berhasil diterima oleh node lain seperti Node 3[cite: 3] dan Node 2[cite: 4].

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

# Jurnal Penggunaan AI - Tugas 5 (Bully Algorithm)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Okt 2026 | Claude (Anthropic) | Mengirim kode `node.py` beserta draf `on_message`, lalu meminta AI fokus hanya pada `on_message`/algoritma Bully, sementara bagian kode lain dianggap sudah lengkap. | AI menemukan 3 bug: (1) `self.node_id = True` menimpa ID node sendiri, seharusnya memakai flag/`threading.Event`; (2) `send_message` menerima port, bukan ID, sehingga harus memakai `self.peers[sender_id]`; (3) tipe pesan lain seperti `PING` perlu diabaikan dengan aman. AI juga menyarankan menambah `self.got_ok = threading.Event()` di `__init__`. | Saya memahami bahwa `node_id` tidak boleh diubah dan bahwa `send_message` membutuhkan port. Saya menulis ulang `on_message` sendiri dengan `self.peers.get(sender_id)`, `self.got_ok.set()` untuk pesan `OK`, dan menjalankan `start_election` di thread terpisah. Saya juga menambahkan `self.got_ok` di `__init__`. |
| 18 Okt 2026 | Claude (Anthropic) | Mengirim versi `on_message` hasil revisi saya dan bertanya "apakah kode ini sudah ok". | AI menyatakan logikanya sudah sesuai TODO 1, dengan catatan: `got_ok` harus ada di `__init__`, teks "(TODO: proses ini)" pada `print` perlu dibersihkan, dan assignment `leader_id` sebaiknya memakai `self.lock` agar konsisten dengan `declare_leader()`. | Saya membersihkan `print` dari teks TODO, membungkus `leader_id = sender_id` dengan `with self.lock:`, dan memastikan `got_ok` sudah dideklarasikan di `__init__`. |
| 18 Okt 2026 | Claude (Anthropic) | Mengirim draf `start_election` yang belum selesai dan meminta AI melengkapi logika Bully (TODO 2-4), dengan batasan hanya boleh mengubah bagian algoritma Bully. | AI menunjukkan bahwa draf saya error: `while` tanpa isi menyebabkan `SyntaxError`, dan `send_message(self.port, ...)` mengirim ke port sendiri, bukan ke peer ber-ID lebih tinggi. AI menyarankan: `start_election` yang mengirim `ELECTION` hanya ke peer dengan ID lebih tinggi dan menunggu `OK` selama `ELECTION_TIMEOUT`; `declare_leader` yang mem-broadcast `COORDINATOR` ke semua peer; `monitor_leader` yang mem-`PING` leader tiap 3 detik; serta `election_lock` agar tidak ada election ganda. | Saya mempelajari alur Bully: kirim `ELECTION` ke ID lebih tinggi, tunggu `OK`, jika tidak ada maka jadi leader dan broadcast `COORDINATOR`. Kode saya masukkan ke `node.py`, saya tambahkan `self.election_lock` di `__init__`, lalu saya uji dengan 5 terminal: node 5 menjadi leader, node 5 dimatikan sehingga node 4 mengambil alih, lalu node 5 dijalankan lagi dan kembali menjadi leader. |

