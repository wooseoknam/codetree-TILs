dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

oppo = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
}


def dist(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def move_hider(hiders):
    global hider_d

    for idx, [hx, hy] in enumerate(hiders):
        if dist(sx, hx, sy, hy) > 3: continue

        nx = hx + dx[hider_d[idx]]
        ny = hy + dy[hider_d[idx]]

        if nx < 1 or nx > n or ny < 1 or ny > n:  # 범위 밖이면
            hider_d[idx] = oppo[hider_d[idx]]

            nx = hx + dx[hider_d[idx]]
            ny = hy + dy[hider_d[idx]]

        if [sx, sy] != [nx, ny]:
            hiders[idx] = [nx, ny]

    return hiders


def move_seeker_red(x, y):
    global sd
    global red

    nx = x + dx[sd]
    ny = y + dy[sd]

    if nx + 1 == ny and nx < center:  # to right
        sd = 1
    elif nx + ny == n + 1 and nx < center:  # to down
        sd = 2
    elif nx == ny and nx > center:  # to left
        sd = 3
    elif nx + ny == n + 1 and nx > center:  # to up
        sd = 0
    elif nx == 1 and ny == 1:
        sd = 2
        red = False
    # elif nx == center and ny == center:
    #     sd = 0

    return nx, ny


def move_seeker_blue(x, y):
    global sd
    global red

    nx = x + dx[sd]
    ny = y + dy[sd]

    if nx + 1 == ny and nx < center:  # to down
        sd = 2
    elif nx + ny == n + 1 and nx < center:  # to left
        sd = 3
    elif nx == ny and nx > center:  # to up
        sd = 0
    elif nx + ny == n + 1 and nx > center:  # to right
        sd = 1
    # elif nx == 1 and ny == 1:
    #     sd = 2
    elif nx == center and ny == center:
        sd = 0
        red = True

    return nx, ny



def catch(x, y, d):
    global hiders, hider_d

    cnt = 0

    for i in range(3):
        tx = x + (dx[d] * i)
        ty = y + (dy[d] * i)

        if tx < 1 or tx > n or ty < 1 or ty > n: break

        if [tx, ty] in trees: continue

        hiders_tmp = []
        hider_d_tmp = []
        for idx, [hx, hy] in enumerate(hiders):
            # print(hx, hy, tx, ty)
            if [hx, hy] == [tx, ty]:
                cnt += 1
                # ind = hiders.index([tx, ty])
                # hiders.pop(ind)
                # hider_d.pop(ind)
            else:
                hiders_tmp.append([hx, hy])
                hider_d_tmp.append(hider_d[idx])
        hiders = hiders_tmp
        hider_d = hider_d_tmp
    return cnt


if __name__ == "__main__":
    n, m, h, k = map(int, input().split())  # m: 도망자, h: 나무, k: 반복

    sx, sy = n // 2 + 1, n // 2 + 1
    center = n // 2 + 1
    sd = 0

    hiders = []
    D = []  # [1, 2, 1]
    hider_d = []  # [1, 2, 1]    # [0, 1, 2, 3] -> [상, 우, 하, 좌]
    for _ in range(m):
        x, y, d = map(int, input().split())  # d -> 1: 좌우, 2: 상하
        hiders.append([x, y])
        D.append(d)
        hider_d.append(d)

    trees = []
    for _ in range(h):
        x, y = map(int, input().split())
        trees.append([x, y])

    ans = 0
    red = True
    for t in range(1, k + 1):
        # print(t, '@@@@@@@@@@@@')
        hiders = move_hider(hiders)

        if red:
            sx, sy = move_seeker_red(sx, sy)
        else:
            sx, sy = move_seeker_blue(sx, sy)

        # print('hiders', hiders)
        # print('hider_d', hider_d)
        # print('sx, sy, sd', sx, sy, sd)
        cnt = catch(sx, sy, sd)
        ans += t * cnt

    print(ans)