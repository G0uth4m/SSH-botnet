from pexpect import pxssh

class Client:
	
	def __init__(self, host, user, password, por):
		self.host = host
		self.user = user
		self.password = password
		self.por  = por
		self.session = self.connect()

	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password, port = self.por)
			return s
		except Exception, e:
			print e
			print '[-] Error Connecting'
			exit()

	def send_command(self, cmd):
		self.session.sendline(cmd)
		self.session.prompt()
		return self.session.before
