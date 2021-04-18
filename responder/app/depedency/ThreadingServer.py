from socketserver import TCPServer, UDPServer, ThreadingMixIn
from threading import Thread
import ssl
import struct

try : 
	from app.depedency.utils import *
except :
	from depedency.utils import *

class ThreadingUDPServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		if OsInterfaceIsSupported():
			try:
				if settings.Config.Bind_To_ALL:
					pass
				else:
					if (sys.version_info > (3, 0)):
						self.socket.setsockopt(socket.SOL_SOCKET, 25, bytes(settings.Config.Interface+'\0', 'utf-8'))
					else:
						self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Interface+'\0')
			except:
				raise
				pass
		UDPServer.server_bind(self)

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
	def server_bind(self):
		if OsInterfaceIsSupported():
			try:
				if settings.Config.Bind_To_ALL:
					pass
				else:
					if (sys.version_info > (3, 0)):
						self.socket.setsockopt(socket.SOL_SOCKET, 25, bytes(settings.Config.Interface+'\0', 'utf-8'))
					else:
						self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Interface+'\0')
			except:
				raise
				pass
		TCPServer.server_bind(self)

class ThreadingTCPServerAuth(ThreadingMixIn, TCPServer):
	def server_bind(self):
		if OsInterfaceIsSupported():
			try:
				if settings.Config.Bind_To_ALL:
					pass
				else:
					if (sys.version_info > (3, 0)):
						self.socket.setsockopt(socket.SOL_SOCKET, 25, bytes(settings.Config.Interface+'\0', 'utf-8'))
					else:
						self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Interface+'\0')
			except:
				raise
				pass
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
		TCPServer.server_bind(self)

class ThreadingUDPMDNSServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		MADDR = "224.0.0.251"
		
		self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		
		Join = self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MADDR) + settings.Config.IP_aton)

		if OsInterfaceIsSupported():
			try:
				if settings.Config.Bind_To_ALL:
					pass
				else:
					if (sys.version_info > (3, 0)):
						self.socket.setsockopt(socket.SOL_SOCKET, 25, bytes(settings.Config.Interface+'\0', 'utf-8'))
					else:
						self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Interface+'\0')
			except:
				raise
				pass
		UDPServer.server_bind(self)

class ThreadingUDPLLMNRServer(ThreadingMixIn, UDPServer):
	def server_bind(self):
		MADDR = "224.0.0.252"
		self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		
		Join = self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MADDR) + settings.Config.IP_aton)
		
		if OsInterfaceIsSupported():
			try:
				if settings.Config.Bind_To_ALL:
					pass
				else:
					if (sys.version_info > (3, 0)):
						self.socket.setsockopt(socket.SOL_SOCKET, 25, bytes(settings.Config.Interface+'\0', 'utf-8'))
					else:
						self.socket.setsockopt(socket.SOL_SOCKET, 25, settings.Config.Interface+'\0')
			except:
				raise
				#pass
		UDPServer.server_bind(self)

def serve_thread_udp_broadcast(host, port, handler):
    try:
        server = ThreadingUDPServer((host, port),handler)
        server.serve_forever()
    except:
        print(color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running.")

def serve_NBTNS_poisoner(host, port, handler):
	serve_thread_udp_broadcast(host, port, handler)

def serve_MDNS_poisoner(host, port, handler):
	try:
		server = ThreadingUDPMDNSServer((host, port), handler)
		server.serve_forever()
	except:
		print(color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running.")

def serve_LLMNR_poisoner(host, port, handler):
	try:
		server = ThreadingUDPLLMNRServer((host, port), handler)
		server.serve_forever()
	except:
		raise
		print(color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running.")

def serve_thread_udp(host, port, handler):
	try:
		if OsInterfaceIsSupported():
			server = ThreadingUDPServer((host, port), handler)
			server.serve_forever()
		else:
			server = ThreadingUDPServer((host, port), handler)
			server.serve_forever()
	except:
		print(color("[!] ", 1, 1) + "Error starting UDP server on port " + str(port) + ", check permissions or other servers running.")

def serve_thread_tcp(host, port, handler):
	try:
		if OsInterfaceIsSupported():
			server = ThreadingTCPServer((host, port), handler)
			server.serve_forever()
		else:
			server = ThreadingTCPServer((host, port), handler)
			server.serve_forever()
	except:
		print(color("[!] ", 1, 1) + "Error starting TCP server on port " + str(port) + ", check permissions or other servers running.")

def serve_thread_tcp_auth(host, port, handler):
	try:
		if OsInterfaceIsSupported():
			server = ThreadingTCPServerAuth((host, port), handler)
			server.serve_forever()
		else:
			server = ThreadingTCPServerAuth((host, port), handler)
			server.serve_forever()
	except:
		print(color("[!] ", 1, 1) + "Error starting TCP server on port " + str(port) + ", check permissions or other servers running.")

def serve_thread_SSL(host, port, handler):
	try:

		cert = os.path.join(settings.Config.ResponderPATH, settings.Config.SSLCert)
		key =  os.path.join(settings.Config.ResponderPATH, settings.Config.SSLKey)

		if OsInterfaceIsSupported():
			server = ThreadingTCPServer((host, port), handler)
			server.socket = ssl.wrap_socket(server.socket, certfile=cert, keyfile=key, server_side=True)
			server.serve_forever()
		else:
			server = ThreadingTCPServer((host, port), handler)
			server.socket = ssl.wrap_socket(server.socket, certfile=cert, keyfile=key, server_side=True)
			server.serve_forever()
	except:
		print(color("[!] ", 1, 1) + "Error starting SSL server on port " + str(port) + ", check permissions or other servers running.")
