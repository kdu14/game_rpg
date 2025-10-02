from gtts import gTTS
from playsound import playsound
import os
import random
import time

def narrador(texto):
    # Recebe um texto, converte para áudio, toca e depois apaga o arquivo de áudio.
    print(texto)

    try:
        tts = gTTS(text=texto, lang='pt-br')
        arquivo_narrador = 'narracao.mp3'
        tts.save(arquivo_narrador)

        playsound(arquivo_narrador)

        os.remove(arquivo_narrador)
    except Exception as e:
        print(f'\n [AVISO: Houve um erro ao gerar o audio: {e}]')
        print('[Verifique sua conexão com a internet]')

status_jogador = {
    'pv':20,
    'pv_max' : 20,
    'dano_min' : 1,
    'dano_max' : 6,
    'inv' : [],
    'xp' : 0
}

status_game = {
    'cena_atual' : 'inicio'
}

def start_combat(inimigos):
    narrador('A batalha começa!')

    while True:
        print("\n------STATUS------")
        print(f'Você: {status_jogador['pv']}/{status_jogador['pv_max']} PV')

        for inimigo in inimigos:
            print(f'{inimigo['nome']}: {inimigo['pv']}/{inimigo['pv_max']} PV')
        print("---------------")

        alvos_vivos = [inimigo['nome'].lower() for inimigo in inimigos if inimigo['pv'] > 0]
        comando = ''
        while comando not in alvos_vivos:
            comando = input(f'Seu turno. Atacar quem? {alvos_vivos}\n').lower()
            if comando not in alvos_vivos:
                print("Alvo inválido")
        for inimigo in inimigos:
            if inimigo['nome'].lower() == comando:
                dano_causado = random.randint(status_jogador['dano_min'], status_jogador['dano_max'])
                inimigo['pv'] = dano_causado
                narrador(f'Você ataca {inimigo['nome']} e causa {dano_causado} de dano')
                if inimigo['pv'] <= 0:
                    narrador(f'{inimigo['nome']} foi derrotado, parabéns')
                break
        
        time.sleep(1)

        inimigo_vivos = [i for i in inimigos if i['pv'] > 0]
        if not inimigo_vivos:
            return True # ganhou
        
        narrador('Turno de inimigos')
        time.sleep(1)

        for inimigo in inimigos:
            if inimigo['pv'] > 0:
                dano_recebido = random.randint(inimigo['dano_min'], inimigo['dano_max'])
                status_jogador['pv'] = dano_recebido
                narrador(f'{inimigo['nome']} ataca você e lhe causa {dano_recebido} de dano')
                time.sleep(1)

        if status_jogador['pv'] <= 0:
            return False # perdeu






def start_game():

    status_game['cena_atual'] = 'emboscada_estrada'

    narrador("Você caminha pela estrada de terra que leva à Cidadela de Pedra, o coração do reino de Eldoria.")
    narrador("O sol do meio-dia esquenta seus ombros e o ar está pesado com o zumbido dos insetos.")
    narrador("De repente, o som pacífico da sua jornada é quebrado por gritos agudos de pânico, vindos de uma curva logo à frente.")
    narrador("Você avança com cautela e vê a cena: uma carroça de mercador, virada. Ao lado dela, dois goblins ameaçam um homem caído.")
    print("-" * 30)
    narrador("O que você faz?")
    print("Comandos: [atacar], [ignorar], [esconder], [gritar]")

def main():
    narrador("Bem vindo a Eldoria! Uma aventura te aguarda.")
    narrador("Digite 'sair' a qualquer momento para terminar o jogo")
    print('-' * 60)

    start_game()

    while True:
        if status_game['cena_atual'] == 'emboscada_estrada':
            comando = input('> ').lower()

            if comando == 'sair':
                narrador("Até a próxima aventureiro")
                break

            elif comando == "atacar":
                narrador("Você saca sua arma e corre em direção à confusão. Os goblins se viram para você, com suas adagas em punho. A luta começa!")
                inimigos_da_luta = [
                    {"nome": "Goblin A", "pv": 8, "pv_max": 8, "dano_min": 1, "dano_max": 4},
                    {"nome": "Goblin B", "pv": 8, "pv_max": 8, "dano_min": 1, "dano_max": 4}
                ]
                # Chamamos a função de combate
                resultado = start_combat(inimigos_da_luta)
                if resultado: # Se o jogador venceu
                    narrador("Você venceu a batalha!")
                    status_game["cena_atual"] = "pos_combate"
                else: # Se o jogador perdeu
                    narrador("Você foi derrotado... Sua jornada termina aqui.")
                    break
                status_jogador["cena_atual"] = "pos_combate" # Mudamos de cena
                narrador("Após uma breve e feroz batalha, os goblins jazem derrotados.")
            
            elif comando == "ignorar":
                narrador("Você decide que a vida de um desconhecido não vale o risco e deixa a cena para trás. Os gritos cessam logo depois. O peso da sua escolha te acompanhará.")
                # O jogo poderia terminar aqui ou ter outras consequências.
                break 

            elif comando == "esconder":
                narrador("Você mergulha na vegetação alta. Você vê que os goblins estão revistando o mercador. Um terceiro goblin sai de trás da carroça. Eles não notaram sua presença.")
            
            elif comando == "gritar":
                narrador("Você solta um grito de guerra! Um dos goblins, covarde, corre para o mato. O outro, porém, avança com raiva na sua direção!")
                print("\n[SISTEMA DE COMBATE (COM 1 GOBLIN) AINDA NÃO IMPLEMENTADO]")
                status_jogador["cena_atual"] = "pos_combate"
                narrador("Você despacha o goblin solitário facilmente.")
            
            else:
                print(f"Não entendi o comando '{comando}'. Tente: [atacar], [ignorar], [esconder], [gritar]")
        
        # Futuramente, podemos ter outros estados aqui (na cidade, na floresta, etc.)
        elif status_jogador["cena_atual"] == "pos_combate":
            narrador("A poeira baixa. O mercador salvo olha para você com gratidão.")
            print("\n[SISTEMA DE DIÁLOGO E RECOMPENSAS AINDA NÃO IMPLEMENTADO]")
            break # Encerra o jogo por enquanto.
if __name__ == '__main__':
    main()
        