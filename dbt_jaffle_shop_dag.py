# DAG CREATED BY PYTHON SCRIPT -> 2022-12-26 23:02:23.389695
from datetime import datetime
import logging
import sys
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator
    
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
tag_list = ["DBT", "jaffle-shop"]
default_args = {
    'start_date': datetime(2021, 1, 1),
    'owner': 'Admin'
}
DOCKER_IMAGE = "dbt-jaffle-shop:latest"
GLOBAL_CLI_FLAGS = "--no-write-json --no-use-colors" #prevents DBT from writing a new manifest.json file and remove colors from logs

def run_dbt_task(subtask_id="", model_path="", is_test=False, **kwargs):
    if kwargs.get('dag_run').conf:
        DBT_TARGET = kwargs.get('dag_run').conf.get("DBT_TARGET", "dev")
        FULL_REFRESH = kwargs.get('dag_run').conf.get("FULL_REFRESH", False)
    else:
        DBT_TARGET = "dev"
        FULL_REFRESH = False
    print(f"DBT_TARGET -> {DBT_TARGET}\nFULL_REFRESH -> {FULL_REFRESH}")
    dbt_command = "run"
    if is_test:
        dbt_command = "test"
    elif FULL_REFRESH:
        dbt_command = "run --full-refresh"
    dbt_task = DockerOperator(
            task_id=subtask_id,
            image=DOCKER_IMAGE,
            api_version='auto',
            auto_remove=True,
            command=f"dbt {GLOBAL_CLI_FLAGS} {dbt_command} --profiles-dir profile --target {DBT_TARGET} --models {model_path}",
            docker_url="unix://var/run/docker.sock",
            network_mode="bridge",
            tty=True
        )
    dbt_task.execute(dict())
    
