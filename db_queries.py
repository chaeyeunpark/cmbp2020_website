import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer
import decimal

db_instance = boto3.resource('dynamodb')

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def scan_scores(regularized_name):
    table = db_instance.Table('cmbp2020-scores')

    response = table.scan(FilterExpression=Attr('group').contains(regularized_name))
    if response['Count'] > 0:
        res = []
        for item in response['Items']:
            python_data = {k: replace_decimals(v) for k,v in item.items()}
            res.append(python_data)
        return res
    else:
        return None

def verify_input(surname, firstname, studentnumber):
    table = db_instance.Table('cmbp2020-participants')
    response = table.scan(FilterExpression=Attr('firstname').eq(firstname) & Attr('surname').eq(surname) & Attr('studentnumber').eq(studentnumber))
    if response['Count'] == 1:
        return response['Items'][0]['regularized_name']
    else:
        return None
    

