from confluent_kafka import Producer
import argparse, json

class KafkaProducer:

    def delivery_callback(self, err, msg):
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

    def produce_file_contents(self, file_path):
        producer_conf = {'bootstrap.servers': 'localhost:9092'}
        producer = Producer(producer_conf)
        topic = 'my_topic'
        with open(file_path, "r") as file:
            string_contents = file.read()
            string_contents.replace("'", "\"")
            data = json.loads(string_contents)

        for data_points in data:
            message = json.dumps(data_points)
            producer.produce(topic, key=None, value=message)

        end_message = "End"
        producer.produce(topic, key=None, value=end_message)
        producer.flush()

if __name__ == "__main__":
    kafka_producer = KafkaProducer()
    parser = argparse.ArgumentParser(description='Produce contents of a file to Kafka')
    parser.add_argument('file_path', help='Path to the file containing JSON data')
    args = parser.parse_args()

    kafka_producer.produce_file_contents(args.file_path)
