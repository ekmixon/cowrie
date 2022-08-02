#!/usr/bin/env python

import datetime
import json
import random

import psutil

command: dict = {"command": {}}
command["command"]["ps"] = []

randomStates = ["Ss", "S<", "D<", "Ss+"]
for proc in psutil.process_iter():
    try:
        info = proc.as_dict(
            attrs=[
                "pid",
                "name",
                "cmdline",
                "username",
                "cpu_percent",
                "memory_percent",
                "memory_info",
                "create_time",
                "terminal",
                "status",
                "cpu_times",
            ]
        )
    except psutil.NoSuchProcess:
        pass
    else:
        object = {
            "USER": info["username"],
            "PID": info["pid"],
            "COMMAND": "/".join(info["cmdline"])
            if info["cmdline"]
            else "[ " + info["name"] + " ]",
            "CPU": info["cpu_percent"],
            "MEM": info["memory_percent"],
            "RSS": info["memory_info"].rss,
            "VSZ": info["memory_info"].vms,
            "START": datetime.datetime.fromtimestamp(
                info["create_time"]
            ).strftime("%b%d"),
        }

        if info["terminal"]:
            object["TTY"] = str(info["terminal"]).replace("/dev/", "")
        else:
            object["TTY"] = "?"
        object["STAT"] = random.choice(randomStates)
        object["TIME"] = info["cpu_times"].user
        command["command"]["ps"].append(object)

print(json.dumps(command, indent=4, sort_keys=True))
