from ai_handler import *
import sys

npcs = []


global sessions
global NPC_Manager_ID
global Conflict_Resolution_Checker_ID
global conflict_resolution_question

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

npc_to_color = {
    "Jett": f"{bcolors.BOLD}{bcolors.OKGREEN}Jett{bcolors.ENDC}",
    "Knox": f"{bcolors.BOLD}{bcolors.OKBLUE}Knox{bcolors.ENDC}",
    "Player": f"{bcolors.BOLD}{bcolors.OKCYAN}Player{bcolors.ENDC}"
}

# Have the NPC manager generate a scenario
def init_npc_manager(session_id, prompt_file):
    with open(prompt_file, 'r') as f:
        NPCmanager_prompt = f.read()

    init_scenario = send_chat(session_id, NPCmanager_prompt, sessions)
    return BeautifulSoup(init_scenario, "html.parser")

# Have the NPC manager generate a scenario
def init_conflict_resolution_checker(session_id, prompt_file):
    with open(prompt_file, 'r') as f:
        ConflictResolution_prompt = f.read()

    send_chat(session_id, ConflictResolution_prompt, sessions)

# Initialize a NPC agent with a system prompt
def init_npc(session_id, prompt):
    return send_system_preset(session_id, prompt, sessions)

# Send a message to an NPC agent
def chat_npc(session_id, prompt):
    return send_chat(session_id, prompt, sessions)

# Send a message to an NPC agent that the agent will "forget"
def chat_npc_forgetful(session_id, prompt):
    return send_chat_without_saving(session_id, prompt, sessions)

end_words=["done", "take care", "bye", "adios", "nvm", "nevermind"]

def evaluate_conflict(n,npc,new_responses):
    print("Evaluating conflict...\n")
    responses = ""
    for n in npcs:
        new_responses[n] = 0
        responses += f"{n}'s response:\n"
        responses += chat_npc_forgetful(n, conflict_resolution_question) + "\n\n"

    evaluation = chat_npc(Conflict_Resolution_Checker_ID, responses)
    print(f"Evaluation: {evaluation}")
    return responses,new_responses


def chat_loop():
    print("\n\n\n\n\n\n")
    print(f"{bcolors.HEADER}~~~ Welcome to the AI NPC chat demo! ~~~{bcolors.ENDC}\n\n")
    print(f"Available NPCs: {npcs}\n\n"
            + "Commands\n\n"
            + "TALK <NPC>\tEnd any current conversations and talk to the given NPC.\n"
            + "QUIT\t\tEnd chat session.\n"
            + "EVALUATE\t\tEvaluate current conflict status.")

    npc = ""
    convo_len=0

    new_responses = {}
    for n in npcs:
        new_responses[n] = 0

    while True:
        user_input = input(f"\n{npc_to_color['Player']}\n> ")
        print()
        user_isdone= any(word in user_input.lower() for word in end_words)
        if (user_input.lower() == "evaluate"):
            responses,new_responses=evaluate_conflict(n,npc,new_responses)
        elif (user_input.lower() == "q" or user_input.lower() == "quit" or user_isdone):
            if(user_isdone):
                responses,new_responses=evaluate_conflict(n,npc,new_responses)
                print("Well Played")
            break
        elif (user_input.split(" ")[0].lower() == "talk"):
            new_npc = " ".join(user_input.split(" ")[1:])
            if (not new_npc in npcs):
                print(f"{new_npc} is not a valid NPC.")
                continue
            if (npc != ""):
                print(f"You are no longer talking to {npc_to_color[npc].strip()}.")
            npc = new_npc
            print(f"You are now talking to {npc_to_color[npc].strip()}.")
        elif (npc == ""):
            print("You are not talking to anyone yet.")
        else:
            convo_len+=1
            response = chat_npc(npc, "" + user_input)
            new_responses[npc] = 1
            print(f"{npc_to_color[npc]}\n{response}\n")

        # uncomment this to see conflict score after each response
        # allNew = True
        # for n in npcs:
        #     if (new_responses[n] == 0):
        #         allNew = False
        #         break
        # if (allNew):
            
            #responses,new_responses=evaluate_conflict(n,npc,new_responses)


