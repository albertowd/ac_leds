clean:
    pyinstaller --clean ac_leds/service.py

install:
    pip install -r requirements.txt

lint:
    pylint ./ac_leds/ --disable=W0718
    pylint ./tests/ --disable=W0718,C413

package:
    pyinstaller --console --icon resources/ac.ico --name "AC Leds" --onefile --paths .venv/Lib/site-packages ac_leds/service.py

test:
    python tests/test_ac_udp_telemetry.py
    python tests/test_leds_api.py
    python tests/test_leds_bgr_color.py
