# For crawling purpose
import requests
from bs4 import BeautifulSoup

# For Graoh purpose
import networkx as nx
import matplotlib.pyplot as plt

def getAllLinks(src):
    try:
        ind = src.find(':')+3
        url = src[ind:]
        page = requests.get(src)

        # Mengubah html ke object beautiful soup
        soup = BeautifulSoup(page.content, 'html.parser')

        tags = soup.findAll("a")

        links = []
        for tag in tags:
            try:
                link = tag['href']
                if not link in links and 'http' in link:
                    links.append(link)
            except KeyError:
                pass
        return links
    except:
        print("Error 404 : Page "+src+" not found")
        return list()
    

def add_nodes_from_list(old_nodes, new_nodes):
    for node in new_nodes:
        if not node in old_nodes:
            old_nodes.append(node)
    return old_nodes

def add_edges_from_list(old_edges, from_, to_list):
    for to_ in to_list:
        edge = (from_, to)
        if not edge in old_edges:
            old_edges.append(edge)
    return old_edges

#root = "https://www.trunojoyo.ac.id/"
root = "http://garuda.ristekdikti.go.id/"
nodelist = [root]
done = [root]
edgelist = []

deep1 = getAllLinks(root)
#nodelist = add_nodes_from_list(nodelist, deep1)
print("banyak root : ", len(deep1))
c=1
for link in deep1:
    # add edge each time accessing new link
    edge = (root, link)
    if not edge in edgelist:
        edgelist.append(edge)
    
    if not link in done:
        nodelist.append(link)
        done.append(link)
        # deep 2
        deep2 = getAllLinks(link)
        #print(c, link, len(deep2)); c+=1
        
        for link2 in deep2:
            edge = (link, link2)
            if not edge in edgelist:
                edgelist.append(edge)
            if not link2 in done:
                nodelist.append(link2)
                done.append(link2)
            
                deep3 = getAllLinks(link2)

                for link3 in deep3:
                    edge = (link2, link3)
                    if not edge in edgelist:
                        edgelist.append(edge)
                    if not link3 in nodelist:
                        nodelist.append(link3)

pesan = """
            Pilih 1 untuk Graph berarah
            Pilih 2 untuk Graph tidak berarah
            Selain pilihan diatas, otomatis graph tidak berarah
        """        
tipe_grap = input(pesan)
g = nx.Graph()
if tipe_grap == "1":
    g = g.to_directed()

# Masukin ke Graph
g.add_edges_from(edgelist)

# deklarasi pos (koordinat) (otomatis)
pos = nx.circular_layout(g)
pos2 = nx.random_layout(g)
pos3 = nx.spring_layout(g)

# hitung pagerank
pr = nx.pagerank(g)

# Membuat Label
print("keterangan node:")
label= {}
for i in range(len(nodelist)):
    label[nodelist[i]]=i
    print(i, nodelist[i], pr[nodelist[i]])

# Draw Graph
plt.figure(1)
plt.title('circle_layout')
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label, font_size=8)

plt.figure(2)
plt.title('random_layout')
nx.draw(g, pos2)
nx.draw_networkx_labels(g, pos2, label, font_size=8)

plt.figure(3)
plt.title('spring_layout')
nx.draw(g, pos3)
nx.draw_networkx_labels(g, pos3, label, font_size=8)


# show figure
plt.axis("off")
plt.show()
