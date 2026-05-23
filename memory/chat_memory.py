class ChatMemory:

    def __init__(self):
        self.history = []

    def add_message(
        self,
        role,
        content
    ):
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):
        return self.history

    def get_formatted_history(self):

        formatted = ""

        for message in self.history:
            formatted += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return formatted
    
    def get_recent_history(
        self,
        limit=4
    ):

        recent_messages = self.history[-limit:]

        formatted = ""

        for message in recent_messages:

            formatted += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return formatted