from ai_handler import *

npcs = []

global sessions

def init_npc_manager(session_id, prompt_file):
    with open(prompt_file, 'r') as f:
        NPCmanager_prompt = f.read()

    init_scenario = send_chat(session_id, NPCmanager_prompt, sessions)
    return BeautifulSoup(init_scenario, "html.parser")

def init_npc(session_id, prompt):
    return send_system_preset(session_id, prompt, sessions)

def chat_npc(session_id, prompt):
    return send_chat(session_id, prompt, sessions)

def chat_loop():
    print("\n\n\n\n\n\n")
    print("~~~ Welcome to the AI NPC chat demo! ~~~\n\n")
    print(f"Available NPCs: {npcs}\n\n"
            + "Commands\n\n"
            + "TALK <NPC>\tEnd any current conversations and talk to the given NPC.\n"
            + "QUIT\t\tEnd chat session.\n")

    npc = ""

    while True:
        user_input = input("\n> ")
        if (user_input.lower() == "q" or user_input.lower() == "quit"):
            break
        elif (user_input.split(" ")[0].lower() == "talk"):
            if (npc != ""):
                print(f"You are no longer talking to {npc}.")
            npc = " ".join(user_input.split(" ")[1:])
            print(f"You are now talking to {npc}.")
        elif (npc == ""):
            print("You are not talking to anyone yet.")
        else:
            response = chat_npc(npc, "" + user_input)
            print(f"{npc}: {response}\n")


if __name__ == "__main__":
    # Add code to run when module2.py is executed from the command line

    NPC_Manager_ID = 'NPC_Manager'
    Jett_ID = "Jett"
    Knox_ID = "Knox"
    npcs.append(Jett_ID)
    npcs.append(Knox_ID)

    sessions = load_sessions()
    if (not sessions):
        sessions = {}
        Bs_data = init_npc_manager(NPC_Manager_ID, 'NPCmanager_prompt.txt')

        background_jett = Bs_data.find('background', class_=Jett_ID)
        background_knox = Bs_data.find('background', class_=Knox_ID)
        met = Bs_data.find('met')
        bond = Bs_data.find('bond')
        pastime = Bs_data.find('pastime')
        conflict = Bs_data.find('conflict')
        pov_jett = Bs_data.find('pov', class_=Jett_ID)
        pov_knox = Bs_data.find('pov', class_=Knox_ID)

        additional_instructions = "Give brief responses, as might be expected from a video game character."

        jett_init_text = "You are role playing as a character called Jett who is recently having a conflict with her close friend Knox. Player is trying to resolve the conflict and get you and Knox to talk to each other again, but you and Knox are bitter about the situation and it is difficult to talk to about it at first." + " " + additional_instructions
        knox_init_text = "You are role playing as a character called Knox who is recently having a conflict with his close friend Jett. Player is trying to resolve the conflict and get you and Jett to talk to each other again, but you and Jett are bitter about the situation and it is difficult to talk to about it at first." + " " + additional_instructions
        jett_full_prompt = f"{jett_init_text}\n\n=== Background ===\n\n{background_jett}\n{met}\n{bond}\n{pastime}\n\n=== Conflict ===\n\n{conflict}\n\n=== POV ===\n\n{pov_jett}"
        knox_full_prompt = f"{knox_init_text}\n\n=== Background ===\n\n{background_knox}\n{met}\n{bond}\n{pastime}\n\n=== Conflict ===\n\n{conflict}\n\n=== POV ===\n\n{pov_knox}"

        init_npc(Jett_ID, jett_full_prompt)
        init_npc(Knox_ID, knox_full_prompt)

    chat_loop()

    save_data(sessions)

