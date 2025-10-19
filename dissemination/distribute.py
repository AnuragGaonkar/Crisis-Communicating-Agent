class DisseminationSystem:
    def __init__(self):
        self.channels = ["email", "sms", "social_media"]

    def distribute(self, message, channel):
        if channel not in self.channels:
            raise ValueError("Unsupported dissemination channel")
        return f"Message sent via {channel}: {message}"
