from collections import deque

INF = int(1e9)

dx = [0, -1, 1, 0, 0]
dy = [0, 0, 0, -1, 1]

rot_ord = {
    1: [1, 3, 4, 2],
    2: [2, 4, 3, 1],
    3: [3, 2, 1, 4],
    4: [4, 1, 2, 3],
    5: [3, 2, 4, 1]
}

def in_range(x, y):
    return (0 <= x < N) and (0 <= y < N)

def is_ocean(x, y):
    return abs(1 - grid[x][y])

def move_adj(x, y, d):
    global have_to_go
    q = deque([(x, y)])
    if not visited[x][y]:
        print(x + 1, y + 1)
        visited[x][y] = True
        have_to_go -= 1

    while q:
        x, y = q.popleft()

        for i in rot_ord[d]:
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue
            if not is_ocean(nx, ny): continue
            if visited[nx][ny]: continue

            q.append((nx, ny))
            visited[nx][ny] = True
            print(nx + 1, ny + 1)
            have_to_go -= 1
            d = i

            break

    return x, y, d

def get_dist_all(x1, y1):
    dist = [[INF for _ in range(N)] for _ in range(N)]
    dirarr = [[-1 for _ in range(N)] for _ in range(N)]

    dist[x1][y1] = 0
    q = deque([(x1, y1)])
    while q:
        x, y = q.popleft()

        for i in rot_ord[5]:
            nx = x + dx[i]
            ny = y + dy[i]

            if not in_range(nx, ny): continue
            if not is_ocean(nx, ny): continue
            if dist[nx][ny] != INF: continue

            dist[nx][ny] = dist[x][y] + 1
            dirarr[nx][ny] = i
            q.append((nx, ny))

    return dist, dirarr

def move_nearest(x, y, d):
    dist, dirarr = get_dist_all(x, y)

    best = None  # (dist, i, j)
    for i in range(N):
        for j in range(N):
            if visited[i][j]: continue
            if dist[i][j] == INF: continue
            cand = (dist[i][j], i, j)
            if best is None or cand < best:
                best = cand

    _, b, c = best
    g = dirarr[b][c]

    return b, c, g

if __name__ == "__main__":
    N, x, y, d = map(int, input().split()); x -= 1; y -= 1
    grid = [list(map(int, input().split())) for _ in range(N)]
    visited = [[False for _ in range(N)] for _ in range(N)]
    have_to_go = 0
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0: have_to_go += 1

    while have_to_go > 0:
        x, y, d = move_adj(x, y, d)
        if have_to_go == 0: break
        x, y, d = move_nearest(x, y, d)
