"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) harus kalian lengkapi sendiri.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        self.got_ok = threading.Event()
        self.election_lock = threading.Lock()

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (LENGKAPI BAGIAN INI) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        # TODO 1: tangani tiga jenis pesan berikut:
        #   - "ELECTION": node lain memulai election. Jika node_id kita LEBIH BESAR
        #     dari sender_id, balas dengan mengirim "OK" ke sender, lalu mulai
        #     election kita sendiri (start_election()) karena kita berpotensi jadi leader.
        #   - "OK": tandai bahwa ada node lebih tinggi yang masih hidup, sehingga
        #     kita TIDAK boleh mendeklarasikan diri sebagai leader.
        #   - "COORDINATOR": simpan sender_id sebagai leader_id yang baru.
        if msg_type == "ELECTION":
            if self.node_id > sender_id:
                target_port = self.peers.get(sender_id)
                if target_port is not None:
                    self.send_message(target_port, "OK")
                threading.Thread(target=self.start_election, daemon=True).start()
        elif msg_type == "OK":
            self.got_ok.set()
        elif msg_type == "COORDINATOR":
            self.leader_id = sender_id
            self.got_ok.set()
        print(f"[Node {self.node_id}] Menerima pesan '{msg_type}' dari node {sender_id} (TODO: proses ini)")

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        # Cegah election ganda yang berjalan bersamaan di node yang sama
        if not self.election_lock.acquire(blocking=False):
            return
        try:
            while True:
                self.got_ok.clear()
                with self.lock:
                    self.leader_id = None

                higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
                print(f"[Node {self.node_id}] Memulai election ke peer lebih tinggi: {list(higher_peers)}")

                # Tidak ada node lebih tinggi -> langsung jadi leader
                if not higher_peers:
                    self.declare_leader()
                    return

                for port in higher_peers.values():
                    self.send_message(port, "ELECTION")

                # Tunggu "OK" (atau "COORDINATOR") selama ELECTION_TIMEOUT
                if not self.got_ok.wait(ELECTION_TIMEOUT):
                    # Tidak ada yang membalas -> kita leader
                    self.declare_leader()
                    return

                # Ada node lebih tinggi yang hidup. Tunggu pengumuman COORDINATOR-nya.
                deadline = time.time() + ELECTION_TIMEOUT * 2
                while time.time() < deadline:
                    with self.lock:
                        if self.leader_id is not None:
                            return  # leader baru sudah diumumkan
                    time.sleep(0.1)

                # Node lebih tinggi sempat membalas OK tapi tidak mengumumkan
                # (kemungkinan mati di tengah jalan) -> ulangi election
                print(f"[Node {self.node_id}] COORDINATOR tidak datang, mengulang election")
        finally:
            self.election_lock.release()

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] Saya menjadi LEADER, broadcast COORDINATOR")
        for port in self.peers.values():
            self.send_message(port, "COORDINATOR")  # node yang mati diabaikan (return False)

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            with self.lock:
                leader = self.leader_id
            # Belum ada leader (election sedang berjalan) atau kita sendiri leader
            if leader is None or leader == self.node_id:
                continue

            leader_port = self.peers.get(leader)
            if leader_port is None:
                continue

            if not self.send_message(leader_port, "PING"):
                print(f"[Node {self.node_id}] Leader {leader} tidak merespons, mulai election")
                self.start_election()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    # Asumsi konvensi port: id N selalu di port 5000+N (lihat contoh perintah di README).
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  # beri waktu semua node lain start dulu sebelum election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
