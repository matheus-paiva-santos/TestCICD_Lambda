import json
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
 

if __name__ == "__main__":

    conn = psycopg2.connect(
        dbname='postgres',
        user='dados_ro',
        password='XiwGtdBY5SjitNdD9gLP',
        host='database-arealogada.clmhxlmjam7w.us-east-1.rds.amazonaws.com',
        port='5432'
    )

    # Query
    query = f"""select u."name" as nome, u.email, u.updated_at as data_atualizacao from users u where u.tipo = 'admin' and u.cliente_id not in(365, 561) and u.email not like '%ita%' 
                union 
                select u."name" as nome, u.email, u.updated_at as data_atualizacao from users u where u.tipo = 'membro' and u.cliente_id not in(365, 561) and u.email not like '%ita%'"""

    df = pd.read_sql(query, conn)
    
    print(df.shape)