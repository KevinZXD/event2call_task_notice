#!/bin/bash
ps -ef|grep "event2call_task_notice"|grep -v "grep"|awk '{print $2}'|xargs kill -9