import psutil

def get_status():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    return {
        "cpu": cpu,
        "ram": ram
    }