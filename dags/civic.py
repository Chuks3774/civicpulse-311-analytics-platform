from datetime import datetime, timedelta

from airflow import DAG
from airflow.sdk import task

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator

from include.transform import transform
from include.upload_raw_data import upload_huge_file

default_args = {
    'owner': 'chuks',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': '@hourly',
    "azure_data_factory_conn_id": "azure_data_factory",
    "factory_name": "civiclogic25",
    "resource_group_name": "civicpulserg24"  
}


@task()
def extract_data_from_api():
  api_response = upload_huge_file()
  return api_response

@task()
def transform_data():
  clean_data = transform()
  return clean_data

with DAG(dag_id='civic_logic', 
         catchup=False, default_args=default_args) as dag: 

  create_db_table = SQLExecuteQueryOperator(
    sql = "sql/civic_table.sql",
    task_id = "create_civic_logic_table",
    conn_id = "postgres_conn"
  )
  
  data_factory = AzureDataFactoryRunPipelineOperator(
    task_id="run_data_factory",
    pipeline_name="civic_logic_factory",
  )


  (
    extract_data_from_api()
    >> transform_data()
    >> create_db_table
    >> data_factory
  )