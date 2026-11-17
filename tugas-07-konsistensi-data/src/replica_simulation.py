"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server
POLL_INTERVAL = 0.1      # detik, jeda antar pengecekan versi replika
RYW_TIMEOUT = 5.0        # detik, batas menunggu sebelum redirect ke Jakarta


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}
        self.lock = threading.Lock()  # write terjadi dari thread Timer

    def write(self, user_id: str, saldo_baru: float, version: int):
        with self.lock:
            # Abaikan replikasi yang datang terlambat dengan versi lebih lama
            if version < self.last_write_version.get(user_id, 0):
                return
            self.saldo[user_id] = saldo_baru
            self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        with self.lock:
            return self.saldo.get(user_id, 0.0)

    def version(self, user_id: str) -> int:
        with self.lock:
            return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def _replica(self, server: str) -> Replica:
        return self.jakarta if server == "Jakarta" else self.bandung

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: replikasi asinkron ke Bandung yang tertunda
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version),
        )
        timer.daemon = True
        timer.start()
        print(f"[Replikasi] Ke Bandung dijadwalkan dalam {REPLICATION_DELAY} detik")

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        return self._replica(server).read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """TODO 2: Read-Your-Writes.
        Jika versi data di replika tujuan < versi_minimal, lakukan polling
        sampai replika menyusul. Jika melewati RYW_TIMEOUT, redirect ke
        Jakarta (primary) yang pasti sudah punya versi terbaru."""
        replica = self._replica(server)
        mulai = time.time()

        while replica.version(user_id) < versi_minimal:
            if time.time() - mulai > RYW_TIMEOUT:
                print(f"[RYW] {server} belum sinkron setelah {RYW_TIMEOUT} detik "
                      f"-> redirect ke Jakarta")
                return self.jakarta.read(user_id)
            print(f"[RYW] {server} masih versi {replica.version(user_id)}, "
                  f"butuh >= {versi_minimal}, menunggu...")
            time.sleep(POLL_INTERVAL * 5)

        durasi = time.time() - mulai
        print(f"[RYW] {server} sudah versi {replica.version(user_id)} "
              f"(menunggu {durasi:.2f} detik)")
        return replica.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter
    time.sleep(0.5)  # sama seperti skenario naif: baca < REPLICATION_DELAY detik kemudian

    # TODO 3: baca dengan Read-Your-Writes, hasilnya selalu benar
    print("Baca naif dari Bandung (pembanding):", system.baca_saldo_naif(user_id, "Bandung"))
    saldo = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print("Baca saldo dari Bandung (Read-Your-Writes):", saldo)
    assert saldo == 70000, f"Saldo salah: {saldo}"
    print("-> Benar 70000 (50000 + 20000), walau dibaca sebelum replikasi selesai")


if __name__ == "__main__":
    main()