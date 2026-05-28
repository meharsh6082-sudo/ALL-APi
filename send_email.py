import os
import resend


def get_api_key():
    # It is best to use an environment variable for your API key.
    return os.getenv("RESEND_API_KEY") or "re_NuKaHP6n_Ekg1WtHHTYLWTBv9mgRW1uwk"


def send_email(to_email, subject, html=None, text=None, from_email="onboarding@resend.dev"):
    resend.api_key = get_api_key()

    payload = {
        "from": from_email,
        "to": to_email,
        "subject": subject,
    }

    if html:
        payload["html"] = html
    if text:
        payload["text"] = text

    return resend.Emails.send(payload)


def send_default_welcome():
    print("Sending default welcome email...")
    response = send_email(
        to_email="meharsh6082@gmail.com",
        subject="Hello World",
        html="<p>Congrats on sending your <strong>first email</strong>!</p>",
    )
    print("Email sent! Response:", response)


def send_custom_email():
    to_email = input("Enter recipient email: ").strip()
    subject = input("Enter subject: ").strip()
    body_type = input("Choose body type (1=HTML, 2=Plain text): ").strip()

    if body_type == "2":
        text = input("Enter plain text body: ").strip()
        response = send_email(to_email=to_email, subject=subject, text=text)
    else:
        html = input("Enter HTML body: ").strip()
        response = send_email(to_email=to_email, subject=subject, html=html)

    print("Email sent! Response:", response)


def main():
    print("Resend Email Sender")
    print("1. Send default welcome email")
    print("2. Send custom email")
    print("3. Exit")

    while True:
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            send_default_welcome()
        elif choice == "2":
            send_custom_email()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
