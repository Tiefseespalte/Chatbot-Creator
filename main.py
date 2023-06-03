import json
import random

# Laden der vorhandenen Wissensdatenbank (falls vorhanden)
try:
    with open('knowledge.json', 'r') as file:
        knowledge = json.load(file)
except FileNotFoundError:
    knowledge = {}

# Funktion zum Speichern der aktualisierten Wissensdatenbank
def save_knowledge():
    with open('knowledge.json', 'w') as file:
        json.dump(knowledge, file)

# Funktion zum Hinzufügen von neuen Fragen und Antworten zum Wissen in einem bestimmten Modus
def add_to_knowledge(question, answers, mode):
    if mode not in knowledge:
        knowledge[mode] = {'description': ''}
    knowledge[mode][question] = answers
    save_knowledge()

# Funktion zum Abrufen der Antwort auf eine Frage in einem bestimmten Modus
def get_answer(question, mode):
    if mode in knowledge and question in knowledge[mode]:
        answers = knowledge[mode][question]
        return random.choice(answers)
    else:
        return None

# Funktion zum Erstellen eines benutzerdefinierten Modus mit Beschreibung und optionalem Passwort
def create_custom_mode():
    mode_name = input("Gib den Namen des Modus ein: ")
    mode_description = input("Gib eine Beschreibung für den Modus ein: ")
    use_password = input("Soll der Modus mit einem Passwort geschützt sein? (ja/nein): ")

    if use_password.lower() == 'ja':
        password = input("Gib das Passwort für den Modus ein: ")
        knowledge[mode_name] = {'description': mode_description, 'password': password}
    else:
        knowledge[mode_name] = {'description': mode_description}

    save_knowledge()
    print(f"Der Modus '{mode_name}' wurde erfolgreich erstellt.")

# Funktion zum Ändern des Passworts, Namens und der Beschreibung eines Modus
def change_mode_settings(mode):
    if mode in knowledge:
        print(f"Aktuelle Einstellungen für den Modus '{mode}':")
        print(f"Beschreibung: {knowledge[mode]['description']}")
        print(f"Passwort: {'Ja' if 'password' in knowledge[mode] else 'Nein'}")

        change_description = input("Möchtest du die Beschreibung ändern? (ja/nein): ")
        if change_description.lower() == 'ja':
            new_description = input("Gib die neue Beschreibung ein: ")
            knowledge[mode]['description'] = new_description

        change_password = input("Möchtest du das Passwort ändern? (ja/nein): ")
        if change_password.lower() == 'ja':
            new_password = input("Gib das neue Passwort ein: ")
            knowledge[mode]['password'] = new_password

        save_knowledge()
        print(f"Die Einstellungen für den Modus '{mode}' wurden erfolgreich geändert.")

# Funktion zum Starten des Chatbots im Adminmodus
def start_admin_chatbot():
    while True:
        admin_username = input("Gib den Benutzernamen des Admins ein: ")
        admin_password = input("Gib das Passwort des Admins ein: ")

        if admin_username == 'Main_Admin' and admin_password == 'Admin_D':
            print("Admin-Modus aktiviert!")
            print("1. Modus erstellen")
            print("2. Modus-Einstellungen ändern")
            print("3. Beenden")

            choice = input("Gib die Nummer der gewünschten Aktion ein: ")

            if choice == '1':
                create_custom_mode()
            elif choice == '2':
                mode_to_change = input("Gib den Namen des Modus ein, dessen Einstellungen du ändern möchtest: ")
                change_mode_settings(mode_to_change)
            elif choice == '3':
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Auswahl. Bitte versuche es erneut.")
        else:
            print("Falscher Benutzername oder Passwort. Fortsetzung der Konversation.")

# Funktion zum Starten des Chatbots im Normalmodus
def start_normal_chatbot():
    modes = list(knowledge.keys())

    # Auswahl des Modus
    print("Willkommen im Chatbot!")
    print("Wähle einen Modus aus:")
    for i, mode in enumerate(modes):
        print(f"{i+1}. {mode}")

    print(f"{len(modes)+1}. Neuen Modus erstellen")

    selected_mode_index = int(input("Gib die Nummer des Modus ein: ")) - 1

    if selected_mode_index == len(modes):
        create_custom_mode()
        return

    selected_mode = modes[selected_mode_index]

    # Überprüfen des Modus-Passworts, falls vorhanden
    if 'password' in knowledge[selected_mode]:
        password = input("Gib das Passwort für den Modus ein: ")

        while password != knowledge[selected_mode]['password']:
            print("Falsches Passwort! Bitte versuche es erneut.")
            password = input("Gib das Passwort für den Modus ein: ")

    # Chatbot-Logik
    while True:
        user_input = input("Frag mich etwas: ")

        if user_input.lower() == 'bye':
            print("Auf Wiedersehen!")
            break

        if user_input.lower() == 'beschreibung':
            mode_description = knowledge[selected_mode]['description']
            print(f"Beschreibung des Modus '{selected_mode}': {mode_description}")
            continue

        answer = get_answer(user_input, selected_mode)

        if answer is not None:
            print(answer)
        else:
            print("Das weiß ich nicht. Kannst du mir die richtige Antwort sagen?")
            correct_answer = input("Richtige Antwort: ")
            is_multiple_choice = input("Gibt es mehrere Antwortmöglichkeiten? (ja/nein): ")

            if is_multiple_choice.lower() == 'ja':
                answers = []
                while True:
                    answer_option = input("Antwortmöglichkeit (eine leere Eingabe beendet die Eingabe): ")
                    if answer_option == '':
                        break
                    answers.append(answer_option)
            else:
                answers = [correct_answer]

            add_to_knowledge(user_input, answers, selected_mode)
            print("Danke, ich habe das Wissen aktualisiert.")

# Hauptprogramm
print("Willkommen!")
print("Wähle einen Modus:")
print("1. Adminmodus")
print("2. Normaler Modus")

mode_choice = input("Gib die Nummer des gewünschten Modus ein: ")

if mode_choice == '1':
    start_admin_chatbot()
elif mode_choice == '2':
    start_normal_chatbot()
else:
    print("Ungültige Auswahl. Das Programm wird beendet.")
