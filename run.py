import threading
from controller.main import loop
from web.app import app

threading.Thread(target=loop, daemon=True).start()
app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
