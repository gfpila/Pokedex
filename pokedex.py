import pandas as pd
import curses, pygame, keyboard, threading
from PIL import Image
import numpy as np
import os, sys
import time


# A BIBLIOTECA PANDAS RECUPERA OS DADOS DA PLANILHA
caminho = "pokemons.xlsx"
df = pd.read_excel(caminho, dtype={"Numero Pokedex": str})

# ESSA É A CLASSE QUE VAI INSTANCIAR O OBJETO POKEMON
class Pokemon:
    def __init__(self, numero, nome, tipo, fraqueza, altura, peso, genero, vida, ataque, velocidade, defesa, imagem, curiosidade):
        self.numero = numero
        self.nome = nome
        self.tipo = tipo
        self.fraqueza = fraqueza
        self.altura = altura
        self.peso = peso
        self.genero = genero
        self.vida = vida
        self.ataque = ataque
        self.velocidade = velocidade
        self.defesa = defesa
        self.imagem = imagem
        self.curiosidade = curiosidade

    # PARAMETRO PARA DAR AO OBJETO O NOME DO POKEMON
    def __repr__(self):
        return self.nome

# ARRAY CONTENDO UMA LISTA DOS OBJETOS POKEMON
pokemons = []

# LOOP PARA CRIAR CADA UM DOS OBJETOS UTILIZANDO O DATAFRAME DO PANDAS
for i in range(151):
    numero = df.iloc[i, 0]
    nome = df.iloc[i, 1]
    tipo = df.iloc[i, 2]
    fraqueza = df.iloc[i, 3]
    altura = df.iloc[i, 4]
    peso = df.iloc[i, 5]
    genero = df.iloc[i, 6]
    vida = df.iloc[i, 7]
    ataque = df.iloc[i, 8]
    velocidade = df.iloc[i, 9]
    defesa = df.iloc[i, 10]
    imagem = os.path.join("imagens", f"{numero}.jpg")
    curiosidade = df.iloc[i, 11]

    # INSTANCIA E ADICIONA O OBJETO NO ARRAY
    objPokemon = Pokemon(numero, nome, tipo, fraqueza, altura, peso, genero, vida, ataque, velocidade, defesa, imagem, curiosidade)
    pokemons.append(objPokemon)

# PARA RECUPERAR O NOME DOS POKEMONS
nomes = []
for i in range(151):
    nome = pokemons[i].nome
    nome = nome.lower()
    nomes.append(nome)

exit_signal = threading.Event()

