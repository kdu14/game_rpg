from gtts import gTTS
from playsound import playsound
import os
import random
import time
import markovify

try:
    with open("corpus.txt", encoding="utf-8") as f:
        modelo_narrador_ia = markovify.Text(f.read())
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o corpus.txt: {e}")
    modelo_narrador_ia = None

# Corrigido para bater com os nomes dos seus arquivos
try:
    with open("corpus_atq_jogador.txt", encoding="utf-8") as f:
        modelo_ataque_jogador = markovify.Text(f.read())
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o corpus_atq_jogador.txt: {e}")
    modelo_ataque_jogador = None

try:
    with open("corpus_atq_inimigo.txt", encoding="utf-8") as f:
        modelo_ataque_inimigo = markovify.Text(f.read())
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o corpus_atq_inimigo.txt: {e}")
    modelo_ataque_inimigo = None

def narrador(texto):
    print(texto)
    try:
        tts = gTTS(text=texto, lang='pt-br')
        arquivo_narrador = 'narracao.mp3'
        tts.save(arquivo_narrador)
        playsound(arquivo_narrador)
        os.remove(arquivo_narrador)
    except Exception as e:
        print(f'\n [AVISO: Houve um erro ao gerar o audio: {e}]')

status_jogador = {
    'pv': 20, 'pv_max': 20, 'dano_min': 1, 'dano_max': 6, 'xp': 0
}

status_game = {
    'cena_atual': 'inicio'
}

def start_combat(inimigos):
    narrador('A batalha começa!')
    while True:
        print("\n------STATUS------")
        print(f'Você: {status_jogador["pv"]}/{status_jogador["pv_max"]} PV')
        for inimigo in inimigos:
            print(f'{inimigo["nome"]}: {inimigo["pv"]}/{inimigo["pv_max"]} PV')
        print("---------------")

        alvos_vivos = [inimigo['nome'].lower() for inimigo in inimigos if inimigo['pv'] > 0]
        if not alvos_vivos: return True

        comando = ''
        while comando not in alvos_vivos:
            comando = input(f'Seu turno. Atacar quem? {alvos_vivos}\n> ').lower()
            if comando not in alvos_vivos: print("Alvo inválido")
        
        for inimigo in inimigos:
            if inimigo['nome'].lower() == comando:
                # ===== CONEXÃO COM A IA DO JOGADOR =====
                if modelo_ataque_jogador:
                    frase_ataque = modelo_ataque_jogador.make_sentence(tries=100) or "Você ataca!"
                    narrador(frase_ataque)
                else: # Fallback se o modelo não carregar
                    narrador(f'Você ataca {inimigo["nome"]}!')
                
                dano_causado = random.randint(status_jogador['dano_min'], status_jogador['dano_max'])
                inimigo['pv'] -= dano_causado
                print(f"({dano_causado} de dano em {inimigo['nome']})")
                
                if inimigo['pv'] <= 0:
                    narrador(f'{inimigo["nome"]} foi derrotado!')
                break
        
        time.sleep(1)
        if not any(i['pv'] > 0 for i in inimigos): return True

        narrador('Turno dos inimigos...')
        time.sleep(1)
        for inimigo in inimigos:
            if inimigo['pv'] > 0:
                # ===== CONEXÃO COM A IA DO INIMIGO =====
                if modelo_ataque_inimigo:
                    frase_ataque = modelo_ataque_inimigo.make_sentence(tries=100) or "O inimigo ataca!"
                    narrador(f"{inimigo['nome']}: {frase_ataque}")
                else: # Fallback
                     narrador(f'{inimigo["nome"]} ataca você!')

                dano_recebido = random.randint(inimigo['dano_min'], inimigo['dano_max'])
                status_jogador['pv'] -= dano_recebido
                print(f"({dano_recebido} de dano em você)")
                time.sleep(1)

        if status_jogador['pv'] <= 0: return False

def start_game():
    status_game['cena_atual'] = 'emboscada_estrada'
    narrador("Você caminha pela estrada de terra...")
    narrador("...dois goblins ameaçam um homem caído.")
    print("-" * 30)
    narrador("O que você faz?")
    print("Comandos: [atacar], [ignorar], [esconder]")

def main():
    narrador("Bem vindo a Eldoria! Uma aventura te aguarda.")
    narrador("Digite 'sair' a qualquer momento para terminar o jogo.")
    print('-' * 60)
    start_game()

    while True:
        if status_game['cena_atual'] == 'emboscada_estrada':
            comando = input('> ').lower()

            if comando == 'sair':
                narrador("Até a próxima aventureiro!")
                break

            elif comando == "atacar":
                # Você tinha mudado os stats dos goblins, voltei para o original para o combate ser mais rápido
                inimigos_da_luta = [
                    {"nome": "Goblin A", "pv": 8, "pv_max": 8, "dano_min": 1, "dano_max": 4},
                    {"nome": "Goblin B", "pv": 8, "pv_max": 8, "dano_min": 1, "dano_max": 4}
                ]
                resultado = start_combat(inimigos_da_luta)
                
                if resultado:
                    narrador("Você venceu a batalha!")
                    time.sleep(1)
                    xp_ganho = 50
                    status_jogador['xp'] += xp_ganho
                    narrador(f"Você ganhou {xp_ganho} pontos de experiência!")
                    print(f"(XP Total: {status_jogador['xp']})")
                    time.sleep(1)
                    status_game["cena_atual"] = "pos_combate"
                else:
                    narrador("Você foi derrotado... Sua jornada termina aqui.")
                    break
            
            elif comando == "ignorar":
                narrador("Você decide que a vida de um desconhecido não vale o risco e sai de fininho.")
                narrador("\nFIM")
                break 

            # ===== CONEXÃO COM A IA DE AMBIENTE =====
            elif comando == "esconder":
                narrador("Você mergulha na vegetação alta e observa a cena...")
                time.sleep(1)
                if modelo_narrador_ia:
                    frase_gerada = modelo_narrador_ia.make_short_sentence(100, tries=100)
                    narrador(frase_gerada or "O silêncio da mata é pesado e opressor.")
                else:
                    narrador("Você se esconde e observa os goblins roubarem o mercador e irem embora.")
                
                narrador("Você espera eles irem embora e continua seu caminho em segurança.")
                narrador("\nFIM")
                break
            
            else:
                print(f"Não entendi o comando '{comando}'.")
        
        elif status_game["cena_atual"] == "pos_combate":
            narrador("A poeira baixa. O mercador salvo se levanta e olha para você com gratidão...")
            narrador("'Meu herói! Você me salvou! Tome, não é muito, mas é o mínimo que posso fazer.'")
            narrador("Ele te entrega um pequeno saco com algumas moedas de prata.")
            narrador("\nCom seu primeiro ato heroico concluído, você continua sua jornada.")
            narrador("\nFIM")
            break

if __name__ == '__main__':
    main()