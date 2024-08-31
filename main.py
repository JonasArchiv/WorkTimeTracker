import json
import os
from datetime import datetime

data_file = 'work_manager.json'


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return {'users': [], 'work': []}


def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


def generate_id(users):
    return max([user['id'] for user in users], default=0) + 1


def list_users(data):
    print("ID | Name | Nachname | Stundenlohn")
    for user in data['users']:
        print(f"{user['id']} | {user['name']} | {user['lastname']} | {user['hourly_wage']:.2f}")


def add_user(data):
    try:
        name = input("Name: ")
        lastname = input("Nachname: ")
        hourly_wage = float(input("Stundenlohn: "))
        user_id = generate_id(data['users'])
        data['users'].append({'id': user_id, 'name': name, 'lastname': lastname, 'hourly_wage': hourly_wage})
        save_data(data)
        print(f"User hinzugefügt mit ID {user_id}")
    except ValueError:
        print("Ungültige Eingabe für Stundenlohn. Bitte geben Sie eine Zahl ein.")


def edit_user(data):
    list_users(data)
    try:
        user_id = int(input("Geben Sie die ID des zu bearbeitenden Nutzers ein: "))
        for user in data['users']:
            if user['id'] == user_id:
                user['name'] = input(f"Neuer Name (aktuell {user['name']}): ") or user['name']
                user['lastname'] = input(f"Neuer Nachname (aktuell {user['lastname']}): ") or user['lastname']
                user['hourly_wage'] = float(
                    input(f"Neuer Stundenlohn (aktuell {user['hourly_wage']:.2f}): ") or user['hourly_wage'])
                save_data(data)
                print("User erfolgreich bearbeitet")
                return
        print("User nicht gefunden")
    except ValueError:
        print("Ungültige Eingabe für Stundenlohn oder ID. Bitte geben Sie eine gültige Zahl ein.")
