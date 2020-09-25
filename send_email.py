import smtplib
import os
from email.message import EmailMessage
from env import set_env

# Get email information
set_env()
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_email(date, content):

    # Get email content
    artists_top_listeners, artists_popularity = content

    # Write message
    msg = EmailMessage()
    msg['Subject'] = 'Spotify Top 10 Artists ' + date.replace('-', ' ')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content('Please abilitate HTML to get a better looking result.')
    # Create HTML message
    html_top_artists = ' '.join([f'<tr><td>{i[0]}</td><td>{i[1]}</td></tr>' for i in artists_top_listeners])
    html_popularity_artists = ' '.join([f'<tr><td>{i[0]}</td><td>{i[1]}</td></tr>' for i in artists_popularity])
    msg.add_alternative(f'''\
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    h1, td, h3 {{
                        text-align: center;
                    }}
                    h1 {{
                        margin-top: 0;
                        margin-bottom: 0;
                    }}
                    h3 {{
                        margin-top: 0;
                    }}
                    table, th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                    }}
                    table {{
                        margin-left: auto;
                        margin-right: auto;
                    }}
                    th, td {{
                        padding: 10px;
                        color: white;
                        background-color: black;
                    }}
                    .table-container {{
                        padding: 30px;
                        margin: 30px;
                        border: 3px solid black;
                        background-color: #158467;
                    }}
                </style>
            </head>
            <body>
                <div>
                    <div class='table-container'>
                        <h1>Top Artists by monthly listeners</h1>
                        <h3>{date.replace('_', ' ')}</h3>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Position</th>
                            </tr>
                            {html_top_artists}
                        </table>
                    </div>
                    <br>
                    <div class='table-container'>
                        <h1>Top Artists by popularity</h1>
                        <h3>{date.replace('_', ' ')}</h3>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Popularity</th>
                            </tr>
                            {html_popularity_artists}
                        </table>
                    </div>
                </div>
            </body>
        </html>
    ''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # Send email
        smtp.send_message(msg)
        print('\nEmail sent.\n')