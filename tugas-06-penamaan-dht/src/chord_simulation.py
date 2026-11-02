"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def find_successor(self, key_hash: int) -> int | None:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor
        if not self.nodes:
            return None

        sorted_nodes = sorted(self.nodes.keys())
        
        # Cari node pertama yang nilainya >= key_hash
        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id
        
        # Jika tidak ada yang >= key_hash, wrap-around ke node terkecil
        return sorted_nodes[0]

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 2: cari successor LAMA sebelum node baru didaftarkan
        old_successor = self.find_successor(node_id)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes
        self.nodes[node_id] = node_ip
        print(f"Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 3: cek key di self.data yang berpindah tanggung jawab
        if old_successor is not None and old_successor != node_id:
            for key_hash, (kurir_id, _) in list(self.data.items()):
                # Key berpindah jika successor barunya sekarang adalah node baru
                if self.find_successor(key_hash) == node_id:
                    print(f"  -> Migrasi data: key '{kurir_id}' (hash={key_hash}) diambil alih dari node id={old_successor}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"Node '{node_name}' tidak ditemukan di ring.")
            return

        # Kumpulkan key yang saat ini berada di bawah tanggung jawab node ini
        keys_held = [
            (k, v[0]) for k, v in self.data.items() 
            if self.find_successor(k) == node_id
        ]

        # TODO 4: hapus node_id dari self.nodes
        del self.nodes[node_id]
        print(f"Node '{node_name}' (id={node_id}) keluar dari ring")

        # TODO 5: cari successor baru untuk setiap key yang terdampak
        if self.nodes:
            for key_hash, kurir_id in keys_held:
                new_succ = self.find_successor(key_hash)
                print(f"  -> Migrasi data: key '{kurir_id}' (hash={key_hash}) dipindahkan ke node id={new_succ}")
        else:
            print("  -> Ring sekarang kosong, tidak ada successor tersisa.")

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        # TODO 7: cari successor penanggung jawab, lalu simpan ke self.data
        key_hash = hash_id(kurir_id)
        responsible_node = self.find_successor(key_hash)
        
        if responsible_node is not None:
            self.data[key_hash] = (kurir_id, ip_kurir)
            print(f"Register '{kurir_id}' (hash={key_hash}) -> disimpan di node id={responsible_node} ({self.nodes[responsible_node]})")
        else:
            print(f"Gagal mendaftarkan '{kurir_id}': belum ada node di ring.")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        # TODO 8: cari successor penanggung jawab, lalu ambil ip_kurir dari self.data
        key_hash = hash_id(kurir_id)
        responsible_node = self.find_successor(key_hash)

        if responsible_node is not None and key_hash in self.data:
            _, ip_kurir = self.data[key_hash]
            return ip_kurir
        return None


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()