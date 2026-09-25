import sqlite3
import os
from src.Catho import Catho
from src.Jobbol import Jobbol
from src.Linkedin import Linkedin
from src.DB import DB
from datetime import datetime
from time import sleep
import os
class Main:
    
    def start(self):
        self.sites = [Catho, Jobbol, Linkedin]
        with open('categorias.txt', encoding="utf-8") as categoriaFile:
            self.categorias = (categoriaFile.read()).replace('\n', '').split(',')
            categoriaFile.close()
        self.hora = '13'
        
    def main(self):
        self.start(self)
        try: os.remove("database.db")
        except: pass      
        while True:
            for site in self.sites:
                sleep(5)
                vagas = site.get_vagas(site, self.categorias)
                DB.salvar_vagas(DB, vagas)
                sleep(1)
            sleep( 60 * 1)

Main.main(Main)