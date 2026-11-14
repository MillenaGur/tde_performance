import random
import threading
import time

NUM_FILOSOFOS = 5
PAUSA_ENTRE_GARFOS = 0.5
TEMPO_MAXIMO = 30

TEMPO_PENSAR_MIN = 0.1
TEMPO_PENSAR_MAX = 0.5
TEMPO_COMER_MIN = 0.1
TEMPO_COMER_MAX = 0.3

garfos = {numero: threading.Lock() for numero in range(1, NUM_FILOSOFOS + 1)}
estados = {numero: "pensando" for numero in range(1, NUM_FILOSOFOS + 1)}
trava_saida = threading.Lock()
inicio = time.time()

def registrar(mensagem):
    with trava_saida:
        print(f"[{time.time() - inicio:.3f}s] {mensagem}")

def mudar_estado(numero, estado):
    estados[numero] = estado
    registrar(f"Filósofo {numero} está {estado}")

def pegar_garfo(numero, garfo, lado):
    registrar(f"Filósofo {numero} tenta pegar o garfo {garfo} ({lado})")
    garfos[garfo].acquire()
    registrar(f"Filósofo {numero} pegou o garfo {garfo} ({lado})")

def soltar_garfo(numero, garfo, lado):
    garfos[garfo].release()
    registrar(f"Filósofo {numero} soltou o garfo {garfo} ({lado})")

def filosofo(numero):
    direito = numero
    esquerdo = numero - 1 if numero > 1 else NUM_FILOSOFOS

    while True:
        mudar_estado(numero, "pensando")
        time.sleep(random.uniform(TEMPO_PENSAR_MIN, TEMPO_PENSAR_MAX))

        mudar_estado(numero, "com fome")
        pegar_garfo(numero, esquerdo, "esquerdo")
        time.sleep(PAUSA_ENTRE_GARFOS)
        pegar_garfo(numero, direito, "direito")

        mudar_estado(numero, "comendo")
        time.sleep(random.uniform(TEMPO_COMER_MIN, TEMPO_COMER_MAX))

        soltar_garfo(numero, direito, "direito")
        soltar_garfo(numero, esquerdo, "esquerdo")

def todos_com_fome():
    return all(estado == "com fome" for estado in estados.values())

def main():
    for numero in range(1, NUM_FILOSOFOS + 1):
        threading.Thread(target=filosofo, args=(numero,), daemon=True).start()

    segundos = 0
    while segundos < TEMPO_MAXIMO:
        time.sleep(1)
        segundos += 1
        if todos_com_fome():
            time.sleep(3)
            if todos_com_fome():
                print("Deadlock! Todos os filósofos continuam com fome há mais de 3 segundos e ninguém consegue comer")
                return

    print()
    print(f"Nenhum deadlock no período de {TEMPO_MAXIMO} segundos")

main()