# async_msg_controller.py

import asyncio

async def consumer():
	v = await __msg_q.get()
	print('consumed ', v)

__loop = asyncio.get_event_loop()
__msg_q = asyncio.Queue(loop=__loop)
__loop.create_task(consumer())
__loop.run_until_complete()
def test():
	for i in range(0,100):
		__loop.run_until_complete(send_async_msg(1))
		print('h')

async def send_async_msg(msg_type, **kwargs):
	while True:
		l = 1
	await __msg_q.put(1)



if __name__ == '__main__':
	print('starting')
	test()
	test()
