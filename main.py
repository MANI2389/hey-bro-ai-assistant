from core.assistant import start_assistant
from gui.dashboard import start_dashboard
import threading

# run dashboard in separate thread
threading.Thread(target=start_dashboard).start()

# start AI assistant
start_assistant()