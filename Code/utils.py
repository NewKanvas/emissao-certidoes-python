import time
import random


def sleeper():
    time.sleep(random.uniform(0.1, 0.5))


def write(word, word_input):
    for digit in word:
        word_input.send_keys(digit)
        sleeper()


def remove_format(cpf):
    return "".join(c for c in cpf if c.isdigit())


import psutil


def killprov(downloaded_file_path, log):
    # Verificar se o arquivo está sendo usado por algum processo
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            # Obter a lista de arquivos abertos pelo processo
            open_files = proc.open_files()
            for file in open_files:
                if file.path == downloaded_file_path:
                    # Fechar o processo que está utilizando o arquivo
                    logprint(
                        f"Fechando o processo '{proc.name()}' (PID: {proc.pid})", log
                    )
                    proc.kill()
                    break  # Saia do loop assim que encontrar o processo
        except psutil.AccessDenied:
            # Ignorar processos aos quais não temos permissão para acessar
            pass


def logprint(mess, log):
    print(mess)
    log.append(mess)
