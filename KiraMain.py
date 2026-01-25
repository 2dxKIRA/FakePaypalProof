# ╔════════════════════════════════════════════════════════════════════════════════════════╗
# ║ MIT License                                                                            ║
# ║                                                                                        ║
# ║ Copyright (c) 2026 2DX NEWsociety                                                      ║
# ║                                                                                        ║
# ║ Permission is hereby granted, free of charge, to any person obtaining a copy           ║
# ║ of this software and associated documentation files (the "Software"), to deal          ║
# ║ in the Software without restriction, including without limitation the rights           ║
# ║ to use, copy, modify, merge, publish, distribute, sublicense, and/or sell              ║
# ║ copies of the Software, and to permit persons to whom the Software is                  ║
# ║ furnished to do so, subject to the following conditions:                               ║
# ║                                                                                        ║
# ║ The above copyright notice and this permission notice shall be included in all         ║
# ║ copies or substantial portions of the Software.                                        ║
# ║                                                                                        ║
# ║ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR             ║
# ║ IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,               ║
# ║ FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE            ║
# ║ AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                 ║
# ║ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,          ║
# ║ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE          ║
# ║ SOFTWARE.                                                                              ║
# ╚════════════════════════════════════════════════════════════════════════════════════════╝

# EN: 
#     - ⚠️ Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code. ⚠️
#     - ⚠️ Do not resell this tool, do not credit it to yours. ⚠️
# FR: 
#     - ⚠️ Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code. ⚠️
#     - ⚠️ Ne revendez pas ce tool, ne le créditez pas au vôtre. ⚠️

# j'ai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import requests
import json
import os
import io
import random
import string
from datetime import datetime
import glob
import sys
import shutil
import subprocess
import threading
import webbrowser
import time as _time

# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕

RESET = "\033[0m"
ROUGE = "\033[91m"


def installer_dependances():
    if os.path.exists('.deps_installing'):
        os.remove('.deps_installing')
        return
    modules_requis = ['PIL', 'requests', 'keyboard', 'customtkinter']
    modules_a_installer = []
    for module in modules_requis:
        try:
            __import__(module)
        except ImportError:
            modules_a_installer.append(module)
    if modules_a_installer:
        with open('.deps_installing', 'w') as f:
            f.write('1')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, 'requirements.txt')
        try:
            if os.path.exists(requirements_path):
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], capture_output=True, text=True)
            else:
                packages = ['Pillow>=10.0.0', 'requests>=2.31.0', 'keyboard>=0.13.5', 'customtkinter']
                result = subprocess.run([sys.executable, "-m", "pip", "install"] + packages, capture_output=True, text=True)
            if result.returncode == 0:
                pass
            else:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
                if result.stderr:
                    pass
                if os.path.exists('.deps_installing'):
                    os.remove('.deps_installing')
                sys.exit(1)
        except Exception as e:
            if os.path.exists('.deps_installing'):
                os.remove('.deps_installing')
            sys.exit(1)
        _time.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)

installer_dependances()


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_POLICE_PATH = os.path.join("C:/Windows/Fonts", "arialbd.ttf")
DEFAULT_WEBHOOKS_FILE = os.path.join(SCRIPT_DIR, "webhooks.json")
DEFAULT_TEXTE_TEMPLATE = "Vous avez envoyé {argent} € EUR à {pseudo}"
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "paypalTEMPLATE")
# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕

def charger_webhooks():
    if os.path.exists(DEFAULT_WEBHOOKS_FILE):
        try:
            with open(DEFAULT_WEBHOOKS_FILE, 'r', encoding='utf-8') as f:
                webhooks = json.load(f)
                if isinstance(webhooks, list):
                    return webhooks
        except Exception:
            pass
    return []

