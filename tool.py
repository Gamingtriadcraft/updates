import requests
import os
import json
import colorama
from colorama import Fore, init
import keyboard
from os import system, name








os.system('Title TOOL - by YE')
os.system("cls")
colorama.init(autoreset=True)

# made by gamingtriadcraft, pls dont skid
logo = fr"""
 {Fore.GREEN}_________  ________  ________  ___          
{Fore.WHITE}|\___   ___\\   __   \|\   __   \|\  \         
{Fore.GREEN}\|___ \  \_\ \  \|\  \ \  \|\  \ \  \        
{Fore.WHITE}     \ \  \ \ \  \\\  \ \  \\\  \ \  \       
 {Fore.GREEN}     \ \  \ \ \  \\\  \ \  \\\  \ \  \____  
 {Fore.WHITE}       \ \__\ \ \_______\ \_______\ \_______\
          {Fore.GREEN} \|__|  \|_______|\|_______|\|_______|             Made by: Gamingtriadcraft
"""

while True:
    print(logo)
    print("[1] Kanye west")
    print("[2] STAY TUNED")
    print("[3] STAY TUNED")
    print("[4] discord multitool menu")
    print("[5] Exit")
    
    x = input("Enter your choice: ")

    if x == "1":
        os.system("cls")
        print(logo)
        # Fetching the quote - Kanye API returns {'quote': 'text'}
        r = requests.get("https://api.kanye.rest").json()
        quote = r.get('quote', 'Could not fetch quote.')
        print(f"{Fore.GREEN}{r}.json")
        input(f"{Fore.WHITE}Press Enter to return to menu...")
        os.system("cls")

    elif x == "2" or x == "3":
        os.system("cls")
        print(logo)
        print(f"{Fore.GREEN}More features coming soon!")
        input(f"{Fore.WHITE}Press Enter to return to menu...")
        os.system("cls")

    elif x == "4":
        os.system("cls")
        print(logo)
        print(f"{Fore.RED}get a life you absolute skid")
        input(f"{Fore.WHITE}Press Enter to return to menu...")
        os.system("cls")

    elif x == "5":
        print("Exiting...")
        break
    
    else:
        print(f"{Fore.RED}Invalid selection, try again.")
        os.system("cls")