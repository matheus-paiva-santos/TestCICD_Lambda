import psycopg2
import pandas as pd
import boto3
from datetime import datetime
import io

def get_postgres_params():
    return {
        'host': 'database-arealogada.clmhxlmjam7w.us-east-1.rds.amazonaws.com',
        'port': 5432,
        'dbname': 'postgres',
        'user': 'dados_ro',
        'password': 'XiwGtdBY5SjitNdD9gLP'
    }

def get_query():
    return """
        SELECT DISTINCT
            u.cliente_id, tc.razaosocial AS cliente, u.id AS user_id, u.email,
            u.name, u.tipo, u.last_login_at, u.created_at
        FROM users u
        LEFT JOIN temp_clientes_contrato_corp tc ON tc.codigo = u.cliente_id
        ORDER BY tc.razaosocial, u.name
    """

def get_s3_params():
    return {
        'bucket': 'ita-start',
        'base_path': 'portalclientes/clientes',
        'filename': 'clientes.json'
    }

def query_postgres_to_df(conn_params: dict, query: str) -> pd.DataFrame:
    conn = psycopg2.connect(**conn_params)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def save_df_to_s3_partitioned(df: pd.DataFrame, bucket: str, base_path: str, filename: str, file_format='json'):
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    
    key = f"{base_path}/ano={year}/mes={month}/dia={day}/{filename}"
    s3 = boto3.client('s3')

    if file_format == 'json':
        body = df.to_json(orient='records', lines=True)
    elif file_format == 'parquet':
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        body = buffer
    elif file_format == 'excel':
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        body = buffer
    else:
        raise ValueError("Formato de arquivo não suportado")

    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return key

def run_start_layer_pipeline():
    conn_params = get_postgres_params()
    query = get_query()
    s3_config = get_s3_params()

    df = query_postgres_to_df(conn_params, query)
    save_df_to_s3_partitioned(df, **s3_config, file_format='json')
