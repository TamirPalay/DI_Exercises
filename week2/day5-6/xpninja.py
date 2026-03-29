class Phone:
    def __init__(self, phone_number):
        self.number = phone_number
        self.call_history = []
        self.messages = []
    def call(self, other_phone):
        self.call_history.append(other_phone.number)
        other_phone.call_history.append(self.number)
    def show_call_history(self):
        print(f"Call history for {self.number}:")
        for number in self.call_history:
            print(number)
    def send_message(self, other_phone, message):
        message_info = {
            'to': other_phone.number,
            'from': self.number,
            'content': message
        }
        self.messages.append(message_info)
        other_phone.messages.append(message_info)
    def show_outgoing_messages(self):
        print(f"Outgoing messages from {self.number}:")
        for message in self.messages:
            if message['from'] == self.number:
                print(f"To: {message['to']}, Message: {message['content']}")
    def show_incoming_messages(self):
        print(f"Incoming messages for {self.number}:")
        for message in self.messages:
            if message['to'] == self.number:
                print(f"From: {message['from']}, Message: {message['content']}")
    def show_messages_from(self):
        print(f"Messages received by {self.number} grouped by sender:")
        messages_by_sender = {}
        for message in self.messages:
            if message['to'] == self.number:
                sender = message['from']
                if sender not in messages_by_sender:
                    messages_by_sender[sender] = []
                messages_by_sender[sender].append(message['content'])
        for sender, messages in messages_by_sender.items():
            print(f"From: {sender}")
            for msg in messages:
                print(f"  Message: {msg}")

phone1 = Phone("123-456-7890")
phone2 = Phone("987-654-3210")
phone1.call(phone2)
phone1.send_message(phone2, "Hello, how are you?")
phone2.send_message(phone1, "I'm good, thanks! How about you?")
phone1.show_call_history()
phone1.show_outgoing_messages()
phone1.show_incoming_messages()
phone1.show_messages_from()
