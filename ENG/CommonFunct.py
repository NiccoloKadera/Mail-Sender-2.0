import os
import json
from email.mime.text import MIMEText
from http import server
import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import csv
from email import encoders

class CF:

    __directoryFiles = os.listdir()

    def FileWrite(name: str, message: str):
        if os.path.exists(name):
            try:
                with open(name, "w") as file:
                    file.write(message)
            except Exception:
                print("Unable to write %s file, unexpected error." % name)
        else:
            print("Unable to find %s file in current directory." % name)

    def FileRead(name: str) -> str:
        content = ""
        if os.path.exists(name):
            try:
                with open(name, "r") as file:
                    content = file.read()
            except Exception:
                print("Unable to read %s file, unexpected error." % name)
        else:
            print("Unable to find %s file in current directory." % name)
        return content

    def jsonLoader(name: str) -> str:
        if name in CF.__directoryFiles or os.path.exists(name):
            try:
                with open(name) as file:
                    content = json.load(file)
            except Exception:
                print("Unable to load %s file, unexpected error." % name)
        else:
            print("Unable to find %s file in current directory." % name)
        return content
    
    def jsonWriter(name: str, content) -> str:
        if name in CF.__directoryFiles or os.path.exists(name):
            #try:
            with open(name, 'w') as file:
                json.dump(content, file)
            #except Exception:
                #print("Unable to write %s file, unexpected error." % name)
        else:
            print("Unable to write %s file in current directory." % name)

    def csvLoader(path: str, id: int):
        with open(path, newline="", encoding="ISO-8859-1") as fileCSV:
            risultato = []
            lettore = csv.reader(fileCSV)
            for riga in lettore:
                risultato.append(riga[id])
            return risultato

    def GetCsvId(path: str):
        with open(path, newline="", encoding="ISO-8859-1") as fileCSV:
            lettore = csv.reader(fileCSV)
            header = next(lettore)
            return header

    def sendHtmlEmail(myemail: str, email: str, Subject: str, html: str, email_pass, Allegato_codificato = "") -> None:
        em = MIMEMultipart()
        em["From"] = myemail
        em["To"] = email
        em["Subject"] = Subject
        
        htmlPart = MIMEText(html, "html")
        em.attach(htmlPart)

        if Allegato_codificato != "":
            cont = 1
            for item in Allegato_codificato:
                print("Adding attachments: %d..." % cont)
                if cont == 1:
                    allegat_str = "Allegati:"
                else:
                    allegat_str = ""
                cont += 1
                em.attach(MIMEText(allegat_str, "plain"))
                em.attach(item)
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(myemail, email_pass)
        print("Log in Success")
        if Allegato_codificato != "":
            print("Email with attachments could take several minutes to be sent.")
        server.sendmail(myemail, email, em.as_string())
        print("Success...")

        print("", end="")
        for i in range(0, 20):
            print("-", end="")

        print("> Email inviata a %s.\n" % email, end="")
        print()
        time.sleep(0.5)

    def MIMEBase_Attachments(Percorso_File):
        with open(Percorso_File, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
        return part

    def encoder_base64(file: MIMEBase, filename: str):
        encoders.encode_base64(file)
        file.add_header("Content-Disposition", f"attachment; filename={filename}")
        return file

    def isArray(Variable) -> bool:
        try:
            Variable.append("a")
            result = True
        except:
            result = False
        print(Variable)
        return result

    def Menu_Bool(Testo: str, Opzioni: list, Opzione_Corretta: int, Messaggio_Finale: str) -> bool:
        risultato = False
        print('\n\n' + Testo)
        for i in range(0, len(Opzioni)):
            print(" -%d: %s." % (i + 1, Opzioni[i]))
        try:
            risposta = int(input(Messaggio_Finale))
        except:
            print("Rispondere con un intero raffigurato affianco l'ozpione scelta.")
            risposta = 0
        if risposta == Opzione_Corretta:
            risultato = True
        return risultato
    
    def Menu_Int(Testo: str, Opzioni: list, Messaggio_Finale: str, ErrorMsg: str = "Rispondere con un intero raffigurato affianco l'ozpione scelta.") -> bool:
        print(Testo)
        for i in range(0, len(Opzioni)):
            print(" -%d: %s." % (i + 1, Opzioni[i]))
        try:
            risposta = int(input(Messaggio_Finale))
        except:
            print(ErrorMsg)
            risposta = 0
        return risposta

    def Menu_Text(Testo: str, TerminaCon: str = "0", ErrorMsg: str = "Rispondere con un intero raffigurato affianco l'ozpione scelta.") -> str:
        print('\n' + Testo)
        str_tot = ""
        continua = True
        cont = 0
        while continua:
            risposta = input("")
            if cont != 0 and risposta != TerminaCon:
                str_tot += "\n"
            if risposta == TerminaCon or risposta == "" or risposta.isspace():
                continua = False
            else:
                str_tot += risposta
            cont += 1
        return str_tot
