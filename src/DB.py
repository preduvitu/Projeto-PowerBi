from dataclasses import replace
import sqlite3
class DB:
    
    def start(self):
        self.database = sqlite3.connect('database.db')
        self.cursor = self.database.cursor()
        try:
            self.cursor.execute('CREATE TABLE tb_vagas (titulo, empresa, data, link, descrição, uf, salario, site, categoria);')
        except:
            pass
    def drop_table(self):
        self.start(self)
        self.cursor.execute('DELETE FROM tb_vagas WHERE 1;')

    def salvar_vagas(self, vagas):
        self.start(self)
        for vaga in vagas:
            query  = ("INSERT INTO tb_vagas VALUES ('{titulo}', '{empresa}', '{data}', '{link}', '{descrição}', '{uf}', '{salario}', '{site}', '{categoria}')"
            .replace('{titulo}', vaga[0].replace("'", ""))
            .replace('{empresa}', vaga[1].replace("'", ""))
            .replace('{data}', vaga[2].replace("'", ""))
            .replace('{link}', vaga[3].replace("'", ""))
            .replace('{descrição}', vaga[4].replace("'", ""))
            .replace('{uf}', vaga[5].replace("'", ""))
            .replace('{salario}', vaga[6].replace("'", ""))
            .replace('{site}', vaga[7].replace("'", ""))
            .replace('{categoria}', vaga[8].replace("'", "")))
            self.cursor.execute(query)
        self.database.commit()
    
    def get_vagas(self):
        self.start(self)
        self.cursor.execute('SELECT * FROM tb_vagas')
        print(self.cursor.fetchall())
        
DB.salvar_vagas(DB, '')