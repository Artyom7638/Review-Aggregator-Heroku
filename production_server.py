import os
from src.external.cheroot.wsgi import Server as WSGIServer
from src.external.cheroot.ssl.pyopenssl import pyOpenSSLAdapter
from src import app
import src.external.cheroot.ssl.builtin as builtin


port = int(os.environ.get('PORT', 8100))
server = WSGIServer(('0.0.0.0', port), app)
builtin.IS_BELOW_PY37 = True
adapter = builtin.BuiltinSSLAdapter(certificate="certificate.pem", private_key="certificate_private_key.pem")
# adapter = pyOpenSSLAdapter(certificate="certificate.pem", private_key="certificate_private_key.pem")
server.ssl_adapter = adapter


if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
