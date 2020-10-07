class Message(object):
    seats_available = True
    batch_available = True
    slot_available = True

    @staticmethod
    def seats_fail():
        Message.seats_available = False

    @staticmethod
    def seats_success():
        Message.seats_available = True

    @staticmethod
    def batch_fail():
        Message.batch_available = False

    @staticmethod
    def batch_success():
        Message.batch_available = True

    @staticmethod
    def slot_fail():
        Message.slot_available = False

    @staticmethod
    def slot_success():
        Message.slot_available = True