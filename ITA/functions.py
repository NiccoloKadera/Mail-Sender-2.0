from CommonFunct import CF
from email import encoders
from email.mime.base import MIMEBase
import os
import webbrowser
from datetime import datetime

class Mail:

    def __init__(self) -> None:
        self.__lang = 'It'.title()
        self.__langDict = CF.jsonLoader(f"lang{self.__lang}.json")
        self.subject = ''
        self.recEmails = ''
        self.recEmailsArr = []
        self.__data_dict_keys = [ i for i in CF.jsonLoader(f"mailInfo{self.__lang}.json")]
        self.__mailPath = ""
        self.MailContent = ""
        self.sendedFrom = ""

        #Attachments
        self.attachmentsPosition = self.__langDict['Attachments_Folder']
        self.__attachmentsBool = ""
        self.attachmentsArr = []
        self.attachmentsFullPositionArr = []
        self.attachmentsFullEncodedArr = []
        
    def attachmentsFullPositionCompile(self):
        self.__attachmentsBool = True
        self.attachmentsFullPositionArr = []
        for att in self.attachmentsArr:
            self.attachmentsFullPositionArr.append(f"{self.attachmentsPosition}/{att}")
        return self.attachmentsFullPositionArr
    
    def attachments_addAll(self):
        dirList = os.listdir(f"{self.attachmentsPosition}/")
        self.attachmentsArr = dirList
        self.attachmentsFullPositionCompile()
        return dirList

    def addAttachment(self, attName: str):
        if os.path.exists(f"{self.attachmentsPosition}/{attName}"):
            self.attachmentsArr.append(attName)
            self.attachmentsFullPositionCompile()
    
    def addMultipleAttachments(self, attList):
        for att in attList:
            self.addAttachment(att)
        self.attachmentsFullPositionCompile()

    def MIMEBase_Attachments(self, Percorso_File):
        with open(Percorso_File, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
        return part

    def encoder_base64(self, file: MIMEBase, filename: str):
        encoders.encode_base64(file)
        file.add_header("Content-Disposition", f"attachment; filename={filename}")
        return file

    def attachmentFullEncodedArrCompile(self):
        self.attachmentsFullEncodedArr = []
        for i, el in enumerate(self.attachmentsFullPositionArr):
            name = self.attachmentsArr[i]
            mime_file = self.MIMEBase_Attachments(el)
            encoded_file = self.encoder_base64(mime_file, name)
            self.attachmentsFullEncodedArr.append(encoded_file)

    def webbBrowserViewer(self, tempPath: bool = True):
        if tempPath:
            path = 'file://' + os.path.realpath("temp/mail.html")
        else:
            path = 'file://' + os.path.realpath(self.__mailPath)
        try:
            webbrowser.open(path)
        except:
            print("Error! Webbrowser error, unable to open temp/mail.html with browser")

    def importInfo(self):
        data_dict = CF.jsonLoader(f"mailInfo{self.__lang}.json")
        
        self.subject = data_dict[self.__data_dict_keys[0]]
        if self.subject == '' or self.subject.isspace():
            self.subject = input(self.__langDict[1])
        
        self.recEmails = data_dict[self.__data_dict_keys[1]]
        if self.recEmails == '' or self.recEmails.isspace():
            self.recEmails = input(self.__langDict[2])

        self.recEmailsArr = self.recEmails.split(', ')

        self.__mailPath = data_dict[self.__data_dict_keys[2]]
        if self.__mailPath == '' or self.__mailPath.isspace():
            self.__mailPath = input(self.__langDict['34'])
        with open(self.__mailPath, "r") as file:
            self.MailContent= str(file.read())


        self.__attachmentsBool = data_dict[self.__data_dict_keys[3]]
        if self.__attachmentsBool == '':
            attInput = input(self.__langDict[3]).lower()
            if attInput == "1":
                self.__attachmentsBool = True
                print(self.__langDict[4])
            else:
                print(self.__langDict[5])

        if self.__attachmentsBool:
            attcmentsStr = data_dict[self.__data_dict_keys[4]]
            if attcmentsStr == '' or attcmentsStr.isspace():
                attcmentsStr = input(self.__langDict[6])
                
            self.attachmentsArr = attcmentsStr.split(", ")
            self.attachmentsFullPositionCompile()
            self.attachmentFullEncodedArrCompile()

    def basicInfoUserWrapper(self):
        self.subject = input(self.__langDict['43'])
        self.recEmails = input(self.__langDict['42'])
        self.recEmailsArr = self.recEmails.split(', ')

        '''
            def __str__(self) -> str:
                final = ""
                final += self.__langDict['29']
                final += "\n" + self.__langDict['30'] + self.subject
                if self.__mailPath != "": final += "\n" + self.__langDict['31'] + self.__mailPath
                final += "\n" + self.__langDict['32'] + str(self.recEmailsArr)
                if self.__attachmentsBool: final += "\n" + self.__langDict['33'] + str(self.attachmentsArr)
                return final
        '''
  
    def encodeJson(self):
        final = {
            "recEmailsArr": self.recEmailsArr,
            "subject": self.subject,
            "MailContent": self.MailContent,
            "mailPath": self.__mailPath,
            "attachmentsArr": self.attachmentsArr,
            "sendedFrom": self.sendedFrom
        }
        return final
    
    def decodeJson(self, json):
        self.recEmailsArr = json["recEmailsArr"]
        self.subject = json["subject"]
        self.MailContent = json["MailContent"]
        self.__mailPath = json["mailPath"]
        self.attachmentsArr = json["attachmentsArr"]
        if len(self.attachmentsArr) > 0:
            self.__attachmentsBool = True
        self.sendedFrom = json["sendedFrom"]

class HTMLMailBuilder:

    def addHeader(self):
            self.__fullMailArr.append('''
    <!DOCTYPE html PUBLIC " / /W3C//DTD XHTML 1. 0 Transitional//EN" "http://www.w3.org/
    TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset-utf-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NKMailTemplate</title>
            <style type="text/css">
                body {
                    margin: 0;
                    background-color: #e9e9e9;
                    padding: 10px;
                }

                table {
                    border-spacing: 0;
                }

                td {
                    padding: 0;
                }

                img {
                    border: 0;
                }

                .wrapper {
                    width: 100%;
                    table-layout: fixed;
                    background-color: #eaeaea;
                    
                }

                .main {
                    background-color: #ffffff;
                    margin: 0 auto;
                    width: 100%;
                    max-width: 600px;
                    border-spacing: 0;
                    font-family: sans-serif;
                    color: #494949;
                    border-radius: 8px;
                }
                .SvgBgHead {
                    width: 100%;
                    max-width: 600px;

                }

                .two-columns {
                    text-align: center;
                    font-size: 0;
                }

                .two-columns .column {
                    width: 100%;
                    max-width: 300px;
                    display: inline-block;
                    vertical-align: top;
                }

                .two-columns     .columnBg {
                    width: 100%;
                    max-width: 300px;
                    display: inline-block;
                    vertical-align: top;
                }

                .three-columns {
                    text-align: center;
                    font-size: 0;
                    padding: 15px 0 25px;
                }

                .three-columns .column {
                    width: 100%;
                    max-width: 200px;
                    display: inline-block;
                    vertical-align: top;
                    text-align: center;
                }

                .three-columns .padding {
                    padding: 15px;
                }

                .three-columns .content {
                    font-size: 15px;
                    line-height: 20px;
                    padding: 0 25px;
                }

                .two-columns .last {
                    padding: 15px 0; 
                }
                .two-columns .padding {
                    padding: 20px;
                }
                .two-columns .content {
                    font-size: 15px;
                    line-height: 20px;
                    text-align: left;
                }
                .linkButton {
                    background-color: #ffffff;
                    color: #494949;
                    text-decoration: none;
                    padding: 12px 20px; 
                    border-radius: 5px;
                    font-weight: bold;
                }
                .linkButtonDark {
                    background-color: #494949;
                    color: #ffffff;
                    text-decoration: none;
                    padding: 12px 20px; 
                    border-radius: 5px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body style="padding: 10px;">
            <center class="wrapper">
                <table class="main" width="100%">

    <!-- Border -->

                    <tr>
                        <td height="8" style="background-color: #494949; border-radius: 8px 8px 0px 0px;"></td>
                    </tr>

    <!-- Logo e& link social -->

                    <tr>
                        <td style="padding: 15px 0 5px;">
                            <table width="100%">
                                <tr>
                                    <td class="two-columns">
                                        <table class="column">
                                            <tr>
                                                <td style="padding: 0 120px 10px;">
                                                    <a href="''' + self.__userInfoDict["profile_url"] + '''"><img width="50" src="''' + self.__userInfoDict["profile_pic_url"] + '''" alt=""></a>
                                                </td>
                                            </tr>
                                        </table>
                                        <table class="column">
                                            <tr>
                                                <td style="padding: 10px 10px 62px 80px;">
                                                    <a style="margin-left: 4.5px; margin-right: 4.5px;" href="''' + self.__userInfoDict["x_url"] + '''"><img height="25" style="max-height: 25px; height: 25px; background-color: transparent; background: transparent;" src="https://raw.githubusercontent.com/NiccoloKadera/FiverrUploadedFiles/main/x.png" alt=""></a>
                                                    <a style="margin-left: 4.5px; margin-right: 4.5px;" href="''' + self.__userInfoDict["linkedin_url"] + '''"><img height="25" style="max-height: 25px; height: 25px; background-color: #ffffff;" src="https://raw.githubusercontent.com/NiccoloKadera/FiverrUploadedFiles/main/linked.png" alt=""></a>
                                                    <a style="margin-left: 4.5px; margin-right: 4.5px;" href="''' + self.__userInfoDict["instagram_url"] + '''"><img height="25" style="max-height: 25px; height: 25px; background-color: #ffffff;" src="https://raw.githubusercontent.com/NiccoloKadera/FiverrUploadedFiles/main/insta.png" alt=""></a>
                                                    <a style="margin-left: 4.5px; margin-right: 4.5px;" href="''' + self.__userInfoDict["fiverr_url"] + '''"><img height="25" style="max-height: 25px; height: 25px; background-color: #ffffff;" src="https://raw.githubusercontent.com/NiccoloKadera/FiverrUploadedFiles/main/fiver.png" alt=""></a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>


            ''')


    def __init__(self) -> None:
        self.__lang = 'It'.title()
        self.FullMail = ""
        self.__fullMailArr = []
        self.__langDict = CF.jsonLoader(f"lang{self.__lang}.json")
        self.__userInfoDict = CF.jsonLoader("userInfo.json")
        self.addHeader()
        

    

    def addFooter(self):
        self.__fullMailArr.append('''
    <!-- Title, Text area -->

                <tr>
                    <td style="padding: 15px 0 10px;">
                        <table width="100%">
                            <tr>
                                <td style="text-align: center; padding: 15px;">             
                                        <p style="line-height: 23px; text-align: center; font-size: 15px; padding: 5px 0 15px;">Niccolò Kadera</p>
                                </td>
                            </tr>       
                        </table>
                    </td>
                </tr>
        <!-- Border -->

                <tr>
                    <td height="8" style="background-color: #494949; border-radius: 0px 0px 8px 8px;"></td>
                </tr>

            </table>
        </center>
    </body>
</html>
        ''')


    def addText(self, text: str, align: str = 'left', title: str = ""):
            if title != "":
                title_str = f'<p style="font-size: 20px; font-weight: bold;">{title}</p>'
            else:
                title_str = ""
            initial = f"""<!-- Title, Text area -->

                <tr>
                    <td style="padding: 15px 0 10px;">
                        <table width="100%">
                            <tr>
                                <td style="text-align: center; padding: 15px;">
                                {title_str}
                                <p style="line-height: 23px; text-align: {align}; font-size: 15px; padding: 5px 0 15px;">"""
            for i,line in enumerate(text.splitlines()):
                initial += f'{line}'
                if i != len(text.splitlines()) - 1:
                    initial += '<br>'
            end = """                       </p>     
                                </td>
                            </tr>       
                        </table>
                    </td>
                </tr>"""
            final = initial + end
            self.__fullMailArr.append(final)
        
    def addTextWrapper(self, align):
        mailTitle = CF.Menu_Text(self.__langDict['58'], "0")
        mailText = CF.Menu_Text(self.__langDict['17'], "0")
        self.addText(mailText, align, mailTitle)
    
    def addImage(self, imageUrl: str = "", imagWidth = ""):
        if imageUrl == "" or imageUrl.isspace():
            imageUrl = "https://github.com/NiccoloKadera/FiverrUploadedFiles/blob/main/dan-gold-qgvFR8VkPss-unsplash.jpg?raw=true"
        if imagWidth == "" or imagWidth.isspace():
            imagWidth = "100"
        final = f'''
            <!-- Immage -->

                            <tr>
                                <td>
                                    <img width="{imagWidth}%"src="{imageUrl}" alt="PrimaryImage">
                                </td>
                            </tr>
        '''
        self.__fullMailArr.append(final)

    def addImageAndText(self, imageUrl: str = "", title: str = "", text: str = "", learnMoreLink: str = "", learnMoreButtonText: str = ""):
        if imageUrl == "" or imageUrl.isspace():
            imageUrl = "https://github.com/NiccoloKadera/FiverrUploadedFiles/blob/main/dan-gold-qgvFR8VkPss-unsplash.jpg?raw=true"
        if title == "" or title.isspace():
            title_part = ""
        else:
            title_part = f'<p style="font-weight: bold; font-size: 18px; color: #ffffff">{title}</p>'
        if learnMoreLink == "" or title.isspace():
            learnMore_part= ""
        else:
            learnMore_part = f'<a href="{learnMoreLink}" class="linkButton">{learnMoreButtonText}</a>'
        final = f'''<!-- Different Bg & two column section -->

                <tr>
                    <td style="background-color: #494949">
                        <table width="100%">
                            <tr>
                                <td class="two-columns last">
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            <img width="260" style="max-width: 260px;" src="{imageUrl}" alt="PrimaryImage">
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            {title_part}
                                                            <p style="padding-bottom: 15px; color: #ffffff;">{text}</p>
                                                            {learnMore_part}
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td> 
                            </tr>
                        </table>
                    </td>
                </tr>'''
        self.__fullMailArr.append(final)

    def addImageWrapper(self):
        url = input(self.__langDict['37'])
        imageWidth = input(self.__langDict['38'])
        self.addImage(url, imageWidth)

    def addImageAndTextWrapper(self):
        imageUrl = input(self.__langDict['37'])
        title = input(self.__langDict['50'])
        text = input(self.__langDict['51'])
        learnMoreLink = input(self.__langDict['52'])
        if learnMoreLink != "":
            learnMoreButtonText = input(self.__langDict['53'])
        else:
            learnMoreButtonText = ""
        self.addImageAndText(imageUrl, title, text, learnMoreLink, learnMoreButtonText)

    def addResponse(self, sender: str, object: str, date: str,text: str):
            initial = """<!-- Title, Text area -->

                <tr>
                    <td style="padding: 15px 0 10px;">
                        <table width="100%">
                            <tr>
                                <td style="text-align: center; padding: 15px;">"""
            
            initial += f'<p style="line-height: 23px; text-align: left; font-size: 15px; padding: 5px 0 15px; color: #1699ff;">On {date}, {sender} wrote ({object}):<br>{text}</p>'
            end = """
                                </td>
                            </tr>       
                        </table>
                    </td>
                </tr>"""
            final = initial + end
            self.__fullMailArr.append(final)

    def compile(self, saveHTML: bool = True):
        self.addFooter()
        for el in self.__fullMailArr:
            self.FullMail += el
        if saveHTML:
            with open("temp/mail.html", "w") as file:
                file.write(self.FullMail)
        return self.FullMail

    def builderMenu(self):
        proceed = True
        while proceed:
            user_input = CF.Menu_Int(self.__langDict['39'], [self.__langDict['40'], self.__langDict['41'], self.__langDict['46'], self.__langDict['54']], self.__langDict['45'])
            if user_input == 0:
                proceed = False
            if user_input == 1:
                self.addImageWrapper()
            if user_input == 2:
                self.addTextWrapper('left')
            if user_input == 3:
                self.addTextWrapper('center')
            if user_input == 4:
                self.addImageAndTextWrapper()
        full = self.compile()
        return full
        


class memoryHandler:

    def __init__(self) -> None:
        self.__lang = 'It'.title()
        self.__langDict = CF.jsonLoader(f"lang{self.__lang}.json")
        self.startTime = datetime.now()
        self.stopTime = 0
        self.__memDictPath = self.__langDict["Memory_Folder"] + "memDict.json"
        if os.path.exists(self.__memDictPath):
            self.memoryDict = CF.jsonLoader(self.__memDictPath)
        else:
            raise Exception("Unable to locate memory! %s" % self.__memDictPath)
        self.memoryDict["last_started"] = self.strTime(self.startTime)
        self.version = ""

    def strTime(self, relTime):
        return relTime.strftime("%d/%M/%Y %H:%M:%S")

    def stopTimeUpdate(self):
        self.stopTime = datetime.now()
        return self.stopTime
    
    def addMail(self, mail):
        recEmArr = mail.recEmailsArr
        for m in recEmArr:
            if m not in self.memoryDict["allRecEmails"]:
                self.memoryDict["allRecEmails"].append(m)
        self.memoryDict["emailsSent"].append({"senderVersion": self.version, "senderStartTime": self.strTime(self.startTime), "senderStopTime": self.strTime(self.stopTime),  "mailData": mail.encodeJson()})

    def clearMailMem(self):
        user_input = input(self.__langDict["55"])
        if user_input == "y":
            self.memoryDict["emailsSent"] = []
            self.memoryDict["allRecEmails"] = []
            if self.memoryUpdate(): print(self.__langDict["56"])

    def memoryUpdate(self):
        if os.path.exists(self.__memDictPath):
            CF.jsonWriter(self.__memDictPath, self.memoryDict)
            return True
        else:
            return False

