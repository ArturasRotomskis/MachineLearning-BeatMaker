import pygame
from pygame import mixer
import sqlite3


pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (45, 45, 45)
teal = (0, 128, 128)
gray = (55, 55, 55)
red = (178, 34, 34)
yellow = (204, 204, 102)
orange = (255, 140, 0)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Machine Learning - Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 14)

# ################## exchangeable variables
fps = 60
bpm = 240
beats = 6
instruments = 6

boxes = []
beats_data = beats
timer = pygame.time.Clock()
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
playing = True
active_length = 0
active_beat = 1
beat_changed = True
db_data = "DataAnalytics_BeatMaker.db"
db_machine = "MachineLearning_BeatMaker.db"

# ################## loading sounds
hi_hat = mixer.Sound('sounds\hi hat.wav')
snare = mixer.Sound('sounds\snare.wav')
kick = mixer.Sound('sounds\kick.wav')
crash = mixer.Sound('sounds\crash.wav')
clap = mixer.Sound('sounds\clap.wav')
tom = mixer.Sound('sounds\\tom.wav')


# ################## playing sounds
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


# ############################################## to the database
def crt_db():
    conn = sqlite3.connect(db_data)
    cursor = conn.cursor()
    with conn:
        cursor.execute("""CREATE TABLE IF NOT EXISTS BeatMaker 
        (time numeric, fps integer, 
        hi_hat integer, snare integer, kick integer, crash integer, clap integer, tom integer, 
        beats integer)""")
    for i in range(beats):
        with conn:
            cursor.execute(f"INSERT INTO BeatMaker VALUES (datetime('now'),{fps}, "
                           f"{clicked[0][i]}, {clicked[1][i]}, {clicked[2][i]}, {clicked[3][i]}, "
                           f"{clicked[4][i]}, {clicked[5][i]}, {beats_data})")


# ############################################## layout
def draw_grid(clicks, beat):
    boxes = []
    hi_hat_text = label_font.render('Hit hat (lėkštės su pedalu)', True, teal)
    screen.blit(hi_hat_text, (15, 42))
    snare_text = label_font.render('Snare (solinis būgnas)', True, teal)
    screen.blit(snare_text, (15, 142))
    kick_text = label_font.render('Kick (bosinis būgnas)', True, teal)
    screen.blit(kick_text, (15, 242))
    crash_text = label_font.render('Crash (crash būgnas)', True, teal)
    screen.blit(crash_text, (15, 342))
    clap_text = label_font.render('Clap (lėkštės)', True, teal)
    screen.blit(clap_text, (15, 442))
    tom_text = label_font.render('Tom (didelis būgnas)', True, teal)
    screen.blit(tom_text, (15, 542))
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = red
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     ((HEIGHT - 200) // instruments)], 0, 3)
            pygame.draw.rect(screen, yellow,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))
            pygame.draw.rect(screen, orange,
                             [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100],
                             5, 3)
    return boxes


# ############################################## engine
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    if beat_changed:
        play_notes()
        beat_changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
    beat_length = 3600 // bpm
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True
    pygame.display.flip()
pygame.quit()
crt_db()
