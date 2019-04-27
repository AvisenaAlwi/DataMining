import csv
from pprint import pprint
import random
import matplotlib.pyplot as plt
import sys

# Definisikan fungsi yang dibutuhkan

def item(x):
    # Fungsi ini untuk memetakan data CSV ke bentuk yang dapat digunakan
    return {'Data No':int(x[0]), 'T':int(x[1]), 'K':int(x[2]), 'cluster':0}

def calculate_distance(item1, item2):
    # Fungsi Menghitung jarak antara datum
    return abs(item1['T']-item2['T'])+abs(item1['K']-item2['K'])

def find_distance_and_neighbors(index):
    distances = [calculate_distance(data[index], datum)for datum in data]
    neighbors = [(idx, dist) for idx, dist in enumerate(distances) if dist <= eps and idx != index]
    return distances, neighbors

input_eps = input("Eps : ")
input_min_pts = input("Min Pts : ")
eps = input_eps if input_eps else 15
min_pts = input_min_pts if input_min_pts else 3

print("Epsilon : {}".format(input_eps))
print("Min Pts : {}".format(input_min_pts))

# Membaca data dari file data.csv
f = open('data.csv', 'r')
data = list(csv.reader(f))
data = map(item, data)
data = list(data)
f.close()

# Menyimpan index data mana saja yang sudah dikunjungi
visited = set()

# Proses clustering
cluster = 1
while(len(visited)<len(data)):
    current_idx = -2
    while True:
        current_idx = random.randint(0, len(data)-1)
        if current_idx not in visited:
            break
    distance, neighbors = find_distance_and_neighbors(current_idx)
    if current_idx in visited:
        continue
    visited.add(current_idx)
    if len(neighbors) < min_pts:
        data[current_idx]['cluster'] = -1

    else:
        print("Core = Data {}".format(current_idx+1))
        data[current_idx]['cluster'] = cluster
        for neighbor in neighbors:
            neighbor_idx = neighbor[0]
            neighbor_distances, neighbor_neighbors = find_distance_and_neighbors(neighbor_idx)
            if len(neighbor_neighbors) < min_pts:
                data[neighbor_idx]['cluster'] = -1
            elif neighbor_idx not in visited :
                # Border
                if data[neighbor_idx]['cluster'] == 0:
                    data[neighbor_idx]['cluster'] = cluster
            visited.add(neighbor_idx)
        cluster += 1

# Prosess menghandle jika ada data noise
noises = [idx for idx, datum in enumerate(data) if datum['cluster'] == -1]
for index_datum_noise in noises:
    distances, neighbors = find_distance_and_neighbors(index_datum_noise)
    for i in range(len(distances)):
        if distances[i] == 0:
            distances[i] = sys.maxsize
    nearest_datum_index = distances.index(min(distances))
    data[index_datum_noise]['cluster'] = data[nearest_datum_index]['cluster']

pprint(data)


# REPRESENTASI DATA

idx = 1
all = []

while True:
    d = []
    for datum in data:
        if datum['cluster'] == idx:
            d.append((datum['T'], datum['K'], datum['Data No']))
    if len(d) == 0:
        break
    all.append(d)
    idx+=1
# for i in range(len(all)):
colors = ['red', 'blue', 'green', 'yellow']
groups = ('Cluster 1','Cluster 2', 'cluster 3', 'cluster 4')

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# ax.grid(True)

for al, color, group in zip(all, colors, groups):
    x = []
    y = []
    for a in al:
        x.append(a[0])
        y.append(a[1])
        ax.annotate("Data {}".format(a[2]), (a[0], a[1]))
    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)

plt.title('DBSCAN Clustering')
plt.legend(loc=2)
plt.show()