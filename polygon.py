import matplotlib.pyplot as plt
from matplotlib import collections as mc
import random

# 점의 좌표를 저장할 리스트
coord = []

# 점의 개수 n을 입력받고 -100 ~ 100범위에서 점위 좌표를 임의의로 지정
n = int(input('Numbers of points : '))
for i in range(n):
    coord.append([random.randrange(-100, 100), random.randrange(-100, 100)])

# 두 점 사이의 기울기를 리턴, coord의 인덱스를 parameter로 이용
def slope(i1, i2):
    global coord
    if coord[i1][0] == coord[i2][0]:
        if coord[i2][1] >= coord[i1][1]: return float('inf')
        else: return -float('inf')
    sl = (coord[i2][1] - coord[i1][1]) / (coord[i2][0] - coord[i1][0])
    return sl

# coord를 x좌표 기준으로 정렬
def quick_sort(arr):
    def sort(low, high):
        if high <= low:
            return

        mid = partition(low, high)
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high) // 2][0]
        while low <= high:
            while arr[low][0] < pivot:
                low += 1
            while arr[high][0] > pivot:
                high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low
    return sort(0, len(arr) - 1)
quick_sort(coord)

'''
    sl: 이전까지의 기울기를 저장하는 배열
    index: coord에서 볼록다각형이 지나갈 점의 인덱스를 저장한 배열
    temp_sl: 일시적으로 sl배열의 기울기와 비교할 기울기
'''
# 위쪽 컨벡스 연결
sl = []
index = [0, 1]
sl.append(slope(0, 1))
temp = 1
while temp < n - 1:
    temp_sl = slope(temp, temp + 1)
    while temp_sl > sl[-1]:
        sl.pop()
        index.pop()
        temp_sl = slope(index[-1], temp + 1)
        if not sl: break
    sl.append(temp_sl)
    index.append(temp + 1)
    temp += 1
outlines_upper = []
for i in range(len(index) - 1):
    outlines_upper.append([(coord[index[i]][0], coord[index[i]][1]), (coord[index[i + 1]][0], coord[index[i + 1]][1])])

# 아래쪽 컨벡스 연결
sl = []
index = [0, 1]
sl.append(slope(0, 1))
temp = 1
while temp < n - 1:
    temp_sl = slope(temp, temp + 1)
    while temp_sl < sl[-1]: # 부등호 방향 바뀜
        sl.pop()
        index.pop()
        temp_sl = slope(index[-1], temp + 1)
        if not sl: break
    sl.append(temp_sl)
    index.append(temp + 1)
    temp += 1
outlines_lower = []
for i in range(len(index) - 1):
    outlines_lower.append([(coord[index[i]][0], coord[index[i]][1]), (coord[index[i + 1]][0], coord[index[i + 1]][1])])

# 모든 점의 좌표를 저장
x = []
y = []
for i in range(len(coord)):
    x.append(coord[i][0])
    y.append(coord[i][1])

# 그래프화
top = mc.LineCollection(outlines_upper)
bottom = mc.LineCollection(outlines_lower)
fig, ax = plt.subplots()
ax.add_collection(top)
ax.add_collection(bottom)
ax.autoscale()
plt.scatter(x, y)
plt.show()