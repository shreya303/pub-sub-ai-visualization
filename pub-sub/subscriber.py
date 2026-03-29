import json
import logging
from typing import Dict, Any
from datetime import datetime
from google.cloud import pubsub_v1, bigquery
import constants as const

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventSubscriber:
    def __init__(self, project_id: str, subscription_id: str):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.bq_client = bigquery.Client()

        self.subscription_path = self.subscriber.subscription_path(
            project_id, subscription_id
        )

        self.table_id = f"{project_id}.{const.DATASET}.{const.TABLE}"

    # 🔥 Core processing logic
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        flagged = False
        reason = None

        # Rule: High transaction detection
        if const.AMOUNT in event and event[const.AMOUNT] > const.THRESHOLD_AMOUNT:
            flagged = True
            reason = "High transaction amount"

        return {
            const.EVENT_ID: event.get(const.EVENT_ID),
            const.EVENT_TYPE: event.get(const.EVENT_TYPE),
            const.USER_ID: event.get(const.USER_ID),
            const.AMOUNT: event.get(const.AMOUNT),
            const.TIMESTAMP: event.get(const.TIMESTAMP),
            const.FLAGGED: flagged,
            const.REASON: reason,
            const.RAW_PAYLOAD: json.dumps(event),
        }

    # 🟣 Insert into BigQuery
    def write_to_bigquery(self, row: Dict[str, Any]) -> None:
        errors = self.bq_client.insert_rows_json(self.table_id, [row])

        if errors:
            logger.error(f"BigQuery Insert Error: {errors}")
            raise Exception("BigQuery insert failed")

    # 🔁 Callback function
    def callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        try:
            event = json.loads(message.data.decode("utf-8"))

            processed_event = self.process_event(event)

            self.write_to_bigquery(processed_event)

            logger.info(f"✅ Processed event: {processed_event[const.EVENT_ID]}")

            message.ack()

        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")
            message.nack()  # triggers retry / DLQ

    # 🚀 Start listening
    def start(self) -> None:
        logger.info("🚀 Starting subscriber...")

        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path, callback=self.callback
        )

        with self.subscriber:
            try:
                streaming_pull_future.result()
            except KeyboardInterrupt:
                streaming_pull_future.cancel()
                logger.info("Subscriber stopped")


if __name__ == "__main__":
    subscriber = EventSubscriber(const.PROJECT_ID, const.SUBSCRIPTION_ID)
    subscriber.start()
