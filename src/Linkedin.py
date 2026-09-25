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

class Linkedin:
    
    def start(self):
        self.link = 'https://www.linkedin.com/jobs/'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
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
                for i in range(0, 5):
                    self.driver.execute_script('window.scrollBy(0,'+ str(700*i) +')')
                    sleep(1)
                if len(self.driver.find_elements(By.CSS_SELECTOR, '.empty-results-pivot__see-all-jobs-cta-link')) > 0:
                    self.driver.find_element(By.CSS_SELECTOR, '.empty-results-pivot__see-all-jobs-cta-link').click()
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                cards = soup.select('.base-card')
                for i, card in enumerate(cards):
                    try:
                        link = card.select('.base-card > a')[0].attrs['href']
                        self.driver.find_elements(By.CSS_SELECTOR, '.base-card')[i].click()
                        sleep(1)
                        self.driver.find_elements(By.CSS_SELECTOR, '.show-more-less-html__button')[0].click() 
                        card = BeautifulSoup(self.driver.page_source, 'html.parser')
                        sleep(1)
                        titulo = card.select('.top-card-layout__entity-info-container a')[0].text.strip()
                        nome_empresa = card.select('.top-card-layout__entity-info-container h4 a')[0].text.strip()
                        descricao = self.split_stop_words(self, card.select('.show-more-less-html__markup')[0].text)
                        data = ''
                        link = self.driver.current_url.replace('\n', '')
                        uf = ''
                        salario = ''
                        self.vagas.append([titulo, nome_empresa, data , link, descricao, uf, salario, 'Linkedin', self.categoria])
                        sleep(1)
                    except Exception as err:
                        print(err)
                        sleep(1)
                        if len(self.driver.find_elements(By.CSS_SELECTOR, '#password')) > 0:
                            self.driver.back()
                        continue
            except:
                return 0
            
    def get_vagas(self, categorias):
        self.start(self)
        while len( self.driver.find_elements(By.CSS_SELECTOR, '#JOBS .dismissable-input__input[type="search"]')) < 1:
            sleep(1)
        sleep(2)
        for categoria in categorias:
            sleep(1)
            self.driver.get(self.link) 
            self.categoria = categoria
            sleep(3)
            self.driver.find_elements(By.CSS_SELECTOR, '#JOBS .dismissable-input__input[type="search"]')[0].send_keys(categoria)
            self.driver.find_elements(By.CSS_SELECTOR, '#JOBS .dismissable-input__input[type="search"]')[0].send_keys(Keys.ENTER)
            self.runVagas(self)
        self.driver.quit()
        return self.vagas

            
            
    