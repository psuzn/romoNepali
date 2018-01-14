pip_modules=["requests","time","sys","subprocess","pynput"]
pip_installInstructions=["1.Install pip in your system",
						 "2.Run the following command from the uni-nepal directory",
						 "\tpip install -r requirements.txt",
						 "\t(try with sudo if any error occurred)"]
npm_modules=["http","querystring"]
npm_installInstructions=["1.Install node and npm in your system",
						 "2.Run the following command from the uni-nepal directory",
						 "\tcat requirements-npm.txt | xargs npm install -g",
						 "\t(try with '..| sudo xargs..' if any error occurred)"]
try:
	import requests,time,sys
	import subprocess as sp
	from pynput.keyboard import Key, Controller,Listener
except ImportError: #detection of modules
	print("Some modules are not installed")
	print("[Required modules for python]:")
	for module in pip_modules:
		print(" {}".format(module))
	print("\n#process to install")
	for line in pip_installInstructions:
		print(" {}".format(line))
	exit()

keyboard =Controller()
port=1234 #port for the node server
emulated=False #to detect the emulated key presses
smartConvert=True; #smart convert
rawKeys="" #the unconverted keystrokes
unicodeTyped=0 #track of unicode letter tyoed to handel the backsoace and other
first=True #in some browser(chrome backspace has to be typed twice for first letter)
noOfSpaces=0 #track for no of space typed  for detection of emulated backspace key
noOfBackSpaces=0  #track for no of backspace space typed  for detection of emulated backspace key
vv=False #verbosa output
nodeServer=""; #node server child process

def mvv(*message): #print the message if -v flag is given 
	if(vv):
		print(message)

def startNodeServer(): #start the node server without any logging on console
	global nodeServer
	nodeServer=sp.Popen(["node","uni.js"],stdout=sp.PIPE,stderr=sp.PIPE,encoding='utf-8')

def typeUnicode(code): #tyoe the unicode character corresponding to unicode value with Ctrl+Shift+u and unicode value (in hex)
	keyboard.press(Key.ctrl)
	keyboard.press(Key.shift)
	keyboard.type("u")
	keyboard.release(Key.ctrl)
	keyboard.release(Key.shift)
	keyboard.type(str(hex(code).split('x')[-1]))
	keyboard.press(Key.ctrl)
	keyboard.release(Key.ctrl)
	
def typeRegular(key):
	keyboard.type(key) 

def pressBackspace(no=1): #just press backspace noof time
	global noOfBackSpaces
	for i in range(0,no):
		keyboard.press(Key.backspace)
		noOfBackSpaces+=2 #why?,i dont know but one backspace press is is registered as 2 
		keyboard.release(Key.backspace)




def typeConverted(): #convert the rawinput to corresponding unicode value and type it
	global unicodeTyped,emulated
	try:
		r = requests.post("http://localhost:{}".format(port), data={"smartConvert":smartConvert,"data":rawKeys}) #request for thr node server
		pressBackspace(no=unicodeTyped)
		unicodeTyped=0;
		for c in r.text.split("#"):
			if "¬" in c:
				unicodeTyped+=1
				typeUnicode(int(c.split("¬")[1]))
			else:
				if len(c)>0:
					for key in c:
						unicodeTyped+=1
						lastRegularkey=c;
						typeRegular(c)

	except: 
		print("error occurred")
		raise KeyboardInterrupt


def on_release(key): #it get called once a key is released
	global rawKeys,unicodeTyped,emulated,noOfSpaces,noOfBackSpaces

	if noOfSpaces>0 and key is Key.space: #avoid emulated space
		noOfSpaces=noOfSpaces-1
		mvv("emulated key:",str(key))
		return True

	if noOfBackSpaces>0 and key is Key.backspace: #avoid emulated backspace
		noOfBackSpaces=noOfBackSpaces-1
		mvv("emulated key:",str(key))
		return True


	if emulated: #avoid all emulated character keys
		mvv("emulated key:",str(key))
		return True

	emulated=True
	if nodeServer.poll() is not None: #check is node server is running or not
		print(" node server is not running\n   exiting..  ")
		exit() #exit is not runnong

	if type(key) is not Key: #clear the rew key 
		pressBackspace(1) 


	if key is Key.backspace: 
		mvv("backspace is pressed handelling it")
		rawKeys=""
		unicodeTyped=0;

	if type(key) is not Key or key is Key.space: #reset the rawinput after space key
		if key is Key.space:
			rawKeys=""
			unicodeTyped=0;
		else:
			rawKeys+=str(key)[1] 
			typeConverted() #convert the rawinput to corresponding unicode value and type it

	emulated=False


def main():
	global vv
	print("started listning..")
	if "-v" in sys.argv[1:]: #if -v flag is set or not
		vv=True
	with Listener(on_release=on_release) as listener: #listen the keypresses
		listener.join()

try:
	if __name__ == '__main__':
		print("starting a node nodeServer at {} ".format(port))
		startNodeServer() #start the nodeserver
		time.sleep(0.5)
		if nodeServer.poll() == None: #check if node server is started
			print("  started.. ")
			main()
		else:
			print(" node server can't be started\n required modules might not be installed ..  ")
			print("[Required modules for node]:")
			for module in npm_modules:
				print(" {}".format(module))
			print("\n#process to install")
			for line in npm_installInstructions:
				print(" {}".format(line))
			exit()

except KeyboardInterrupt:
	keyboard.release(Key.ctrl)
	keyboard.release(Key.shift)
	keyboard.release(Key.enter)
	keyboard.release(Key.backspace)

finally:
	if nodeServer.poll() is None:
		nodeServer.terminate() #if any error occurred kill the nodeserver