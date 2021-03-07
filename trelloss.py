# -*- coding: cp1251 -*-
# pip3 install -U  py-trello
# pip3 install matplotlib
# pip3 install pandas
# pip3 install -U python-dotenv


from trello import TrelloClient
from datetime import datetime
from enum import IntEnum
import csv
import os
from dotenv import load_dotenv
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Priority(IntEnum):
    HIGHEST = 1
    HIGH = 2
    MIDDLE = 3
    LOW = 4


class FieldType(IntEnum):
    PROJECT_NAME = 0
    TASK_NAME = 1
    TIME_STAMP = 2
    PRIORITY = 3


def get_list_and_cards(client):
    # get all boards
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == 'GOALS':
            boards = board

    # get all lists
    boards.list_lists()
    my_lists = boards.all_lists()

    # get all cards first list
    return my_lists, my_lists[0].list_cards()


def parse_task(task):
    task_container = [parse_project_name(task[FieldType.PROJECT_NAME]), parse_task_name(task[FieldType.TASK_NAME]),
                      parse_time_stamp(task[FieldType.TIME_STAMP]), parse_priority(task[FieldType.PRIORITY])]
    return task_container


def parse_project_name(field):
    project_name = field.lstrip()
    logging.debug(f"Project name: {project_name}")


def parse_task_name(field):
    task_name = field.lstrip()
    logging.debug(f"Task name: {task_name}")


def parse_time_stamp(field):
    data = field[:field.rfind("at")].lstrip()
    time = field[field.rfind("at") + 3:].lstrip()
    data_time = data + time
    logging.debug(data_time)
    time_stamp = datetime.strptime(data_time, "%B %d %Y %I:%M%p")
    time_stamp = time_stamp.strftime("%Y-%m-%d_%H.%M.%S")
    logging.debug(f"Time_stamp: {time_stamp}")


def parse_priority(field):
    priority = Priority(int(''.join(filter(lambda x: x.isdigit(), field.lstrip()))))
    logging.debug(f"Priority: {priority.name}")


separator = ","
header = ["ProjectName", "TaskName", "DataTime", "Priority"]
current_path = Path(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    client = TrelloClient(
        api_key=os.getenv("TRELLO_API_KEY"),
        api_secret=os.getenv("TRELLO_API_SECRET"),
        token=os.getenv("TRELLO_TOKEN"),
    )

    # create environment
    file_name = current_path / "task_archive.csv"

    if not file_name.exists():
        with open(file_name, "w", encoding='utf-8', newline='') as file_report:
            report_writer = csv.DictWriter(file_report, fieldnames=header, delimiter=separator)
            report_writer.writeheader()
    try:
        file_report = open(file_name, "a+", encoding='utf-8', newline='')
        report_writer = csv.DictWriter(file_report, fieldnames=header, delimiter=separator)
    except:
        logging.error("Whoops, something is wrong! Please make sure no one is using the report file")
        exit(1)

    lists, tasks_card = get_list_and_cards(client)
    # parser cards
    for card in tasks_card:
        report_data = []
        task = card.name.split('\\')
        report_data.extend(parse_task(task))
        # write to csv
        inner_dict = dict(zip(header, report_data))
        report_writer.writerow(inner_dict)
        card.delete()

    file_report.close()
    lists[0].archive_all_cards()
    logging.info("FINISH")
