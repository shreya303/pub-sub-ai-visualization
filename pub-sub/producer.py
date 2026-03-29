import json
import logging
import uuid
import random
import time
from datetime import datetime, timezone
from typing import Dict, Any
import constants as const
from google.cloud import pubsub_v1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class EventProducer:
    def __init__(self, project_id: str, topic_id: str):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def generate_event(self) -> Dict[str, Any]:
        """Generate a realistic event with optional financial data."""
        event_type = random.choice(const.EVENT_TYPES)
        event = {
            const.EVENT_ID: str(uuid.uuid4()),
            const.EVENT_TYPE: event_type,
            const.USER_ID: f"user_{random.randint(1, const.USER_COUNT)}",
            const.TIMESTAMP: datetime.now(timezone.utc).isoformat(),
        }
        
        if event_type in const.FINANCIAL_EVENTS:
            event[const.AMOUNT] = round(random.uniform(50, 10000), 2)
        
        return event

    def publish_batch(self, batch_size: int = const.BATCH_SIZE) -> None:
        """Publish a batch of events."""
        events = [self.generate_event() for _ in range(batch_size)]
        futures = [
            self.publisher.publish(self.topic_path, json.dumps(event).encode("utf-8"))
            for event in events
        ]
        
        for future in futures:
            future.result()
            logger.info(f"Published message ID: {future.result()}")

    def run(self) -> None:
        """Run the producer continuously."""
        logger.info("Starting producer...")
        try:
            while True:
                self.publish_batch()
                time.sleep(const.PUBLISH_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Producer stopped")


if __name__ == "__main__":
    producer = EventProducer(const.PROJECT_ID, const.TOPIC_ID)
    producer.run()