if __name__ == "__main__":

    args = sys.argv

    new_game = False
    if (len(args) > 1):
        if args[1] in ["-n", "--new"]:
            new_game = True
        else:
            print(f"Usage: {args[0]} [-n|--new]")
            sys.exit(1)

    NPC_Manager_ID = 'NPC_Manager'
    Conflict_Resolution_Checker_ID = 'Conflict_Resolver'
    Jett_ID = "Jett"
    Knox_ID = "Knox"
    npcs.append(Jett_ID)
    npcs.append(Knox_ID)

    with open("ConflictResolution_question.txt", 'r') as f:
        conflict_resolution_question = f.read()

    sessions = None
    if not new_game:
        sessions = load_sessions()

    if (not sessions):
        # If failed to load sessions from file
        # Generate a whole new scenario and set up agents
        print("Starting a new game...")
        sessions = {}
        Bs_data = init_npc_manager(NPC_Manager_ID, 'NPCmanager_prompt.txt')
        init_conflict_resolution_checker(Conflict_Resolution_Checker_ID, 'ConflictResolution_prompt.txt')

        background_jett = Bs_data.find('background', class_=Jett_ID)
        background_knox = Bs_data.find('background', class_=Knox_ID)
        met = Bs_data.find('met')
        bond = Bs_data.find('bond')
        pastime = Bs_data.find('pastime')
        conflict = Bs_data.find('conflict')
        pov_jett = Bs_data.find('pov', class_=Jett_ID)
        pov_knox = Bs_data.find('pov', class_=Knox_ID)

        additional_instructions = "You can eventually be convinced to make up with them in this role playing session, if the player does their job well. Give brief responses, as might be expected from a video game character. You should end the conversation if user seems disinterested. Assume the player knows nothing about your conflict or backstories."

        jett_init_text = "You are role playing as a character called Jett (female) who is recently having a conflict with her close friend Knox (male). Player is trying to resolve the conflict and get you and Knox to talk to each other again, but you and Knox are bitter about the situation and it is difficult to talk to about it at first." + " " + additional_instructions
        knox_init_text = "You are role playing as a character called Knox (male) who is recently having a conflict with his close friend Jett (female). Player is trying to resolve the conflict and get you and Jett to talk to each other again, but you and Jett are bitter about the situation and it is difficult to talk to about it at first." + " " + additional_instructions
        jett_full_prompt = f"{jett_init_text}\n\n=== Your Background ===\n\n{background_jett}\n\n=== Knox's Background ===\n{background_knox}\n\n=== How You and Knox Met ===\n{met}\n\n=== What You Bonded Over ===\n{bond}\n\n=== You and Knox's Favorite Pastime ===\n{pastime}\n\n=== Relationship Conflict ===\n\n{conflict}\n\n=== Your POV ===\n\n{pov_jett}"
        knox_full_prompt = f"{knox_init_text}\n\n=== Your Background ===\n\n{background_knox}\n\n=== Jett Background ===\n{background_jett}\n\n=== How You and Jett Met ===\n{met}\n\n=== What You Bonded Over ===\n{bond}\n\n=== You and Jett's Favorite Pastime ===\n{pastime}\n\n=== Relationship Conflict ===\n\n{conflict}\n\n=== Your POV ===\n\n{pov_knox}"

        init_npc(Jett_ID, jett_full_prompt)
        init_npc(Knox_ID, knox_full_prompt)

    else:
        print("Loaded previous session data.")

    try:
        chat_loop()
    except KeyboardInterrupt:
        print("\nSession interrupted by user")
    print("Saving...")
    save_data(sessions)

