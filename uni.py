import requests,time
from pynput.keyboard import Key, Controller,Listener

keyboard =Controller()
port=1234
emulated=False
smartConvert=True;
rawKeys=""
unicodeTyped=0
first=True
noOfSpaces=0
noOfBackSpaces=0

def typeUnicode(code):

	global noOfSpaces
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

def pressBackspace(no=1):
	global noOfBackSpaces
	for i in range(0,no):
		keyboard.press(Key.backspace)
		noOfBackSpaces+=2
		keyboard.release(Key.backspace)




def typeConverted():
	global unicodeTyped,emulated
	try:
		r = requests.post("http://localhost:{}".format(port), data={"smartConvert":smartConvert,"data":rawKeys})
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

	except Exception as e: 
		keyboard.release(Key.ctrl)
		keyboard.release(Key.shift)
		keyboard.release(Key.enter)
		keyboard.release(Key.backspace)
		print("error occurred")






def on_release(key):
	global rawKeys,unicodeTyped,emulated,noOfSpaces,noOfBackSpaces

	if noOfSpaces>0 and key is Key.space:
		noOfSpaces=noOfSpaces-1
		print("emulated key:",str(key))
		return True

	if noOfBackSpaces>0 and key is Key.backspace:
		noOfBackSpaces=noOfBackSpaces-1
		print("emulated key:",str(key))
		return True


	if emulated:
		print("emulated key:",str(key))
		return True

	emulated=True
	if type(key) is not Key:
		pressBackspace(1)


	if type(key) is not Key or key is Key.space:
		if key is Key.space:
			rawKeys=""
			unicodeTyped=0;
		else:
			rawKeys+=str(key)[1]
			typeConverted()

	emulated=False


def main():
	print("started listning..")
	with Listener(on_release=on_release) as listener:
		listener.join()

if __name__ == '__main__':
	main()