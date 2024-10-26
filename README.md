```markdown
# SubSentry

**SubSentry** adalah alat yang dirancang untuk otomatisasi pencarian dan pemantauan subdomain serta pengecekan kerentanannya. Alat ini mengintegrasikan beberapa tools populer untuk menemukan subdomain dan mengecek apakah subdomain tersebut rentan terhadap potensi eksploitasi.

## Fitur

- **Pencarian Subdomain**: Menggunakan `theHarvester`, `sublist3r`, dan `subfinder` untuk menemukan subdomain.
- **Pengecekan Kerentanan**: Menggunakan `subsnipe` untuk mengecek apakah subdomain memiliki kerentanan.
- **Penghapusan Duplikasi**: Menghapus subdomain duplikat untuk hasil yang bersih dan terorganisir.
- **Output Terstruktur**: Menghasilkan laporan dalam format yang jelas dengan bagian subdomain, email, dan kerentanan.
```
## Instalasi

1. **Clone Repository**

   ```bash
   git clone https://github.com/HeroX22/SubSentry.git
   cd SubSentry
   chmod +x install.sh
   ./install.sh
   ```

2. **Instalasi Dependencies**

   Pastikan Python 3 terinstal. Install dependencies Python dengan pip:

## Penggunaan

1. **Jalankan SubSentry**

   ```bash
   python3 sub_sentry.py --target=yourdomain.com
   ```

   Gantilah `yourdomain.com` dengan nama domain target yang ingin Anda analisis.

2. **Struktur Output**

   Laporan akhir akan disimpan dalam file `{target}_subdomain.txt` dengan struktur sebagai berikut:

   ```plaintext
   -=subdomain=-
   (berisi seluruh subdomain dari semua alat)

   -=IP-Addreas=-
   (berisi seluruh ip addreas)

   -=E-Mail=-
   (berisi seluruh email)

   -=Vuln=-
   (berisi hasil dari output.md)
   ```

## Contoh

```bash
python3 sub_sentry.py --target example.com
```
