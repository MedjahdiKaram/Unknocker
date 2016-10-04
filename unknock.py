from os import *
from string import *
import socket
import platform
import optparse

def exist (name):
	if path.isfile(name):
		return True
	elif path.isfile(name):
		return True
	else: 
		return False

def safe_startup (_file,setup_name):
 if getuid() != 0: 
		  print 'This script must be run as root'
		  sys.exit(1) 

 if not exist("/usr/bin/"+_file):
	if platform.system()=='Linux' or platform.system()=="Unix":
		rep=["apt-get","yum","pacman","rug","zypper","emerge"," "]
		for i in rep:
				if exist("/usr/bin/"+i):
					if i==" ":
						raw_input("ERROR: Unknow reposity type. set up knock manually or move it to /usr/bin/\n")
						exit()
					elif i=="zypper":
						system ("zypper install zypper in "+_file)
						break
					elif i=="emerge":
						system ("emerge [-a] "+_file)
						break
					elif i=="rug":
						system ("rug install "+_file)
						break
					elif i=="packman":
						system ("packman -S "+_file)
						break
					elif i=="yum":
						system ("yum install "+_file)
						break
					elif i=="apt-get":
						system ("apt-get install "+_file)
						break
	else:
		raw_input("ERROR: This script must be run only in a linux/unix kernels as root")
		exit()

def nametoip (host):
 try:
	IP=socket.gethostbyname(host)
	return IP
 except:
	raw_input(host+" is not availble or can not be resolved ")	
        exit()
	

	
		
def verif_ip(adress):
	try:
	    socket.inet_aton(adress)
	    print adress+" seems to an availble ip adress"
	    verif_ip=1
	except socket.error:
	    print "invalid ip adress"
	    exit()


def ping_test (ip):
 x=0
 _path="/tmp/ping_test_result.tmp"
 system ("ping "+ip+" -c 5 > "+_path)
 _file=file(_path,'r')
 content=_file.readlines()
 _file.close()
 if len(content)>4:
  e=split (content[len(content)-2],',',4)
  if e[len(e)-2]==" 0% packet loss":
   x=1
  else:
   x=0
   print ("\nWARNING: "+ip+" adress can not be pinged cause to a bad connection, or a rules applied on icmp protocol.\n")
   raw_input("Press ENTER to try other methods or Ctrl-C to exit :")
 else:
   x=0
   system ("clear")
   print ("\nWARNING: the "+ip+" adress can not be pinged cause to a bad connection, or a rules applied on icmp protocol.\n")
   raw_input("Press ENTER to try other methods or Ctrl-C to exit :")
 return x


def scann (ip,param):
 x=0
 _path="/tmp/passive_test.tmp"
 system ("nmap "+param+" "+ip+" > "+_path)
 _file=file(_path,'r')
 content=_file.readlines()
 _file.close()
 if len(content)>5:
  e=split (content[len(content)-1],'(',4)
  e=split(e[len(e)-1],')',10)
  e=split(e[0],' ',3)
  if eval(e[0])>0:
   x=1
  else:
   x=0
   if param=="":
    print ("\nWARNING: "+ip+"  was examinated with a passive test and failed in.\n")
    raw_input("Press ENTER to try other methods or Ctrl-C to exit :")
   else:
    print ("\nSORRY: "+ip+" failed on a full scan it appear offline or unreachble.\n")
    print("\nADVISE: Verify the adress \n")
    exit()
    
 else:
   x=0
   if param=="":
    print ("\nWARNING: "+ip+"  was examinated with a passive test and failed in.\n")
    raw_input("Press ENTER to try other methods or Ctrl-C to exit :")
   else:
    print ("\nSORRY: "+ip+" failed on a full scan it appear offline or unreachble.\n")
    raw_input("\nADVISE: Verify the adress \n")
       
 return x



