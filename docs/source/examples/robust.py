import asyncio
import logging
import aio_pika
from aio_pika import Message
from aio_pika.robust_connection import connect


logging.basicConfig(level=logging.DEBUG)

logging.getLogger('pika.callback').setLevel(logging.INFO)
logging.getLogger('pika.channel').setLevel(logging.INFO)


async def main():
    connection = await connect()
    channel1 = await connection.channel()   # type: aio_pika.Channel
    channel2 = await connection.channel()   # type: aio_pika.Channel

    exchane1 = await channel1.declare_exchange('TEST')
    exchane2 = await channel2.declare_exchange('TEST')

    queue1 = await channel1.declare_queue('test_ch1')   # type: aio_pika.Queue
    queue2 = await channel2.declare_queue('test_ch2')   # type: aio_pika.Queue

    await queue1.bind(exchane1, 'test')
    await queue2.bind(exchane2, 'test')

    queue1.consume(print)
    queue2.consume(print)

    while True:
        try:
            await channel1.default_exchange.publish(Message(b'Test Message 1', expiration=10), routing_key='test_ch1')
            await channel2.default_exchange.publish(Message(b'Test Message 2', expiration=10), routing_key='test_ch2')
        except:
            logging.exception("Error:")
            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
