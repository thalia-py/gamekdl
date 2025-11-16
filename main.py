# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 14:41:36 2025

@author: Thalia
"""

# main.py - Knight & Goblins (kid-friendly roguelike)
import math, random
from pygame import Rect

WIDTH = 640; HEIGHT = 480; TILE_SIZE = 48
MAP_COLS = 10; MAP_ROWS = 8

STATE_MENU="menu"; STATE_PLAY="play"; STATE_GAMEOVER="gameover"
BACKGROUND_TILE="tile"; HERO_BASE="hero"; ENEMY_BASE="enemy"
MUSIC_FILE="music"; SOUND_HIT="hit"; SOUND_DEATH="death"; SOUND_CLICK="click"

class AnimatedSprite:
    def __init__(self, base, frames_idle=2, frames_walk=2, fps=6):
        from pgzero.actor import Actor
        self.base=base; self.frames_idle=frames_idle; self.frames_walk=frames_walk; self.fps=fps
        self.t=0.0; self.frame=0; self.walking=False
        self.actor=Actor(f"{self.base}_idle_0"); self.actor.anchor=("center","center")
    def set_pos(self,x,y): self.actor.pos=(x,y)
    def update(self,dt):
        period=1.0/self.fps; self.t+=dt
        if self.t>=period:
            self.t-=period
            if self.walking:
                self.frame=(self.frame+1)%self.frames_walk; self.actor.image=f"{self.base}_walk_{self.frame}"
            else:
                self.frame=(self.frame+1)%self.frames_idle; self.actor.image=f"{self.base}_idle_{self.frame}"
    def draw(self): self.actor.draw()

class Hero:
    def __init__(self,cx,cy):
        self.cell_x=cx; self.cell_y=cy; self.target_x=cx; self.target_y=cy
        self.speed=6.0; self.sprite=AnimatedSprite(HERO_BASE,frames_idle=2,frames_walk=2,fps=8)
        px,py=self.cell_to_pixel(cx,cy); self.sprite.set_pos(px,py)
        self.health=3; self.invulnerable=0.0
    def cell_to_pixel(self,cx,cy): return cx*TILE_SIZE+TILE_SIZE//2, cy*TILE_SIZE+TILE_SIZE//2
    def move_to(self,nx,ny):
        if 0<=nx<MAP_COLS and 0<=ny<MAP_ROWS and game_map[ny][nx]==0:
            self.target_x=nx; self.target_y=ny; self.sprite.walking=True
    def update(self,dt):
        if self.invulnerable>0: self.invulnerable=max(0.0,self.invulnerable-dt)
        curx,cury=self.sprite.actor.pos; tx,ty=self.cell_to_pixel(self.target_x,self.target_y)
        dx=tx-curx; dy=ty-cury; dist=math.hypot(dx,dy); speed_px=self.speed*TILE_SIZE
        if dist>1:
            move=min(speed_px*dt,dist); nx=curx+dx/dist*move; ny=cury+dy/dist*move; self.sprite.set_pos(nx,ny); self.sprite.walking=True
        else:
            self.cell_x=self.target_x; self.cell_y=self.target_y; self.sprite.set_pos(tx,ty); self.sprite.walking=False
        self.sprite.update(dt)

class Enemy:
    def __init__(self,cx,cy,territory):
        self.cell_x=cx; self.cell_y=cy; self.territory=territory[:]; self.target=(cx,cy)
        self.speed=random.uniform(2.0,4.0); self.sprite=AnimatedSprite(ENEMY_BASE,frames_idle=2,frames_walk=2,fps=6)
        px,py=self.cell_to_pixel(cx,cy); self.sprite.set_pos(px,py); self.choose_new_target()
    def cell_to_pixel(self,cx,cy): return cx*TILE_SIZE+TILE_SIZE//2, cy*TILE_SIZE+TILE_SIZE//2
    def choose_new_target(self): self.target=random.choice(self.territory)
    def update(self,dt):
        tx,ty=self.cell_to_pixel(*self.target); curx,cury=self.sprite.actor.pos
        dx=tx-curx; dy=ty-cury; dist=math.hypot(dx,dy); speed_px=self.speed*TILE_SIZE
        if dist>2:
            move=min(speed_px*dt,dist); nx=curx+dx/dist*move; ny=cury+dy/dist*move; self.sprite.set_pos(nx,ny); self.sprite.walking=True
        else:
            if random.random()<0.02: self.choose_new_target()
            self.sprite.walking=False
        self.sprite.update(dt); px,py=self.sprite.actor.pos; self.cell_x=int(px//TILE_SIZE); self.cell_y=int(py//TILE_SIZE)

def make_empty_map(c,r): return [[0 for _ in range(c)] for __ in range(r)]
game_map=make_empty_map(MAP_COLS,MAP_ROWS)
for x in range(2,5): game_map[3][x]=1
for y in range(1,3): game_map[y][6]=1

game_state=STATE_MENU; hero=None; enemies=[]; music_on=True; score=0

def start_new_game():
    global hero,enemies,score,game_state
    score=0; hero=Hero(1,1); enemies.clear()
    t1=[(2,2),(2,3),(3,2),(3,3)]; t2=[(6,1),(7,1),(7,2)]; t3=[(5,5),(6,5),(6,6),(5,6)]
    enemies.append(Enemy(3,2,t1)); enemies.append(Enemy(7,1,t2)); enemies.append(Enemy(5,5,t3))
    try:
        if music_on: music.play(MUSIC_FILE)
    except Exception: pass
    game_state=STATE_PLAY

def on_key_down(key):
    global game_state
    if game_state==STATE_PLAY and hero is not None:
        if key==keys.LEFT: hero.move_to(hero.cell_x-1,hero.cell_y)
        elif key==keys.RIGHT: hero.move_to(hero.cell_x+1,hero.cell_y)
        elif key==keys.UP: hero.move_to(hero.cell_x,hero.cell_y-1)
        elif key==keys.DOWN: hero.move_to(hero.cell_x,hero.cell_y+1)
    elif game_state==STATE_MENU:
        if key==keys.SPACE: start_new_game()
    elif game_state==STATE_GAMEOVER:
        if key==keys.SPACE: game_state=STATE_MENU

def on_mouse_down(pos,button):
    global music_on, game_state
    x,y=pos
    if game_state==STATE_MENU:
        if 180<=x<=460 and 170<=y<=230:
            try: sounds.click.play()
            except Exception: pass
            start_new_game()
        if 180<=x<=460 and 240<=y<=300:
            music_on= not music_on
            try: sounds.click.play()
            except Exception: pass
            if music_on:
                try: music.play(MUSIC_FILE)
                except Exception: pass
            else:
                try: music.stop()
                except Exception: pass
        if 180<=x<=460 and 310<=y<=370:
            try: sounds.click.play()
            except Exception: pass
            exit()

def update(dt):
    global game_state, score
    if game_state==STATE_PLAY and hero is not None:
        hero.update(dt)
        for e in enemies: e.update(dt)
        for e in enemies:
            if e.cell_x==hero.cell_x and e.cell_y==hero.cell_y:
                if hero.invulnerable<=0:
                    hero.health-=1; hero.invulnerable=1.0
                    try: sounds.hit.play()
                    except Exception: pass
                    if hero.health<=0:
                        try: sounds.death.play()
                        except Exception: pass
                        game_state=STATE_GAMEOVER
        score += dt * 1.0

def draw():
    screen.clear()
    if game_state==STATE_MENU: draw_menu()
    elif game_state==STATE_PLAY: draw_game()
    elif game_state==STATE_GAMEOVER:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=48)
        screen.draw.text("Press SPACE to return to menu", center=(WIDTH//2, HEIGHT//2+50), fontsize=24)

def draw_menu():
    screen.fill((255,200,190))
    screen.blit("menu_banner",(120,30))
    screen.draw.filled_rect(Rect((180,170),(280,60)), (255,180,60)); screen.draw.text("Start Game", center=(320,200), fontsize=34)
    screen.draw.filled_rect(Rect((180,240),(280,60)), (120,200,120)); screen.draw.text("Music: " + ("On" if music_on else "Off"), center=(320,270), fontsize=28)
    screen.draw.filled_rect(Rect((180,310),(280,60)), (240,120,140)); screen.draw.text("Exit", center=(320,340), fontsize=28)

def draw_game():
    try:
        for cx in range(MAP_COLS):
            for cy in range(MAP_ROWS):
                screen.blit(BACKGROUND_TILE, (cx * TILE_SIZE, cy * TILE_SIZE))
    except Exception: pass
    for cy in range(MAP_ROWS):
        for cx in range(MAP_COLS):
            if game_map[cy][cx]==1:
                screen.draw.rect(Rect((cx*TILE_SIZE, cy*TILE_SIZE),(TILE_SIZE,TILE_SIZE)), (100,100,100))
    for e in enemies: e.sprite.draw()
    if hero is not None: hero.sprite.draw()
    if hero is not None: screen.draw.text(f"HP: {hero.health}", (10,10))
    screen.draw.text(f"Score: {int(score)}", (10,30))