with DAG('DBT-jaffle-shop', schedule_interval='@daily', default_args=default_args, tags=tag_list, catchup=False) as dag:

    quickstart_schema_stg_employee = PythonOperator(
        task_id="quickstart_schema.stg_employee",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_employee", "model_path": "core.stg_employee", "is_test": False}
    )

    quickstart_schema_stg_employee_append = PythonOperator(
        task_id="quickstart_schema.stg_employee_append",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_employee_append", "model_path": "core.stg_employee_append", "is_test": False}
    )

    quickstart_schema_my_first_dbt_model = PythonOperator(
        task_id="quickstart_schema.my_first_dbt_model",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.my_first_dbt_model", "model_path": "example.my_first_dbt_model", "is_test": False}
    )

    test_quickstart_schema_my_first_dbt_model = PythonOperator(
        task_id="test.quickstart_schema.my_first_dbt_model",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.my_first_dbt_model", "model_path": "example.my_first_dbt_model", "is_test": True}
    )

    quickstart_schema_my_second_dbt_model = PythonOperator(
        task_id="quickstart_schema.my_second_dbt_model",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.my_second_dbt_model", "model_path": "example.my_second_dbt_model", "is_test": False}
    )

    test_quickstart_schema_my_second_dbt_model = PythonOperator(
        task_id="test.quickstart_schema.my_second_dbt_model",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.my_second_dbt_model", "model_path": "example.my_second_dbt_model", "is_test": True}
    )

    quickstart_schema_dim_dbt__current_models = PythonOperator(
        task_id="quickstart_schema.dim_dbt__current_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__current_models", "model_path": "dim_dbt__current_models", "is_test": False}
    )

    quickstart_schema_dim_dbt__exposures = PythonOperator(
        task_id="quickstart_schema.dim_dbt__exposures",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__exposures", "model_path": "dim_dbt__exposures", "is_test": False}
    )

    quickstart_schema_dim_dbt__models = PythonOperator(
        task_id="quickstart_schema.dim_dbt__models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__models", "model_path": "dim_dbt__models", "is_test": False}
    )

    quickstart_schema_dim_dbt__seeds = PythonOperator(
        task_id="quickstart_schema.dim_dbt__seeds",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__seeds", "model_path": "dim_dbt__seeds", "is_test": False}
    )

    quickstart_schema_dim_dbt__snapshots = PythonOperator(
        task_id="quickstart_schema.dim_dbt__snapshots",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__snapshots", "model_path": "dim_dbt__snapshots", "is_test": False}
    )

    quickstart_schema_dim_dbt__sources = PythonOperator(
        task_id="quickstart_schema.dim_dbt__sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__sources", "model_path": "dim_dbt__sources", "is_test": False}
    )

    quickstart_schema_dim_dbt__tests = PythonOperator(
        task_id="quickstart_schema.dim_dbt__tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.dim_dbt__tests", "model_path": "dim_dbt__tests", "is_test": False}
    )

    quickstart_schema_fct_dbt__invocations = PythonOperator(
        task_id="quickstart_schema.fct_dbt__invocations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_dbt__invocations", "model_path": "fct_dbt__invocations", "is_test": False}
    )

    quickstart_schema_fct_dbt__model_executions = PythonOperator(
        task_id="quickstart_schema.fct_dbt__model_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_dbt__model_executions", "model_path": "fct_dbt__model_executions", "is_test": False}
    )

    quickstart_schema_fct_dbt__seed_executions = PythonOperator(
        task_id="quickstart_schema.fct_dbt__seed_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_dbt__seed_executions", "model_path": "fct_dbt__seed_executions", "is_test": False}
    )

    quickstart_schema_fct_dbt__snapshot_executions = PythonOperator(
        task_id="quickstart_schema.fct_dbt__snapshot_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_dbt__snapshot_executions", "model_path": "fct_dbt__snapshot_executions", "is_test": False}
    )

    quickstart_schema_fct_dbt__test_executions = PythonOperator(
        task_id="quickstart_schema.fct_dbt__test_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_dbt__test_executions", "model_path": "fct_dbt__test_executions", "is_test": False}
    )

    quickstart_schema_exposures = PythonOperator(
        task_id="quickstart_schema.exposures",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.exposures", "model_path": "sources.exposures", "is_test": False}
    )

    quickstart_schema_invocations = PythonOperator(
        task_id="quickstart_schema.invocations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.invocations", "model_path": "sources.invocations", "is_test": False}
    )

    quickstart_schema_models = PythonOperator(
        task_id="quickstart_schema.models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.models", "model_path": "sources.models", "is_test": False}
    )

    quickstart_schema_model_executions = PythonOperator(
        task_id="quickstart_schema.model_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.model_executions", "model_path": "sources.model_executions", "is_test": False}
    )

    quickstart_schema_seeds = PythonOperator(
        task_id="quickstart_schema.seeds",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.seeds", "model_path": "sources.seeds", "is_test": False}
    )

    quickstart_schema_seed_executions = PythonOperator(
        task_id="quickstart_schema.seed_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.seed_executions", "model_path": "sources.seed_executions", "is_test": False}
    )

    quickstart_schema_snapshots = PythonOperator(
        task_id="quickstart_schema.snapshots",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.snapshots", "model_path": "sources.snapshots", "is_test": False}
    )

    quickstart_schema_snapshot_executions = PythonOperator(
        task_id="quickstart_schema.snapshot_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.snapshot_executions", "model_path": "sources.snapshot_executions", "is_test": False}
    )

    quickstart_schema_sources = PythonOperator(
        task_id="quickstart_schema.sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.sources", "model_path": "sources.sources", "is_test": False}
    )

    quickstart_schema_tests = PythonOperator(
        task_id="quickstart_schema.tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.tests", "model_path": "sources.tests", "is_test": False}
    )

    test_quickstart_schema_tests = PythonOperator(
        task_id="test.quickstart_schema.tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.tests", "model_path": "sources.tests", "is_test": True}
    )

    quickstart_schema_test_executions = PythonOperator(
        task_id="quickstart_schema.test_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.test_executions", "model_path": "sources.test_executions", "is_test": False}
    )

    test_quickstart_schema_test_executions = PythonOperator(
        task_id="test.quickstart_schema.test_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.test_executions", "model_path": "sources.test_executions", "is_test": True}
    )

    quickstart_schema_stg_dbt__exposures = PythonOperator(
        task_id="quickstart_schema.stg_dbt__exposures",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__exposures", "model_path": "staging.stg_dbt__exposures", "is_test": False}
    )

    quickstart_schema_stg_dbt__invocations = PythonOperator(
        task_id="quickstart_schema.stg_dbt__invocations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__invocations", "model_path": "staging.stg_dbt__invocations", "is_test": False}
    )

    quickstart_schema_stg_dbt__models = PythonOperator(
        task_id="quickstart_schema.stg_dbt__models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__models", "model_path": "staging.stg_dbt__models", "is_test": False}
    )

    quickstart_schema_stg_dbt__model_executions = PythonOperator(
        task_id="quickstart_schema.stg_dbt__model_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__model_executions", "model_path": "staging.stg_dbt__model_executions", "is_test": False}
    )

    quickstart_schema_stg_dbt__seeds = PythonOperator(
        task_id="quickstart_schema.stg_dbt__seeds",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__seeds", "model_path": "staging.stg_dbt__seeds", "is_test": False}
    )

    quickstart_schema_stg_dbt__seed_executions = PythonOperator(
        task_id="quickstart_schema.stg_dbt__seed_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__seed_executions", "model_path": "staging.stg_dbt__seed_executions", "is_test": False}
    )

    quickstart_schema_stg_dbt__snapshots = PythonOperator(
        task_id="quickstart_schema.stg_dbt__snapshots",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__snapshots", "model_path": "staging.stg_dbt__snapshots", "is_test": False}
    )

    quickstart_schema_stg_dbt__snapshot_executions = PythonOperator(
        task_id="quickstart_schema.stg_dbt__snapshot_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__snapshot_executions", "model_path": "staging.stg_dbt__snapshot_executions", "is_test": False}
    )

    quickstart_schema_stg_dbt__sources = PythonOperator(
        task_id="quickstart_schema.stg_dbt__sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__sources", "model_path": "staging.stg_dbt__sources", "is_test": False}
    )

    quickstart_schema_stg_dbt__tests = PythonOperator(
        task_id="quickstart_schema.stg_dbt__tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__tests", "model_path": "staging.stg_dbt__tests", "is_test": False}
    )

    test_quickstart_schema_stg_dbt__tests = PythonOperator(
        task_id="test.quickstart_schema.stg_dbt__tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.stg_dbt__tests", "model_path": "staging.stg_dbt__tests", "is_test": True}
    )

    quickstart_schema_stg_dbt__test_executions = PythonOperator(
        task_id="quickstart_schema.stg_dbt__test_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_dbt__test_executions", "model_path": "staging.stg_dbt__test_executions", "is_test": False}
    )

    test_quickstart_schema_stg_dbt__test_executions = PythonOperator(
        task_id="test.quickstart_schema.stg_dbt__test_executions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.stg_dbt__test_executions", "model_path": "staging.stg_dbt__test_executions", "is_test": True}
    )

    quickstart_schema_int_all_dag_relationships = PythonOperator(
        task_id="quickstart_schema.int_all_dag_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.int_all_dag_relationships", "model_path": "marts.core.int_all_dag_relationships", "is_test": False}
    )

    quickstart_schema_int_all_graph_resources = PythonOperator(
        task_id="quickstart_schema.int_all_graph_resources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.int_all_graph_resources", "model_path": "marts.core.int_all_graph_resources", "is_test": False}
    )

    test_quickstart_schema_int_all_graph_resources = PythonOperator(
        task_id="test.quickstart_schema.int_all_graph_resources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.int_all_graph_resources", "model_path": "marts.core.int_all_graph_resources", "is_test": True}
    )

    quickstart_schema_int_direct_relationships = PythonOperator(
        task_id="quickstart_schema.int_direct_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.int_direct_relationships", "model_path": "marts.core.int_direct_relationships", "is_test": False}
    )

    test_quickstart_schema_int_direct_relationships = PythonOperator(
        task_id="test.quickstart_schema.int_direct_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.int_direct_relationships", "model_path": "marts.core.int_direct_relationships", "is_test": True}
    )

    quickstart_schema_fct_direct_join_to_source = PythonOperator(
        task_id="quickstart_schema.fct_direct_join_to_source",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_direct_join_to_source", "model_path": "marts.dag.fct_direct_join_to_source", "is_test": False}
    )

    test_quickstart_schema_fct_direct_join_to_source = PythonOperator(
        task_id="test.quickstart_schema.fct_direct_join_to_source",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_direct_join_to_source", "model_path": "marts.dag.fct_direct_join_to_source", "is_test": True}
    )

    quickstart_schema_fct_marts_or_intermediate_dependent_on_source = PythonOperator(
        task_id="quickstart_schema.fct_marts_or_intermediate_dependent_on_source",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_marts_or_intermediate_dependent_on_source", "model_path": "marts.dag.fct_marts_or_intermediate_dependent_on_source", "is_test": False}
    )

    test_quickstart_schema_fct_marts_or_intermediate_dependent_on_source = PythonOperator(
        task_id="test.quickstart_schema.fct_marts_or_intermediate_dependent_on_source",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_marts_or_intermediate_dependent_on_source", "model_path": "marts.dag.fct_marts_or_intermediate_dependent_on_source", "is_test": True}
    )

    quickstart_schema_fct_model_fanout = PythonOperator(
        task_id="quickstart_schema.fct_model_fanout",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_model_fanout", "model_path": "marts.dag.fct_model_fanout", "is_test": False}
    )

    test_quickstart_schema_fct_model_fanout = PythonOperator(
        task_id="test.quickstart_schema.fct_model_fanout",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_model_fanout", "model_path": "marts.dag.fct_model_fanout", "is_test": True}
    )

    quickstart_schema_fct_multiple_sources_joined = PythonOperator(
        task_id="quickstart_schema.fct_multiple_sources_joined",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_multiple_sources_joined", "model_path": "marts.dag.fct_multiple_sources_joined", "is_test": False}
    )

    test_quickstart_schema_fct_multiple_sources_joined = PythonOperator(
        task_id="test.quickstart_schema.fct_multiple_sources_joined",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_multiple_sources_joined", "model_path": "marts.dag.fct_multiple_sources_joined", "is_test": True}
    )

    quickstart_schema_fct_rejoining_of_upstream_concepts = PythonOperator(
        task_id="quickstart_schema.fct_rejoining_of_upstream_concepts",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_rejoining_of_upstream_concepts", "model_path": "marts.dag.fct_rejoining_of_upstream_concepts", "is_test": False}
    )

    test_quickstart_schema_fct_rejoining_of_upstream_concepts = PythonOperator(
        task_id="test.quickstart_schema.fct_rejoining_of_upstream_concepts",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_rejoining_of_upstream_concepts", "model_path": "marts.dag.fct_rejoining_of_upstream_concepts", "is_test": True}
    )

    quickstart_schema_fct_root_models = PythonOperator(
        task_id="quickstart_schema.fct_root_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_root_models", "model_path": "marts.dag.fct_root_models", "is_test": False}
    )

    test_quickstart_schema_fct_root_models = PythonOperator(
        task_id="test.quickstart_schema.fct_root_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_root_models", "model_path": "marts.dag.fct_root_models", "is_test": True}
    )

    quickstart_schema_fct_source_fanout = PythonOperator(
        task_id="quickstart_schema.fct_source_fanout",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_source_fanout", "model_path": "marts.dag.fct_source_fanout", "is_test": False}
    )

    test_quickstart_schema_fct_source_fanout = PythonOperator(
        task_id="test.quickstart_schema.fct_source_fanout",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_source_fanout", "model_path": "marts.dag.fct_source_fanout", "is_test": True}
    )

    quickstart_schema_fct_staging_dependent_on_marts_or_intermediate = PythonOperator(
        task_id="quickstart_schema.fct_staging_dependent_on_marts_or_intermediate",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_staging_dependent_on_marts_or_intermediate", "model_path": "marts.dag.fct_staging_dependent_on_marts_or_intermediate", "is_test": False}
    )

    test_quickstart_schema_fct_staging_dependent_on_marts_or_intermediate = PythonOperator(
        task_id="test.quickstart_schema.fct_staging_dependent_on_marts_or_intermediate",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_staging_dependent_on_marts_or_intermediate", "model_path": "marts.dag.fct_staging_dependent_on_marts_or_intermediate", "is_test": True}
    )

    quickstart_schema_fct_staging_dependent_on_staging = PythonOperator(
        task_id="quickstart_schema.fct_staging_dependent_on_staging",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_staging_dependent_on_staging", "model_path": "marts.dag.fct_staging_dependent_on_staging", "is_test": False}
    )

    test_quickstart_schema_fct_staging_dependent_on_staging = PythonOperator(
        task_id="test.quickstart_schema.fct_staging_dependent_on_staging",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_staging_dependent_on_staging", "model_path": "marts.dag.fct_staging_dependent_on_staging", "is_test": True}
    )

    quickstart_schema_fct_unused_sources = PythonOperator(
        task_id="quickstart_schema.fct_unused_sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_unused_sources", "model_path": "marts.dag.fct_unused_sources", "is_test": False}
    )

    test_quickstart_schema_fct_unused_sources = PythonOperator(
        task_id="test.quickstart_schema.fct_unused_sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_unused_sources", "model_path": "marts.dag.fct_unused_sources", "is_test": True}
    )

    quickstart_schema_fct_documentation_coverage = PythonOperator(
        task_id="quickstart_schema.fct_documentation_coverage",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_documentation_coverage", "model_path": "marts.documentation.fct_documentation_coverage", "is_test": False}
    )

    test_quickstart_schema_fct_documentation_coverage = PythonOperator(
        task_id="test.quickstart_schema.fct_documentation_coverage",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_documentation_coverage", "model_path": "marts.documentation.fct_documentation_coverage", "is_test": True}
    )

    quickstart_schema_fct_undocumented_models = PythonOperator(
        task_id="quickstart_schema.fct_undocumented_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_undocumented_models", "model_path": "marts.documentation.fct_undocumented_models", "is_test": False}
    )

    test_quickstart_schema_fct_undocumented_models = PythonOperator(
        task_id="test.quickstart_schema.fct_undocumented_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_undocumented_models", "model_path": "marts.documentation.fct_undocumented_models", "is_test": True}
    )

    quickstart_schema_fct_chained_views_dependencies = PythonOperator(
        task_id="quickstart_schema.fct_chained_views_dependencies",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_chained_views_dependencies", "model_path": "marts.performance.fct_chained_views_dependencies", "is_test": False}
    )

    test_quickstart_schema_fct_chained_views_dependencies = PythonOperator(
        task_id="test.quickstart_schema.fct_chained_views_dependencies",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_chained_views_dependencies", "model_path": "marts.performance.fct_chained_views_dependencies", "is_test": True}
    )

    quickstart_schema_fct_exposure_parents_materializations = PythonOperator(
        task_id="quickstart_schema.fct_exposure_parents_materializations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_exposure_parents_materializations", "model_path": "marts.performance.fct_exposure_parents_materializations", "is_test": False}
    )

    test_quickstart_schema_fct_exposure_parents_materializations = PythonOperator(
        task_id="test.quickstart_schema.fct_exposure_parents_materializations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_exposure_parents_materializations", "model_path": "marts.performance.fct_exposure_parents_materializations", "is_test": True}
    )

    quickstart_schema_fct_model_directories = PythonOperator(
        task_id="quickstart_schema.fct_model_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_model_directories", "model_path": "marts.structure.fct_model_directories", "is_test": False}
    )

    test_quickstart_schema_fct_model_directories = PythonOperator(
        task_id="test.quickstart_schema.fct_model_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_model_directories", "model_path": "marts.structure.fct_model_directories", "is_test": True}
    )

    quickstart_schema_fct_model_naming_conventions = PythonOperator(
        task_id="quickstart_schema.fct_model_naming_conventions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_model_naming_conventions", "model_path": "marts.structure.fct_model_naming_conventions", "is_test": False}
    )

    test_quickstart_schema_fct_model_naming_conventions = PythonOperator(
        task_id="test.quickstart_schema.fct_model_naming_conventions",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_model_naming_conventions", "model_path": "marts.structure.fct_model_naming_conventions", "is_test": True}
    )

    quickstart_schema_fct_source_directories = PythonOperator(
        task_id="quickstart_schema.fct_source_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_source_directories", "model_path": "marts.structure.fct_source_directories", "is_test": False}
    )

    test_quickstart_schema_fct_source_directories = PythonOperator(
        task_id="test.quickstart_schema.fct_source_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_source_directories", "model_path": "marts.structure.fct_source_directories", "is_test": True}
    )

    quickstart_schema_fct_test_directories = PythonOperator(
        task_id="quickstart_schema.fct_test_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_test_directories", "model_path": "marts.structure.fct_test_directories", "is_test": False}
    )

    test_quickstart_schema_fct_test_directories = PythonOperator(
        task_id="test.quickstart_schema.fct_test_directories",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_test_directories", "model_path": "marts.structure.fct_test_directories", "is_test": True}
    )

    quickstart_schema_fct_missing_primary_key_tests = PythonOperator(
        task_id="quickstart_schema.fct_missing_primary_key_tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_missing_primary_key_tests", "model_path": "marts.tests.fct_missing_primary_key_tests", "is_test": False}
    )

    test_quickstart_schema_fct_missing_primary_key_tests = PythonOperator(
        task_id="test.quickstart_schema.fct_missing_primary_key_tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_missing_primary_key_tests", "model_path": "marts.tests.fct_missing_primary_key_tests", "is_test": True}
    )

    quickstart_schema_fct_test_coverage = PythonOperator(
        task_id="quickstart_schema.fct_test_coverage",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.fct_test_coverage", "model_path": "marts.tests.fct_test_coverage", "is_test": False}
    )

    test_quickstart_schema_fct_test_coverage = PythonOperator(
        task_id="test.quickstart_schema.fct_test_coverage",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.fct_test_coverage", "model_path": "marts.tests.fct_test_coverage", "is_test": True}
    )

    quickstart_schema_int_model_test_summary = PythonOperator(
        task_id="quickstart_schema.int_model_test_summary",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.int_model_test_summary", "model_path": "marts.tests.intermediate.int_model_test_summary", "is_test": False}
    )

    test_quickstart_schema_int_model_test_summary = PythonOperator(
        task_id="test.quickstart_schema.int_model_test_summary",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema.int_model_test_summary", "model_path": "marts.tests.intermediate.int_model_test_summary", "is_test": True}
    )

    quickstart_schema_stg_exposures = PythonOperator(
        task_id="quickstart_schema.stg_exposures",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_exposures", "model_path": "staging.graph.stg_exposures", "is_test": False}
    )

    quickstart_schema_stg_exposure_relationships = PythonOperator(
        task_id="quickstart_schema.stg_exposure_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_exposure_relationships", "model_path": "staging.graph.stg_exposure_relationships", "is_test": False}
    )

    quickstart_schema_stg_metrics = PythonOperator(
        task_id="quickstart_schema.stg_metrics",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_metrics", "model_path": "staging.graph.stg_metrics", "is_test": False}
    )

    quickstart_schema_stg_metric_relationships = PythonOperator(
        task_id="quickstart_schema.stg_metric_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_metric_relationships", "model_path": "staging.graph.stg_metric_relationships", "is_test": False}
    )

    quickstart_schema_stg_nodes = PythonOperator(
        task_id="quickstart_schema.stg_nodes",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_nodes", "model_path": "staging.graph.stg_nodes", "is_test": False}
    )

    quickstart_schema_stg_node_relationships = PythonOperator(
        task_id="quickstart_schema.stg_node_relationships",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_node_relationships", "model_path": "staging.graph.stg_node_relationships", "is_test": False}
    )

    quickstart_schema_stg_sources = PythonOperator(
        task_id="quickstart_schema.stg_sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_sources", "model_path": "staging.graph.stg_sources", "is_test": False}
    )

    quickstart_schema_stg_naming_convention_folders = PythonOperator(
        task_id="quickstart_schema.stg_naming_convention_folders",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_naming_convention_folders", "model_path": "staging.variables.stg_naming_convention_folders", "is_test": False}
    )

    quickstart_schema_stg_naming_convention_prefixes = PythonOperator(
        task_id="quickstart_schema.stg_naming_convention_prefixes",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema.stg_naming_convention_prefixes", "model_path": "staging.variables.stg_naming_convention_prefixes", "is_test": False}
    )

    quickstart_schema_elementary_alerts_anomaly_detection = PythonOperator(
        task_id="quickstart_schema_elementary.alerts_anomaly_detection",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.alerts_anomaly_detection", "model_path": "edr.alerts.alerts_anomaly_detection", "is_test": False}
    )

    quickstart_schema_elementary_alerts_dbt_models = PythonOperator(
        task_id="quickstart_schema_elementary.alerts_dbt_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.alerts_dbt_models", "model_path": "edr.alerts.alerts_dbt_models", "is_test": False}
    )

    quickstart_schema_elementary_alerts_dbt_source_freshness = PythonOperator(
        task_id="quickstart_schema_elementary.alerts_dbt_source_freshness",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.alerts_dbt_source_freshness", "model_path": "edr.alerts.alerts_dbt_source_freshness", "is_test": False}
    )

    quickstart_schema_elementary_alerts_dbt_tests = PythonOperator(
        task_id="quickstart_schema_elementary.alerts_dbt_tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.alerts_dbt_tests", "model_path": "edr.alerts.alerts_dbt_tests", "is_test": False}
    )

    quickstart_schema_elementary_anomaly_threshold_sensitivity = PythonOperator(
        task_id="quickstart_schema_elementary.anomaly_threshold_sensitivity",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.anomaly_threshold_sensitivity", "model_path": "edr.data_monitoring.anomaly_detection.anomaly_threshold_sensitivity", "is_test": False}
    )

    quickstart_schema_elementary_metrics_anomaly_score = PythonOperator(
        task_id="quickstart_schema_elementary.metrics_anomaly_score",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.metrics_anomaly_score", "model_path": "edr.data_monitoring.anomaly_detection.metrics_anomaly_score", "is_test": False}
    )

    quickstart_schema_elementary_data_monitoring_metrics = PythonOperator(
        task_id="quickstart_schema_elementary.data_monitoring_metrics",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.data_monitoring_metrics", "model_path": "edr.data_monitoring.data_monitoring.data_monitoring_metrics", "is_test": False}
    )

    quickstart_schema_elementary_dbt_exposures = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_exposures",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_exposures", "model_path": "edr.dbt_artifacts.dbt_exposures", "is_test": False}
    )

    quickstart_schema_elementary_dbt_invocations = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_invocations",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_invocations", "model_path": "edr.dbt_artifacts.dbt_invocations", "is_test": False}
    )

    quickstart_schema_elementary_dbt_metrics = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_metrics",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_metrics", "model_path": "edr.dbt_artifacts.dbt_metrics", "is_test": False}
    )

    quickstart_schema_elementary_dbt_models = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_models",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_models", "model_path": "edr.dbt_artifacts.dbt_models", "is_test": False}
    )

    quickstart_schema_elementary_dbt_run_results = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_run_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_run_results", "model_path": "edr.dbt_artifacts.dbt_run_results", "is_test": False}
    )

    quickstart_schema_elementary_dbt_snapshots = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_snapshots",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_snapshots", "model_path": "edr.dbt_artifacts.dbt_snapshots", "is_test": False}
    )

    quickstart_schema_elementary_dbt_sources = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_sources",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_sources", "model_path": "edr.dbt_artifacts.dbt_sources", "is_test": False}
    )

    quickstart_schema_elementary_dbt_tests = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_tests",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_tests", "model_path": "edr.dbt_artifacts.dbt_tests", "is_test": False}
    )

    quickstart_schema_elementary_dbt_source_freshness_results = PythonOperator(
        task_id="quickstart_schema_elementary.dbt_source_freshness_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.dbt_source_freshness_results", "model_path": "edr.run_results.dbt_source_freshness_results", "is_test": False}
    )

    quickstart_schema_elementary_elementary_test_results = PythonOperator(
        task_id="quickstart_schema_elementary.elementary_test_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.elementary_test_results", "model_path": "edr.run_results.elementary_test_results", "is_test": False}
    )

    test_quickstart_schema_elementary_elementary_test_results = PythonOperator(
        task_id="test.quickstart_schema_elementary.elementary_test_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_test.quickstart_schema_elementary.elementary_test_results", "model_path": "edr.run_results.elementary_test_results", "is_test": True}
    )

    quickstart_schema_elementary_model_run_results = PythonOperator(
        task_id="quickstart_schema_elementary.model_run_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.model_run_results", "model_path": "edr.run_results.model_run_results", "is_test": False}
    )

    quickstart_schema_elementary_snapshot_run_results = PythonOperator(
        task_id="quickstart_schema_elementary.snapshot_run_results",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.snapshot_run_results", "model_path": "edr.run_results.snapshot_run_results", "is_test": False}
    )

    quickstart_schema_elementary_monitors_runs = PythonOperator(
        task_id="quickstart_schema_elementary.monitors_runs",
        python_callable=run_dbt_task,
        provide_context=True,
        op_kwargs={"subtask_id": "docker_quickstart_schema_elementary.monitors_runs", "model_path": "edr.system.monitors_runs", "is_test": False}
    )

    quickstart_schema_my_first_dbt_model >> test_quickstart_schema_my_first_dbt_model
    quickstart_schema_my_second_dbt_model >> test_quickstart_schema_my_second_dbt_model
    test_quickstart_schema_my_first_dbt_model >> quickstart_schema_my_second_dbt_model
    quickstart_schema_stg_dbt__models >> quickstart_schema_dim_dbt__current_models
    quickstart_schema_stg_dbt__model_executions >> quickstart_schema_dim_dbt__current_models
    quickstart_schema_stg_dbt__exposures >> quickstart_schema_dim_dbt__exposures
    quickstart_schema_stg_dbt__models >> quickstart_schema_dim_dbt__models
    quickstart_schema_stg_dbt__seeds >> quickstart_schema_dim_dbt__seeds
    quickstart_schema_stg_dbt__snapshots >> quickstart_schema_dim_dbt__snapshots
    quickstart_schema_stg_dbt__sources >> quickstart_schema_dim_dbt__sources
    quickstart_schema_stg_dbt__tests >> quickstart_schema_dim_dbt__tests
    quickstart_schema_stg_dbt__invocations >> quickstart_schema_fct_dbt__invocations
    quickstart_schema_stg_dbt__model_executions >> quickstart_schema_fct_dbt__model_executions
    quickstart_schema_stg_dbt__seed_executions >> quickstart_schema_fct_dbt__seed_executions
    quickstart_schema_stg_dbt__snapshot_executions >> quickstart_schema_fct_dbt__snapshot_executions
    quickstart_schema_stg_dbt__test_executions >> quickstart_schema_fct_dbt__test_executions
    quickstart_schema_exposures >> quickstart_schema_stg_dbt__exposures
    quickstart_schema_invocations >> quickstart_schema_stg_dbt__invocations
    quickstart_schema_models >> quickstart_schema_stg_dbt__models
    quickstart_schema_model_executions >> quickstart_schema_stg_dbt__model_executions
    quickstart_schema_seeds >> quickstart_schema_stg_dbt__seeds
    quickstart_schema_seed_executions >> quickstart_schema_stg_dbt__seed_executions
    quickstart_schema_snapshots >> quickstart_schema_stg_dbt__snapshots
    quickstart_schema_snapshot_executions >> quickstart_schema_stg_dbt__snapshot_executions
    quickstart_schema_sources >> quickstart_schema_stg_dbt__sources
    quickstart_schema_tests >> quickstart_schema_stg_dbt__tests
    quickstart_schema_test_executions >> quickstart_schema_stg_dbt__test_executions
    quickstart_schema_int_direct_relationships >> quickstart_schema_int_all_dag_relationships
    quickstart_schema_int_all_graph_resources >> quickstart_schema_int_all_dag_relationships
    quickstart_schema_stg_nodes >> quickstart_schema_int_all_graph_resources
    quickstart_schema_stg_exposures >> quickstart_schema_int_all_graph_resources
    quickstart_schema_stg_metrics >> quickstart_schema_int_all_graph_resources
    quickstart_schema_stg_sources >> quickstart_schema_int_all_graph_resources
    quickstart_schema_stg_naming_convention_prefixes >> quickstart_schema_int_all_graph_resources
    quickstart_schema_stg_naming_convention_folders >> quickstart_schema_int_all_graph_resources
    quickstart_schema_int_all_graph_resources >> quickstart_schema_int_direct_relationships
    quickstart_schema_stg_node_relationships >> quickstart_schema_int_direct_relationships
    quickstart_schema_stg_exposure_relationships >> quickstart_schema_int_direct_relationships
    quickstart_schema_stg_metric_relationships >> quickstart_schema_int_direct_relationships
    quickstart_schema_fct_direct_join_to_source >> test_quickstart_schema_fct_direct_join_to_source
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_direct_join_to_source
    quickstart_schema_fct_marts_or_intermediate_dependent_on_source >> test_quickstart_schema_fct_marts_or_intermediate_dependent_on_source
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_marts_or_intermediate_dependent_on_source
    quickstart_schema_fct_model_fanout >> test_quickstart_schema_fct_model_fanout
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_model_fanout
    quickstart_schema_fct_multiple_sources_joined >> test_quickstart_schema_fct_multiple_sources_joined
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_multiple_sources_joined
    quickstart_schema_fct_rejoining_of_upstream_concepts >> test_quickstart_schema_fct_rejoining_of_upstream_concepts
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_rejoining_of_upstream_concepts
    quickstart_schema_fct_root_models >> test_quickstart_schema_fct_root_models
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_root_models
    quickstart_schema_fct_source_fanout >> test_quickstart_schema_fct_source_fanout
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_source_fanout
    quickstart_schema_fct_staging_dependent_on_marts_or_intermediate >> test_quickstart_schema_fct_staging_dependent_on_marts_or_intermediate
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_staging_dependent_on_marts_or_intermediate
    quickstart_schema_fct_staging_dependent_on_staging >> test_quickstart_schema_fct_staging_dependent_on_staging
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_staging_dependent_on_staging
    quickstart_schema_fct_unused_sources >> test_quickstart_schema_fct_unused_sources
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_unused_sources
    quickstart_schema_fct_documentation_coverage >> test_quickstart_schema_fct_documentation_coverage
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_documentation_coverage
    quickstart_schema_fct_undocumented_models >> test_quickstart_schema_fct_undocumented_models
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_undocumented_models
    quickstart_schema_fct_chained_views_dependencies >> test_quickstart_schema_fct_chained_views_dependencies
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_chained_views_dependencies
    quickstart_schema_fct_exposure_parents_materializations >> test_quickstart_schema_fct_exposure_parents_materializations
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_exposure_parents_materializations
    quickstart_schema_fct_model_directories >> test_quickstart_schema_fct_model_directories
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_model_directories
    quickstart_schema_stg_naming_convention_folders >> quickstart_schema_fct_model_directories
    quickstart_schema_int_all_dag_relationships >> quickstart_schema_fct_model_directories
    quickstart_schema_fct_model_naming_conventions >> test_quickstart_schema_fct_model_naming_conventions
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_model_naming_conventions
    quickstart_schema_stg_naming_convention_prefixes >> quickstart_schema_fct_model_naming_conventions
    quickstart_schema_fct_source_directories >> test_quickstart_schema_fct_source_directories
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_source_directories
    quickstart_schema_fct_test_directories >> test_quickstart_schema_fct_test_directories
    quickstart_schema_int_all_graph_resources >> quickstart_schema_fct_test_directories
    quickstart_schema_int_direct_relationships >> quickstart_schema_fct_test_directories
    quickstart_schema_fct_missing_primary_key_tests >> test_quickstart_schema_fct_missing_primary_key_tests
    quickstart_schema_int_model_test_summary >> quickstart_schema_fct_missing_primary_key_tests
    quickstart_schema_fct_test_coverage >> test_quickstart_schema_fct_test_coverage
    quickstart_schema_int_model_test_summary >> quickstart_schema_fct_test_coverage
    quickstart_schema_int_all_graph_resources >> quickstart_schema_int_model_test_summary
    quickstart_schema_int_direct_relationships >> quickstart_schema_int_model_test_summary
    quickstart_schema_elementary_elementary_test_results >> quickstart_schema_elementary_alerts_anomaly_detection
    quickstart_schema_elementary_model_run_results >> quickstart_schema_elementary_alerts_dbt_models
    quickstart_schema_elementary_snapshot_run_results >> quickstart_schema_elementary_alerts_dbt_models
    quickstart_schema_elementary_dbt_source_freshness_results >> quickstart_schema_elementary_alerts_dbt_source_freshness
    quickstart_schema_elementary_dbt_sources >> quickstart_schema_elementary_alerts_dbt_source_freshness
    quickstart_schema_elementary_elementary_test_results >> quickstart_schema_elementary_alerts_dbt_tests
    quickstart_schema_elementary_metrics_anomaly_score >> quickstart_schema_elementary_anomaly_threshold_sensitivity
    quickstart_schema_elementary_data_monitoring_metrics >> quickstart_schema_elementary_metrics_anomaly_score
    quickstart_schema_elementary_dbt_run_results >> quickstart_schema_elementary_model_run_results
    quickstart_schema_elementary_dbt_models >> quickstart_schema_elementary_model_run_results
    quickstart_schema_elementary_dbt_run_results >> quickstart_schema_elementary_snapshot_run_results
    quickstart_schema_elementary_dbt_snapshots >> quickstart_schema_elementary_snapshot_run_results
    quickstart_schema_elementary_data_monitoring_metrics >> quickstart_schema_elementary_monitors_runs