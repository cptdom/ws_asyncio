''' heartbeat coroutine '''
import websockets
import asyncio
import json
from time import time
from asyncio import sleep as asleep
from exchange.logger import logger
from exchange.rates import Exchanger


_HEARTBEAT = json.dumps({'type': 'heartbeat'})

class Client:
    '''
    '''

    def __init__(self, server, max_gap: int=2):
        self.server = server
        self.Exchanger = Exchanger()
        self.max_gap = max_gap
        self._last_heartbeat_at = time()


    def _update_last_heartbeat(self):
        '''
        setter proxy
        '''
        self._last_heartbeat_at = time()


    def _marshal_error(self, original_message: str, error_message: str):
        response = {}
        response['type'] = 'error'
        response['id'] = original_message['id']
        response['message'] = f'Unable to convert stake. Error: {error_message}'


    async def _heartbeat_handler(self, websocket, period: int=1):
        '''
        beats out for the server and
        checks the health of the connection
        '''
        while True:
            if self._last_heartbeat_at < time()-self.max_gap:
                logger.warning('Heartbeat disappeared, reconnecting...')
                raise ConnectionError('Remote heartbeat lost!')

            logger.debug('Heartbeating out...')
            await websocket.send(_HEARTBEAT)
            await asleep(period)


    async def _receive_handler(self, websocket):
        '''
        message reception branching
        '''
        async for message in websocket:
            json_message = json.loads(message)

            match json_message.get('type'):
                case 'heartbeat':
                    logger.debug('Received heartbeat: %s', message)
                    self._update_last_heartbeat()

                case 'message':
                    logger.info('Received message: %s', message)
                    # get payload
                    received_payload = json_message.get('payload')
                    # let Exchanger do its work
                    new_payload = self.Exchanger.calculate(received_payload)
                    # if OK
                    if isinstance(new_payload, dict):
                        json_message['payload'] = new_payload
                        logger.info('Responding with message: %s', json_message)
                        await websocket.send(json.dumps(json_message))
                    # if error
                    elif isinstance(new_payload, str):
                        error_response = self._marshal_error(json_message, new_payload)
                        await websocket.send(json.dumps(error_response))

                case _ :
                    continue


    async def run(self):
        '''
        makes the mountains move
        '''
        async for websocket in websockets.connect(self.server):
            try:
                await asyncio.gather(
                    self._receive_handler(websocket),
                    self._heartbeat_handler(websocket)
                )
                await asyncio.Future()
            # automatically tries to reconnect
            except ConnectionError:
                continue
