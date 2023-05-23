from tweeter import bootstrap


def get_message_bus():
    bus = bootstrap.bootstrap()
    return bus
