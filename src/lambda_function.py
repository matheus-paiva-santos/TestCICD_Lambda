import json
from utils import run_start_layer_pipeline

def lambda_handler(event, context):
    run_start_layer_pipeline()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Arquivo JSON salvo com sucesso.'
        })
    }