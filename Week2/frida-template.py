import frida
import sys
import time

sol = 2653079950

def on_message(message, data):
	print(message)

def on_detached_with_reason(reason):
    global done
    assert reason == 'process-terminated'
    done = True

pid = frida.spawn("./be-quick-or-be-dead-3")
print("pid =", pid)
session = frida.attach(pid)

retvalue = 2031515575192820568

script = session.create_script("""
'use strict';
Interceptor.replace(ptr('0x00400706'), new NativeCallback(function() {
	return 2653079950;
},'int64', []));

""")


script.on('message', on_message)

done = False

session.on('detached', on_detached_with_reason)

script.load()
frida.resume(pid)
while not done:
    time.sleep(1)
