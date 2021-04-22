<?php
// Turn on rabbit mq: go to this dir (C:\Program Files\RabbitMQ Server\rabbitmq_server-3.8.11\sbin), cmd and rabbitmq-server.bat start
// Run the receiving.php first
// To run in browser php -S localhost:8000, in browser type http://localhost:8000/sending.php
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();

$channel->queue_declare('forecast', false, false, false, false);

$msg = new AMQPMessage('weather-rainy');
$channel->basic_publish($msg, '', 'forecast');

echo " [x] Sent 'weather-rainy'\n";

$channel->close();
$connection->close();
?>