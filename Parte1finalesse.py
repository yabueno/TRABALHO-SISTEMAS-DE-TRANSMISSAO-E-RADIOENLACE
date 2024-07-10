import matplotlib.pyplot as plt
import numpy as np
import math
import random  # Importando a biblioteca random para gerar ruído gaussiano aleatorio

# Função para quantizar o sinal recebe dois parametros o sinal do seno gerado e quantidade de niveis para separar os niveis e alocar para cada valor mais proximo
def quantizar_sinal(sinal_original, Nivel):
    amplitude = np.max(np.abs(sinal_original)) #amplitude é o maximo no sinal senoidal
    quantizacao_step = 2 * amplitude / Nivel
    dados_quantizados_y = np.round(sinal_original / quantizacao_step) * quantizacao_step # Aplica a quantização arrendondando matematicamente inteiros proximos
    return dados_quantizados_y, quantizacao_step  #retorna 


# Função para converter para binário com N bits
def binario_com_zeros(numero, N):
    return format(numero, f'0{N}b') #função que transforma em binario

def awgn(signal, snr_db):
    
    '''Adiciona ruído gaussiano branco aditivo (AWGN) ao sinal.'''
    
    # Calcular a potência do sinal
    signal_power = np.mean(np.abs(signal) ** 2)
    
    # Converter SNR de dB para escala linear
    snr_linear = 10 ** (snr_db / 10)
    
    # Calcular a potência do ruído necessária para a SNR desejada
    PotenciaRuido = signal_power / snr_linear
    
    # Gerar ruído gaussiano com a potência calculada usando random.gauss
    ruido = [random.gauss(0, np.sqrt(PotenciaRuido)) for _ in range(len(signal))]
    
    # Adicionar o ruído ao sinal original
    Ruido_sinal = signal + ruido
    
    return Ruido_sinal



# Entrada de parâmetros pelo o usuário
dBm = int(input("Digite a amplitude em dBm: "))
amplitude = 10 ** (dBm / 10)  # Convertendo dBm para amplitude linear

frequencia = float(input("Digite a frequência (Hz): "))
qtd_periodo = int(input("Digite a Quantidade de Período: "))
ntaxa_amostragem = int(input("Digite a taxa de amostragem (deve ser múltiplo de 2, 3, 4, ...): "))

while ntaxa_amostragem < 2:
    ntaxa_amostragem = int(input("Digite a taxa de amostragem (deve ser múltiplo de 2, 3, 4, ...): ")) #tratamento de erro para ser no minimo a taxa nquist

# Calculando a frequência de amostragem
frequencia_amostragem = frequencia * ntaxa_amostragem

# Gerando o sinal senoidal amostrado
tempo_total = qtd_periodo / frequencia
t = np.linspace(0, tempo_total, int(frequencia_amostragem * tempo_total), endpoint=False)
'''np.linspace(start, stop, num, endpoint=False) é uma função do NumPy que retorna um número especificado de valores igualmente espaçados entre dois limites.
start = 0 é o ponto inicial do vetor de tempo (início do sinal).
stop = tempo_total é o ponto final do vetor de tempo (fim do sinal).
num = int(frequencia_amostragem * tempo_total) é o número total de pontos de amostragem. Calculamos isso multiplicando a frequência de amostragem pelo tempo total. Por exemplo, se a frequência de amostragem é 100 Hz e o tempo total é 5 segundos, teremos 500 pontos de amostragem.'''
sinal_original = amplitude * np.sin(2 * np.pi * frequencia * t) # np.sin(x) é uma função do NumPy que retorna o seno de cada valor de x.
'''2 * np.pi é uma constante que converte a frequência do sinal de ciclos por segundo (Hz) para radianos por segundo. Um ciclo completo (360 graus) corresponde a 2 * np.pi radianos.
frequencia * t multiplica a frequência (em Hz) pelo vetor de tempo (t), resultando em um vetor de valores em radianos.
amplitude * np.sin(...) escala a função seno pela amplitude do sinal, resultando no sinal senoidal desejado.'''

