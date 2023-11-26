import os
import sys
import yaml
import logging
import requests
import subprocess

class CheckRequirements():
    """ Check python3 & OS packages requirements, at running tool """
    def __init__(self, config: dict) -> None:
        logging.info("Check requirements..")
        with open("requirements.txt", "r") as reqfile:
            self.python3_pip_requirements: list[str] = reqfile.readlines()
            reqfile.close()
        self.logfile: str = config.get("loggpath")
        if self.logfile is None:
            self.logfile: str = "/var/log/yc.log"
        self.python3_required: list[int] = [3, 7, 0] 
        self.python3_version: list[int, int, int] = [
            sys.version_info[0],
            sys.version_info[1],
            sys.version_info[2]
        ]
        self.python3_is_ok: bool = self.python3_ok() # if returned True, then OK
        self.pip_is_ok: bool = self.check_pip() # if returned True, then OK
        self.yc_tool_is_ok: bool = self.check_yc_tool() # if returned True, then OK
        logging.info("All requirements is OK")
    
    def python3_ok(self) -> bool:
        print("⚙️ Проверка установленного python3...")
        logging.debug(f"python3 version is: {self.python3_version}")
        err_msg: str = ( f"⚠️  Версия Python не подходит для запуска установщика!\nВаша: {self.python3_version} - Требуется: {self.python3_required}")
        for i in range(2):
            if self.python3_version[i] < self.python3_required[i]: raise RuntimeError(err_msg)
        else: return True

    def check_pip(self) -> bool:
        logging.info("Check pip modules..")
        modules: list[str] = tuple(sys.modules)
        for module in self.python3_pip_requirements:
            if module not in modules: break
        else: return True

        logging.info("Пытаюсь удовлетворить зависимости")
        cmd: str = "bin/pip3 install -r requirements.txt"
        if self.python3_version[1] >= 11: cmd += " --break"
        try: subprocess.run(cmd, shell=True, stdout=self.logfile)
        except Exception as err:
            logging.error(f"В процессе установки зависимостей возникли ошибки.. {err}")
            raise RuntimeError("⚠️  Ошибка! Установить зависимости PIP не удалось!")
        finally: return True

    def check_yc_tool(self) -> bool:
        import shutil
        logging.info("Check yandex cloud tool..")
        if shutil.which("yc") is None:
            logging.debug("yc tool is absent.. tring to resolve")
            response = requests.get('https://storage.yandexcloud.net/yandexcloud-yc/install.sh')
            script = open('/tmp/install.sh', 'wb')
            script.write(response.content)
            subprocess.run("bash /tmp/install.sh", shell=True)
            subprocess.run("yc init")
            return True
        return True

class Monitor():
    """ Check state of VMs """
    pass

def main(config: dict):
    logging.info("Running tool..")
    try:
        CheckRequirements(config)
    except RuntimeError as err:
        logging.error(str(err))

if __name__ == '__main__':
    config_file = open(".config.yml", "r")
    config: dict = yaml.safe_load(config_file)
    logglevel: str = config.get("logglevel") # may return one of DEBUG, INFO, ERROR and etc..
    if logglevel is None:
        logglevel: logging._Level = logging.INFO
    elif logglevel == "DEBUG":
        logglevel: logging._Level = logging.DEBUG
    elif logglevel == "ERROR":
        logglevel: logging._Level = logging.ERROR
    logging.basicConfig(
        level=logglevel,
        filename="yc.log",
        format="%(asctime)s (%(filename)s: %(lineno)d) %(levelname)s %(message)s",
        filemode="a")
    main(config)