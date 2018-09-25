compile:
	python3.7 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. message.proto


test:
	python3 server.py
   	python3 client.py
requirements:	
	pip3 install -r requirements.txt
