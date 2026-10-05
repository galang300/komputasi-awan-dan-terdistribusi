# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 38
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): ...

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: kendala dalam pengerjaan proyek kami adalah, kami sempat mengalami "failed to build: failed to solve: python:__ISI_VERSI__-slim: failed to resolve source metadata for docker.io/library/python:__ISI_VERSI__-slim: docker.io/library/python:__ISI_VERSI__-slim: not found", dan solusi nya adalah dengan menambahkan kode versi python komputer lokal yaitu 3.10-slim

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 05/10/26 | Gemini | Berikan struktur logika atau kode pembagian tugas multithreading, dengan pembagian 100 pesanan dengan 10 item | Menyarankan konsep pembagian batch (*chunking*) berbasis *step size* menggunakan `range(0, NUM_ORDERS, chunk_size)` untuk mengiris list ID pesanan ke tiap thread. | Mengubah pendekatan *step size* menjadi iterasi berbasis indeks worker `range(NUM_WORKERS)` dengan formula eksplisit `start` dan `end` (`start = i * NUM_ORDERS // NUM_WORKERS`, `end = (i + 1) * ...`) agar pembagian list terikat langsung pada ID tiap worker. |
