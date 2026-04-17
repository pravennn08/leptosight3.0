from ui.app import App
import atexit
from hardware.relay import cleanup

app = App()

atexit.register(cleanup)
app.attributes("-zoomed", True)
app.mainloop()
