# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: ...
- Kesimpulan akhir & alasan: ...

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 17 November 2026 | Claude  | Memberikan kerangka kode Tugas 7 "Simulasi Replikasi Dua Server (Jakarta & Bandung)" berisi TODO 1–3, disertai permintaan "tolong lengkapi kode ini". | **TODO 1:** replikasi ke Bandung dibuat tertunda dengan `threading.Timer(REPLICATION_DELAY, self.bandung.write, args=(...))`, sehingga `top_up` tidak menunggu sinkronisasi. **TODO 2:** Read-Your-Writes dibuat dengan polling versi replika sampai `>= versi_minimal`; jika melewati `RYW_TIMEOUT` (5 detik), pembacaan dialihkan ke Jakarta (primary). **TODO 3:** pembacaan dilakukan 0,5 detik setelah top-up, dibandingkan dengan baca naif, dan dicek dengan `assert saldo == 70000`. **Tambahan:** `threading.Lock` pada `Replica`, method `version()`, dan penolakan replikasi dengan versi lebih lama. Hasil uji: baca naif = 0.0 (bug terlihat), baca Read-Your-Writes = 70000.0 (benar). | *(isi sendiri)* Contoh: menjalankan ulang kode dan mencocokkan output; mempelajari alur `threading.Timer` dan polling; mengganti `time.sleep(POLL_INTERVAL * 5)` menjadi `time.sleep(POLL_INTERVAL)`; menulis penjelasan konsep replication lag dan Read-Your-Writes dengan kata-kata sendiri di laporan. |
| 17 November 2026 | Claude | "Tolong lengkapi file .md berikut sesuai hasil prompt saya ini" (template tabel log penggunaan AI). | Mengisi tabel log dengan tanggal, tool, prompt, dan ringkasan saran AI dari sesi pengerjaan Tugas 7. | *(isi sendiri)* Contoh: memeriksa kesesuaian isi log dengan percakapan asli dan melengkapi kolom pengolahan sesuai yang benar-benar dilakukan. |
