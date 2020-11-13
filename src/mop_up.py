import json
import os
from google.cloud import pubsub_v1


def server_down(config):

    payload = config.get("pubsub_payload")

    project_id = config.get("gcs_project_id")
    topic_id =  config.get("gcs_topic_id")

    publisher = pubsub_v1.PublisherClient()

    topic_name = f"projects/{project_id}/topics/{topic_id}"

    publisher.publish(topic_name, json.dumps(payload).encode())