# Quantização do sinal
Nivel = int(input("Digite o número de níveis de quantização: "))
dados_quantizados_y, quantizacao_step = quantizar_sinal(sinal_original, Nivel) #chama a função e retorna os dados quantizados e os passos de quantização

# Codificação dos níveis quantizados em binário. De acordo com o quantidade de bits necessarias cria a lista de bits por niveis
qtdbitsniveis = math.ceil(math.log2(Nivel)) #faz o calculo para achar a qtd de bits dado o Nivel que o usuário deu 
bitsniveisdigitalizados = [binario_com_zeros(int(y / quantizacao_step), qtdbitsniveis) for y in dados_quantizados_y] #Apenas a transformção em binario pelo python retornava alguns '-'no lugar do zero então chama a função para organizar todos os zeros certo
lista_modificada = []
'''Percorre toda a lista de binario com zeros que não deu certo e substitui e devolve ao lugar exato cada bit corrigido com o numero correto de bits'''
# Percorrer a lista original
for binario in bitsniveisdigitalizados:
    # Verificar se há '-' no binário
    if '-' in binario:
        # Substituir '-' por '0' e adicionar à lista modificada
        binario_modificado = binario.replace('-', '0')
        lista_modificada.append(binario_modificado)
    else:
        # Se não houver '-', adicionar o binário original à lista modificada
        lista_modificada.append(binario)



# Codificação em linha polar RZ
''' Utiliza a lista binaria anterior para fazer a codificação polar RZ acrescentando os bits de tamanho especifico com o extend
Usa o extend para estender encoded_signal adicionando cada elemento da lista passada como argumento.
Adiciona uma sequência de 1s com o comprimento calculado ao final de encoded_signal'''
encoded_signal = []
for valor_binario in lista_modificada:
    for bit in valor_binario:
        if bit == '1':
            encoded_signal.extend([1] * int(frequencia_amostragem / (2 * frequencia)))  # '1' é "alta" durante meio período
            encoded_signal.extend([0] * int(frequencia_amostragem / (2 * frequencia)))  # Seguido de "baixa" durante o outro meio período
        elif bit == '0':
            encoded_signal.extend([0] * int(frequencia_amostragem / frequencia))  # '0' é "baixa" durante todo o período
        else:
            encoded_signal.extend([0] * int(frequencia_amostragem / frequencia))  # Tratamento para '-')

# Calcular a transformada de Fourier
'''np.fft.fft(x) é uma função do NumPy que calcula a Transformada Rápida de Fourier (FFT) do vetor x.
A FFT transforma um sinal no domínio do tempo para o domínio da frequência, representando a amplitude das diferentes componentes de frequência que compõem o sinal.'''

fft_seno = np.fft.fft(sinal_original)
fft_codificado = np.fft.fft(encoded_signal)

# Frequências associadas
frequencias_seno = np.fft.fftfreq(len(fft_seno), 1 / frequencia_amostragem)
frequencias_codificado = np.fft.fftfreq(len(fft_codificado), 1 / frequencia_amostragem)

# Adicionar ruído gaussiano ao sinal codificado
snr_db = float(input("Digite a relação sinal-ruído (SNR) em dB: "))
encoded_signal_com_ruido = awgn(np.array(encoded_signal), snr_db)

# Calcular a transformada de Fourier do sinal com ruído
fft_codificado_com_ruido = np.fft.fft(encoded_signal_com_ruido)

# Plotagem dos resultados
plt.figure(figsize=(14, 10))

#cria um subplot com 4 linhas, 2 colunas e ocupa a primeira posição (índice 1) na matriz de subplots. 
#Isso significa que haverá 4 linhas de subplots e 2 colunas, e o gráfico atual será o primeiro da esquerda para a direita e de cima para baixo.
plt.subplot(4, 2, 1)

# Está plotando o sinal original no gráfico. 
# O eixo x é representado pelo array t e o eixo y pelo array sinal_original. 
# O rótulo ‘Sinal Original’ é usado para a legenda do gráfico.
plt.plot(t, sinal_original, label='Sinal Original')

# Definição dos eixos X e Y
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')

# Definição do Titulo do Grafico
plt.title('Sinal Senoidal Original')

