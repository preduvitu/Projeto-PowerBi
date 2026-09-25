import enum
from msilib import init_database
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from time import sleep

class Jobbol:
    
    def start(self):
        self.link = 'https://www.jobbol.com.br'
        options = Options()
        options.add_argument("--window-size=750,1080")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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
            sleep(2) 
            try:
                for i in range(int(self.driver.find_element(By.CSS_SELECTOR, '.PaginationLine').text[-1])):
                    try:
                        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                        cards = soup.select('.loop')
                        for i, card in enumerate(cards):
                            titulo = card.select('.jobtitle')[0].text.replace('\n', '')
                            self.driver.find_elements(By.CSS_SELECTOR, '.loop')[i].click()
                            sleep(2)
                            card = BeautifulSoup(self.driver.page_source, 'html.parser')
                            while len(self.driver.find_elements(By.CSS_SELECTOR, '#IntroTD_L')) < 1:
                                sleep(1)
                            nome_empresa = card.select('.Titletop0001 > span')[0].text.replace('\n', '')
                            data = card.select('.Resumo')[0].text[-12::].replace('.', '').replace('\n', '')
                            link = self.driver.current_url.replace('\n', '')
                            descricao = self.split_stop_words(self, card.select('.content span')[0].text)
                            uf = card.select('#IntroTD_L')[0].text[-3::].replace('\n', '')
                            salario = card.select('.marksingle2')[1].text.replace('\n', '')
                            self.vagas.append([titulo, nome_empresa, data , link, descricao, uf, salario, 'Jobbol', self.categoria])
                            self.driver.back()
                        sleep(1)
                        element = self.driver.find_element(By.CSS_SELECTOR, 'a.next.page-numbers')
                        self.driver.execute_script("arguments[0].click();", element)
                    except Exception as err:
                        print(err)
                        continue
            except:
                return 0
            
    def get_vagas(self, categorias):
        self.start(self)
        while len( self.driver.find_elements(By.CSS_SELECTOR, '#cargo')) < 1:
            sleep(1)
        sleep(2)
        for categoria in categorias:
            sleep(1)
            self.driver.get(self.link) 
            self.categoria = categoria
            sleep(3)
            self.driver.find_elements(By.CSS_SELECTOR, '#cargo')[0].send_keys(categoria)
            self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
            self.runVagas(self)
        self.driver.quit()
        return self.vagas

            
            
    