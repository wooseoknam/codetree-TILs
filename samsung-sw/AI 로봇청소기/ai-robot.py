from collections import deque

INF = int(1e9)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(x, y):
    return (0 <= x < N) and (0 <= y < N)

def get_dist(sx, sy, blocked):
    dist = [[INF for _ in range(N)] for _ in range(N)]
    q = deque([(sx, sy)])
    dist[sx][sy] = 0
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]; ny = y + dy[i]
            if not in_range(nx, ny): continue
            if dist[nx][ny] < INF: continue
            if grid[nx][ny] == -1: continue          # 물건(벽)
            if (nx, ny) in blocked: continue           # 다른 청소기가 있는 칸
            q.append((nx, ny))
            dist[nx][ny] = dist[x][y] + 1
    return dist

def get_next_dust(dist):
    best = (INF, INF, INF)
    for x in range(N):
        for y in range(N):
            if grid[x][y] <= 0: continue
            if (dist[x][y], x, y) < best:
                best = (dist[x][y], x, y)
    return best

def get_tot_dust(x, y):
    rot = {1: [0, 1, 2], 2: [1, 2, 3], 3: [2, 3, 0], 4: [3, 0, 1]}
    ret = 0; max_d = None
    for d in range(1, 5):
        tot = min(grid[x][y], 20)
        for i in rot[d]:
            nx = x + dx[i]; ny = y + dy[i]
            if not in_range(nx, ny): continue
            if grid[nx][ny] == -1: continue
            tot += min(grid[nx][ny], 20)
        if tot > ret:
            ret = tot; max_d = d
    if max_d is not None:
        grid[x][y] -= min(grid[x][y], 20)
        for i in rot[max_d]:
            nx = x + dx[i]; ny = y + dy[i]
            if not in_range(nx, ny): continue
            if grid[nx][ny] == -1: continue
            grid[nx][ny] -= min(grid[nx][ny], 20)
    return ret

def move():
    for i in range(len(robots)):
        x, y = robots[i]
        # 나(i) 자신을 제외한, 현재(갱신된) 다른 로봇들의 위치를 장애물로 사용
        blocked = set(robots[j] for j in range(len(robots)) if j != i)

        dist = get_dist(x, y, blocked)
        nxt_dust = get_next_dust(dist)

        if nxt_dust[0] == INF:
            continue  # 갈 수 있는 오염 격자가 없음 -> 제자리 유지

        robots[i] = (nxt_dust[1], nxt_dust[2])

def plus_5():
    for x in range(N):
        for y in range(N):
            if grid[x][y] > 0: grid[x][y] += 5

def spread_dust():
    tmp_grid = [row[:] for row in grid]
    for x in range(N):
        for y in range(N):
            if grid[x][y] != 0: continue
            tot = 0
            for i in range(4):
                nx = x + dx[i]; ny = y + dy[i]
                if not in_range(nx, ny): continue
                if grid[nx][ny] == -1: continue
                tot += grid[nx][ny]
            tmp_grid[x][y] += int(tot / 10)
    return tmp_grid

if __name__ == "__main__":
    N, K, L = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    robots = []
    for _ in range(K):
        r, c = map(int, input().split())
        robots.append((r - 1, c - 1))

    for _ in range(L):
        move()

        for x, y in robots:
            get_tot_dust(x, y)

        plus_5()
        grid = spread_dust()

        ans = 0
        for x in range(N):
            for y in range(N):
                if grid[x][y] == -1: continue
                ans += grid[x][y]
        print(ans)