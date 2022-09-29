from datetime import timedelta, datetime
from database import Database
from send_email import Message, AutoEmail


class DateFormatError(Exception):
    """Exception when date format is wrong"""


class Reminder:
    def __init__(self, database : Database):
        self.database = database
        self.database.check_if_exist()

    def show_all_entries(self):
        return self.database.get_content()

    def add_entry(self, entry : dict):
        self.database.put_content(entry['name'], entry['mail'], entry['book_name'], entry['date'])

    def remove_entry(self, id = str):
        self.database.delete_content(id=id)

    def check_if_late(self):
        entries = self.show_all_entries()
        for entry in entries:
            try:
                entry_date = datetime.strptime(entry['date'], '%Y-%m-%d')
                if datetime.now() - entry_date > timedelta(days = 30):
                    yield entry['mail']
            except ValueError as exception:
                raise DateFormatError(f'Wrong date format in {entry}') from exception

    def send_remind(self, args=None):
        reminder_recipients = []
        if args:
            for arg in args:
                reminder_recipients.append(self.database.get_content(column='mail', id = arg)[0])
        else:
            reminder_recipients.append(self.database.get_content())

        for recipient in reminder_recipients:
            recipiend_address = recipient['mail']
            recipient_name = recipient['name']
            recipient_book = recipient['book_name']
            message = f"""Hi {recipient_name}, you have my book '{recipient_book}'. Please bring it back to me"""

            mail = Message(recipiend_address, message).create_message()

            with AutoEmail() as mail_box:
                if mail_box.send_message(mail):
                    yield f"Failure send mail to: {mail['to']}"
                else:
                    yield f"Correct send mail to: {mail['to']}"

if __name__ == '__main__':
    reminder = Reminder(Database('entries.db'))
    while True:
        choice = int(input("""
        1. Show all entries
        2. Send email to every late
        3. Add entry
        4. Delete entry
        5. Exit
        """))

        if choice == 1:
            entries = reminder.show_all_entries()
            for entry in entries:
                print(f"{entry['name']} has book {entry['book_name']} since {entry['date']}")

        if choice == 2:
            try:
                emaill = reminder.check_if_late()
                confirm = reminder.send_remind(emaill)
                for conf in confirm:
                    print(conf)   
            except DateFormatError as err:
                print(err)

        if choice == 3:
            name = input('Your name: ')
            email = input('Email: ')
            book = input('Book title: ')
            date = input('From(yyyy-mm-dd): ')
            reminder.add_entry({'name' : name, 'mail' : email, 'book_name' : book, 'date' : date})

        if choice == 4:
            entries = reminder.show_all_entries()
            for entry in entries:
                print(f"{entry['id']}, {entry['name']}, {entry['book_name']}")
            choice = input('Which one? ')
            reminder.remove_entry(choice)

        if choice == 5:
            break