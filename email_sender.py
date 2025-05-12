import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os

def clean_html(content):
    """
    Function to clean up the HTML content for email formatting.
    This version ensures proper tag handling and removes unnecessary tags.
    """
    # Remove all tags except for allowed ones: p, ul, li, strong, em, code, pre, br
    content = re.sub(r'<(?!p|ul|li|ol|strong|em|code|pre|br)[^>]*>', '', content)

    # Clean up broken or redundant <p> tags
    content = re.sub(r'<p>\s*</p>', '', content)  # Remove empty <p> tags
    content = re.sub(r'</p>\s*<p>', '<p>', content)  # Fix consecutive <p> tags
    
    # Remove redundant or broken <br> tags from the content
    content = re.sub(r'<br\s*/?>', '<br>', content)  # Standardize <br> tags
    content = re.sub(r'\n+', ' ', content)  # Remove any unnecessary line breaks
    
    # Fix nested <strong> tags
    content = re.sub(r'<strong>([^<]+)<strong>', r'<strong>\1</strong>', content)
    content = re.sub(r'</strong><strong>', '</strong>', content)

    # Clean multiple spaces into one space
    content = re.sub(r'\s+', ' ', content)

    return content



def send_email(problem_details, hint, recipient_email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Clean the HTML content
    description_html = clean_html(problem_details['content'])

    # Email credentials and server
    sender_email = "aamirbaugwala@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"🚀 LeetCode Challenge of the Day: {problem_details['title']}"

    # Build the HTML body
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <h2>🌟 LeetCode Daily Problem: <strong>{problem_details['title']}</strong></h2>
        <p><strong>📊 Difficulty:</strong> {problem_details['difficulty']}</p>
        <hr>
        <div style="padding: 10px; background-color: #f8f8f8; border-radius: 5px;">
          {description_html}
        </div>
        <hr>
        <p>🧠 <strong>Hint:</strong> {hint}</p>
        <p>💪 Keep pushing your limits! One problem a day keeps the bugs away 🐛💻</p>
        <p>🔥 You've got this, coder! See you at the top! 🚀</p>
      </body>
    </html>
    """

    # Attach the HTML content
    msg.attach(MIMEText(html, 'html'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