# Adiciona grade ao grafico
plt.grid(True)

# Mostra a legenda no gráfico, usando o rótulo definido 
plt.legend()

#cria um subplot na posição (4, 2, 2) da matriz de subplots. 
#Assim como o anterior, ele faz parte de uma grade de 4 linhas e 2 colunas. 
#O gráfico atual será o segundo da esquerda para a direita e de cima para baixo.
plt.subplot(4, 2, 2)

# Plotando o espectro de frequência (FFT) do sinal senoidal. 
# frequencias_seno, é o eixo x do gráfico, representando as frequências. 
# np.abs(fft_seno) calcula o valor absoluto da Transformada Rápida de Fourier (FFT) do sinal senoidal.
plt.plot(frequencias_seno, np.abs(fft_seno))

# Definição do Titulo do Grafico
plt.title('Espectro do Sinal Senoidal Original')

# Definição dos eixos X e Y
plt.xlabel('Frequência [Hz]')
plt.ylabel('Magnitude')

# cria um subplot em uma matriz de 4 linhas por 2 colunas e seleciona o terceiro subplot
# contando da esquerda para a direita e de cima para baixo). 
# Isso significa que você terá 8 subplots no total, e o terceiro será o ativo nesse momento.
plt.subplot(4, 2, 3)

# O código está criando um gráfico de passos para o sinal quantizado. 
# t é o eixo x do gráfico, representando os valores de tempo.
# dados_quantizados_y usa os valores do sinal quantizado para o eixo y.
# where='mid' define onde os passos devem ser posicionados. No caso, eles ocorrem exatamente no meio entre as posições x.
# label='Sinal Quantizado' define o rótulo para a legenda do gráfico.
plt.step(t, dados_quantizados_y, where='mid', label='Sinal Quantizado')

# Definição dos eixos X e Y
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')

# Definição do Titulo do Grafico
plt.title('Sinal Quantizado')

# Adiciona grade ao grafico
plt.grid(True)

# Mostra a legenda no gráfico, usando o rótulo definido
plt.legend()

# cria um subplot em uma matriz de 4 linhas por 2 colunas e seleciona o quarto subplot 
# contando da esquerda para a direita e de cima para baixo.
# Isso significa que você terá 8 subplots no total, e o quarto será o ativo nesse momento.
plt.subplot(4, 2, 4)

# plota a magnitude da transformada de Fourier em relação às frequências. 
# A função cria um gráfico de linha com os valores de frequencias_codificado no eixo x e np.abs(fft_codificado) no eixo y. 
# A magnitude é calculada usando np.abs(), que retorna o valor absoluto dos elementos da transformada.
plt.plot(frequencias_codificado, np.abs(fft_codificado))

# Definição do Titulo do Grafico
plt.title('Espectro do Sinal Codificado')

# Definição dos eixos X e Y
plt.xlabel('Frequência [Hz]')
plt.ylabel('Magnitude')

# cria uma subplot na quinta posição. 
# Isso significa que o gráfico total terá 4 linhas e 2 colunas de subplots, 
# e a quinta posição, contando da esquerda para a direita e de cima para baixo, será ocupada pela subplot criada por essa função. 
plt.subplot(4, 2, 5)

# Esta usando a função np.linspace do NumPy para criar um array de valores igualmente espaçados entre 0 e tempo_total.
# O número de valores gerados é igual ao comprimento do array encoded_signal. 
# Isso cria uma sequência de pontos no eixo do tempo para o gráfico
t_encoded = np.linspace(0, tempo_total, len(encoded_signal))

#Cria um gráfico de passos com base nos valores de t_encoded (eixo x) e encoded_signal (eixo y).
# O gráfico resultante terá passos conectando os pontos correspondentes nos eixos x e y.
plt.step(t_encoded, encoded_signal)

# Definição dos eixos X e Y
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')

# Definição do Titulo do Grafico
plt.title('Sinal Codificado Polar RZ')

# Adiciona grade ao grafico
plt.grid(True)

