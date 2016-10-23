# -*- coding: utf-8 -*-

import json
import schedule
import threading

from functions.manager import FunctionManager
from notifier.between import Between
from slack.slackbot import SlackerAdapter
from utils.data_handler import DataHandler
from utils.resource import MessageResource
from utils.state import State

class Worker(object):

    def __init__(self):
        self.slackbot = SlackerAdapter()
        self.data_handler = DataHandler()

    def run(self):
        self.__set_schedules()
        schedule.run_continuously(interval=1)
        self.slackbot.send_message(text=MessageResource.WORKER_START)

    def __set_schedules(self):
        schedule_fname = "scheduler.json"
        schedule_data = self.data_handler.read_file(schedule_fname)
        alarm_data = schedule_data.get('alarm', {})
        between_data = schedule_data.get('between', {})

        for k,v in alarm_data.items():
            if type(v) != type({}):
                continue

            if 'time' in v:
                time = v['time']
                # Do only once
                param = {
                    "repeat": False,
                    "func_name": v['f_name'],
                    "params": v.get('params', {})
                }

                try:
                    function = FunctionManager().load_function
                    schedule.every().day.at(time).do(self.__run_threaded,
                                                            function, param)
                except Exception as e:
                    print("Error: " + e)

            if 'between_id' in v:
                between = between_data[v['between_id']]
                start_time, end_time = self.__time_interval2start_end(between['time_interval'])
                # Repeat
                period = v['period'].split(" ")
                number = int(period[0])
                datetime_unit = self.__replace_datetime_unit_ko2en(period[1])

                param = {
                    "start_time": start_time,
                    "end_time": end_time,
                    "repeat": True,
                    "func_name": v['f_name'],
                    "params": v.get('params', {})
                }

                try:
                    function = FunctionManager().load_function
                    getattr(schedule.every(number), datetime_unit).do(self.__run_threaded,
                                                                    function, param)
                except Exception as e:
                    print("Error: " + e)


    def __replace_datetime_unit_ko2en(self, datetime_unit):
        ko2en_dict = {
            "초": "seconds",
            "분": "minutes",
            "시간": "hours"
        }

        if datetime_unit in ko2en_dict:
            return ko2en_dict[datetime_unit]
        return datetime_unit

    def __time_interval2start_end(self, time_interval):
        if "~" in time_interval:
            time_interval = time_interval.split("~")
            start_time = time_interval[0].split(":")
            end_time = time_interval[1].split(":")

            start_time = tuple(map(lambda x: int(x), start_time))
            end_time = tuple(map(lambda x: int(x), end_time))
        else:
            start_time = time_interval
            end_time = None
        return start_time, end_time

    def __run_threaded(self, job_func, param):
        job_thread = threading.Thread(target=job_func, kwargs=param)
        job_thread.start()

    def stop(self):
        self.__set_schedules()
        schedule.clear()

        self.slackbot.send_message(text=MessageResource.WORKER_STOP)