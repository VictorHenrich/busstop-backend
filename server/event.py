from typing import Any, Callable, List, Optional, Sequence, TypeAlias
from threading import Thread
from kafka import KafkaConsumer, KafkaProducer
import logging

from utils.constants import BROKER_KAFKA_URL


CallbackType: TypeAlias = Callable[[Any], None]


class ServerConsumer(KafkaConsumer):
    def __init__(self, topic: str, default_callback: CallbackType, **kwargs: Any):
        self.__default_callback: CallbackType = default_callback

        super().__init__(topic, bootstrap_servers=BROKER_KAFKA_URL, **kwargs)

    def __start(self, callback: Optional[CallbackType]) -> None:
        cb: CallbackType = callback or self.__default_callback

        for message in self:
            cb(message)

    def start(self, callback: Optional[CallbackType] = None, wait: bool = True) -> None:
        thread: Thread = Thread(target=self.__start, args=(callback,))

        thread.start()

        if wait is True:
            thread.join()


class ServerProducer(KafkaProducer):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(bootstrap_servers=BROKER_KAFKA_URL, **kwargs)


class ServerEvents:
    def __init__(self, *consumers: ServerConsumer) -> None:
        self.__listeners: List[ServerConsumer] = [*consumers]

    def add_listener(
        self, topic: str, **params: Any
    ) -> Callable[[CallbackType], CallbackType]:
        def wrapper(callback: CallbackType) -> CallbackType:
            consumer: ServerConsumer = ServerConsumer(topic, callback, **params)

            self.__listeners.append(consumer)

            return callback

        return wrapper

    def add_consumer(self, consumer: ServerConsumer) -> None:
        self.__listeners.append(consumer)

    def run_consumers(self) -> None:
        threads: Sequence[Thread] = [
            Thread(target=listener.start, args=(None, True))
            for listener in self.__listeners
        ]

        logging.info("...Initializing  Workers...")

        logging.info(f"Total Workers: {len(threads)}")

        [thread.start() for thread in threads]

        [thread.join() for thread in threads]
