# Simulador de RPG de Texto com IA Narrativa

Este é um mini-RPG de texto desenvolvido em Python, onde o jogador vivencia uma pequena aventura com combate por turnos e um final conclusivo. O projeto foi criado como um exercício prático para iniciantes em programação Python, explorando não apenas a lógica de jogos, mas também a implementação de narração por voz e uma IA simples para geração de texto dinâmico.

## ✨ Funcionalidades

* **Aventura Completa:** Uma história curta e autônoma com início, meio e fim (a cena da "Emboscada na Estrada").
* **Combate por Turnos:** Um sistema de luta simples onde o jogador e os inimigos trocam ataques até que um dos lados seja derrotado.
* **Narração por Voz:** Todas as falas do narrador são convertidas para áudio em português do Brasil usando a biblioteca `gTTS`.
* **IA Narrativa (Cadeia de Markov):** O coração do projeto! Descrições de ambiente, ataques em combate e narrações de vitória são geradas dinamicamente pela biblioteca `markovify`, garantindo que cada jogada seja uma experiência única.

## 🕹️ Exemplo de Gameplay

atacar goblin a
Você se move com a graça de um dançarino antes de golpear.
(6 de dano em Goblin A)

Turno dos inimigos...
Goblin A: A criatura revida com ferocidade.
(3 de dano em você)

Goblin B: O goblin ataca de forma desajeitada mas perigosa.
(1 de dano em você)

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
    * `gTTS`: Para conversão de texto em fala.
    * `playsound`: Para executar os arquivos de áudio gerados.
    * `markovify`: Para a geração de texto procedural baseada em Cadeia de Markov.

## 🧠 O Cérebro da IA

A personalidade do narrador é moldada por vários arquivos de texto (`.txt`), cada um servindo como um "cérebro" especializado para diferentes situações:

* `corpus.txt`: Descrições de ambiente e exploração.
* `corpus_atq_jogador.txt`: Narrações para os ataques do jogador.
* `corpus_atq_inimigo.txt`: Narrações para os ataques dos inimigos.
* `corpus_vitoria.txt`: Frases para celebrar a vitória no combate.

Quanto mais texto for adicionado a esses arquivos, mais criativa e variada a IA se tornará.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o jogo em sua máquina local.

### Pré-requisitos

* Python 3.x instalado.
* Acesso à internet (para a biblioteca `gTTS`).
* Um sistema com saída de áudio (caixas de som ou fones de ouvido).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/kdu14/game_rpg.git](https://github.com/kdu14/game_rpg.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd game_rpg
    ```

3.  **Instale as dependências:**
    * É uma boa prática criar um ambiente virtual:
        ```bash
        python -m venv venv
        source venv/bin/activate  # No Windows: venv\Scripts\activate
        ```
    * Instale as bibliotecas necessárias:
        ```bash
        pip install gtts playsound==1.2.2 markovify
        ```

### Executando o Jogo

Com as dependências instaladas, basta executar o script principal:

```bash
python game.py