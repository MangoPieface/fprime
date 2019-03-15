#!/usr/bin/python

import sys
import subprocess
import os
import time
import signal
from optparse import OptionParser

def main(argv=None):
    
    python_bin = "python"
    
    build_root = os.environ["BUILD_ROOT"]
    
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", action="store", type="int", help="Set the threaded TCP socket server port [default: %default]", default=50000)
    parser.add_option("-a", "--addr", dest="addr", action="store", type="string", help="set the threaded TCP socket server address [default: %default]", default="localhost")
    parser.add_option("-n", "--nobin", dest="nobin", action="store_true", help="Disables the binary app from starting [default: %default]", default=False)
    parser.add_option("-t", "--twin", dest="twin", action="store_true", help="Runs Threaed TCP Server in window, otherwise backgrounds [default: %default]", default=False)

    (opts, args) = parser.parse_args(argv)
    used_port = opts.port
    #nobin = opts.nobin
    addr = opts.addr
    twin = opts.twin
#     print 'nobin =', nobin
#     print 'port = ', used_port
#     print 'addr = ', addr 

    # run ThreadedTCPServer
    if twin:
        TTS_args = [python_bin,"%s/Gse/bin/pexpect_runner.py"%build_root,"ThreadedTCP.log","Threaded TCP Server",python_bin,"%s/Gse/bin/ThreadedTCPServer.py"%build_root,"--port","%d"%used_port, "--host",addr]
        TTS = subprocess.Popen(TTS_args)
    else:
        tts_log = open("ThreadedTCP.log",'w')
        TTS_args = [python_bin, "-u", "%s/Gse/bin/ThreadedTCPServer.py"%build_root,"--port","%d"%used_port, "--host",addr]
        TTS = subprocess.Popen(TTS_args,stdout=tts_log,stderr=subprocess.STDOUT)
    
    # wait for TCP Server to start
    time.sleep(2)
    
    # run Gse GUI
    GUI_args = [python_bin,"%s/Gse/bin/gse.py"%build_root,"--port","%d"%used_port,"--dictionary","%s/Gse/generated/Ref"%build_root,"--connect","--addr",addr,"-L","%s/Ref/logs"%build_root]
    #print ("GUI: %s"%" ".join(GUI_args))
    GUI = subprocess.Popen(GUI_args)
    
    GUI.wait()

    try:
        TTS.send_signal(signal.SIGINT)
    except:
        pass
        
    try:
        TTS.wait()
    except:
        pass
            
    # Run Gse interface
    
            
         

if __name__ == "__main__":
    sys.exit(main())