def is_ip_up(ip):
 x=0
 verif_ip(ip)
 if ping_test(ip)==0:
	 if scann(ip,'')==0:
	  if scann(ip,'-Pn')==0:
	   print("\nERROR: The ip adress: \""+ip+"\" appear offline or unreachble \ncheck your/his connectivitie\n")
	   x=0  
	  else:
		x=1
	 else:
		x=1
 else:
		x=1
 return x

def restarter (ip):
	if is_ip_up(ip)==0:
		ch=raw_input("Press ENTER to restart the unknocker or Ctrl-C to exit")
		system ("python /root/Desktop/unknock.py")
	else:
	 print ("\n"+ip+" is OK, let\'s go ")

def opened(ip,parameters,services):
 chemin="/tmp/opened.tmp"
 i=0

 if services!="*":
	parameters+=" -p "
	parameters+=services
 comm="nmap "+ip+" "+parameters+" | grep open > /tmp/opened.tmp" 
 system(comm)
	
 x=file(chemin,'r')
 y=x.readlines()
 x.close()
 t=''
 for i in y:
  z=split(i,' ',10)
  z=split(z[0],'/',2)
  t+=z[0]+','
 z=split(t,',',10)
 z.remove('')
 print(z)
 return z

safe_startup("knock","knock*")
system("clear")

print " _____ _____ _   _ _____ ____   _____"
print "|  ___| ____| \ | | ____/ ___| |_   _|__  __ _ _ __ ___"
print "| |_  |  _| |  \| |  _|| |       | |/ _ \/ _` | '_ ` _ \ "
print "|  _| | |___| |\  | |__| |___    | |  __/ (_| | | | | | |"
print "|_|   |_____|_| \_|_____\____|   |_|\___|\__,_|_| |_| |_|"
print "___________________________________________________________Present :\n"
print "			     THE UNKNOCKER 1.0 		"
print "____________________________________________________________________"

parser = optparse.OptionParser("usage :python unknock.py -t <target> -p <_port>"+"\nexample :python unknock.py -t www.fenec.net -p 21,8080")
parser.add_option('-t', dest='_target', type='string', help='put your target by name or ip exemple nasa.gov / 192.168.1.15')
parser.add_option('-p', dest='_port', type='string', help='put your port(s)')
(options, args) = parser.parse_args()

_port=options._port
try:
	_target=options._target
       	ip=nametoip(_target)
	restarter (ip)
except:
	print parser.usage
	ip=nametoip(raw_input("\n!!! You dont used the unknocker properly but OK, Put the target name/ip : "))
	restarter (ip)
try:
	p=_port
	if p==None:
		p=raw_input("Set ports separated by a comas \',\' or * for a random test: ")
except:
	p=raw_input("Set ports separated by a comas \',\' or * for a random test: ")


i=1024
port1=port2=port3=list()
while i<10001:
 port1.append(i)
 i+=1

i=2
while i<10:
 port1.append(10000*i)
 i+=1
k=i=j=0
while i<len(port1)-1:
 while j<len(port1):
  while k<len(port1):
   x=str(port1[i])+" "+str(port1[j])+" "+str(port1[k])
   line="knock -v "+ip+" "+x
   system(line)
   m=opened(ip,"-sS",p)
   print(m)
   if m==split(p,',',10):
	comand="echo \""+ip+" "+" knocked in "+x+" and success to open following ports "+str(m)+" \" > /tmp/result_unknocker.txt && clear"
	system(comand)
	break
	exit()
   elif (m==[]):
    comand="echo "+ip+" "+" knocked in "+x+" and following ports: "+str(split(p,',',10))+" was not opened"" >> /tmp/result_unknocker.txt && clear"
    system(comand)
   else:
    comand="echo "+ip+" "+" knocked in "+x+" and following ports was opened"+str(m)+" > /tmp/result_unknocker.txt && clear"
    system(comand)
   k+=1
  j+=1
  k=0
 i+=1
 j=0

  

