import time

import pika
import json
import threading

from api_games.src.player.event.parser import PlayerEventsParser


class PlayerEventsHandler(threading.Thread):
    """ Class represents handler for Player events.
    Child of threading.Thread class so could be used
    as other thread for handling events in background.
    """

    def __init__(self, url: str = 'amqp://guest:guest@rabbitmq/%2f', queue_name: str = 'players_events_queue', no_connections_tries: int = 5):
        super(PlayerEventsHandler, self).__init__()

        self._is_interrupted = False
        # self._service_url = 'amqps://gtqxiusc:EWfENRrRkc8Dko7dWDQPyTRX4jGy0k6z@sparrow.rmq.cloudamqp.com/gtqxiusc'
        self._service_url = url
        self._queue_name = queue_name
        self._no_connections_tries = no_connections_tries
        self._validate_state()

        self._connection = self._create_queue_connection()
        self._events_parser = PlayerEventsParser()

    def _create_queue_connection(self):
        """ Create new connection to service which
            contains the message queue instance.

        Raises
        ------
        ConnectionError
            When queue service in unreachable.
        """
        for _ in range(self._no_connections_tries):
            try:
                params = pika.URLParameters(self._service_url)
                return pika.BlockingConnection(params)
            except pika.exceptions.AMQPConnectionError as exc:
                print("Could not connect to rabbitmq service. Try again after 5 seconds.")
            time.sleep(5)
        raise ConnectionError("Failed to connect to RabbitMQ service")

    def stop(self):
        self._is_interrupted = True

    def run(self):
        self.channel_ = self._connection.channel()
        self.channel_.queue_declare(queue=self._queue_name, durable=True, auto_delete=False)

        for message in self.channel_.consume(self._queue_name, inactivity_timeout=1):
            if self._is_interrupted:
                self._handle_interruption()
                break
            if not all(message):
                continue

            method, properties, body = message
            self.channel_.basic_ack(method.delivery_tag)
            self._handle_message(body)

    def _handle_interruption(self):
        """ Handle interrupt event on self """
        if self._connection.is_open:
            self._connection.close()
        if hasattr(self, 'channel_') and self.channel_.is_open:
            self.channel_.close()

    def _handle_message(self, message: bytes):
        """ Handle received message and do proper action.

        Parameters
        ----------
        message : bytes
            Received message bytes.
        """
        if not isinstance(message, bytes):
            return

        message = json.loads(message.decode('utf-8'))
        self._events_parser.parse(message)

    def _validate_state(self):
        if not isinstance(self._service_url, str):
            raise TypeError(f'Invalid type of "url" parameter. Has to be str not {type(self._service_url)}')

        if not isinstance(self._queue_name, str):
            raise TypeError(f'Invalid type of "queue_name" parameter. Has to be str, not {type(self._queue_name)}')

        if not isinstance(self._no_connections_tries, int):
            raise TypeError(f'Invalid type of "no_connections_tries" parameter. Has to be int, not {(type(self._no_connections_tries))}')

    def __del__(self):
        self.stop()
