# For DataFrame Purpose
import numpy as numpy
import pandas as pd

# For crawling purpose
import requests
from bs4 import BeautifulSoup

# For Graoh purpose
import networkx as nx
import matplotlib.pyplot as plt

def simplifiedURL(url):
    '''
    asumsi: alamat url tidak mengandung http(s) (misalnya "true-http-website.com"
            atau www (misalnya "true-www-website.com")
    '''
    # cek 1 : www
    if "www." in url:
        ind = url.index("www.")+4
        url = "http://"+url[ind:]
    # cek 3 : tanda / di akhir
    if url[-1] == "/":
        url = url[:-1]
    # Cek 4 : cuma domain utama
    parts = url.split("/")
    url = ''
    for i in range(3):
        url += parts[i] + "/"
    return url

def crawl(url, max_deep,  show=False, deep=0, done=[]):
    # returnnya ada di edgelist, 
    global edgelist

    # menambah counter kedalaman
    deep += 1
    
    # menyamakan format url, agar tidak ada url yg dobel
    url = simplifiedURL(url)
    #menampilkan proses

    if not url in done:
        # crawl semua link
        links = getAllLinks(url)
        done.append(url)
        if show:
            if deep == 1:
                print(url)
            else:
                print("|", end="")
                for i in range(deep-1): print("--", end="")
                print(url)
            
        for link in links:
            # Membentuk format jalan (edge => (dari, ke))
            link = simplifiedURL(link)
            edge = (url,link)
            # Mengecek jalan, apabila belum dicatat, maka dimasukkan ke list
            if not edge in edgelist:
                edgelist.append(edge)
            # Cek kedalaman, jika belum sampai terakhir, maka crawling.
            if (deep != max_deep):
                crawl(link, max_deep, show, deep, done)
			
def getAllLinks(src):
    # Pencegahan eror apabila link yang diambil mati
    try:
        # Get page html
        page = requests.get(src)

        # Mengubah html ke object beautiful soup
        soup = BeautifulSoup(page.content, 'html.parser')

        # GET all tag <a>
        tags = soup.findAll("a")

        links = []
        for tag in tags:
            # Pencegahan eror apabila link tidak memiliki href
            try:
                # Get all link
                link = tag['href']
                if not link in links and 'http' in link:
                    links.append(link)
            except KeyError:
                pass
        return links
    except:
        #print("Error 404 : Page "+src+" not found")
        return list()

# Inisialisasi variabel awal
#root = "https://www.trunojoyo.ac.id/"
root = "http://garuda.ristekdikti.go.id/"
nodelist = [root]
edgelist = []

#crawl
crawl(root, 3, show=True)
edgelistFrame = pd.DataFrame(edgelist, None, ("From", "To"))

#membuat Graph
g = nx.from_pandas_edgelist(edgelistFrame, "From", "To", None, nx.DiGraph())

# deklarasi pos (koordinat) (otomatis)
pos = nx.spring_layout(g)

# hitung pagerank
damping = 0.85
max_iterr = 100
error_toleransi = 0.0001
pr = nx.pagerank(g, alpha = damping, max_iter=max_iterr, tol=error_toleransi)

# Membuat Label && print pagerank
print("keterangan node:")
nodelist = g.nodes
label= {}
data = []
for i, key in enumerate(nodelist):
    data.append((pr[key], key))
    label[key]=i

data = pd.DataFrame(data, None, ("PageRank", "Node"))

# Draw Graph
#plt.figure(1)
#plt.title('circle_layout')
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label, font_color="b")

# show figure
plt.axis("off")
plt.show()

'''
Documentasi di github. Lanjutin yang kemaren
konfigurasi:
    - Home
    - Content mining
    - Structure Mining
Ini minggu depan

url tergantung analisis. jika ttg domain per domain, cukup sampe ".com/". kalo sampe direktori, ya gpp, tapi bedal lagi
Kalo LaTex ga nge load, tambahin mathjax di konfigurasi.

selebihnya bahas soal tugas akhir. ampas
    Pakai LaTeX untuk bikin rumus
    Bingung bikin rumus pake LateX? pake Mathpix aja. Jalankan, trus ctrl+alt+m
    ngetik di Tex Studio  ->> ini untuk bikin proposal juga. AMpas yg hqq

Selayang pandang soal Tugas akhir.
    Crawling->> plagiarism.
        bisa lewat text
            Kek yg kemaren
        bisa lewat graph
            dilihat struktur graphnya.
            misal ada 3 kalimat, dipecah per kalimat. Node = kata atau apalah, lupa. dilihat strukturnya sama apa ngga.
            anyway, di indo belum ada.
    Apa kabar hoax? wkwk
'''
