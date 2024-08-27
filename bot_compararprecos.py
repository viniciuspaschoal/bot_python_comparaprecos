from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
from time import sleep

# Abrir navegador
def abrir_navegador(url):
    navegador = webdriver.Chrome()
    navegador.get(url)
    sleep(2)
    return navegador

# Realiza a busca
def buscar_produto(navegador, preco_max, preco_min, produto):
    try:
        buscar = navegador.find_element(By.XPATH, '//*[@id="cb1-edit"]')
    except Exception as e:
        print(f'Elemento de busca não encontrado: {e}')
        return
    buscar.send_keys(produto)
    buscar.send_keys(Keys.ENTER)
    sleep(2)




    # Encontra os produtos
    pesquisa = []
    itens = navegador.find_elements(By.XPATH, '//div[@class="ui-search-result__wrapper"]')
    

    for item in itens:
        # Capturando o preço e convertendo para número
        try:
            preco = item.find_element(By.XPATH, './/span[@class="andes-money-amount__fraction"]').text
            preco = int(preco.replace('.', ''))  # Remove pontos e converte para inteiro
        except:
            preco = None

        # Se o preço for menor que o preço mínimo ou se o preço não foi encontrado, ignore este item
        if preco is None or preco < preco_min or preco > preco_max:
            continue
                
        # Capturando o link do produto
        try:
            link = item.find_element(By.XPATH, './/a[@class="ui-search-item__group__element ui-search-link__title-card ui-search-link"]').get_attribute('href')
        except:
            link = "Link não encontrado"

        # Capturando o título/especificação do produto
        try:
            titulo = item.find_element(By.TAG_NAME, 'h2').text
        except:
            titulo = 'Título não localizado'

        # Faz uma lista com os dados
        pesquisa.append({'Titulo': titulo, 'Preço': preco, 'Link': link})

        # Se já capturamos 5 produtos, paramos a busca
        if len(pesquisa) == 5:
            break
        

    return pesquisa


# Salva os dados coletados na planilha
def salvar_dados(dados):
    # Formatação da planilha
    with open('lista_de_produtos.csv', mode='w', newline='') as meu_csv:
        cabecalho = ['Titulo', 'Preço', 'Link']
        writer = csv.DictWriter(meu_csv, delimiter=';', fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(dados)
        
        


# Uso das funções de INPUT
input_produto = str(input('Qual produto você procura? Expecifique...   '))
preco_min = int(input('Qual o valor mínimo do produto que deseja? '))
preco_max = int(input('Qual o valor máximo que deseja pagar no produto? '))  # Preço máximo como um número inteiro, sem aspas
print('Iniciando busca...')
sleep(1)
print('Abrindo o Mercado Livre')
sleep(3)

navegador = abrir_navegador("https://www.mercadolivre.com.br/")

dados = buscar_produto(navegador, preco_max, preco_min, input_produto)

if dados:
    salvar_dados(dados)
    
else:
    print("Nenhum dado foi encontrado para salvar.")

navegador.quit()
