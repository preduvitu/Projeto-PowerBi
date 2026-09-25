import enum
from msilib import init_database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from time import sleep
class Catho:
    
    def start(self):
        self.link = 'https://www.catho.com.br'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.vagas = []
        self.indice = 0
        self.driver.get(self.link) 
        with open('stop_words.txt')  as split_stop_words:
            self.stop_words = split_stop_words.read().replace('\n', '').split(',')
            split_stop_words.close()
    
    def split_stop_words(self, description):
        for word in self.stop_words:
            description = description.replace(word, ' ')
        return description
    
    def runVagas(self):
            sleep(5) 
            for i in range(int(self.driver.find_element(By.CSS_SELECTOR, '.glochE').text[-1])):
                try:
                    sleep(1) 
                    for i,card_button in enumerate(self.driver.find_elements(By.CSS_SELECTOR,'.job-description + button')):
                        self.driver.find_elements(By.CSS_SELECTOR,'.job-description + button')[i].click()
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    cards = soup.select('#search-result article')
                    
                    for i, card in enumerate(cards):
                        if i%2 != 0 : continue
                        nome_empresa = card.select('header p')[0].text
                        data = card.select('header time span')[0].text[-5::]+'/2022' 
                        titulo = card.select('header a')[0].text
                        link = card.select('header a')[0].attrs['href']   
                        self.vagas.append([titulo, nome_empresa, data , link])
               
                    for i, card in enumerate(cards):
                        if i%2 == 0 : continue
                        uf = card.select('header a')[1].text.split(' (')[0][-2::]
                        card_description = card.select('.job-description')[0].text
                        salario = card.select('header p + div div')[0].text
                        self.vagas[self.indice].append(self.split_stop_words(self , card_description))
                        self.vagas[self.indice].append(uf)
                        self.vagas[self.indice].append(salario)
                        self.vagas[self.indice].append('Catho')
                        self.vagas[self.indice].append(self.categoria)
                        self.indice+=1
                    sleep(1)
                    self.driver.find_element(By.CSS_SELECTOR, '.PuQfc').click()
                except Exception as err:
                    print(err)
                    continue
            
    def get_vagas(self, categorias):
        self.start(self)
        while len( self.driver.find_elements(By.CSS_SELECTOR, '.widget-policy-button')) < 1:
            sleep(1)
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, '.widget-policy-button').click()
        sleep(2)
        for categoria in categorias:
            self.driver.get(self.link) 
            self.categoria = categoria
            self.driver.find_element(By.CSS_SELECTOR, '#input-0').send_keys(categoria)
            self.driver.find_element(By.CSS_SELECTOR, 'button.searchJob').click()
            self.runVagas(self)
        self.driver.quit()
        return self.vagas

            
            
    