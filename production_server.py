import os
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl import BuiltinSSLAdapter
from cheroot.ssl.pyopenssl import pyOpenSSLAdapter
from src import app
import cheroot.ssl.builtin


port = int(os.environ.get('PORT', 8100))
server = WSGIServer(('0.0.0.0', port), app)
adapter = BuiltinSSLAdapter(certificate="certificate.pem", private_key="certificate_private_key.pem")
cheroot.ssl.builtin.IS_BELOW_PY37 = True
# adapter = pyOpenSSLAdapter(certificate="certificate.pem", private_key="certificate_private_key.pem")
server.ssl_adapter = adapter


if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
