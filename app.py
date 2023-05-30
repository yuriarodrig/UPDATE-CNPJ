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
