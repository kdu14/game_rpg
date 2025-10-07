from gtts import gTTS
from playsound import playsound
import os
import random
import time
import markovify

# --- CONFIGURAÇÃO DOS MODELOS DE IA ---
try:
    with open("corpus.txt", encoding="utf-8") as f:
        modelo_narrador_ia = markovify.Text(f.read())
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o corpus.txt: {e}")
    modelo_narrador_ia = None

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

try:
    with open("corpus_vitoria.txt", encoding="utf-8") as f:
        modelo_vitoria = markovify.Text(f.read())
except Exception as e:
    print(f"[AVISO] Não foi possível carregar o corpus_vitoria.txt: {e}")
    modelo_vitoria = None
# -----------------------------------------

def narrador(texto):
    # verificação para evitar o erro de áudio com 'None'
    if not texto:
        return
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
                if modelo_ataque_jogador:
                    frase_ataque = modelo_ataque_jogador.make_sentence(tries=100)
                    narrador(frase_ataque or "Você ataca!")
                else:
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
                if modelo_ataque_inimigo:
                    frase_ataque = modelo_ataque_inimigo.make_sentence(tries=100)
                    narrador(f"{inimigo['nome']}: {frase_ataque or 'ataca sem piedade!'}")
                else:
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
    print("Comandos: [atacar], [esconder]")

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
                inimigos_da_luta = [
                    {"nome": "Goblin A", "pv": 7, "pv_max": 7, "dano_min": 1, "dano_max": 3},
                    {"nome": "Goblin B", "pv": 7, "pv_max": 7, "dano_min": 1, "dano_max": 3}
                ]
                resultado = start_combat(inimigos_da_luta)
                
                if resultado:
                    if modelo_vitoria:
                        frase_vitoria = modelo_vitoria.make_sentence(tries=100)
                        narrador(frase_vitoria or "Você venceu a batalha!")
                    else:
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

            elif comando == "esconder":
                narrador("Você mergulha na vegetação alta para observar a cena...")
                time.sleep(1)

                frase_gerada = None
                if modelo_narrador_ia:
                    frase_gerada = modelo_narrador_ia.make_short_sentence(140, tries=100)
                
                # checamos se a frase foi gerada com sucesso ANTES de usá-la
                if frase_gerada:
                    narrador(frase_gerada)
                else:
                    # se a IA falhou ou não foi carregada, usamos a frase padrão
                    narrador("O silêncio da mata é pesado e opressor.")
                
                time.sleep(1)
                narrador("Você decide não se arriscar e espera os goblins irem embora. Você continua seu caminho em segurança.")
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