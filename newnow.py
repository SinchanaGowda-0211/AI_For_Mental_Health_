import time
import random
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# ---------------------- Helper UI functions ----------------------
def type_print(text, color=Fore.WHITE, delay=0.03):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(text="Thinking"):
    type_print(text, Fore.CYAN, 0.05)
    for _ in range(3):
        print(Fore.CYAN + ".", end='', flush=True)
        time.sleep(0.4)
    print("\n")

# ---------------------- Safety and emotion detection ---------------------- 
def detect_harmful(user_input):
    harmful_keywords = [
        "die", "suicide", "kill myself", "end my life",
        "no reason to live", "hurt myself", "i want to die", "i'm gonna die"
    ]
    return any(word in user_input.lower() for word in harmful_keywords)

def handle_harmful_input():
    type_print(Fore.RED + "\n💔 That sounds really heavy. You’re not alone.", Fore.RED)
    type_print(Fore.YELLOW + "Please talk to someone you trust or a professional. 🌸", Fore.YELLOW)
    type_print(Fore.CYAN + "If you’re in immediate danger, reach out to your local helpline or go to a safe place.\n", Fore.CYAN)

    # Calming tips
    type_print("Meanwhile, here are a few gentle ways to feel a bit better:", Fore.GREEN)
    calming_tips = [
        "🌿 Take deep breaths slowly",
        "🎶 Listen to soft music or nature sounds",
        "💬 Talk to a close friend or family member",
        "🕯️ Sit somewhere peaceful and comfortable",
        "📔 Write your thoughts or doodle something small",
        "🐾 Pet an animal if you have one nearby"
    ]
    for tip in calming_tips:
        type_print(tip, Fore.MAGENTA)
        time.sleep(0.3)

    type_print("\nLet’s try some fun things to lift your mood a bit. 💛", Fore.CYAN)
    fun_suggestions()

# ---------------------- Chat flow ----------------------
def get_age():
    while True:
        type_print(Fore.YELLOW + "Hey there! How old are you?", Fore.YELLOW)
        age_input = input()
        try:
            age = int(age_input)
            if age < 12:
                type_print(Fore.RED + "Sorry, this chat is for ages 12 and above. 😊")
                type_print(Fore.CYAN + "Thank you and have a good day! 🌸")
                exit()
            else:
                return age
        except ValueError:
            type_print(Fore.RED + "Oops! That doesn’t seem like a number. Try again.", Fore.RED)

def show_worries(age):
    if 12 <= age <= 18:
        worries = ["School stress", "Friends/Family issues", "Body image/social media", "Big life changes"]
    elif 18 < age <= 25:
        worries = ["Career choices", "Money worries", "Independence & changes", "Relationship stuff"]
    elif 25 < age <= 35:
        worries = ["Work stress", "Balancing family", "Financial planning", "Relationship concerns"]
    elif 35 < age <= 50:
        worries = ["Work pressure", "Raising kids/teens", "Caring for parents", "Health concerns"]
    else:
        worries = ["General worries"]

    type_print("\nHere are some things people your age often feel stressed about:", Fore.MAGENTA)
    for idx, w in enumerate(worries, 1):
        type_print(f"{idx}. {w}", Fore.CYAN)

    type_print("\nPick one that feels most relevant to you (just the number is fine):", Fore.YELLOW)
    choice = input("Your choice: ").strip()
    try:
        idx = int(choice)
        if 1 <= idx <= len(worries):
            selected_worry = worries[idx - 1]
        else:
            selected_worry = worries[0]
    except:
        selected_worry = worries[0]

    loading_animation("Thinking about it")
    return selected_worry

