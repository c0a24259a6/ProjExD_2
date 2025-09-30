import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
            pg.K_UP: (0, -5),
            pg.K_DOWN: (0, 5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT: (5, 0),
        }

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向, 縦方向）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    引数：screenのSurface
    戻り値：None
    こうかとんに爆弾が着弾した際に,画面をブラックアウトし,泣いているこうかとん画像と「Game Over」の文字列を5秒間表示させる関数
    """
    bo_img = pg.Surface((1100, 650))
    pg.draw.rect(bo_img, (0, 0, 0), pg.Rect(0, 0, 1100, 650))
    bo_img.set_alpha(230)
    gm_font = pg.font.Font(None, 80)
    gm_txt = gm_font.render("Game Over", True, (255, 255, 255))
    bo_img.blit(gm_txt, [410, 300])
    kc_img = pg.image.load("fig/8.png")
    bo_img.blit(kc_img, [340, 295])
    bo_img.blit(kc_img, [740, 295])
    screen.blit(bo_img, [0, 0])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数:なし
    戻り値：タプル（爆弾Surfaceのリスト,加速度のリスト）
    時間とともに爆弾が拡大，加速する関数
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：移動量タプルと対応する画像Surfaceの辞書
    飛ぶ方向に従ってこうかとん画像を切り替えるための関数
    """
    kk_img = pg.image.load("fig/3.png")
    KK_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1.0),
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 1.0),
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1.0),
        (0, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 1.0),
    }
    return KK_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒の透過
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()

    kk_imgs = get_kk_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突
            gameover(screen)  # ゲームオーバー
            return
        
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        key_lst = pg.key.get_pressed()

        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
