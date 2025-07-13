import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
my_mail = "devagyagoyal7564@gmail.com"
auth_key = os.environ["AUTH_KEY_FOR_MAIL"]
st.title(" ╰(*°▽°*)╯ 📤Python Email Sender")

to_addrs = st.text_input(label="Enter The receiver's EMAIL:")
subject = st.text_input(label="Enter the Subject of the mail:")
content = st.text_area(label="Enter the Content of the mail:")

uploaded_file = st.file_uploader("Upload an image (JPG, PNG, GIF, etc.)", type=["jpg", "jpeg", "png", "gif"])

if st.button(label="Submit"):
    msg = MIMEMultipart()
    msg['From'] = my_mail
    msg['To'] = to_addrs
    msg['Subject'] = subject

    msg.attach(MIMEText(content, 'plain'))

    if uploaded_file is not None:
        try:
            image_data = uploaded_file.read()
            img = MIMEImage(image_data)
            img.add_header('Content-Disposition', 'attachment', filename=uploaded_file.name)
            msg.attach(img)
            st.info(f"Image '{uploaded_file.name}' attached successfully.")
        except Exception as e:
            st.error(f"Error attaching image: {e}")
            st.stop()
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as sm:
            sm.starttls()
            sm.login(user=my_mail, password=auth_key)
            sm.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        st.error("Authentication failed. You might have entered wrong email or App Password.")
        st.error("For Gmail, ensure you're using an App Password if 2FA is on.")
    except smtplib.SMTPConnectError:
        st.error("Could not connect to the SMTP server. Check your internet connection or server details.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    else:
        st.success(f"Email sent successfully to {to_addrs}")