def main():
    #Função Som
    global mute
    mute = False

    pygame.mixer.init()
    def play(sound_file):
        if mute == False:
            if sound_file == 'sons/musica.mp3':
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(-1)
            else:
                effect_sound = pygame.mixer.Sound(sound_file)
                effect_sound.play()

    #Sempre ouvir Alt
    def on_key_event(e):
        global mute
        if e.event_type == keyboard.KEY_DOWN and (e.name == "left alt" or e.scan_code == 56) and mute == False:
            mute = True
            pygame.mixer.music.stop()
        elif e.event_type == keyboard.KEY_DOWN and (e.name == "left alt" or e.scan_code == 56) and mute == True:
            mute = False
            play('sons/musica.mp3')

    def ouvir():
        keyboard.on_press(on_key_event)
        keyboard.wait()

    ouvirAlt = threading.Thread(target=ouvir)
    ouvirAlt.start()

    # INICIA A BIBLIOTECA CURSES
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Função para criar uma janela com borda
    def create_bordered_window(stdscr, height, width, y, x):
        window = stdscr.subwin(height, width, y, x)
        window.box()  # Desenha a borda ao redor da janela
        return window

    pokedex_win = create_bordered_window(stdscr, 39, 162, 1, 3)

    pokedex_win.addstr(7, 45, " ███████    ███████   ██   ██ ████████ ███████   ████████ ██     ██")
    pokedex_win.addstr(8, 45, "░██░░░░██  ██░░░░░██ ░██  ██ ░██░░░░░ ░██░░░░██ ░██░░░░░ ░░██   ██")
    pokedex_win.addstr(9, 45, "░██   ░██ ██     ░░██░██ ██  ░██      ░██    ░██░██       ░░██ ██")
    pokedex_win.addstr(10, 45, "░███████ ░██      ░██░████   ░███████ ░██    ░██░███████   ░░███")
    pokedex_win.addstr(11, 45, "░██░░░░  ░██      ░██░██░██  ░██░░░░  ░██    ░██░██░░░░     ██░██")
    pokedex_win.addstr(12, 45,"░██      ░░██     ██ ░██░░██ ░██      ░██    ██ ░██        ██ ░░██")
    pokedex_win.addstr(13, 45,"░██       ░░███████  ░██ ░░██░████████░███████  ░████████ ██   ░░██")

    pokedex_win.addstr(18, 45,"######   #######  ######", curses.color_pair(3))
    pokedex_win.addstr(19, 45," ##  ##   ##  ##    ##  ##", curses.color_pair(3))
    pokedex_win.addstr(20, 45," ##  ##   ##        ##  ##", curses.color_pair(3))
    pokedex_win.addstr(21, 45," #####    ####      ##  ##", curses.color_pair(3))
    pokedex_win.addstr(22, 45," ####     ##        ##  ##", curses.color_pair(3))
    pokedex_win.addstr(23, 45," ## ##    ##  ##    ##  ##", curses.color_pair(3))
    pokedex_win.addstr(24, 45,"###  ##  #######  ######", curses.color_pair(3))

    pokedex_win.addstr(18, 78,"######    ####     ##  ##  #######", curses.color_pair(4))
    pokedex_win.addstr(19, 78," ##  ##    ##      ##  ##   ##  ##", curses.color_pair(4))
    pokedex_win.addstr(20, 78," ##  ##    ##      ##  ##   ##", curses.color_pair(4))
    pokedex_win.addstr(21, 78," #####     ##      ##  ##   ####", curses.color_pair(4))
    pokedex_win.addstr(22, 78," ##  ##    ##      ##  ##   ##", curses.color_pair(4))
    pokedex_win.addstr(23, 78," ##  ##    ## ##   ##  ##   ##  ##", curses.color_pair(4))
    pokedex_win.addstr(24, 78,"######    ######    ####   #######", curses.color_pair(4))


    pokedex_win.addstr(30, 64,"Aperte 'ENTER' para continuar.")


    pokedex_win.refresh()
    play("sons/musica.mp3")


    # Loop principal para manter a interface aberta
    while True:
        key = pokedex_win.getch()  # Aguarda a entrada do usuário
        if key == 10:
            play("sons/efeito.mp3")
            break  # Saia do loop se o usuário pressionar 'q'

    curses.endwin()  # Restaura a tela do terminal


    # Função para desenhar a Pokedex na tela com uma janela com borda
    def draw_pokedex(stdscr, pokemons, page, play_animation=False, pokemons_per_page=30):

        play_animation = False

        pokedex_win = create_bordered_window(stdscr, 39, 66, 2, 2)
        image_win = create_bordered_window(stdscr, 39, 97, 2, 67)

        image_win.addstr(5, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(6, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣶⢿⣿⣻⣟⣿⣻⣟⣿⣻⣟⣿⣻⢿⡿⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(7, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡾⣟⡿⣽⡾⣽⣻⢾⣷⣻⢾⣷⣻⢾⣷⣻⣞⣯⡿⣽⣯⢿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(8, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡿⣿⣽⣻⡽⣿⣽⣻⣽⢯⣿⣞⣯⡿⣞⣯⣿⢾⡽⣯⣷⢿⣻⢾⣟⣾⡽⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(9, 16, "    ⠀⠀⠀⠀⠀⠀⠀⣠⣾⠿⣽⡛⡷⢯⡷⣿⣳⣯⣟⣾⣟⡷⣯⢿⣽⣻⣽⢾⣻⣟⣷⢯⡿⣯⡿⣞⣯⢿⣳⣯⢿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(10, 16, "    ⠀⠀⠀⠀⠀⢀⣴⡿⣝⡿⡿⡿⡿⡿⣽⣳⢯⣷⣻⢷⣯⣟⡿⣯⣷⢿⣽⣻⣽⡾⣯⣟⣿⣳⢿⣻⡽⣟⡿⣞⣿⣽⣻⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀")
        image_win.addstr(11, 16, "    ⠀⠀⠀⠀⣠⣿⢯⡟⡿⡿⡿⡿⡿⡿⢧⣟⣯⡷⣟⡿⣾⣽⣻⢷⣯⢿⣞⣯⡷⣿⣽⢾⣳⣿⣻⡽⣟⣯⣿⣻⢷⣯⢿⣽⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀")
        image_win.addstr(12, 16, "    ⠀⠀⠀⣰⣿⡽⣯⣟⡿⡿⡿⡿⡿⡽⣞⡿⣾⡽⣿⡽⣷⢯⣟⡿⣾⣻⡽⣷⣻⣽⡾⣟⡿⣾⣽⣻⢯⣷⢯⣟⡿⣾⢯⣷⢿⣿⣿⣿⣿⣿⣄⠀⠀⠀")
        image_win.addstr(13, 16, "    ⠀⠀⣸⣿⣳⡿⣽⡾⣽⣻⢾⡽⣯⢿⣽⣻⢷⣟⡷⣿⢯⣟⣯⡿⣷⣻⣽⢿⣽⣳⡿⣯⣟⣷⢯⣟⣯⣟⣯⡿⣽⣯⢿⡽⣯⣿⣿⣿⣿⣿⣿⡆⠀⠀")
        image_win.addstr(14, 16, "    ⠀⢰⣿⣳⡿⣽⡷⣟⣯⣟⣯⣿⡽⣯⣷⣟⡿⣾⣻⣽⣟⣯⡷⣿⣽⣻⢾⣯⡷⣿⡽⣷⣻⣽⣻⢯⣟⣾⢯⣟⣷⣻⣯⢿⣻⣞⣿⣿⣿⣿⣿⣿⡄⠀")
        image_win.addstr(15, 16, "    ⠀⣿⢷⣻⣽⡷⣟⡿⣽⣾⣻⢾⣽⣟⣾⣽⣻⢷⣻⢷⣻⡾⣽⣷⣿⣿⣿⢿⣿⣷⣿⣯⣟⣾⣻⢯⣿⢾⣻⣽⡾⣷⣻⢿⡽⣯⣿⣿⣿⣿⣿⣿⣷⠀")
        image_win.addstr(16, 16, "    ⢸⣿⣻⣽⢾⣻⣽⣟⡿⣾⡽⣯⣷⢿⣞⡷⣿⣻⢯⣿⣻⣿⡿⢋⣥⣶⣶⣶⠠⠈⠛⢿⣿⣷⣟⣯⣟⣯⣟⡷⣿⡽⣯⣟⣿⣳⣿⣿⣿⣿⣿⣿⣿⡄")
        image_win.addstr(17, 16, "    ⣾⣳⣯⣟⣯⣿⣾⣽⣻⣷⣟⣿⣞⣯⣿⣽⣷⣻⣯⣿⣿⠏⣼⡿⢛⠁⠀⠀⠈⢰⡀⠀⣿⣿⣿⣽⣾⣻⣾⣻⣷⣟⣯⣿⣾⣽⣷⣿⣿⣿⣿⣿⣿⡇")
        image_win.addstr(18, 16, "    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⡿⠁⠀⠀⠀⠀⠀⠀⢻⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷")
        image_win.addstr(19, 16, "    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢾⣷⡀⠀⠀⠈⠆⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿")
        image_win.addstr(20, 16, "    ⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣻⣿⣎⠋⠳⣄⡀⠀⠀⣀⣴⣿⣿⣿⣿⡟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⣿⣿⡗")
        image_win.addstr(21, 16, "    ⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣧⣄⣈⢹⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⡇")
        image_win.addstr(22, 16, "    ⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣳⣿⣿⠀")
        image_win.addstr(23, 16, "    ⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣻⣿⠇⠀")
        image_win.addstr(24, 16, "    ⠀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢲⣿⡟⠀⠀")
        image_win.addstr(25, 16, "    ⠀⠀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣻⡟⠀⠀⠀")
        image_win.addstr(26, 16, "    ⠀⠀⠀⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣟⡟⠀⠀⠀⠀")
        image_win.addstr(27, 16, "    ⠀⠀⠀⠀⠀⠑ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀")
        image_win.addstr(28, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢞⠟⠁⠀⠀⠀⠀⠀⠀")
        image_win.addstr(29, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(30, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(31, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.addstr(32, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠒⠂⠀⠤⠤⠤⠤⠤⠤⠀⠀⠒⠂⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        image_win.refresh()

        row = 2
        col = 2  # Aumente a margem esquerda para acomodar a borda

        for i, pokemon in enumerate(pokemons):
            pokedex_win.addstr(row, col, f"{pokemon.numero} - {pokemon.nome}", curses.A_BOLD)
            row += 1

            if (i + 1) % 26 == 0:
                row = 2
                col += 25

        pokedex_win.refresh()

    pokemons_per_page = 52  # Defina o número de Pokémon por página aqui
    page = 1

    def display_pokemon_info(stdscr, pokemon):
        play_animation = True

        if play_animation is True:
            time.sleep(0.8)
            play('sons/pokebola.mp3')

            image_win = create_bordered_window(stdscr, 39, 97, 2, 67)
            image_win.clear()
            open_win = create_bordered_window(stdscr, 39, 97, 2, 67)
            open_win.addstr(7, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⠶⠶⠟⠟⠛⠛⠛⠛⠛⠲⢶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(8, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣟⠋⠉⠠⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⢀⣴⠾⠛⠻⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(9, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⡛⠁⠀⠀⠉⠀⠀⠀⠀⠀⢀⣀⣤⣤⣀⣀⠀⠀⢸⣇⠀⠀⠀⠀⠙⠛⠻⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(10, 16, "    ⠀⠀⠀⠀⠀⠀⢀⣴⣿⡏⠃⠀⠀⠀⠀⠀⠀⠀⠀⣤⡾⣛⣽⠴⠦⢬⣽⠻⣦⡀⠹⣧⣄⠀⠀⠀⠀⠁⠀⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(11, 16, "    ⠀⠀⠀⠀⢀⣴⣿⣿⡿⠃⠀⠀⠀⠀⣀⣀⣠⣤⣾⢏⣾⠋⢀⣀⣀⣀⠈⢻⡟⢿⣤⣀⣙⣃⠀⠀⠀⠀⠀⠀⠀⠙⢷⡄⠀⠀⠀⠀⠀")
            open_win.addstr(12, 16, "    ⠀⠀⠀⢠⣾⣿⣿⣿⣆⣠⣤⡶⠟⠛⠉⠉⠉⢀⣆⣿⡁⠀⢯⣀⣀⣸⠇⢀⣿⣆⣈⠉⠉⠉⠛⠛⠶⢦⣤⣀⠀⠀⠀⢻⣆⠀⠀⠀⠀")
            open_win.addstr(13, 16, "    ⠀⠀⢠⣿⣿⣿⣿⡿⠟⠋⣁⣠⣤⣶⣾⣿⣿⣿⣿⣿⢿⣦⡄⠀⠀⣀⣤⣾⢟⣿⣿⣿⣿⣿⣶⣦⣤⣀⠈⠙⠿⣦⣀⠀⠹⣦⠀⠀⠀")
            open_win.addstr(14, 16, "    ⠀⢀⣿⣿⣿⠟⣉⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⣛⠚⠛⢛⣛⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠙⠷⣌⢹⣦⠀⠀")
            open_win.addstr(15, 16, "    ⠀⣾⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡘⢿⣿⡆⠀")
            open_win.addstr(16, 16, "    ⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠉⣷⠀")
            open_win.addstr(17, 16, "    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢻⡀")
            open_win.addstr(18, 16, "    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇")
            open_win.addstr(19, 16, "    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇")
            open_win.addstr(20, 16, "    ⢻⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⠀")
            open_win.addstr(21, 16, "    ⢸⣟⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⡾⠀")
            open_win.addstr(22, 16, "    ⠀⣿⡌⠳⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣰⠇⠀")
            open_win.addstr(23, 16, "    ⠀⠸⣷⠀⠈⠻⢮⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⢠⡟⠀⠀")
            open_win.addstr(24, 16, "    ⠀⠀⠘⣿⡆⠀⠀⠈⠙⠂⠉⣙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀")
            open_win.addstr(25, 16, "    ⠀⠀⠀⠘⣷⡆⡀⠀⠀⠀⠀⠀⠀⠀⠒⠂⠉⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⠀")
            open_win.addstr(26, 16, "    ⠀⠀⠀⠀⠈⢻⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠋⠀⠀⠀⠀⠀")
            open_win.addstr(27, 16, "    ⠀⠀⠀⠀⠀⠀⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀")
            open_win.addstr(28, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(29, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⢦⣄⡀⠀⠀⠀⠈⠓⠦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.addstr(30, 16, "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠶⠤⢤⣤⣀⣀⣈⣉⣀⣀⣠⣤⠤⠴⠚⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            open_win.refresh()
            time.sleep(0.8)

        open_win = create_bordered_window(stdscr, 39, 97, 2, 67)
        open_win.clear()
        info_win = create_bordered_window(stdscr, 39, 43, 2, 67)

        height, width = 17, 39

        sub_window = info_win.subwin(height, width, 23, 69)
        sub_window.refresh()  

        height, width = 4, 39

        fraq_window = info_win.subwin(height, width, 19, 68)
        fraq_window.refresh()  

        info_win.addstr(2, 14, f"{pokemon.nome}", curses.color_pair(2))
        info_win.addstr(6, 19, f"Tipo:", curses.color_pair(2))
        info_win.addstr(6, 25, f"{pokemon.tipo}", curses.A_BOLD)
        info_win.addstr(6, 3, f"Altura:", curses.color_pair(2))
        info_win.addstr(6, 11, f"{pokemon.altura}", curses.A_BOLD)
        info_win.addstr(9, 3, f"Peso:", curses.color_pair(2))
        info_win.addstr(9, 9, f"{pokemon.peso}", curses.A_BOLD)
        info_win.addstr(9, 19, f"Gênero:", curses.color_pair(2))
        info_win.addstr(9, 27, f"{pokemon.genero}", curses.A_BOLD)
        info_win.addstr(12, 3, f"Vida:", curses.color_pair(2))
        info_win.addstr(12, 9, f"{pokemon.vida}", curses.A_BOLD)
        info_win.addstr(12, 19, f"Ataque:", curses.color_pair(2))
        info_win.addstr(12, 27, f"{pokemon.ataque}", curses.A_BOLD)
        info_win.addstr(15, 3, f"Defesa:", curses.color_pair(2))
        info_win.addstr(15, 11, f"{pokemon.defesa}", curses.A_BOLD)
        info_win.addstr(15, 19, f"Velocidade:", curses.color_pair(2))
        info_win.addstr(15, 31, f"{pokemon.velocidade}", curses.A_BOLD)
        fraq_window.addstr(1, 2, f"Fraqueza:", curses.color_pair(2))
        fraq_window.addstr(1, 12, f"{pokemon.fraqueza}", curses.A_BOLD)
        sub_window.addstr(1, 13, f"Curiosidade:", curses.color_pair(2))
        sub_window.addstr(3, 0, f"{pokemon.curiosidade}", curses.A_BOLD)
        info_win.refresh()

    def display_pokemon_image(stdscr, pokemon):
        image_win = create_bordered_window(stdscr, 39, 55, 2, 109)
        
        caminho_imagem = pokemon.imagem
        try:
            img = Image.open(caminho_imagem)
            img.thumbnail((32, 32))  # Redimensione a imagem mantendo a proporção
            img = img.convert('L')  # Converta a imagem em escala de cinza
            pixels = img.load()

            # Use blocos de caracteres Unicode para representar a imagem
            char_map = [' ', '░', '▒', '▓', '█']
            
            # Calcule a posição de início para centralizar a imagem
            start_x = (image_win.getmaxyx()[1] - img.width) // 2
            start_y = (image_win.getmaxyx()[0] - img.height) // 2

            for y in range(img.height):
                row_text = ""
                for x in range(img.width):
                    pixel_value = pixels[x, y]
                    # Mapeie o valor do pixel para os blocos de caracteres Unicode
                    char_index = min(int(pixel_value / 51), len(char_map) - 1)
                    char = char_map[char_index]
                    row_text += char
                image_win.addstr(start_y + y, start_x, row_text)
            
            image_win.refresh()
        except Exception as e:
            image_win.addstr(5, 1, f"Erro ao carregar a imagem: {e}")
        
        image_win.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                play("sons/efeito.mp3")
                break

    while True:
        stdscr.clear()
        draw_pokedex(stdscr, pokemons[(page - 1) * pokemons_per_page:page * pokemons_per_page], page, pokemons_per_page)
        stdscr.addstr(31, 4, f"Página {page}/{len(pokemons) // pokemons_per_page + 1}.")
        stdscr.addstr(32, 6, "<--->")
        stdscr.addstr(34, 4, "Pressione 'Q' para sair ou ENTER para pesquisar.")
        stdscr.addstr(31, 20, "ALT: Silenciar som")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            play("sons/efeito.mp3")
            ouvirAlt._delete()
            pygame.mixer.stop()
            pygame.quit()
            curses.endwin()
            exit_signal.set()
            os._exit(1)
            sy
             
        elif key == curses.KEY_RIGHT:
            if page < len(pokemons) // pokemons_per_page + 1:
                page += 1
        elif key == curses.KEY_LEFT:
            if page > 1:
                page -= 1
        elif key == ord('\n') or key == 459:
            play("sons/efeito.mp3")
            stdscr.addstr(36, 4, "Digite o nome ou o número do pokémon de sua escolha. ")
            stdscr.refresh()
            search_input = ""
            curses.echo()
            while True:
                c = stdscr.getch()
                if c == ord('\n') or c == 459:
                    play("sons/efeito.mp3")
                    curses.noecho()
                    break
                elif c == 27:  # 27 is the escape key
                    play("sons/efeito.mp3")
                    curses.noecho()
                    break
                else:
                    search_input += chr(c)
            search_input = search_input.strip().lower()

            # Realize a pesquisa pelo nome ou número e exiba as informações se encontradas
            found_pokemon = None
            for pokemon in pokemons:
                if search_input == pokemon.nome.lower() or search_input == pokemon.numero.lower():
                    found_pokemon = pokemon
                    stdscr.addstr(38, 4, "Pressione 'Q' para voltar para a lista. ")
                    break
                else:
                    
                    try:
                        search_input = int(search_input)
                        if search_input == int(pokemon.numero):
                            found_pokemon = pokemon
                            stdscr.addstr(38, 4, "Pressione 'Q' para voltar para a lista. ")
                            break
                    except:
                        pass

            if found_pokemon:
                display_pokemon_info(stdscr, found_pokemon)
                display_pokemon_image(stdscr, found_pokemon)
            else:
                stdscr.addstr(38, 4, "Pokémon não encontrado, pressione 'Q' para tentar novamente. ")
                stdscr.refresh()
                while True:
                    key = stdscr.getch()
                    if key == ord('q') or key == ord('Q'):
                        play("sons/efeito.mp3")
                        break

                play_animation = False

main()