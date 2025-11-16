# Knight & Goblins

Um mini-jogo roguelike 2D, amigável para crianças, desenvolvido em Python com a biblioteca **PgZero (Pygame Zero)**.

O jogador controla um cavaleiro que deve sobreviver o máximo de tempo possível em um mapa patrulhado por goblins.

---

## 🎮 Como Jogar (Regras do Jogo)

* **Objetivo:** Seu objetivo é sobreviver o máximo de tempo possível! A pontuação é baseada no tempo que você permanece vivo.
* **Controles:** Use as **Setas do Teclado** (Cima, Baixo, Esquerda, Direita) para mover o cavaleiro.
* **Inimigos:** Evite colidir com os Goblins que patrulham o mapa.
* **Vidas:** Você começa com **3 pontos de vida (HP)**. Cada colisão com um inimigo remove um ponto.
* **Invulnerabilidade:** Após ser atingido, o herói fica invulnerável por 1 segundo, dando a você tempo para escapar.
* **Game Over:** O jogo termina quando seus pontos de vida chegam a 0. Você pode pressionar `ESPAÇO` para voltar ao menu principal.

---

## ✨ Funcionalidades Principais

* **Menu Principal:** Menu completo com botões clicáveis para "Start Game", "Music: On/Off" e "Exit".
* **Animação de Sprites:** O jogo usa uma classe `AnimatedSprite` customizada que gerencia animações de *idle* (parado) e *walk* (andando) tanto para o herói quanto para os inimigos.
* **IA de Patrulha:** Em vez de vagar aleatoriamente, os inimigos patrulham uma "zona de território" predefinida, tornando seu comportamento mais previsível e justo.
* **Gerenciamento de Estado:** O código é organizado em três estados de jogo: `STATE_MENU`, `STATE_PLAY` e `STATE_GAMEOVER`.
* **Música e Efeitos Sonoros:** O jogo inclui música de fundo (que pode ser desativada) e efeitos sonoros para cliques, dano (`hit`) e morte do herói (`death`).

---

## 🛠️ Bibliotecas e Tecnologias

* **Python 3**
* **PgZero (Pygame Zero):** O framework principal do jogo, que simplifica o desenvolvimento de jogos em Python.
* **Pygame:** (Usado parcialmente para a classe `Rect`, como uma dependência do PgZero).
* **Bibliotecas Padrão do Python:** `math` (para cálculos de movimento suave) e `random` (para a IA dos inimigos).

---

## 🚀 Como Executar

Para rodar este projeto, você precisará ter o Python e o PgZero instalados.

1.  **Clone ou baixe este repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd SEU-REPOSITORIO
    ```

2.  **Instale a biblioteca PgZero:**
    ```bash
    pip install pgzero
    ```

3.  **Estrutura de Pastas (Obrigatório):**
    O PgZero exige uma estrutura de pastas específica para carregar imagens e sons automaticamente. Certifique-se de que seu projeto esteja organizado desta forma:

    ```
    Game-Kodland/
    ├── main.py           (O arquivo de código principal)
    │
    ├── images/
    │   ├── hero_idle_0.png
    │   ├── hero_idle_1.png
    │   ├── hero_walk_0.png
    │   ├── ... (etc.)
    │   ├── enemy_idle_0.png
    │   ├── ... (etc.)
    │   ├── tile.png
    │   └── menu_banner.png
    │
    ├── music/
    │   └── music.mp3     (ou .ogg)
    │
    └── sounds/
        ├── hit.wav       (ou .ogg)
        ├── death.wav
        └── click.wav
    ```

4.  **Execute o jogo:**
    Abra seu terminal na pasta raiz do projeto (`Game-Kodland/`) e execute o seguinte comando:

    ```bash
    pgzrun main.py
    ```

---

## 🎨 Créditos dos Assets

Todo o trabalho de arte visual (personagens, tiles, animações) foi retirado do incrível pacote **"Kings and Pigs"** da artista **PixelFrog**.

O pacote está disponível gratuitamente e pode ser encontrado em:
**[https://pixelfrog-assets.itch.io/kings-and-pigs](https://pixelfrog-assets.itch.io/kings-and-pigs)**