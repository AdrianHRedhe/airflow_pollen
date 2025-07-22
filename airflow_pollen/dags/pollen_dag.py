from datetime import datetime

from airflow.decorators import dag

from airflow_pollen.common.tasks import (
    fetch_data_task,
    store_in_db_task,
    create_scd2_view_task,
    find_new_scd2_events_task,
    send_telegram_message_task,
)


@dag(
    dag_id="pollen_dag",
    start_date=datetime(2025, 7, 15),
    schedule="0 7 * * *",
    catchup=False,
)
def pollen_dag():
    data = fetch_data_task()
    data = store_in_db_task(data)
    data = create_scd2_view_task(data)
    new_events = find_new_scd2_events_task(data)
    send_telegram_message_task(new_events)


pollen_dag()