def sauvegarder_webhook(webhook_url):
    if not webhook_url or not webhook_url.strip():
        return
    webhook_url = webhook_url.strip()
    webhooks = charger_webhooks()
    if webhook_url in webhooks:
        return
    webhooks.append(webhook_url)
    try:
        with open(DEFAULT_WEBHOOKS_FILE, 'w', encoding='utf-8') as f:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
            json.dump(webhooks, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def trouver_premier_png():
    if os.path.isdir(TEMPLATE_DIR):
        pngs = glob.glob(os.path.join(TEMPLATE_DIR, '*.png'))
        if pngs:
            return pngs[0]
    racine_png = os.path.join(SCRIPT_DIR, 'paypalTEMPLATE.png')
    if os.path.isfile(racine_png):
        return racine_png
    return ""

def generer_numero_transaction():
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(16))

def obtenir_date_fr():
    now = datetime.now()# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    mois_fr = ["jan", "fév", "mar", "avr", "mai", "juin", "juil", "août", "sep", "oct", "nov", "déc"]
    return f"{now.day} {mois_fr[now.month - 1]} {now.year}"


class PaypalSimGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Simulateur de Transaction PayPal (GUI)")
        self.geometry("600x400+40+40")
        self.resizable(False, False)
        self.configure(bg="#000000")
        self._set_widgets_bg_black(self)
        self.after(100, self._animate_open)

    def _animate_open(self):
        target_w, target_h = 1200, 900
        cur_w, cur_h = self.winfo_width(), self.winfo_height()
        step_w = max((target_w - cur_w) // 10, 1)
        step_h = max((target_h - cur_h) // 10, 1)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
        if cur_w < target_w or cur_h < target_h:
            new_w = min(cur_w + step_w, target_w)
            new_h = min(cur_h + step_h, target_h)
            self.geometry(f"{new_w}x{new_h}+40+40")
            self.after(15, self._animate_open)
        else:
            self.geometry(f"{target_w}x{target_h}+40+40")

    def _set_widgets_bg_black(self, parent):
        for widget in parent.winfo_children():
            try:
                widget.configure(bg="#000000")
            except Exception:
                pass
            self._set_widgets_bg_black(widget)
        self.webhooks = charger_webhooks()
        self.image_path = trouver_premier_png()
        self.font_path = DEFAULT_POLICE_PATH if os.path.exists(DEFAULT_POLICE_PATH) else ""
        self._build_ui()
        self.generated_image = None

    def _build_ui(self):
        titre = ctk.CTkLabel(self, text="Simulateur de Transaction PayPal", font=("Arial", 38, "bold"), fg_color="transparent", text_color="#ff003c")# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
        titre.place(x=220, y=30)
        self.webhook_var = ctk.StringVar(value="")
        ctk.CTkLabel(self, text="Webhook Discord:", font=("Arial", 22)).place(x=60, y=120)
        self.webhook_entry = ctk.CTkEntry(self, textvariable=self.webhook_var, width=700, font=("Arial", 20))
        self.webhook_entry.place(x=320, y=120)
        if self.webhooks:
            ctk.CTkLabel(self, text="(Sélection rapide)", font=("Arial", 18), fg_color="transparent", text_color="#888").place(x=1050, y=120)
        self.username_var = ctk.StringVar(value="2dx")
        ctk.CTkLabel(self, text="Username:", font=("Arial", 22)).place(x=60, y=200)
        ctk.CTkEntry(self, textvariable=self.username_var, width=350, font=("Arial", 20)).place(x=320, y=200)
        self.montant_var = ctk.StringVar(value="0")
        ctk.CTkLabel(self, text="Montant (€):", font=("Arial", 22)).place(x=60, y=280)
        ctk.CTkEntry(self, textvariable=self.montant_var, width=350, font=("Arial", 20)).place(x=320, y=280)
        self.canvas = ctk.CTkCanvas(self, width=800, height=450, bg="#000000", bd=0, highlightthickness=5, highlightbackground="#ff003c")
        self.canvas.place(x=200, y=370)
        btn_send = ctk.CTkButton(self, text="Envoyer au webhook", command=self.envoyer_webhook, width=250, fg_color="#222", hover_color="#222", text_color="#ff003c", font=("Arial", 20, "bold"))
        btn_send.place(x=475, y=320)
        self.status_var = ctk.StringVar(value="Prêt.")
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=("Arial", 22, "bold"), fg_color="transparent", text_color="#ff003c")
        self.status_label.place(x=400, y=870)
        self.after(100, self._auto_update_image)

    def _auto_update_image(self):
        new_path = trouver_premier_png()
        if new_path != self.image_path:
            self.image_path = new_path
            self.generer_image()
        else:
            self.generer_image()
        self.after(100, self._auto_update_image)

    def generer_image(self):
        if not self.image_path or not os.path.exists(self.image_path):
            self.status_var.set("Aucune image trouvée dans paypalTEMPLATE.")
            self.generated_image = None
            self._afficher_apercu(Image.new("RGBA", (520, 260), (24, 20, 28, 255)))
            return
        try:
            img = Image.open(self.image_path).convert("RGBA")
            draw = ImageDraw.Draw(img)
            username = self.username_var.get() or "2dx"
            montant = self.montant_var.get() or "0"# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
            texte = DEFAULT_TEXTE_TEMPLATE.format(argent=montant, pseudo=username)
            font = self._charger_police(self.font_path, 44)
            largeur_max = int(img.size[0] * 0.9)
            lignes = self._diviser_texte(draw, texte, font, largeur_max)
            y = 60
            for ligne in lignes:
                bbox = draw.textbbox((0, 0), ligne, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x = (img.size[0] - w) // 2
                draw.text((x, y), ligne, fill=(0, 0, 0), font=font)
                y += h + 8
            font_date = self._charger_police(DEFAULT_POLICE_PATH, 12)
            draw.text((450, 262), obtenir_date_fr(), fill=(0, 0, 0), font=font_date)
            font_tr = self._charger_police(DEFAULT_POLICE_PATH, 12)
            num_tr = generer_numero_transaction()
            draw.text((37, 262), num_tr, fill=(122, 184, 224), font=font_tr)
            font_a2 = self._charger_police(DEFAULT_POLICE_PATH, 13)
            font_a3 = self._charger_police(DEFAULT_POLICE_PATH, 11)
            draw.text((465, 477), f"{montant} € EUR", fill=(0, 0, 0), font=font_a2)
            draw.text((465, 325), f"{montant} € EUR", fill=(41, 41, 41), font=font_a3)
            draw.text((465, 420), f"{montant} € EUR", fill=(41, 41, 41), font=font_a3)
            self.generated_image = img
            self._afficher_apercu(img)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
            self.status_var.set("")
        except Exception as e:
            self.status_var.set(f"Erreur: {e}")

    def _charger_police(self, path, size):
        try:
            if path and os.path.exists(path):
                return ImageFont.truetype(path, size)
        except Exception:
            pass
        return ImageFont.load_default()

    def _diviser_texte(self, draw, texte, font, largeur_max):
        mots = texte.split()
        lignes = []
        ligne = ""
        for mot in mots:
            test = ligne + (" " if ligne else "") + mot
            bbox = draw.textbbox((0, 0), test, font=font)
            w = bbox[2] - bbox[0]
            if w <= largeur_max:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
                ligne = test
            else:
                if ligne:
                    lignes.append(ligne)
                ligne = mot
        if ligne:
            lignes.append(ligne)
        return lignes

    def _afficher_apercu(self, img):
        img_resized = img.copy()
        img_resized.thumbnail((760, 420))
        self.tk_img = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        canvas_w = 800
        canvas_h = 450
        img_w = self.tk_img.width()
        img_h = self.tk_img.height()
        x = (canvas_w - img_w) // 2
        y = (canvas_h - img_h) // 2
        self.canvas.create_image(x, y, anchor="nw", image=self.tk_img)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕

    def envoyer_webhook(self):
        webhook_url = self.webhook_var.get().strip()
        if not webhook_url:
            self.status_var.set("Webhook manquant.")
            return
        if self.generated_image is None:
            self.status_var.set("Générez d'abord l'image.")
            return
        try:
            img_buffer = io.BytesIO()
            self.generated_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            username = self.username_var.get() or "2dx"
            montant = self.montant_var.get() or "0"
            embed = {
                "title": "💸 Simulateur de Transaction",
                "description": f"**@{username}** a reçu **{montant}€**\n\n"
                               f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                               f"❤️ **Merci d'avoir utilisé notre simulateur !** ❤️\n"
                               f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                               f"Cette transaction est une **simulation** créée à des fins de démonstration. "
                               f"Merci d'avoir testé notre simulateur de transaction !",
                "color": 0xFF0000,
                "image": {"url": "attachment://image.png"},
                "footer": {"text": "Simulateur de transaction • Créé par 2dx"}
            }
            payload = {"content": "", "embeds": [embed]}
            files_data = {"file": ("image.png", img_buffer, "image/png")}
            data = {"payload_json": json.dumps(payload)}
            r = requests.post(webhook_url, files=files_data, data=data, timeout=10)
            if r.status_code in [200, 204]:
                self.status_var.set("Envoyé avec succès !")
                sauvegarder_webhook(webhook_url)
            else:
                self.status_var.set(f"Erreur HTTP: {r.status_code}")
        except Exception as e:
            self.status_var.set(f"Erreur: {e}")


def print_rouge_centre(texte, largeur=80):
    lignes = texte.split('\n')
    for ligne in lignes:
        ligne_strip = ligne.strip()
        if ligne_strip:
            espace = (largeur - len(ligne_strip)) // 2
            espace = max(0, espace)
            print(" " * espace + ROUGE + ligne_strip + RESET)
        else:
            print()

def effacer_console():# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_ascii_art():
    ascii_art_original = """
                                                                      
                                                                      
 ░▓████▒   █████▒    ██▓  ▓██              ▒████▒  ████████  ███   ██ 
 ███████▒  ███████   ▒██  ██▒             ▓██████  ████████  ███   ██ 
 █▒░  ▓██  ██  ▒██▒   ██▓▓██             ▒██▒  ░█  ██        ███▒  ██ 
       ██  ██   ▒██   ▒████▒             ██▒       ██        ████  ██ 
      ▒█▓  ██   ░██    ████              ██░       ██        ██▒█▒ ██ 
      ██   ██    ██    ▒██▒              ██        ███████   ██ ██ ██ 
    ░██▒   ██    ██    ▒██▒              ██  ████  ███████   ██ ██ ██ 
   ░██▒    ██   ░██    ████              ██░ ████  ██        ██ ▒█▒██ 
  ▒██▒     ██   ▒██   ▒████▒             ██▒   ██  ██        ██  ████ 
 ▒██▒      ██  ▒██▒   ██▒▒██             ▒██▒  ██  ██        ██  ▒███ 
 ████████  ███████   ▒██  ██▒             ███████  ████████  ██   ███ 
 ████████  █████▒    ██▓  ▓██              ▒████░  ████████  ██   ███ 
                                                                      
                                                                      
                                                                      
                                                                      """
    try:
        colonnes = shutil.get_terminal_size().columns
    except:
        colonnes = 200
    lignes = ascii_art_original.strip().split('\n')
    lignes_agrandies = []
    for ligne in lignes:
        if ligne.strip():
            ligne_agrandie = ''.join(c * 2 for c in ligne)
            ligne_largeur = len(ligne_agrandie)
            espace = (colonnes - ligne_largeur) // 2
            espace = max(0, espace)
            lignes_agrandies.append(" " * espace + ligne_agrandie)
        else:
            lignes_agrandies.append("")
            lignes_agrandies.append("")
    ascii_art_final = '\n'.join(lignes_agrandies)
    for ligne in ascii_art_final.split('\n'):
        print(ligne.center(colonnes))
    print_rouge_centre("━" * 70, colonnes)
    print_rouge_centre("Générateur de fausse transaction PayPal", colonnes)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    print_rouge_centre("━" * 70, colonnes)
    print()
    print_rouge_centre("⚠️  Ce logiciel génère des images de simulation de transaction PayPal.", colonnes)
    print_rouge_centre("Il s'agit uniquement d'un générateur à des fins de démonstration.", colonnes)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    print_rouge_centre("Les transactions générées ne sont PAS réelles.", colonnes)
    print()
    print_rouge_centre("Créé par 2dx", colonnes)
    print()
    print_rouge_centre("⚠️  IMPORTANT: Ne modifiez pas le code source de ce programme.", colonnes)
    print()
    print_rouge_centre("━" * 70, colonnes)
    print()

def afficher_loading_bar():
    import random
    import math
    ascii_art = [
        "                                                                                                                                  .-'''-.        .-'''-.            ",
        "                                                                                                                                 '   _    \\     '   _    \\          ",
        "                                                        .     .--.                            _________   _...._               /   /` '.   \\  /   /` '.   \\         ",
        "                                                      .'|     |__|                            \\        |.'      '-.           .   |     \\  ' .   |     \\  '   _.._  ",
        "                                                    .'  |     .--..-,.--.                      \\        .'```'.    '. .-,.--. |   '      |  '|   '      |  '.' .._| ",
        "                                                   <    |     |  ||  .-. |    __                \\      |       \\     \\|  .-. |\\    \\     / / \\    \\     / / | '     ",
        "                                                    |   | ____|  || |  | | .:--.'.               |     |        |    || |  | | `.   ` ..' /   `.   ` ..' /__| |__   ",
        "                                                    |   | \\ .'|  || |  | |/ |   \\ |              |      \\      /    . | |  | |    '-...-'`       '-...-'`|__   __|  ",
        "                                                    |   |/  . |  || |  '- `\" __ | |              |     |\\`'-.-'   .'  | |  '-                               | |     ",
        "                                                    |    /\\  \\|__|| |      .'.''| |              |     | '-....-'`    | |                                   | |     ",
        "                                                    |   |  \\  \\   | |     / /   | |_            .'     '.             | |                                   | |     ",
        "                                                    '    \\  \\  \\  |_|     \\ \\._,\\ '/          '-----------'           |_|                                   | |     ",
        "                                                   '------'  '---'         `--'  `\"                                                                         |_|     "
    ]
    points = []
    for y, line in enumerate(ascii_art):
        for x, c in enumerate(line):
            if c != ' ':
                points.append((x, y, c))
    nb_particules = len(points)
    largeur = max(len(l) for l in ascii_art)
    hauteur = len(ascii_art)
    try:
        colonnes = shutil.get_terminal_size().columns
    except:
        colonnes = 120
    offset_x = (colonnes - largeur) // 2
    particules = [
        [random.randint(0, largeur-1), random.randint(0, hauteur-1)]
        for _ in range(nb_particules)
    ]
    steps = 32
    for step in range(steps+1):
        frame = [[' ' for _ in range(largeur)] for _ in range(hauteur)]# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
        for i, (tx, ty, c) in enumerate(points):
            sx, sy = particules[i]
            px = int(sx + (tx - sx) * (step / steps))
            py = int(sy + (ty - sy) * (step / steps))
            frame[py][px] = c
        print("\033c", end="")
        for line in frame:
            print(' ' * offset_x + ROUGE + ''.join(line) + RESET)
        _time.sleep(0.04)
    print("\033c", end="")
    for line in ascii_art:
        print(' ' * offset_x + ROUGE + line + RESET)
    print()
    espace = (colonnes - len("\n                                                   ")) // 2
    print(" " * max(0, espace) + ROUGE + "\n\n\n                                                                               " + RESET)
    print()

def input_clean(prompt):
    valeur = input(prompt)
    sys.stdout.write('\033[1A\033[2K')
    sys.stdout.flush()
    return valeur
# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
def demander_informations():
    try:
        colonnes = shutil.get_terminal_size().columns
    except:
        colonnes = 200
    webhooks_enregistres = charger_webhooks()
    if webhooks_enregistres:
        print()
        print_rouge_centre("Webhooks enregistrés:", colonnes)
        for i, wh in enumerate(webhooks_enregistres, 1):
            print_rouge_centre(f"webhook{i} \"{wh}\"", colonnes)
        print()
    espace_webhook = (colonnes - len("🔗 Webhook URL (numéro ou nouveau lien): ")) // 2
    espace_webhook = max(0, espace_webhook)
    webhook_input = input_clean(" " * espace_webhook + ROUGE + "🔗 Webhook URL (numéro ou nouveau lien): " + RESET).strip()
    if not webhook_input:
        if webhooks_enregistres:
            webhook = webhooks_enregistres[0]
        else:
            webhook = ""# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    elif webhook_input.isdigit():
        index = int(webhook_input) - 1
        if 0 <= index < len(webhooks_enregistres):
            webhook = webhooks_enregistres[index]
        else:
            webhook = ""
    else:
        webhook = webhook_input
    sauvegarder_webhook(webhook)
    espace_username = (colonnes - len("👤 Username: ")) // 2
    espace_username = max(0, espace_username)
    username = input_clean(" " * espace_username + ROUGE + "👤 Username: " + RESET).strip()
    if not username:
        username = "2dx"# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    espace_montant = (colonnes - len("💰 Montant: ")) // 2
    espace_montant = max(0, espace_montant)
    montant = input_clean(" " * espace_montant + ROUGE + "💰 Montant: " + RESET).strip()
    if not montant:
        montant = "0"
    montant_clean = ''.join(c for c in montant if c.isdigit() or c in [',', '.'])
    if not montant_clean:
        montant_clean = "0"
    return webhook, username, montant_clean

def diviser_texte_en_lignes(draw, texte, font, largeur_max):
    mots = texte.split()
    lignes = []# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
    ligne_actuelle = ""
    for mot in mots:
        test_ligne = ligne_actuelle + (" " if ligne_actuelle else "") + mot
        bbox = draw.textbbox((0, 0), test_ligne, font=font)
        largeur_test = bbox[2] - bbox[0]
        if largeur_test <= largeur_max:
            ligne_actuelle = test_ligne
        else:
            if ligne_actuelle:
                lignes.append(ligne_actuelle)
                ligne_actuelle = mot
            else:
                lignes.append(mot)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
                ligne_actuelle = ""
    if ligne_actuelle:
        lignes.append(ligne_actuelle)
    return lignes

def envoyer_image_webhook():
    try:
        webhook_url, username, montant = demander_informations()
        chemin_image = trouver_premier_png()
        if not chemin_image or not os.path.exists(chemin_image):
            try:
                colonnes = shutil.get_terminal_size().columns
            except:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
                colonnes = 200
            print_rouge_centre("❌ Erreur: Aucune image trouvée dans paypalTEMPLATE!", colonnes)
            return
        img = Image.open(chemin_image)
        texte = DEFAULT_TEXTE_TEMPLATE.format(argent=montant, pseudo=username)
        draw = ImageDraw.Draw(img)
        largeur_max = int(img.size[0] * 0.9)
        font = ImageFont.truetype(DEFAULT_POLICE_PATH, 44) if os.path.exists(DEFAULT_POLICE_PATH) else ImageFont.load_default()
        lignes = diviser_texte_en_lignes(draw, texte, font, largeur_max)
        hauteur_ligne = 0
        largeur_max_ligne = 0
        for ligne in lignes:
            bbox = draw.textbbox((0, 0), ligne, font=font)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
            hauteur_ligne = max(hauteur_ligne, bbox[3] - bbox[1])
            largeur_max_ligne = max(largeur_max_ligne, bbox[2] - bbox[0])
        espacement_lignes = int(hauteur_ligne * 0.2)
        hauteur_totale = len(lignes) * hauteur_ligne + (len(lignes) - 1) * espacement_lignes
        pos_y = 60
        y_position = pos_y
        for ligne in lignes:
            bbox_ligne = draw.textbbox((0, 0), ligne, font=font)
            largeur_ligne = bbox_ligne[2] - bbox_ligne[0]
            pos_x_ligne = (img.size[0] - largeur_ligne) // 2
            draw.text((pos_x_ligne, y_position), ligne, fill=(0, 0, 0), font=font)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕
            y_position += hauteur_ligne + espacement_lignes
        font_date = ImageFont.truetype(DEFAULT_POLICE_PATH, 12) if os.path.exists(DEFAULT_POLICE_PATH) else ImageFont.load_default()
        draw.text((450, 262), obtenir_date_fr(), fill=(0, 0, 0), font=font_date)
        font_tr = ImageFont.truetype(DEFAULT_POLICE_PATH, 12) if os.path.exists(DEFAULT_POLICE_PATH) else ImageFont.load_default()
        num_tr = generer_numero_transaction()
        draw.text((37, 262), num_tr, fill=(122, 184, 224), font=font_tr)
        font_a2 = ImageFont.truetype(DEFAULT_POLICE_PATH, 13) if os.path.exists(DEFAULT_POLICE_PATH) else ImageFont.load_default()
        font_a3 = ImageFont.truetype(DEFAULT_POLICE_PATH, 11) if os.path.exists(DEFAULT_POLICE_PATH) else ImageFont.load_default()
        draw.text((465, 477), f"{montant} € EUR", fill=(0, 0, 0), font=font_a2)
        draw.text((465, 325), f"{montant} € EUR", fill=(41, 41, 41), font=font_a3)
        draw.text((465, 420), f"{montant} € EUR", fill=(41, 41, 41), font=font_a3)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        embed = {
            "title": "💸 Simulateur de Transaction",
            "description": f"**@{username}** a reçu **{montant}€**\n\n"# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                           f"❤️ **Merci d'avoir utilisé notre simulateur !** ❤️\n"
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                           f"Rejoin notre discord : https://discord.gg/v5sdJTfAAW\n"
                           f"Merci d'avoir testé notre simulateur de transaction !",
            "color": 0xFF0000,
            "image": {"url": "attachment://image.png"},
            "footer": {"text": "Simulateur de transaction • Créé par 2dx"}
        }
        payload = {"content": "", "embeds": [embed]}
        files_data = {"file": ("image.png", img_buffer, "image/png")}
        data = {"payload_json": json.dumps(payload)}
        r = requests.post(webhook_url, files=files_data, data=data, timeout=10)# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX
        if r.status_code in [200, 204]:
            print_rouge_centre("Envoyé avec succès !")
            sauvegarder_webhook(webhook_url)
        else:
            print_rouge_centre(f"Erreur HTTP: {r.status_code}")
    except Exception as e:
        print_rouge_centre(f"Erreur: {e}")

def ouvrir_lien_discord_si_premiere_fois():
    flag_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".first_launch")
    if os.path.exists(flag_path):
        def open_link():
            _time.sleep(3)
            webbrowser.open_new("https://discord.gg/v5sdJTfAAW")
            try:
                os.remove(flag_path)
            except Exception:
                pass
        threading.Thread(target=open_link, daemon=True).start()


if __name__ == "__main__":
    ouvrir_lien_discord_si_premiere_fois()
    try:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX
        import ctypes
        import platform
        if platform.system() == "Windows":
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 3)
                import keyboard
                _time.sleep(0.2)
                keyboard.press_and_release('f11')
    except Exception:
        pass
    afficher_loading_bar()
    _time.sleep(3)
    first_flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".first_launch")
    if not os.path.exists(first_flag):
        with open(first_flag, "w") as f:
            f.write("1")
        PaypalSimGUI().mainloop()
        try:
            os.remove(first_flag)
        except Exception:
            pass
    else:# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX
        PaypalSimGUI().mainloop()
# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX# jai pris du temps a fair donc copiez pas svp juste utiliser le tool cest tout pls 🤕 2DX