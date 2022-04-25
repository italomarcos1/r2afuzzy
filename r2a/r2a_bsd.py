#   @file: r2a_bsd.py
#   @author: Marina Pinho Garcia      - 170110702
#   @author: Guilherme Mattos Camargo - 170104508
#   @author: Rafael Fernandes Barbosa - 170163857 
#   @disciplina: Transmissão de Dados
#   @Professor: Marcelo Fagundes Caetano
#   Implementação do algoritmo BSD  

from r2a.ir2a import IR2A
from player.parser import *
import time
from statistics import mean
import numpy as np

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

class R2A_BSD(IR2A):
    def __init__(self, id):
        IR2A.__init__(self, id)
        self.throughputs = []
        self.request_time = 0
        self.qualities_indexes = []
        self.selected_index = 7
        self.buffer_increase_time = 0

    def handle_xml_request(self, msg):
        # Salva tempo em que é feito o request
        self.request_time = time.perf_counter()

        # Passa o request para a mensagem camada de baixo
        self.send_down(msg)
    def handle_xml_response(self, msg):
        # Obtem o índice de qualidades
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qualities_indexes = parsed_mpd.get_qi()

        # Calcula a última vazão
        t = time.perf_counter() - self.request_time
        self.throughputs.append(msg.get_bit_length() / t)

        # Envia a mensagem pra próxima camada
        self.send_up(msg)
    def handle_segment_size_request(self, msg):
        # Desenvolvimento
        # print(CYAN+"-----inicio-----"+RESET)
        
        # Salva tempo de pedido para calcular a próxima vazão
        self.request_time = time.perf_counter()

        # Quantidade de vazões utilizadas na média móvel
        n = 15
        
        # Normaliza a quantiade de vazões
        n = min(len(self.throughputs), n)

        # Média móvel das vazões
        last_n_avg = mean(self.throughputs[-n:])

        # Salva último index
        last_index = self.selected_index

        # Reincializa último index
        self.selected_index = 0
        # Seleciona o maior index menor q a última média
        for x in range(len(self.qualities_indexes)):
            if(self.qualities_indexes[x] < last_n_avg):
                self.selected_index = x
        
        # Imprime o índice selecionado pela média móvel
        # print("Índice da média móvel:", self.selected_index)

        # Tamanho do buffer utilizado para calcular a tendência
        buffer_slice_size = 7
        buffer_playback_slice = self.whiteboard.get_playback_buffer_size()
        buffer_slice_size = min(len(buffer_playback_slice), buffer_slice_size)

        # Fatia últimos n elementos com tamanho do buffer
        buffer_slice = []
        buffer_playback_slice = buffer_playback_slice[-buffer_slice_size:]
        for t, buffer_s in buffer_playback_slice:
            buffer_slice.append(buffer_s)

        # Inicializa coeficiente angular
        ang_coef = 0

        # Calcula o coeficiente angular
        if(buffer_slice_size > 3):
            ang_coef, linear_coef = np.polyfit(list(range(len(buffer_slice))), buffer_slice, 1)

        # Constantes
        desired_buffer_size = 25
        minimum_buffer_size = 20
        
        if(len(buffer_slice) > 1):
            # Se o tamanho atual for menor q o desejado, aumenta um pouquinho a qualidade
            buffer_len = buffer_slice[-1]
            if(buffer_slice[-1] > desired_buffer_size):
                self.selected_index = min(19, int(self.selected_index*(buffer_len/desired_buffer_size)**0.5))
            else:
                self.selected_index = int(self.selected_index*(buffer_len/desired_buffer_size)**0.5) 

            # Faz alterações na qualidade de acordo com a tendêcia do buffer
            if(ang_coef < 0):
                self.selected_index = int(self.selected_index*(1+max(-0.5, ang_coef))**0.5)
            elif(ang_coef > 0 and buffer_len > minimum_buffer_size):
                self.selected_index = min(19,int(self.selected_index*(1+min(0.5, ang_coef))**0.5))

        # Limita a quantidade de subidas em um intervalo de tempo
            increase_block_time = 5
            if(self.selected_index > last_index and time.perf_counter() > self.buffer_increase_time + increase_block_time):
                self.buffer_increase_time = time.perf_counter()
                # print(CYAN+"Subiu nessa"+RESET)
            elif(self.selected_index > last_index and time.perf_counter() < self.buffer_increase_time + increase_block_time):
                self.selected_index = last_index
                # print(CYAN+"Não sobe nessa"+RESET)

        # Impressões para desenvolvimento
        # print("Ultimos tamanhos do buffer: ", buffer_slice)
        # print("Inclinação do tamanho do buffer: ", ang_coef)
        # print("new self.selected_index :", self.selected_index)
        # print("Qtd pausas: ", RED+str(len(self.whiteboard.get_playback_pauses()))+RESET)

        # Altera qualidade usada
        selected_qi = self.qualities_indexes[self.selected_index]
        msg.add_quality_id(selected_qi)

        # Envia mensagem pra camada inferior(Connection handler)
        self.send_down(msg)

        # Desenvolvimento
        # print(CYAN+"-----final------"+RESET)
    def handle_segment_size_response(self, msg):
        # Calcula vazão 
        t = time.perf_counter() - self.request_time
        self.throughputs.append(msg.get_bit_length() / t)

        # Repassa mensagem para o player
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass