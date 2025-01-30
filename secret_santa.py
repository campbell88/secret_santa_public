import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

participants = {
    "Shathar": {
        "email": "myemail@gmail.com",
        "previous_secret_santa": ["Justin", "Amy", "Brendan"]
    },
    "Billy": {
        "email": "bemail@gmail.com",
        "previous_secret_santa": ["Amy", "Brendan"]
    },
    "Amy": {
        "email": "aemail@me.com",
        "previous_secret_santa": ["Abbey"]
    },
    "Abbey": {
        "email": "aemail@gmail.com",
        "previous_secret_santa": ["Shathar", "Billy"]
    },
    "Brendan": {
        "email": "broemail@gmail.com",
        "previous_secret_santa": ["Jack", "Justin"]
    },
    "Justin": {
        "email": "broemail@me.com",
        "previous_secret_santa": ["Brendan", "Billy", "Shathar"]
    },
    "Jack": {
        "email": "Jemail@gmail.com",
        "previous_secret_santa": ["Billy"]
    }
}

def assign_secret_santa(participants):
    names = list(participants.keys())
    assignments = {}
    
    # Keep looping until we get a valid assignment
    while True:
        random.shuffle(names)

        can_assign = True
        for i, name in enumerate(participants):
            assignee = names[i]
            print(f"checking if {name} can be assigned to {assignee}")
            # check if the assignee has been a previous Secret Santa or is the same as the name
            if assignee in participants[name]["previous_secret_santa"] or assignee == name:
                print(f"{name} cannot be assigned to {assignee} because {assignee} is in {name}'s previous_secret_santa list or is the same as {name}")
                can_assign = False
                break
        if can_assign:
            print("Went through shuffle and all names can be assigned!!!")
            break

    # Build the final assignments
    for i, name in enumerate(participants):
        assignments[name] = names[i]
    return assignments

def send_email(to_email, secret_santa_name, your_name, your_email, your_password):
    subject = "Your Secret Santa!"
    body = f"Oh hey {your_name},\n\nYour Secret Santa assignment is: {secret_santa_name}.\n\nMerry Christmas ya filthy animal!"
    
    msg = MIMEMultipart()
    msg['From'] = your_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(your_email, your_password)
            server.sendmail(your_email, to_email, msg.as_string())
        print(f"Email sent to {to_email} for {your_name}'s Secret Santa assignment.")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

def main():
    # assign Secret Santas
    assignments = assign_secret_santa(participants)
    
    # print assignments to make sure no errors
    for giver, receiver in assignments.items():
        print(f"{giver} -> {receiver}")

    # my email info and gmail app password to void 2FA
    your_email = "myemail@gmail.com"
    your_password = ""
    

    # send the emails
    for giver, receiver in assignments.items():
        giver_email = participants[giver]["email"]
        send_email(giver_email, receiver, giver, your_email, your_password)

    # email master list to me
    organizer_email = "myemail@gmail.com"
    organizer_subject = "Secret Santa MASTER LIST"
    organizer_body = "Here are the Secret Santa assignments:\n\n" + \
                     "\n".join([f"{giver} -> {receiver}" for giver, receiver in assignments.items()]) + \
                     "\n\nPeace in the Middle East"
    send_email(organizer_email, organizer_subject, organizer_body, your_email, your_password)


if __name__ == "__main__":
    main()