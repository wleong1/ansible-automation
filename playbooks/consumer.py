from confluent_kafka import Consumer, KafkaException
import json

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}
def receive_data():
    consumer = Consumer(consumer_conf)

    topic = ['my_topic']
    consumer.subscribe(topic)

    missing_data = []
    producing = True
    while producing:
        try:
            msg = consumer.poll(timeout=1000)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    print(f'Got end of partition event for {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')
                    continue
                else:
                    print(f'Error: {msg.error()}')
                    break
            message = msg.value().decode("utf-8")
            if message == "End":
                producing = False
                break
        except KeyboardInterrupt:
            break
        
        data_in_dict = json.loads(message.replace("'", "\""))
        missing_data.append(data_in_dict)

    consumer.close()
    return missing_data

if __name__ == "__main__":
    result = receive_data()
    print(result)
