# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:
1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut *successor*).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

1. Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal.
2. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.
3. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.

## Analisis 
## 1. Perbandingan DHT/Chord, Flat Naming, dan DNS

- **Flat Naming:** Mengandalkan tabel pemetaan langsung antara ID dan alamat IP. Jika pengelolaan tabel ini hanya dipegang oleh satu server, maka akan muncul risiko *Single Point of Failure* (SPOF) ketika server mengalami gangguan.
- **DNS (Domain Name System):** Menggunakan pendekatan hierarkis untuk menerjemahkan nama menjadi alamat IP. DNS sudah memiliki sistem terdistribusi, tetapi mekanismenya berbeda dengan DHT yang secara khusus membagi tanggung jawab penyimpanan data ke berbagai node.
- **Chord:** Memanfaatkan *Distributed Hash Table* (DHT) untuk membagi tanggung jawab penyimpanan berdasarkan hasil fungsi *hashing* dari ID node dan ID kurir. Pendekatan ini membuat sistem pemetaan menjadi terdesentralisasi dan mengurangi ketergantungan pada satu server pusat.

## 2. Alasan Penggunaan Chord pada FoodGo

Penerapan Chord pada aplikasi FoodGo sesuai dengan kebutuhan sistem karena alamat IP kurir dapat berubah ketika berpindah lokasi atau jaringan, sementara ID kurir tetap digunakan sebagai identitas.

Melalui mekanisme *hashing* dan *lookup*, sistem dapat menemukan node yang bertanggung jawab atas pemetaan ID kurir ke alamat IP. Hal ini membuat proses pencarian lebih fleksibel serta mengurangi ketergantungan terhadap satu server pusat.

## 3. Analisis Perubahan Topologi Ring

Dalam simulasi awal yang terdiri dari empat node, terjadi penambahan `node-medan-1` (ID 123) dan keluarnya `node-jakarta-1` (ID 177) dari *ring*.

- Saat `node-medan-1` bergabung, tanggung jawab data dapat berpindah jika terdapat *hash* kurir yang masuk ke dalam rentang tanggung jawab node tersebut. Namun, dalam simulasi ini tidak ada data pemetaan kurir yang dialihkan ke node tersebut.
- Saat `node-jakarta-1` keluar, *successor* berikutnya adalah `node-bandung-1` (ID 40) melalui mekanisme *wrap-around*. Namun, tidak ada data pemetaan yang perlu dialihkan karena node tersebut tidak bertanggung jawab atas ketiga data kurir yang didaftarkan.

Hasil *lookup* setelah perubahan topologi tetap menunjukkan alamat IP yang sama seperti semula:

| **ID Kurir** | **Alamat IP** |
|---|---|
| `kurir-001` | `192.168.1.10` |
| `kurir-002` | `192.168.1.11` |
| `kurir-003` | `192.168.1.12` |

## 4. Contoh Proses Lookup

Berikut adalah simulasi alur pencarian data `kurir-001`:

1. Sistem menerima masukan berupa ID `kurir-001`.
2. Fungsi *hashing* dijalankan dan menghasilkan nilai `50`.
3. Sistem mencari node dengan ID terkecil yang nilainya lebih besar atau sama dengan `50`.
4. Ditemukan `node-jakarta-2` dengan ID `102` sebagai *successor*.
5. Sistem mengambil alamat IP kurir dari data pemetaan yang tersimpan pada `self.data`.
6. Proses *lookup* selesai dan mengembalikan alamat IP `192.168.1.10`.

## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi lookup/join/leave benar | 35% | Consistent hashing & successor lookup sesuai aturan Chord |
| Bukti perubahan topologi (join/leave) | 25% | Output menunjukkan mapping berpindah dengan benar |
| Analisis kenapa DHT vs flat naming/DNS | 25% | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
