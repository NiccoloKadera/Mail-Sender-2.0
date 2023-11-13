from email.utils import formataddr
from CommonFunct import CF
from functions import Mail
from functions import HTMLMailBuilder
from functions import memoryHandler
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib
import time
import os
from imaplib import IMAP4
import email
import imaplib



class MailSender:

    __version = "2.0"

    def __init__(self) -> None:
        
        # Dict
        self.__lang = 'Eng'.title()
        self.__data_dict = CF.jsonLoader(f"mailInfo{self.__lang}.json")
        self.__langDict = CF.jsonLoader(f"lang{self.__lang}.json")
        self.__userInfoDict = CF.jsonLoader("userInfo.json")

        #Params
        self.__myEmail = self.__userInfoDict["myEmail"]
        self.__formatEmail = formataddr((self.__userInfoDict["name"], self.__userInfoDict["myEmail"]))
        self.__email_pass = self.__userInfoDict["gmailPass"]
        self.__replyEmail = formataddr((self.__userInfoDict["name"], self.__userInfoDict["myEmail"]))
        self.ExitMail = Mail()
        self.ExitMail.sendedFrom = self.__myEmail
        

        print('''
              

     _  _   __  .       ___  __       _    __  __      .    .  ___
    | \/ | |__| | |     |__ |__ |\ | | \  |__ |__|      \  /   ___|
    |    | |  | | |__   __| |__ | \| |__| |__ | \        \/   |___
    
    By Niccolò Kadera
              ''')
        self.mem = memoryHandler()
        print(self.__langDict['47'] + str(self.mem.strTime(self.mem.startTime)))
        print(self.__langDict['49'] + str(MailSender.__version))
        self.mem.version = MailSender.__version

        if self.__myEmail == "" or self.__myEmail.isspace() or self.__email_pass == "" or self.__email_pass.isspace() or self.__userInfoDict["name"] == "" or self.__userInfoDict["name"].isspace():
            print(self.__langDict['57'])
            self.conf_minimum = False
        else:
            self.conf_minimum = True

    def compileMail(self):
        mail = Mail()
        mail.importInfo()
        self.ExitMail = mail
        return mail
    
    def sendHTMLMail(self, mail: Mail) -> None:
        em = MIMEMultipart()
        em["From"] = self.__formatEmail
        em["Subject"] = mail.subject
        em.add_header('reply-to', self.__replyEmail)
        
        htmlPart = MIMEText(mail.MailContent, "html")
        em.attach(htmlPart)

        if len(mail.attachmentsFullEncodedArr) > 0:
            for i, item in enumerate(mail.attachmentsFullEncodedArr):
                print("Adding attachments: %d..." % (i + 1))
                em.attach(MIMEText("Allegati:", "plain"))
                em.attach(item)
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.__myEmail, self.__email_pass)
        print("\n\n - Log in Success")
        if len(mail.attachmentsFullEncodedArr) > 0:
            print(' - ' + self.__langDict['26'])

        em["To"] = ""
        for email in mail.recEmailsArr:
            em.replace_header("To", email)
            server.sendmail(self.__myEmail, email, em.as_string())
            print("\n -> Email inviata a %s." % email)
        print()
        time.sleep(0.5)

    def sendCurrentLoadedMail(self):
        self.sendHTMLMail(self.ExitMail)
    
    def attachmentsMenu(self):
        add_att_dec = CF.Menu_Bool(self.__langDict['18'], [self.__langDict['19'], self.__langDict['20']], 1, self.__langDict['15']) # If True -> Add attachments
        if add_att_dec:
            add_att_dec_two = CF.Menu_Bool(self.__langDict['12'], [self.__langDict['21'], self.__langDict['22']], 1, self.__langDict['15']) # If True -> Add attachments
            if add_att_dec_two:
                attList = CF.Menu_Text(self.__langDict['23']).splitlines()
                self.ExitMail.addMultipleAttachments(attList)
                print(self.__langDict['25'] + str(attList))
            else:
                attList = self.ExitMail.attachments_addAll()
                print(self.__langDict['24'] + str(attList))
            self.ExitMail.attachmentFullEncodedArrCompile()


    def mailReader(self, mailFrom = "ALL"):
        imapUrl = "imap.gmail.com"
        connection = imaplib.IMAP4_SSL(imapUrl)
        connection.login(self.__myEmail, self.__email_pass)
        connection.select('Inbox')
        if mailFrom == "ALL":
            mail_id_list_byte = connection.search(None, 'ALL')[1][0]
        else:
            mail_id_list_byte = connection.search(None, 'FROM', mailFrom)[1][0]
        mail_id_list_str = str(mail_id_list_byte)
        mail_id_list_str = mail_id_list_str[:-1][2:].split(" ")

        if len(mail_id_list_str) > 1 or mail_id_list_str[0] != "":
            mail_id_list = [int(id) for id in mail_id_list_str]
            mail_id_list.reverse()
            
            recent_mails = []

            msgs = []
            for i in range(0, len(mail_id_list)):
                if i < 10:
                    mail_id = mail_id_list[i]
                    typ, data = connection.fetch(str(mail_id), '(RFC822)')
                    msgs.append(data)

            for msg in msgs[::-1]:
                for response_part in msg:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        try:
                            mail_from = str(msg['from']).split("<")[1].split(">")[0]
                        except Exception:
                            mail_from = msg['from'].splitlines()[0]
                        mail_subject = msg['subject']
                        mail_date = msg['date']
                        mail_body = ""
                        for part in msg.walk():
                            if part.get_content_maintype() == 'text' or part.get_content_maintype() == 'plain':
                                mail_body = part.get_payload().replace('<div dir="auto">', "")
                        
                        msg_dict = {"From": mail_from, "Subject": mail_subject, "Date": mail_date, "Body": mail_body}
                        recent_mails.append(msg_dict)
                        

            recent_mails_formatted = []
            for mail in recent_mails:
                mail_formatted = f" -From: {mail['From']} -Subject: {mail['Subject']} -Date: {mail['Date']} -Body: {mail['Body'][:8]}..."
                recent_mails_formatted.append(mail_formatted)
            return {"recent_mails": recent_mails, "recent_mails_formatted": recent_mails_formatted}
        else:
            return {"recent_mails": "", "recent_mails_formatted": ""}

    def menuWrapper(self):
        mail_is_sent = False
        if self.conf_minimum:
            buildOrSelect = CF.Menu_Bool(self.__langDict['12'], [self.__langDict['13'], self.__langDict['14']], 1, self.__langDict['15']) # If True -> Select existing email
            if buildOrSelect:
                newOrImport = CF.Menu_Bool(self.__langDict['12'], [self.__langDict['27'], self.__langDict['28']], 1, self.__langDict['15']) # If True -> Build new mail
                if newOrImport:
                    self.ExitMail.basicInfoUserWrapper()
                    HTMLMail = HTMLMailBuilder()
                    mail_content = HTMLMail.builderMenu()
                    self.attachmentsMenu()
                    self.ExitMail.MailContent = mail_content
                    self.ExitMail.webbBrowserViewer(True)
                    send_dec = CF.Menu_Bool(self.__langDict['44'], [self.__langDict['19'], self.__langDict['20']], 1, self.__langDict['15']) # If True -> Send mail
                    if send_dec:
                        self.sendCurrentLoadedMail()
                        mail_is_sent = True
                    else:
                        print(self.__langDict['36'])
                else:
                    self.ExitMail.importInfo()
                    print(self.ExitMail)
                    self.ExitMail.webbBrowserViewer(False)
                    send_dec = CF.Menu_Bool(self.__langDict['35'], [self.__langDict['19'], self.__langDict['20']], 1, self.__langDict['15']) # If True -> Send mail
                    if send_dec:
                        self.sendCurrentLoadedMail()
                        mail_is_sent = True
                    else:
                        print(self.__langDict['36'])
            else:
                
                recent_mails_t = self.mailReader(input(self.__langDict['16']))
                recent_mails_f = recent_mails_t["recent_mails_formatted"]
                recent_mails = recent_mails_t["recent_mails"]
                EmailSelect_i = CF.Menu_Int(self.__langDict['12'], recent_mails_f, self.__langDict['15']) # If True -> Select existing email
                EmailSelect = recent_mails[EmailSelect_i - 1]
                

                HTMLMail = HTMLMailBuilder()

                HTMLMail.addResponse(EmailSelect["From"], EmailSelect["Subject"], EmailSelect["Date"], EmailSelect["Body"])
                mail_content = HTMLMail.builderMenu()

                self.ExitMail.recEmailsArr = [EmailSelect["From"]]
                self.ExitMail.MailContent = mail_content
                if "re" in EmailSelect["Subject"].lower():
                    self.ExitMail.subject = EmailSelect["Subject"]
                else:
                    self.ExitMail.subject = "Re: " + EmailSelect["Subject"]
                
                self.attachmentsMenu()
                self.ExitMail.webbBrowserViewer(True)
                send_dec = CF.Menu_Bool(self.__langDict['44'], [self.__langDict['19'], self.__langDict['20']], 1, self.__langDict['15']) # If True -> Send mail
                if send_dec:
                    self.sendCurrentLoadedMail()
                    mail_is_sent = True
                else:
                    print(self.__langDict['36'])

        print(self.__langDict['48'] + str(self.mem.strTime(self.mem.stopTimeUpdate())) + '\n')

        if mail_is_sent:
            self.mem.addMail(self.ExitMail)
            self.mem.memoryUpdate()

        
        