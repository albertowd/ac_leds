buid:
    python -m build

install:
    pip install -r requirements.txt

lint:
    pylint ./ac_aura/ --disable=W0718
    pylint ./tests/ --disable=W0718,C413

test:
    python tests/test_ac_udp_telemetry.py
    python tests/test_aura_api.py
    python tests/test_aura_bgr_color.py