# Essa linha de código cria uma subplot na sexta posição de uma matriz 4x2. 
# No gráfico total, haverá 4 linhas e 2 colunas de subplots, e a sexta posição 
# contando da esquerda para a direita e de cima para baixo será ocupada por esse subplot
plt.subplot(4, 2, 6)

# linha de código está usando a função np.linspace do NumPy para criar um array de valores igualmente espaçados entre 0 e tempo_total. 
# O número de valores gerados é igual ao comprimento do array encoded_signal_com_ruido. 
# Isso cria uma sequência de pontos no eixo do tempo para o gráfico
t_encoded_ruido = np.linspace(0, tempo_total, len(encoded_signal_com_ruido))

# cria um gráfico com o tempo no eixo x e os valores do sinal com ruído no eixo y.
# A legenda “Sinal com Ruído” é exibida na legenda do gráfico
plt.plot(t_encoded_ruido, encoded_signal_com_ruido, label='Sinal com Ruído')

# Definição dos eixos X e Y
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')

# Definição do Titulo do Grafico
plt.title('Sinal Codificado com Ruído Gaussiano')

# Adiciona grade ao grafico
plt.grid(True)

# Adiciona legenda ao grafico
plt.legend()


# está criando um subplot (um gráfico dentro de um conjunto de gráficos) na sétima posição de uma matriz 4x2. 
# A matriz de subplots é organizada em 4 linhas e 2 colunas, e o subplot atual ocupa a sétima posição. 
# Cada posição na matriz é numerada sequencialmente de cima para baixo e da esquerda para a direita
plt.subplot(4, 2, 7)

# Esse trecho de código cria uma série de gráficos, cada um representando uma janela de tamanho largura_olho do sinal com ruído. 
# O eixo x é o tempo (t[:largura_olho]), e o eixo y é o valor do sinal com ruído (encoded_signal_com_ruido[i:i + largura_olho]). 
largura_olho = int((frequencia_amostragem / frequencia)+1)
for i in range(0, len(encoded_signal_com_ruido) - largura_olho, largura_olho // 2):
    end_index = max(i + largura_olho, len(encoded_signal_com_ruido))  # Garantir que não exceda o tamanho do sinal
    plt.plot(t[:largura_olho], encoded_signal_com_ruido[i:i + largura_olho], color='blue')

# Definição do Titulo do Grafico
plt.title('Diagrama de Olho da Codificação com Ruido')

# Definição dos eixos X e Y
plt.ylabel('Amplitude')
plt.xlabel('Tempo (s)')


# Adiciona grade ao grafico
plt.grid(True)

# Está criando um subplot na oitava posição de uma matriz 4x2.
# Essa matriz de subplots é organizada em 4 linhas e 2 colunas, e o subplot atual ocupa a oitava posição. 
# Cada posição na matriz é numerada sequencialmente de cima para baixo e da esquerda para a direita.
plt.subplot(4, 2, 8)

# Esse trecho de código cria uma série de gráficos, cada um representando uma janela de tamanho largura_olho do sinal sem ruído. 
# O eixo x é o tempo (t[:largura_olho]), e o eixo y é o valor do sinal sem ruido (encoded_signal[i:i + largura_olho]).
largura_olho = int((frequencia_amostragem / frequencia)+1)
for i in range(0, len(encoded_signal) - largura_olho, largura_olho // 2):
    end_index = max(i + largura_olho, len(encoded_signal))  # Garantir que não exceda o tamanho do sinal
    plt.plot(t[:largura_olho], encoded_signal[i:i + largura_olho], color='blue')

# Definição do Titulo do Grafico
plt.title('Diagrama de Olho da Codificação')

# Definição dos eixos X e Y
plt.ylabel('Amplitude')
plt.xlabel('Tempo (s)')

# Adiciona grade ao grafico
plt.grid(True)


# utilizada para ajustar automaticamente os subplots ou eixos dentro de uma figura, de modo que eles se encaixem bem sem sobreposição.
plt.tight_layout()

# Mostra todos os graficos
plt.show()

# Saída dos Bits Digitalizados
print("Os bits digitalizados são:")
print(lista_modificada)
#print(encoded_signal)




