import smtplib,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv,find_dotenv
_=load_dotenv(find_dotenv())

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



def send_captche_email(receiver, captche):
    # 连接到smtp服务器
    smtp = smtplib.SMTP('smtp.163.com', 25)     # 未加密
    # 连接成功后使用login方法登录自己的邮箱
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = "【InterviewMock】注册验证码"
    # 创建MIMEMultipart对象
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = subject

    # 创建HTML邮件内容
    html = f"""\
        <html>
        <head>
            <title>Uibe Interview Mock</title>
        </head>

        <body style="background-color: rgba(0, 0, 0, 0.05);">
            <div
                style="width: 80%;background-color: #fff;margin: 40px auto;border-radius: 20px;padding: 30px;padding-top: 20px;max-height:fit-content;">
                <h1>🥳UIBE INTERVIEW MOCK 🙌</h1>
                <div
                    style="margin-top: 50px;font-weight: 600;font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
                    🤗欢迎您来到Interview Mock，以下是您的验证码</div>
                <div
                    style="margin-top: 50px;font-weight: 400;font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;color: rgba(0,0,0,0.6);">
                    复制并粘贴此验证码，注意验证码仅在接下来的 5 分钟内有效🤓。</div>
                <div
                    style="height: 80px;width: 70%;margin: 50px auto;background-color: rgba(0,0,0,0.1);border-radius: 10px;display: flex;align-items: center;justify-content: center;">
                    <h1>{captche}</h1>
                </div>
                <div
                    style="font-weight: 400;font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;color: rgba(0,0,0,0.6);">
                    如果您没有发起请求，请不要担心。您可以安全地忽略此电子邮件🔐。</div>
                <div style="font-weight: 400;color: rgba(0,0,0,0.6);font-size: small;margin-top: 10px;margin-bottom: 30px;">
                    © &nbsp;<span id="nowyear"></span> &nbsp; UIBE 𝕏 Interview Mock.</div>

            </div>
            <script>
                document.getElementById('nowyear').textContent = new Date().getFullYear();
            </script>
        </body>

        </html>
    """
    # 将HTML内容添加到MIMEMultipart对象中
    part = MIMEText(html, 'html', 'utf-8')
    msg.attach(part)

    # 连接到smtp服务器
    try:
        # 发送邮件
        smtp.sendmail(EMAIL_ADDRESS, receiver, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"邮件发送失败：{e}")
    finally:
        smtp.quit()  # 发送完毕后使用 quit 方法关闭连接





