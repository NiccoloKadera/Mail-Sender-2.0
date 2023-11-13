import os
import json
import os

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
