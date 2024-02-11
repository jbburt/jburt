# Observer Pattern


class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received message: {message}")


class Publisher:
    def __init__(self):
        self.subscribers = set()

    def register(self, subscriber):
        self.subscribers.add(subscriber)

    def unregister(self, subscriber):
        self.subscribers.discard(subscriber)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)


if __name__ == "__main__":
    pub = Publisher()

    alice = Subscriber("Alice")
    bob = Subscriber("Bob")

    pub.register(alice)
    pub.register(bob)

    pub.notify("Breaking News! Water is wet.")
