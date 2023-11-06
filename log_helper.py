import logging
import os.path
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s--->: %(message)s',
                    level=logging.DEBUG,
                    filemode='a')


def createLogFile(name, level):
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关

    # 创建一个handler，用于写入日志文件
    rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # log_date = rq[:10]
    log_path = os.getcwd() + '/Logs/'
    isExists = os.path.exists(log_path)
    # # 判断结果
    if not isExists:
        os.makedirs(log_path)
    log_name = os.getcwd() + '/Logs/{}-'.format(rq) + name + '.log'
    fh = logging.FileHandler(log_name, mode='a')
    fh.setLevel(level)  # 输出到file的log等级的开关

    # 定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s--->: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def print_info(info, *args):
    createLogFile("info", logging.INFO)
    if len(args) > 0:
        log = ""
        for arg in args:
            log += "{}"
        logging.info((info + log).format(*args))
    else:
        logging.info(info)


def print_error(error, *args):
    createLogFile("error",logging.ERROR)
    if len(args) > 0:
        log = ""
        for arg in args:
            log += "{}"
        logging.error((error + log).format(*args))
    else:
        logging.error(error)

def deleteBigFile(path):
    for file in os.listdir(path):
        fsize = os.path.getsize(f'{path}{file}')
        if (fsize > 1 * 1024 * 1024 * 1024):
            os.remove(f'{path}{file}')

if __name__ == '__main__':
    createLogFile("info", logging.INFO)