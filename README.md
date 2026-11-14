# TDE Programação Concorrente: Filósofos, Semáforos e Deadlock

Vídeo da apresentação: (link do YouTube)

Grupo: TDE2 4

Integrantes:  
Willian Anderson da Rocha  
Felipe Rodrigues Milicio  
Millena Gurczakovski  
Clara Miyamoto Yajima  

Linguagem: Python 3.10 ou superior.

## Parte 1: Jantar dos filósofos

### Como o problema funciona
Cinco filósofos se sentam em volta de uma mesa redonda e entre cada par de vizinhos fica um garfo, então são cinco garfos no total. Cada filósofo repete a mesma rotina: pensa durante um tempo, fica com fome e come. Só que para comer, ele precisa dos dois garfos ao lado dele, o da esquerda e o da direita, e só devolve os dois quando termina de comer.

### PARTE 1 - Versão ingênua
Nessa versão, o protocolo é o mais direto possível. Quando fica com fome, o filósofo pega o garfo esquerdo, depois ele pega o direito, come e solta os dois.
Se o garfo que o filósofo quer está com o filósofo vizinho, a thread fica bloqueada no "acquire" até o vizinho soltar.
O programa escreve no console cada mudança de estado (pensando, com fome, comendo) junto com o tempo desde o início, assim como registra quando um filósofo tenta pegar, pegou ou soltou um garfo.

### Por que o impasse acontece
O problema acontece quando os cinco ficam com fome mais ou menos no mesmo tempo. Cada filósofo consegue pegar o garfo esquerdo, porque ninguém estava usando. Depois todos tentam pegar o direito, mas o garfo direito de cada filósofo é o esquerdo do vizinho que já foi pego. Por consequência, cada um espera um garfo que só volta para a mesa depois que o vizinho comer, e o vizinho não come porque também está esperando. Ninguém solta nada e o programa fica parado para sempre.

Nesse caso, as quatros condições de Coffman se encontram presentes. O garfo só pode estar com um filósofo por vez (exclusão mútua), cada um segura um garfo enquanto espera o outro (manter e esperar), ninguém tira o garfo da mão do vizinho (não preempção), e por fim, a espera dá a volta na mesa: o 1 espera o 2, o 2 espera o 3, e por assim vai até chegar no 5 que espera o 1 (espera circular).

O impasse não é garantido porque depende de como o escalonador intercala as threads. Para fins de reprodução, foi utilizado um "time.sleep" entre pegar o garfo esquerdo e pegar o garfo direito. Com a pausa de 0,5 segundos entre os garfos, o impasse ocorreu durante as execuções. Porém, com a pausa em 0, não foi apresentado nenhum impasse. Quando ajustado para 0,1, ocorre ocasionalmente. O erro está presente no protocolo em todos os testes, a questão é que o tempo pode ajudar a mascarar isso.

### Como o programa detecta impasse
A thread principal olha o dicionário "estados" a cada segundo. Se todos os filósofos estiverem "com fome", ele vai esperar mais 3 segundos e vai olhar de novo. Se permanecerem com fome, conclui que travou, avisa e encerra o programa. 

Obs: O "daemon" foi utilizado para conseguir finalizar o programa.

### Como executar
Abra o cmd ou terminal correspondente (No caso abaixo, utilizamos o cmd):
```
cd parte_1
python parte_1_versao_ingenua.py
```
No topo do arquivo ficam as constantes usadas no programa. Se quiser testar sem a pausa entre pegar o garfo, basta substituir o valor da constante "PAUSA_ENTRE_GARFOS" para 0

### Pseudocódigo da versão ingênua
```
N = 5
garfos 1..N, o garfo i fica entre os filósofos i e i+1 (o garfo N fica entre N e 1)

para cada filósofo p:
    direito = p
    esquerdo = p - 1, ou N se p = 1

    repetir:
        pensar()
        estado[p] <- "com fome"
        adquirir(esquerdo)
        dormir(pausa)
        adquirir(direito)
        estado[p] <- "comendo"
        comer()
        liberar(direito)
        liberar(esquerdo)
        estado[p] <- "pensando"
```
### Log de uma execução com deadlock
```
[0.001s] Filósofo 1 está pensando
[0.001s] Filósofo 2 está pensando
[0.002s] Filósofo 3 está pensando
[0.002s] Filósofo 4 está pensando
[0.002s] Filósofo 5 está pensando
[0.220s] Filósofo 2 está com fome
[0.220s] Filósofo 2 tenta pegar o garfo 1 (esquerdo)
[0.220s] Filósofo 2 pegou o garfo 1 (esquerdo)
[0.242s] Filósofo 1 está com fome
[0.243s] Filósofo 1 tenta pegar o garfo 5 (esquerdo)
[0.243s] Filósofo 1 pegou o garfo 5 (esquerdo)
[0.421s] Filósofo 4 está com fome
[0.422s] Filósofo 4 tenta pegar o garfo 3 (esquerdo)
[0.422s] Filósofo 4 pegou o garfo 3 (esquerdo)
[0.470s] Filósofo 5 está com fome
[0.470s] Filósofo 5 tenta pegar o garfo 4 (esquerdo)
[0.470s] Filósofo 5 pegou o garfo 4 (esquerdo)
[0.501s] Filósofo 3 está com fome
[0.501s] Filósofo 3 tenta pegar o garfo 2 (esquerdo)
[0.501s] Filósofo 3 pegou o garfo 2 (esquerdo)
[0.720s] Filósofo 2 tenta pegar o garfo 2 (direito)
[0.743s] Filósofo 1 tenta pegar o garfo 1 (direito)
[0.922s] Filósofo 4 tenta pegar o garfo 4 (direito)
[0.970s] Filósofo 5 tenta pegar o garfo 5 (direito)
[1.002s] Filósofo 3 tenta pegar o garfo 3 (direito)
Deadlock! Todos os filósofos continuam com fome há mais de 3 segundos e ninguém consegue comer
```
Como deu para ver: Nenhum filósofo chegou a comer. Cada um pegou o seu garfo esquerdo e ficou tentando pegar o direito, e as cinco últimas linhas do log mostram isso.

## PARTE 1 - Versão corrigida

## PARTE 2

## PARTE 3
