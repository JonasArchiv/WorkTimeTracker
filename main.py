import json
import os
from datetime import datetime

data_file = 'work_manager.json'


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return {'users': [], 'work': [], 'current_sessions': {}}


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


def start_session(data):
    list_users(data)
    try:
        user_id = int(input("Geben Sie die ID des Nutzers zum Starten der Arbeitszeit ein: "))
        if user_id in data['current_sessions']:
            print("Eine Sitzung ist bereits aktiv. Bitte beenden Sie diese zuerst.")
            return
        data['current_sessions'][user_id] = datetime.now().isoformat()
        save_data(data)
        print("Arbeitszeit gestartet.")
    except ValueError:
        print("Ungültige Eingabe für ID. Bitte geben Sie eine gültige Zahl ein.")


def end_session(data):
    try:
        user_id = int(input("Geben Sie die ID des Nutzers zum Beenden der Arbeitszeit ein: "))
        if user_id not in data['current_sessions']:
            print("Keine aktive Sitzung für diese ID gefunden.")
            return
        start_time = datetime.fromisoformat(data['current_sessions'].pop(user_id))
        end_time = datetime.now()
        hours_worked = (end_time - start_time).total_seconds() / 3600
        date = end_time.strftime('%Y-%m-%d')
        data['work'].append({'id': user_id, 'hours': hours_worked, 'paid': False, 'date': date})
        save_data(data)
        print(f"Arbeitszeit beendet. Erfasste Stunden: {hours_worked:.2f}")
    except ValueError:
        print("Ungültige Eingabe für ID. Bitte geben Sie eine gültige Zahl ein.")


def show_hours(data):
    try:
        user_id = int(input("Geben Sie die ID des Nutzers ein: "))
        total_hours = 0
        total_paid = 0
        total_unpaid = 0
        for work in data['work']:
            if work['id'] == user_id:
                total_hours += work['hours']
                if work['paid']:
                    total_paid += work['hours']
                else:
                    total_unpaid += work['hours']
        print(f"Gesamtstunden: {total_hours:.2f}")
        print(f"Bezahlte Stunden: {total_paid:.2f}")
        print(f"Unbezahlte Stunden: {total_unpaid:.2f}")
    except ValueError:
        print("Ungültige Eingabe für ID. Bitte geben Sie eine gültige Zahl ein.")


def calculate_pay(data):
    try:
        user_id = int(input("Geben Sie die ID des Nutzers ein: "))
        user = next((u for u in data['users'] if u['id'] == user_id), None)
        if user:
            total_hours = 0
            for work in data['work']:
                if work['id'] == user_id:
                    total_hours += work['hours']
            pay = total_hours * user['hourly_wage']
            print(f"Gesamtverdienst: {pay:.2f}")
        else:
            print("User nicht gefunden")
    except ValueError:
        print("Ungültige Eingabe für ID. Bitte geben Sie eine gültige Zahl ein.")


def generate_report(data):
    try:
        user_id = int(input("Geben Sie die ID des Nutzers für den Bericht ein: "))
        start_date = input("Startdatum (YYYY-MM-DD): ")
        end_date = input("Enddatum (YYYY-MM-DD): ")
        user = next((u for u in data['users'] if u['id'] == user_id), None)
        if user:
            total_hours = 0
            total_paid = 0
            total_unpaid = 0
            for work in data['work']:
                if work['id'] == user_id and start_date <= work['date'] <= end_date:
                    total_hours += work['hours']
                    if work['paid']:
                        total_paid += work['hours']
                    else:
                        total_unpaid += work['hours']
            print(f"Bericht für {user['name']} {user['lastname']}:")
            print(f"Gesamtstunden: {total_hours:.2f}")
            print(f"Bezahlte Stunden: {total_paid:.2f}")
            print(f"Unbezahlte Stunden: {total_unpaid:.2f}")
        else:
            print("User nicht gefunden")
    except ValueError:
        print("Ungültige Eingabe für ID oder Datum. Bitte geben Sie gültige Zahlen oder Daten ein.")