def follow_up(worry):
    type_print(f"\nThanks for sharing about '{worry}'. That can really weigh on someone’s mind.", Fore.MAGENTA)
    while True:
        type_print("Can you tell me a little about what makes it stressful?", Fore.YELLOW)
        answer = input()
        if detect_harmful(answer):
            handle_harmful_input()
            continue  # continue chat
        if answer.strip() == "":
            type_print(Fore.RED + "Please type something, even a few words. 😊")
            continue
        type_print(random.choice([
            "That sounds understandable. You’re doing your best. 💛",
            "I get it, sometimes things really pile up. You’re not alone. 🌸",
            "Thank you for opening up — it takes courage. 🌿"
        ]), Fore.GREEN)
        break

    while True:
        type_print("Here are some activities that might help you feel a bit better: 🎉", Fore.CYAN)
        fun_suggestions()
        type_print("Do you feel a bit lighter now? (type 'yes' or 'no')", Fore.YELLOW)
        answer2 = input().lower()
        if detect_harmful(answer2):
            handle_harmful_input()
            continue
        break

def fun_suggestions():
    # Predefined suggestions
    game_suggestions = [
        "Play a quick puzzle or funny game 🎮",
        "Try a light mobile game to laugh a bit 😂",
        "Play a memory or brain teaser game 🧠"
    ]
    music_suggestions = [
        "Listen to an upbeat playlist 🎵",
        "Try relaxing classical or lo-fi beats 🎹",
        "Sing along to a song you love! 🎤"
    ]
    movie_suggestions = [
        "Watch a funny short film or cartoon 🎬",
        "Try a light-hearted comedy show 🍿",
        "Watch an uplifting or inspiring clip online 🌈"
    ]
    mini_activities = [
        "Draw or doodle something silly ✏️",
        "Step outside for a few minutes 🌿",
        "Message a friend who makes you laugh 😄",
        "Try a 1-minute silly dance 💃"
    ]

    type_print(random.choice(game_suggestions), Fore.MAGENTA)
    type_print(random.choice(music_suggestions), Fore.MAGENTA)
    type_print(random.choice(movie_suggestions), Fore.MAGENTA)
    type_print(random.choice(mini_activities), Fore.MAGENTA)

def mood_tracker():
    while True:
        try:
            rating = int(input(Fore.YELLOW + "\nOn a scale of 1–10, how stressed are you feeling right now? "))
            if 1 <= rating <= 10:
                break
            else:
                type_print(Fore.RED + "Please pick a number between 1 and 10.", Fore.RED)
        except:
            type_print(Fore.RED + "That’s not a number, try again.", Fore.RED)
    loading_animation("Analyzing your stress level")
    type_print(f"Your stress level: {rating}/10", Fore.GREEN)
    if rating >= 7:
        type_print("Take a deep breath 😌. Maybe a calm playlist or gentle walk could help.", Fore.CYAN)
    elif rating >= 4:
        type_print("A small fun activity might make your day brighter. 🌈", Fore.CYAN)
    else:
        type_print("You seem relaxed. Keep enjoying your peaceful energy. 😄", Fore.CYAN)

# ---------------------- Continuous chat ----------------------
def chat_loop():
    type_print(Fore.CYAN + "\nYou can talk to me about anything, or type 'bye' to exit anytime.", Fore.CYAN)
    while True:
        type_print(Fore.YELLOW + "\nWhat would you like to talk about or do now?")
        user_input = input()
        if user_input.strip().lower() in ["bye", "exit", "quit"]:
            type_print(Fore.CYAN + "\nIt was really nice chatting with you! Take care and stay safe. 💖")
            break
        if detect_harmful(user_input):
            handle_harmful_input()
            continue
        if user_input.strip() == "":
            type_print(Fore.RED + "Please type something. 😊")
            continue

        # Random friendly responses or suggestions
        type_print(random.choice([
            "That’s interesting! 🌟",
            "I see… let’s think of something fun you can do! 🎉",
            "Hmm… I’ve got a few ideas that might cheer you up. 😄"
        ]), Fore.GREEN)
        fun_suggestions()

# ---------------------- Main ----------------------
def main():
    type_print(Fore.CYAN + "🌸 Welcome to the Friendly & Safe Chatbot 🌸")
    age = get_age()
    worry = show_worries(age)
    follow_up(worry)
    mood_tracker()
    chat_loop()

if __name__ == "__main__":
    main()
