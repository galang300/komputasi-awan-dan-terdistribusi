"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time
import os


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    rpc_server_url = os.getenv("RPC_SERVER_URL", "http://localhost:8000")
    proxy = xmlrpc.client.ServerProxy(rpc_server_url)  # ganti dengan xmlrpc.client.ServerProxy(...)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    start = time.time()
    saldo = proxy.cek_saldo("user1")
    print(f"Saldo user1: {saldo} (waktu tempuh: {time.time() - start:.2f} detik)")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    start = time.time()
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil: {hasil} (waktu tempuh: {time.time() - start:.2f} detik)")


if __name__ == "__main__":
    main()
