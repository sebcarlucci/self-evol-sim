# async_msg.py
import time
import threading
from multiprocessing import Queue

'''
Behaviour of the abstract_async_msg_objects
'''
class AbstractAsyncMsgObject():
	def __init__(self):
		pass

	def receive(self):
		pass

	def send(self, msg, msg_q):
		pass

	def start(self):
		raise NotImplementedError()

	def handle_msg(self, msg):
		pass

	def get_msg_q(self):
		pass

'''
Module responsible of relaying messages to other AsyncMsgOperators.
'''
class AsyncMsgController(AbstractAsyncMsgObject):

	valid_id = [	 			 \
				'UI-Engine', 	 \
				'Sim-Engine'     \
			   ]

	def __init__(self):
		self.__msg_q = Queue()		
		self.operator_map = {}
		self.operator_map['Controller'] = self

	def start(self):
		self.receive()

	def receive(self):
		while True:
			# Blocks until message is received	
			id,msg = self.__msg_q.get(block=True)
			self.relay(msg_payload=msg, msg_to=id)

	def send(self, msg, msg_q):
		msg_q.put(msg)

	def handle_msg(self, msg):
		msg_from, msg_to, msg_payload = self.decode(msg)
		self.relay(msg_payload, msg_to)

	def relay(self, msg_payload, msg_to):
		rcv_opersator = self.operator_map[msg_to]
		self.send(msg_payload, rcv_opersator.get_msg_q())

	def assign_operator(self, op_id, op):
		self.operator_map[op_id] = op

	def build_operator(self, op_id):
		if op_id not in self.valid_id:
			raise IllegalArgumentException()
		op = AsyncMsgOperator()
		self.operator_map[op_id] = op
		return op

	def send_to(self, op_id, msg):
		to_op = self.operator_map[op_id]
		to_q = to_op.get_msg_q()
		self.send(msg, to_q)

	def get_msg_q(self):
		return self.__msg_q
		
class AsyncMsgOperator(AbstractAsyncMsgObject):

	def __init__(self):
		self.__msg_q = Queue()	
		
	def receive(self):
		while True:
			msg = self.__msg_q.get(block=True)
			self.handle_msg(msg)

	def send(self, msg, msg_q):
		msg_q.put(msg)

	def start(self):
		self.receive()

	def set_msg_handler(self, handler):
		self.handler = handler

	def handle_msg(self, msg):
		self.handler(msg)

	def get_msg_q(self):
		return self.__msg_q

'''
Runs an AbstractAsyncMsgObject in a separate Thread
'''
class AsyncMsgThread(threading.Thread):
	
	def __init__(self, async_msg_object, controller):
		self.async_msg_object = async_msg_object
		self.controller = controller
		super().__init__()

	def run(self):
		self.async_msg_object.start()

	def send_msg(self, id, msg):
		self.async_msg_object.send((id, msg), self.controller.get_msg_q())
		time.sleep(0.001)


