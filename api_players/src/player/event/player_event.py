import json
import pika

from api_players.src.player.models.models import Player


class PlayerEvent(object):
    """ Class responsible for adding and deleting
    players in other Microservices """

    @staticmethod
    def create(player: Player):
        message = json.dumps({
            'method': 'POST',
            'body': {
                'username': player.username
            }
        }).encode('utf-8')
        PlayerEventQueueManager().send_message(message)

    @staticmethod
    def delete(id: int):
        message = json.dumps({
            'method': 'DELETE',
            'body': {
                'id': id
            }
        }).encode('utf-8')
        PlayerEventQueueManager().send_message(message)

    @staticmethod
    def update(player: Player):
        message = json.dumps({
            'method': 'PUT',
            'body': {
                'id': player.id,
                'username': player.username
            }
        }).encode('utf-8')
        PlayerEventQueueManager().send_message(message)


class PlayerEventQueueManager(object):
    """ Class represents player event queue manager responsible for
        queue messages management. """

    def __init__(self):
        self._service_url = 'amqps://gtqxiusc:EWfENRrRkc8Dko7dWDQPyTRX4jGy0k6z@sparrow.rmq.cloudamqp.com/gtqxiusc'
        self._queue_name = 'players_events_queue'
        self._connection = self._create_queue_connection()

    def _create_queue_connection(self):
        """ Create new connection to service which
            contains the message queue instance.

        Raises
        ------
        ConnectionError
            When queue service in unreachable.
        """
        try:
            params = pika.URLParameters(self._service_url)
            return pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError as exc:
            raise ConnectionError("Failed to connect to RabbitMQ service")

    def send_message(self, message: bytes):
        """ Send message to the queue.

        Parameters
        ----------
        message : bytes
            Message to send.

        Raises
        ------
        AttributeError
            When `message` attribute type is different than allowed.
        """
        if not isinstance(message, bytes):
            raise AttributeError('Invalid type of message attribute')

        with self._connection.channel() as channel:
            channel.queue_declare(queue=self._queue_name, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=self._queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))

    def __del__(self):
        if self._connection.is_open:
            self._connection.close()
