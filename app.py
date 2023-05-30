import pyodbc
import requests
import pandas as pd
import numpy as np
from os import getenv
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)
server = getenv("SERVER")
database = getenv("DATABASE")
username = getenv("USERNAME")
password = getenv("PASSWORD")

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

def Consult_CNPJ(cnpj):
    try:
        site = requests.get(f'https://minhareceita.org/{cnpj}').json()
        cnpj_id = cnpj
        
        simples = site['opcao_pelo_simples']
        simples_nao = site['data_exclusao_do_simples']
        
        if simples:
            simples = 'Sim'
        
        elif simples_nao:
            simples = 'Não'
        
        elif simples == None and simples_nao == None:
            simples = 'Não'
            
        return {'CNPJ':cnpj_id, 'Simples':simples}
    
    except:
        print(f'Erro no cnpj {cnpj}')