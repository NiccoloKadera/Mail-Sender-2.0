# Mail-Sender-2.0





🇬🇧 English
It is a wrapper that let you send and build HTML with a gmail e-mail address. This tool can also respond to mail in your mailbox.

This script is built using the following dependencies:
 - email
 - smtplib
 - imaplib

Set-up:
To set up please configure the following files:

userInfo.json -> {
    "name": "", (Es: "Niccolò Kadera")
    "myEmail": "", (Es: "niccolokadera@gmail.com")
    "gmailPass": "", (Go to: https://myaccount.google.com/ -> Security -> Two-step verification -> login -> scroll down -> Passwords for apps -> Set MailSender as name and paste the gmail password)
    "instagram_url": "", (Es: "https://www.instagram.com/kadera_niccolo/")
    "linkedin_url": "", (Es: "https://www.linkedin.com/in/niccolò-kadera-6b5aa3207")
    "fiverr_url": "", (Es: "https://www.fiverr.com/niccolo_kadera")
    "x_url": "", (Es: "https://twitter.com/KaderaNiccolo")
    "profile_pic_url": "",
    "profile_url": "" (Es: "https://niccolokadera.github.io/Portfolio/")
}



To respond and view e-mails in your mail box:
  Go to: Gmail.com -> settings (top right) -> view all settings -> POP/IMAP -> Set IMAP access to enable



You can also send pre compiled HTML e-mails, to do so place .html files in the Templates/ folder and configure mailInfoIt.json as:

mailInfoIt.json -> {
    "Subject": "", (Identifies the subject of the email)
    "Recipient_email": "", (This is the list of people you are sending the e-mail to, please spearate e-mail addresses with ", ")
    "Mail_path": "", (The relative path to the .html file in Templates/ folder. Es: Templates/example.html)
    "Attachments_Bool": true, (To enable sending the attachments specified below [true/false])
    "Attachments": "" (This is the list of the attachments to send with the e-mail. These must be contained in Attachments/ folder, please spearate attachments names with ", " Es: example.txt, exampleTwo.txt)
}





🇮🇹 Italian
È un wrapper che ti consente di inviare e creare HTML con un indirizzo e-mail gmail. Questo strumento può anche rispondere alla posta nella tua casella di posta.

Questo script è costruito utilizzando le seguenti dipendenze:
 - email
 - smtplib
 - imaplib

Configurazione:
Per configurare, impostare correttamente i seguenti file:
userInfo.json -> {
    "name": "", (Es: "Niccolò Kadera")
    "myEmail": "", (Es: "niccolokadera@gmail.com")
    "gmailPass": "", (Vai a: https://myaccount.google.com/ -> Sicurezza -> Verifica in due passaggi -> login -> scorri verso il basso -> Password per le app -> Imposta MailSender come nome e incolla la password di gmail)
    "instagram_url": "", (Es: "https://www.instagram.com/kadera_niccolo/")
    "linkedin_url": "", (Es: "https://www.linkedin.com/in/niccolò-kadera-6b5aa3207")
    "fiverr_url": "", (Es: "https://www.fiverr.com/niccolo_kadera")
    "x_url": "", (Es: "https://twitter.com/KaderaNiccolo")
    "profile_pic_url": "",
    "profile_url": "" (Es: "https://niccolokadera.github.io/Portfolio/")
}



Per rispondere e visualizzare le e-mail nella tua casella di posta:
  Vai a: Gmail.com -> impostazioni (in alto a destra) -> visualizza tutte le impostazioni -> POP/IMAP -> Imposta l'accesso IMAP per abilitare



Puoi anche inviare e-mail HTML pre-copilate, per farlo posiziona i file .html nella cartella Templates/ e configura mailInfoIt.json come:
mailInfoIt.json -> {
    "Oggetto": "", (Identifica l'oggetto dell'e-mail)
    "Email_destinatario": "", (Questo è l'elenco delle persone a cui stai inviando l'e-mail, per favore separa gli indirizzi di posta elettronica con ", ")
    "Mail_percorso": "", (Il percorso relativo del file .html da inviare situato nella cartella Templates/. Es: Templates/esempio.html)
    "Allegati_Bool": true, (Per abilitare l'invio degli allegati specificati di seguito [true/false])
    "Allegati": "" (Questo è l'elenco degli allegati da inviate con l'e-mail. Devono essere contenuti nella cartella Allegati/, si prega di i nomi degli allegati con ", " Es: esempio.txt, esempioDue.txt)
}


Niccolò Kadera

