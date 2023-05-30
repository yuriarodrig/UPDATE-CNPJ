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
            
        return {'CNPJ':cnpj_id, 'SIMPLES_NACIONAL':simples}
    
    except:
        print(f'Erro no cnpj {cnpj}')
        
def Consult_BD():
    df = pd.read_sql("SELECT CNPJ FROM TABELA_CNPJ WHERE D_E_L_E_T_='' AND TABELA_MSBLQL= '2' ", con=conn)
    df['CNPJ'] = df['CNPJ'].str.strip()
    df = df[df['CNPJ'].str.len() == 14]
    cnpj_list = df['CNPJ'].drop_duplicates().tolist()
    
    result_list = []
    for cnpj in cnpj_list:
        result = Consult_CNPJ(cnpj)
        
        if result:
            result_list.append(result)
            print(result)
    
    df_result = pd.DataFrame(result_list)
    df_result_filtered = df_result.dropna(subset=['SIMPLES_NACIONAL'])
    df_result_filtered = df_result_filtered[df_result_filtered['SIMPLES_NACIONAL'].isin(['Sim', 'Não'])]
    print(df_result_filtered)
    
    for _, row in df_result_filtered.iterrows():
        cnpj = row['CNPJ']
        simples = row['SIMPLES_NACIONAL']
        query = f"UPDATE TABELA SET CAMPO_PREENCHER = '{simples}' WHERE CAMPO_CNPJ = '{cnpj}'"
        cursor.execute(query)
        conn.commit()
Consult_BD()
conn.close()
    