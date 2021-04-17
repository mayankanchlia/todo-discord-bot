class Task:
    def __init__(self, guild, memberId, date, message):
        self.guild = guild
        self.memberId = memberId
        self.date = date
        self.message = message
        self.isCompleted = False