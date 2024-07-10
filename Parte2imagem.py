from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def quantizar(matrizimag_original, nivel):
    # Definir o intervalo de quantização
    quantizacao_step = (valor_max - valor_min) / (nivel - 1) #divisao da amplitude (max-min) pelos niveis que foi escolhido pelo usuario
    # Aplicar a quantização
    array_quantizado = np.round(matrizimag_original / quantizacao_step) * quantizacao_step # Aplica a quantização arrendondando matematicamente inteiros proximos
    return array_quantizado

'''A imagem só é carregada se estiver na pasta do código
   Deve ficar atento ao formato da imagem '''

# Carregar a imagem
im_colorida = Image.open("img3.png")

# Converter para escala de cinza 
img_cinza = im_colorida.convert('L')

# Converter imagem para array
img_array = np.array(img_cinza)

# Encontrar valor máximo e mínimo na imagem
valor_max = np.max(img_array)
valor_min = np.min(img_array)

# Definir o número de níveis desejados para a quantização
nivel = int(input("Digite o número de níveis: "))
qtd_amostras = int(input("Digite o número de amostras da matriz deve ser impressa: "))

# Aplicar a quantização na matriz de imagem
img_quantizada_array = quantizar(img_array, nivel)

# Converter NumPy array de volta para imagem PIL
img_quantizada = Image.fromarray(np.uint8(img_quantizada_array))


# Configurar a figura do matplotlib para exibir as imagens lado a lado
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Plotar a imagem colorida original na primeira sub-figura
axs[0].imshow(im_colorida)
axs[0].set_title('Original')

# Plotar a imagem em escala de cinza na segunda sub-figura
axs[1].imshow(img_cinza, cmap='gray')
axs[1].set_title('Escala de Cinza')

# Plotar a imagem quantizada na terceira sub-figura
axs[2].imshow(img_quantizada_array, cmap='gray')
axs[2].set_title('Quantizada')

# Ajustar layout da figura
plt.tight_layout()

# Exibir a figura 
plt.show()

# Imprimir amostras da imagem quantizada e original
print('amostras da imagem quantizada: ')
print(img_quantizada_array[:qtd_amostras,:qtd_amostras])
print('amostras da imagem original: ')
print(img_array[:qtd_amostras,:qtd_amostras])

matriz_bits = [] # Inicializa uma lista vazia para armazenar os bits

Byte = 8 # Define o tamanho de cada byte (8 bits)

# A etapa tem o objetivo de transformar cada decimal da matriz da imagem em binário.
# Itera sobre as amostras da matriz img_quantizada_array
for i in range(qtd_amostras):
    linha_bits = [] # Inicializa uma lista para os bits de cada linha
    for j in img_quantizada_array[i, :qtd_amostras]:
        bit = [] # Inicializa uma lista para os bits do valor j
        while j > 0:
            resto = j % 2
            bit.append(resto)  # Adiciona o bit ao final da lista
            j = j // 2 
        while len(bit) < 8:
            bit.append(0)  # Preenche com zeros à esquerda se necessário
        bit.reverse() # Inverte a ordem dos bits (para representação correta)
        linha_bits.append(bit) # Adiciona os bits da linha à lista
        matriz_bits.append(bit) # Adiciona os bits à matriz completa


# Convertendo a lista para um array NumPy para melhor visualização
matriz_bits_array = np.array(matriz_bits)
print(matriz_bits_array)
