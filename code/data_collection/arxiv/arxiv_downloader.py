import xml.etree.ElementTree as ET
from easydict import EasyDict
import argparse
import queue
import subprocess
import signal
import sys
import threading
import os

THREAD_NUM = 4
CMD_TEMPLATE = "s3cmd get --recursive --skip-existing --requester-pays -q s3://arxiv/{} {} "
OUTPUT_DIR ="ArxivSrc"
ERROR_LOG = "error.log"

def xml2dict(node):
    if not isinstance(node, ET.Element):
        raise Exception("node format error.")

    if len(node) == 0:
        return node.tag, node.text

    data = {}
    temp = None
    for child in node:
        key, val = xml2dict(child)
        if key in data:
            if type(data[key]) == list:
                data[key].append(val)
            else:
                temp = data[key]
                data[key] = [temp, val]
        else:
            data[key] = val

    return node.tag, data

def check_data(yymm, start_yymm):
    if yymm > 5000 or yymm < start_yymm:
        return False
    return True


running_processes=[]
stop_event=threading.Event()
def signal_handler(signal,frame):
    print("Ctrl+C detected. Stopping all threads and processes.")
    stop_event.set()
    for process in running_processes:
        process.terminate()
    sys.exit(0)


def task(task_queue,cmd_template, output_dir, error_log):
    while not task_queue.empty() and not stop_event.is_set():
        task = task_queue.get()
        cmd = cmd_template.format(task,output_dir)
        completed_process=subprocess.Popen(cmd,shell=True,text=True)
        running_processes.append(completed_process)
        completed_process.wait()
        print(f"{task} return code:",completed_process.returncode)
        if completed_process.returncode != 0:
            with open(error_log,"a",encoding="utf-8") as f:
                f.write(task+"\n")







if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_yymm",type=str,default="2309")
    parser.add_argument("--num",type=int,default=-1)
    
    args=parser.parse_args()
    print(args)
    
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    tree = ET.parse("arXiv_src_manifest.xml")
    node = tree.getroot()
    tag, data = xml2dict(node)
    #print(data)
    data = EasyDict(data)
    dumps=[]
    for dump in data.file:
        if check_data(int(dump.yymm),int(args.start_yymm)):
            dumps.append(dump)
            
    if args.num != -1:        
        dumps = dumps[:args.num]
    
    threads=[]
    signal.signal(signal.SIGINT, signal_handler)
    print("Total Num of Dumps:",len(dumps))
    
    task_queue=queue.Queue()
    for dump in dumps:
        task_queue.put(dump.filename)
    for i in range(THREAD_NUM):
        t = threading.Thread(target=task,args=(task_queue,CMD_TEMPLATE,OUTPUT_DIR,ERROR_LOG))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("All tasks done.")


