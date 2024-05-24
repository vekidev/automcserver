import urllib.request
from rich import prompt
from rich.console import Console
import sys, os, zipfile

import os, sys, tarfile

def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])



console = Console()

OS = sys.platform

with console.status("[bold green]Downloading server file... (1.20.6)[/bold green]") as status:
    try:
        urllib.request.urlretrieve("https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar", "server.jar")
        console.log("Download sucessful.")
    except:
        console.log("[red] Download unsucessful. [/red]")
        sys.exit()

agreement = prompt.Confirm.ask("Do you agree to the EULA?")

if agreement:
    with console.status("[bold green]Creating eula.txt...[/bold green]") as status:
        with open("eula.txt","w") as f:
            f.write("""#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
#Fri May 24 17:18:38 CEST 2024
eula=true""")
    
    ram = prompt.IntPrompt.ask("How much RAM do you want to allocate? (GB)")
    portforward = prompt.Prompt.ask("Do you want to setup port forwarding automatically?", choices=["ngrok","localtonet","no"], default="no")
    if portforward == "ngrok":
        if str(OS).find("linux") != -1:
            with console.status("[bold green]Downloading ngrok...[/bold green]") as status:
                try:
                    urllib.request.urlretrieve("https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz", "ngrok.tgz")
                    console.log("Download sucessful.")
                except:
                    console.log("[red] Download unsucessful. [/red]")
                    sys.exit()
                extract("ngrok.tgz")
            token = prompt.Prompt.ask("Go to https://dashboard.ngrok.com/signup and sign up. Then copy the token into this prompt.")
            os.popen("chmod +x ngrok")
            os.popen(f"./ngrok config add-authtoken {token}")
            os.remove("ngrok.tgz")

        elif OS == "windows":
            with console.status("[bold green]Downloading ngrok...[/bold green]") as status:
                try:
                    urllib.request.urlretrieve("https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip", "ngrok.zip")
                    console.log("Download sucessful.")
                except:
                    console.log("[red] Download unsucessful. [/red]")
                    sys.exit()
            with console.status("[bold green]Extracting ngrok...[/bold green]") as status:
                with zipfile.ZipFile("ngrok.zip","r") as zip_ref:
                    zip_ref.extractall()
                console.log("Sucessfuly extracted ngrok.")
                
            token = prompt.Prompt.ask("Go to https://dashboard.ngrok.com/signup and sign up. Then copy the token into this prompt.")
            os.popen(f".\ngrok config add-authtoken {token}")
            os.remove("ngrok.zip")
                
        else:
            console.log("[yellow] No port forward options available, skipping...")
    elif portforward == "localtonet":
        if str(OS).find("linux") != -1:
            with console.status("[bold green]Downloading ngrok...[/bold green]") as status:
                try:
                    urllib.request.urlretrieve("https://localtonet.com/download/localtonet-linux-x64.zip", "localtonet.zip")
                    console.log("Download sucessful.")
                except:
                    console.log("[red] Download unsucessful. [/red]")
                    sys.exit()
                with zipfile.ZipFile("localtonet.zip","r") as zip_ref:
                    zip_ref.extractall()
            token = prompt.Prompt.ask("Go to https://localtonet.com/Identity/Account/Register and sign up. Then go to https://localtonet.com/documents/using-localtonet-with-minecraft and follow the instructions. After that, click ENTER.")
            os.popen("chmod +x localtonet")
            os.remove("localtonet.zip")

        elif OS == "windows":
            with console.status("[bold green]Downloading ngrok...[/bold green]") as status:
                try:
                    urllib.request.urlretrieve("https://localtonet.com/download/localtonet-win-64.zip", "localtonet.zip")
                    console.log("Download sucessful.")
                except:
                    console.log("[red] Download unsucessful. [/red]")
                    sys.exit()
                with zipfile.ZipFile("localtonet.zip","r") as zip_ref:
                    zip_ref.extractall()
            token = prompt.Prompt.ask("Go to https://localtonet.com/Identity/Account/Register and sign up. Then go to https://localtonet.com/documents/using-localtonet-with-minecraft and follow the instructions. After that, click ENTER.")
            os.remove("localtonet.zip")
                
        else:
            console.log("[yellow] No port forward options available, skipping...")

    with console.status("[bold green]Creating startup script...[/bold green]") as status:
        with open("start.py","w") as f:
            f.write(f"""import os
input("Open the ngrok/localtonet application(if you selected auto port forwarding), then click ENTER.")
os.system("java -Xmx{ram*1024}M -Xms{ram*1024}M -jar server.jar nogui")""")
    
    console.log("Finished! To start the server, run python start.py")

else:
    console.log("Sorry then, this is not for you... :(")
            
    