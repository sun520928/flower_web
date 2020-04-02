# -*- coding: utf-8 -*-
import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

from flask import Flask
from config import config

def setup_log(config_name):
	# # 设置日志的的登记
	# logging.basicConfig(level=config[config_name].LOG_LEVEL)
	# # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
	# file_log_handler = RotatingFileHandler("log", maxBytes=1024*1024*100, backupCount=100)
	# # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
	# formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
	# # 为日志记录器设置记录格式
	# file_log_handler.setFormatter(formatter)
	# # 为全局的日志工具对象（flaks app使用的）加载日志记录器
	# logging.getLogger().addHandler(file_log_handler)

	logger = logging.getLogger('ALL')
	err_logger = logging.getLogger('EXCEPTION')

	log_file = 'log' + os.path.sep + 'all.log'
	fileHandler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='a+')
	fileHandler.setLevel(logging.DEBUG)
	fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	logger.addHandler(fileHandler)

	fileTimeHandler = TimedRotatingFileHandler(filename=log_file,
	when='midnight', 
	interval=1, 
	backupCount=7,
	encoding='utf-8',
	)
	fileTimeHandler.suffix = '%Y%m%d.log' 
	logger.addHandler(fileTimeHandler)

	#exception log
	err_log_file = 'log' + os.path.sep + 'exception.log'
	errfileHandler = logging.FileHandler(filename=err_log_file, encoding='utf-8', mode='a+')
	errfileHandler.setLevel(logging.ERROR)
	errfileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	err_logger.addHandler(errfileHandler)

	errfileTimeHandler = TimedRotatingFileHandler(filename=err_log_file,
    when='midnight', 
	interval=1, 
	backupCount=7,
	encoding='utf-8',
	)
	errfileTimeHandler.suffix = '%Y%m%d.log' 
	err_logger.addHandler(errfileTimeHandler)