# Simple-Structure-Mining
(example) Contoh Analisa Struktur Web menggunakan page rank. 

Masih dengan mata kuliah yang sama. lol.

# Notice
Agar program tidak menampilkan proses Crawling, ubah nilai variabel `tampilkan` pada baris 94 menjadi `False`

# Cara Kerja
`def crawl(url, max_deep, show=False, deep=0)` 

berfungsi untuk melakukan crawling semua link secara iteratif hingga kedalaman yang telah ditentukan. Parameter yang digunakan :

* url : alamat web awal yang digunakan untuk crawling

* max_deep : kedalaman maksimal

* show : menampilkan proses/tidak

* deep : untuk pengecekan kedalaman. **Jangan ubah parameter ini! Parameter ini digunakan untuk keperluan rekursif**

`simplifiedUrl(url)`

berfungsi untuk menyeragamkan format url, agar tidak ada url yang sama. Misal www.trunojoyo.ac.id akan dianggap berbeda denga trunojoyo.ac.id. Maka, perlu dilakukan format link.

`getAllLinks(src)`

berfungsi untuk mendapatkan semua link dalam html hasil crawl.

> Keterangan code lainnya terdapat pada komentar yang terdapat dalam file `Structure Mining v1.py`

# referensi:

* https://dzone.com/refcardz/data-mining-discovering-and?chapter=8

* https://www.geeksforgeeks.org/page-rank-algorithm-implementation/

* https://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm

* https://networkx.github.io/documentation/latest/_modules/networkx/drawing/layout.html
