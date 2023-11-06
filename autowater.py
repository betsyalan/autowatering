# -*- coding: utf-8 -*- 
# 通过config.ini文件配置开始时间和浇水时间，可以配置两个开始时间
# 可以配置引脚定义，引脚为物理引脚，靠左为单数，靠外为偶数   
# lowtrig =1 为低电平触发 =0 为高电平触发
import RPi.GPIO as GPIO    
import time    
import os
import sys
# 配置文件
import configparser
#时间
import datetime
#log
import logging
import logging.handlers

# 第一步，创建一个logger
logger = logging.getLogger()

def autowater():
    bHasStart = False
    playtimesec =0
    while True:
        #2019.11.1 随时更新配置
        # 读取配置文件
        cf = configparser.ConfigParser()
        # 2023.11.1 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        cf.read(os.path.join(BASE_DIR ,'config.ini'))
        #cf.read('config.ini')
        #开始时间
        starttime1= int(cf.get('config', 'starttime1'))
        #自动时间
        starttime2= int(cf.get('config', 'starttime2'))
        playtime= int(cf.get('config', 'palytime'))
        #pin num
        pin =int(cf.get('config', 'pinnum'))
        # 2023.11.3 增加配置，是否低电平触发
        bLowtrig=int(cf.get('config', 'lowtrig'))
        #获取时间
        curhour=int(datetime.datetime.now().hour)    
        #logger.debug("+++curtime:%d,starttime:%d,%d,playtime:%d" % (curhour,starttime1,starttime2,playtime))
        #获取当前时间的时间戳
        #startsec = time.time()
        logger.debug(f'{bHasStart}')
        if bHasStart == False and (curhour == starttime1 or curhour == starttime2):
            bHasStart = True
            #计算浇水时间
            #playtimesec = float(playtime) + float(startsec)
            #2023 11.3 增加判断是否低电平触发
            #低电平
            if bLowtrig == 1:
                GPIO.output(pin, GPIO.LOW)    
                logger.debug("start...")
                time.sleep(playtime)    
                GPIO.output(pin, GPIO.HIGH)
                logger.debug("end time:%f"%playtime)
                logger.debug(f'{bHasStart}')
            else:#高电平
                GPIO.output(pin, GPIO.HIGH)    
                logger.debug("start...")
                time.sleep(playtime)    
                GPIO.output(pin, GPIO.LOW)
                logger.debug("end time:%f"%playtime)
           
        if curhour != int(starttime1) and curhour != int(starttime2):
            bHasStart = False

        time.sleep(10)


if __name__ == '__main__':
    # 2023.10.30 获取当前目录，修正获取config.ini路径不对的问题
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read(os.path.join(BASE_DIR ,'config.ini'))
    #cf.read('config.ini')
    #播放时间
    starttime1= cf.get('config', 'starttime1')
    #自动时间
    starttime2= cf.get('config', 'starttime2')
    #pin num
    pin =int(cf.get('config', 'pinnum'))
    # 2023.11.3 增加配置，是否低电平触发
    bLowtrig=int(cf.get('config', 'lowtrig'))
    # GPIO设置
    # BOARD编号方式，基于插座引脚编号    
    GPIO.setmode(GPIO.BOARD)    
    # 输出模式    
    GPIO.setup(pin, GPIO.OUT)    
    #2023 11.3 增加判断是否低电平触发       
    # 低电平
    if bLowtrig == 1:
        GPIO.output(pin, GPIO.HIGH)   
    else:#高电平
        GPIO.output(pin, GPIO.LOW)    

    logger.setLevel(logging.DEBUG)  # Log等级总开关
    # 创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关

    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_path = BASE_DIR + '/Logs/'
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile,encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s: %(message)s")
    fh.setFormatter(formatter)

    # 控制台
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)

    logger.debug("程序启动。")
    autowater()
