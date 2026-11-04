# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Sistem gagal menemukan successor yang tepat ketika nilai hash lebih besar dari ID node terbesar di ring, karena pencarian linier atau iterasi standar tidak otomatis berputar kembali ke awal ring (contoh: pemetaan hash yang salah jika melewati node-jakarta-1 id=177).
- Cara memperbaikinya: Menambahkan logika wrap-around pada fungsi pencarian; jika nilai hash data lebih besar dari semua ID node yang ada (atau tidak ada node dengan ID > hash), maka successor yang dituju harus diatur secara paksa ke node pertama dengan ID terkecil di ring (misalnya node-bandung-1 dengan ID=40).

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Ring terdiri dari 4 node (node-bandung-1 id:40, node-jakarta-2 id:102, node-surabaya-1 id:136, dan node-jakarta-1 id:177). Registrasi key kurir-001 (hash=50) masuk ke node 102, kurir-002 (hash=28) masuk ke node 40, dan kurir-003 (hash=132) masuk ke node 136.
- Hasil sebelum & sesudah node keluar: Node baru node-medan-1 (id:123) bergabung dan menempati posisi antara node-jakarta-2 (id:102) dan node-surabaya-1 (id:136). Penambahan node ini tidak merusak pemetaan data yang sudah ada, dibuktikan dengan lookup kurir-001 yang tetap mengembalikan alamat 192.168.1.10 dengan benar.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2 Nov 2026 | Gemini | *"Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)... tolong lengkapi kode berikut"* (menyertakan seluruh kerangka kode awal Python dengan TODO 1 s.d. 8) | Menyediakan implementasi lengkap untuk semua `TODO` pada class `ChordRing`: algoritma `find_successor` berbasis `sorted()` dan *wrap-around*, alur migrasi penanggung jawab data pada `join()` dan `leave()`, serta mekanisme penyimpanan dan pembacaan pada `register_kurir()` dan `lookup()`. | • Mengkaji dan memverifikasi logika ring melingkar (*modulo/wrap-around*) pada `find_successor` agar sesuai konsep asli paper Chord.<br>• Menyusun ulang urutan eksekusi pada `join()` (mencari *successor* lama sebelum mendaftarkan ID baru ke kamus `nodes`).<br>• Menyesuaikan pesan log terminal migrasi data agar rapi dan mudah dievaluasi saat skenario `main()` dijalankan.<br>• Menambahkan penanganan kasus batas (*edge cases*), seperti kondisi ketika ring masih kosong. |
