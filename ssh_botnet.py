from pexpect import pxssh
import os
import nmap
from termcolor import colored
import getpass
from datetime import datetime,date

print("""
Author : Goutham Ramesh
GitHub : https://github.com/G0uth4m
	
	- This is a simple tool handy for linux administrators 
	in schools, colleges, etc where all the systems used by students
	in the lab or elsewhere have same usernames and passwords.

	- Future releases will be having a choice to input different usernames
	and passwords via a file.

	- This code was tested on a bunch metasploitable 2 servers.

	- Using this tool for illegal stuff is highly not recommended.

	- 'sudo' is unsupported. You can use root as username for superuser access.

	 _         _           _              _   
 ___ ___| |__     | |__   ___ | |_ _ __   ___| |_ 
/ __/ __| '_ \    | '_ \ / _ \| __| '_ \ / _ \ __|
\__ \__ \ | | |   | |_) | (_) | |_| | | |  __/ |_ 
|___/___/_| |_|___|_.__/ \___/ \__|_| |_|\___|\__|
             |_____|                              
""")

f = open('logs.txt', 'a')
f2 = open('session.txt', 'a')

interface = raw_input('[*] Interface : ')
user_name = raw_input('[*] Single username for all systems : ')
password = raw_input('[*] Single password for all users : ')

f2.write(interface + '\n' + user_name + '\n' + password + '\n')

#myip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read().replace('\n', '')
myip = os.popen("ifconfig " + interface + " | grep \"inet \" | awk \'{print $2}\'").read().replace("\n", "")
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

def botnetCommand(command):
	f.write(" -> " + str(date.today().strftime("%B %d, %Y")) + " ( " + datetime.now().strftime("%H:%M:%S") + ' ) ' + '\n\n')
	for client in botNet:
		output = client.send_command(command)
		print '[*] Output from ' + client.host
		#print '[*] ssh service running on port : ' + str(client.por)
		print '[+] ' + output
		f.write('[*] Output from ' + client.host + '\n')
		f.write('[+] ' + output + '\n')
	f.write(100*'-' + '\n')
def addClient(host, user, password, por):
	if por != -1:
		client = Client(host, user, password, por)
		botNet.append(client)
	else:
		print '[-] ssh server not running on ' + host	

botNet = []

nm = nmap.PortScanner()
#os.system("figlet ssh_botnet")
print("\n")
print "[*] Scanning network for ssh servers ..."
nm.scan(myip + '/24')
print "[+] Scan complete"
hosts = nm.all_hosts()
hosts.remove(myip)

if len(hosts) == 0:
	print "[-] No ssh servers found on the network"
	exit()

ssh_servers = []

for i in hosts:
	openPorts = list(nm[i]['tcp'].keys())
	for j in openPorts:
		if nm[i]['tcp'][j]['name'] == 'ssh':
			por = j
			ssh_servers.append([i,j])
			break
		por = -1	
	addClient(i, user_name, password, por)

print "\nRunning ssh servers : "

for i in ssh_servers:
	print "Host : " + i[0] + "\t\t" + "port : " + str(i[1])
	f2.write(i[0] + ":" + str(i[1]) + '\n')

f2.close()	

while True:
	strr = colored('ssh@botnet:~$ ', 'red', None, ['bold'])
	a = raw_input(strr)

	if a == "exit()" or a == "exit":
		f.close()
		break;
	else:	
		botnetCommand(a)
	
	

#run commands as root
#botnetCommand('sh login.sh')#change login.sh to do certain task

#botnetCommand('ls')
 