from pocket import create_account
from utils import logger
import pandas as pd

df = pd.read_excel("accs.xlsx", sheet_name="Planilha1")

for index, row in df.iterrows():
    create_account({"username": row.tolist()[0], "password": row.tolist()[1]})
    logger.info(f"Conta criada: {index}")
