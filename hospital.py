#gerenciamento de fila de um hospital
import time

#implementa classe que sera utilizada como elemento da fila
class Element:
    def __init__(self, valor, priority):
        self.item = valor
        self.priority = priority
    def __str__(self):
        return str(self.item) + " " + str(self.priority)
    
#implementa classe fila
class PriorityQueue:
    #inicia com sua fila vazia
    def __init__(self):
        self.items = []
        self.pronto_socorro_ferimento_profundo = []  #fila para casos de perigos de morte

    #verifica se ta vazia
    def is_Empty(self):
        return len(self.items) == 0
    
    #retorna o numero de elementos na fila
    def size(self):
        return len(self.items)
    
    #adiciona o elemento no final da fila com sua prioridade
    def enqueue(self, item, priority):
        elemento = Element(item, priority)
        self.items.insert(0, elemento)
        print('foi adicionado o paciente %s' %elemento )
    def enqueue_pronto_socorro_ferimento_profundo(self, item):
        self.pronto_socorro_ferimento_profundo.append(item)
        print(f'Paciente com ferimento profundo {item} enviado para pronto socorro')
    #remove elemento com maior prioridade
    def dequeue(self):
        if self.is_Empty():
            print('não ha pacientes a ser atendido')
        else:
            print('chamando paciente')
            posicao = 0
            menor = self.items[posicao].priority
            for i in range(self.size()):
                if self.items[i].priority < menor:
                    posicao = i
                    menor = self.items[i].priority
            #remove elemento da fila
            removido = self.items.pop(posicao)
            return removido.item
        
    #imprime fila na tela
    def print_queue(self):
        L = []
        for x in self.items:
            L.append(x.item)
        print(L)  
#cria os consultorios para servir de exemplo
class Sala:
    def __init__(self, numero):
        self.numero = numero
        self.paciente_atual = None

    def atender_paciente(self, paciente):
        self.paciente_atual = paciente
        print(f'Paciente {paciente} está na sala {self.numero}')

    def liberar_paciente(self):
        print(f'Paciente {self.paciente_atual} liberado da sala {self.numero}')
        self.paciente_atual = None
paciente = PriorityQueue()
#coleta de informações do paciente
def coletar_informacoes_paciente(fila_pacientes, fila_pronto_socorro_ferimento_profundo):
    while True:
        prioridade = 9
        nome = str(input("Nome do paciente: "))        
        ano_nascimento = int(input("Digite o ano de nascimento do paciente: "))
        idade = 2023 - ano_nascimento
        sexo = input("Digite M para masculino e F para feminino: ").upper()
        if sexo == "F":
            gestante = input("É gestante? Responda com S (sim) ou N (não): ").upper()
            if gestante == "S":
                prioridade -= 3
        #de acordo com a lei pra ser considerada uma criança de colo ou criança que tenha alguma prioridade é de bom senso do estabelecimento e após uma pesquisa com mães elas tem uma preferencia que seja considerada ate os 4 anos
        if idade <= 4:
            prioridade -= 3
        elif idade >= 60:
            prioridade -= 3
        #laço pra ir coletando as informações de sintomas pra estabelecer uma prioridade
        while True:
            sintomas = int(input("1 = ferimento profundo\n2 = doença crônica\n3 = ferimento leve\n4 = gripe\ndigite a condição relatada. Caso não tenha mais nenhum sintoma, digite 0: "))
            if sintomas == 0:
                break
            #esse é um dos casos mais graves onde há o risco de morte e que tem de ser atendida em um pronto socorro
            elif sintomas == 1:
                fila_pronto_socorro_ferimento_profundo.enqueue_pronto_socorro_ferimento_profundo(nome)
                return
                
            elif sintomas == 2:
                prioridade -= 3
            elif sintomas == 3:
                prioridade -= 1
            else:
                prioridade -= 1
        
        fila_pacientes.enqueue(nome, prioridade)
        mais_pacientes = input("Deseja cadastrar outro paciente? (S/N): ").upper()
        if mais_pacientes != 'S':
            break

sala1 = Sala(1)
salas = [sala1]
pacientes_geral = PriorityQueue()
pronto_socorro_ferimento_profundo = PriorityQueue()

while True:
    coletar_informacoes_paciente(pacientes_geral, pronto_socorro_ferimento_profundo)
#função pra simular um consultorio que ira chamar os pacientes em ordem de prioridade
    while not pacientes_geral.is_Empty() or sala1.paciente_atual is not None:
        for sala in salas:
            if sala1.paciente_atual is None and not pacientes_geral.is_Empty():
                proximo_paciente = pacientes_geral.dequeue()
                if proximo_paciente is not None:
                    sala.atender_paciente(proximo_paciente)
                    time.sleep(5)
                    sala.liberar_paciente()
                    time.sleep(1)