import random
import re
import math
import sys

# =====================================================================
# 1. NEURAL NETWORK ENGINE
# =====================================================================
class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_hidden = [[0.1, -0.2, 0.4], [-0.3, 0.5, -0.6]]
        self.weights_hidden_output = [[-0.4], [0.2], [0.7]]
        self.bias_hidden = [0.1, -0.1, 0.2]
        self.bias_output = [-0.1]

    def forward(self, inputs):
        self.inputs = inputs
        self.hidden_layer_input = [0.0] * len(self.bias_hidden)
        for j in range(len(self.bias_hidden)):
            act = self.bias_hidden[j] + sum(inputs[i] * self.weights_input_hidden[i][j] for i in range(len(inputs)))
            self.hidden_layer_input[j] = 1 / (1 + math.exp(-max(-50, min(50, act))))
        act_out = self.bias_output + sum(self.hidden_layer_input[j] * self.weights_hidden_output[j] for j in range(len(self.bias_hidden)))
        self.output_layer_input = 1 / (1 + math.exp(-max(-50, min(50, act_out))))
        return self.output_layer_input

# =====================================================================
# 2. MASTER ACADEMIC & WORLD ENCYCLOPEDIA ENGINE
# =====================================================================
class UnifiedMasterAI:
    def __init__(self):
        self.nn = SimpleNeuralNetwork(2, 3, 1)

        self.chat_kb = {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "greetings", "yo", "sup"],
                "responses": ["Hello! Ask me any question about the world, science, English, or try a math problem!", "Hey there! Ready to explore facts?"]
            },
            "identity": {
                "patterns": ["who are you", "what is your name", "tell me about yourself", "your name"],
                "responses": ["I am a zero-dependency AI engine running natively in your VS Code.", "You can call me PythonLocalAI. I don't need external keys or modules!"]
            },
            "status": {
                "patterns": ["how are you", "how is it going", "how do you feel"],
                "responses": ["I am functioning optimally on your CPU!", "Systems are 100% green and ready."]
            },
            "jokes": {
                "patterns": ["tell me a joke", "make me laugh", "joke"],
                "responses": [
                    "Why do programmers wear glasses? Because they can't C#!",
                    "There are 10 types of people in the world: those who understand binary, and those who don't."
                ]
            }
        }

        self.geography_kb = {
            "asia": "Asia is the largest and most populous continent, covering 30% of Earth's land and holding over 4.7 billion people.",
            "africa": "Africa is the second-largest continent, containing 54 sovereign countries and the massive Sahara Desert.",
            "europe": "Europe is divided into roughly 50 sovereign states, known historically for its global industrial impact.",
            "north america": "North America contains Canada, the US, Mexico, and Greenland.",
            "south america": "South America is home to the Amazon Rainforest and the spectacular Andes Mountain range.",
            "australia": "Australia (Oceania) is the smallest continent, famous for its completely unique wildlife ecosystems.",
            "antarctica": "Antarctica is the coldest continent on Earth. It is 98% covered by ice sheet layers.",
            "earth": "Earth is the third planet from the Sun and is roughly 4.54 billion years old.",
            "population": "The human population of Earth has surpassed 8 billion people across 7 continents.",
            "oceans": "Earth has 5 major oceans: Pacific (largest), Atlantic, Indian, Southern, and Arctic.",
            "mountains": "The highest mountain is Mount Everest (8,848m). The longest range is the Andes."
        }

        self.country_kb = {
            "brazil": "Brazil is the largest country in South America, speaking Portuguese and holding the Amazon Basin.",
            "japan": "Japan is an island country in East Asia known for rich traditional culture and cutting-edge tech.",
            "egypt": "Egypt links northeast Africa with the Middle East, featuring monuments like the Giza Pyramids.",
            "canada": "Canada is the second-largest country by area and shares the world's longest land border with the USA.",
            "india": "India is located in South Asia and is the world's most populous country.",
            "china": "China is a powerhouse in East Asia, featuring historical marvels like the Great Wall."
        }

        self.history_kb = {
            "ancient egypt": "Ancient Egypt was a powerful Nile civilization thriving from 3100 BCE, known for pyramids and writing.",
            "roman empire": "The Roman Empire established modern foundations for Western law, engineering, and art.",
            "industrial revolution": "The Industrial Revolution (1760–1840) was a global transition to machine manufacturing.",
            "world war": "The 20th century saw World War I (1914-1918) and World War II (1939-1945), reshaping world boundaries."
        }

        self.science_kb = {
            "photosynthesis": "Photosynthesis is the process where plants use sunlight, water, and CO2 to create oxygen and energy.",
            "gravity": "Gravity pulls objects together. On Earth, it causes objects to accelerate downward at roughly 9.8 m/s².",
            "atom": "An Atom is the basic building block of chemistry, consisting of a nucleus surrounded by electrons.",
            "dna": "DNA contains the genetic instructions for the development and functioning of all living organisms.",
            "water": "Water is H2O. It freezes at 0°C (32°F) and boils at 100°C (212°F).",
            "speed of light": "The speed of light in a vacuum is exactly 299,792,458 meters per second."
        }

        self.english_kb = {
            "noun": "A Noun identifies a person, place, or thing. Examples: 'VS Code', 'Python'.",
            "verb": "A Verb is an action word describing what the subject is doing. Examples: 'run', 'calculate'.",
            "adjective": "An Adjective modifies or describes a noun. Examples: 'intelligent', 'fast'.",
            "pronoun": "A Pronoun replaces a noun to avoid repetition. Examples: 'he', 'she', 'it'.",
            "synonym": "Synonyms are different words that share identical meanings. Example: 'Fast' and 'Quick'."
        }

    def is_prime(self, n):
        if n < 2: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    def process_math_and_neural(self, text):
        numbers = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]

        if "xor" in text and len(numbers) == 2:
            val1, val2 = int(numbers[0]), int(numbers[1])
            if (val1 == 0 or val1 == 1) and (val2 == 0 or val2 == 1):
                pred = self.nn.forward([val1, val2])
                return f"🧠 [Neural Network Engine]: XOR prediction for [{val1}, {val2}] is {pred:.4f} (Binary: {1 if pred > 0.5 else 0})"

        if "prime" in text and len(numbers) >= 1:
            num = int(numbers[0])
            status = "PRIME" if self.is_prime(num) else "COMPOSITE"
            return f"🔢 [Math Engine]: The number {num} is a {status} number."

        if len(numbers) < 2: return None
        n1, n2 = numbers[0], numbers[1]
        n1 = int(n1) if n1.is_integer() else n1
        n2 = int(n2) if n2.is_integer() else n2

        if any(w in text for w in ["add", "plus", "+"]): return f"🔢 [Math Engine]: {n1} + {n2} = {n1 + n2}"
        if any(w in text for w in ["subtract", "minus", "-"]): return f"🔢 [Math Engine]: {n1} - {n2} = {n1 - n2}"
        if any(w in text for w in ["multiply", "times", "*"]): return f"🔢 [Math Engine]: {n1} × {n2} = {n1 * n2}"
        if any(w in text for w in ["divide", "divided by", "/"]):
            return f"🔢 [Math Engine]: {n1} ÷ {n2} = {n1 / n2:.4f}" if n2 != 0 else "🔢 [Math Engine]: Error: Division by zero!"
        return None

    def get_response(self, user_query):
        cleaned = user_query.lower().strip()
        
        math_res = self.process_math_and_neural(cleaned)
        if math_res: return math_res

        for key, fact in self.science_kb.items():
            if key in cleaned: return f"🔬 [Science Fact]: {fact}"

        for key, rule in self.english_kb.items():
            if key in cleaned: return f"📖 [English Rule]: {rule}"

        for key, fact in self.geography_kb.items():
            if key in cleaned: return f"🌍 [Geography Fact]: {fact}"

        for country, fact in self.country_kb.items():
            if country in cleaned: return f"🏳️‍🌈 [Country Fact]: {fact}"

        for event, fact in self.history_kb.items():
            if event in cleaned: return f"⏳ [History Fact]: {fact}"

        for intent, data in self.chat_kb.items():
            for pattern in data["patterns"]:
                if pattern in cleaned: return f"🤖 AI Response: {random.choice(data['responses'])}"
                    
        return "🤖 AI Response: I don't have that in my system database yet. Ask about 'XOR 1 0', 'gravity', 'nouns', 'Japan', or 'multiply 12 by 12'."

# =====================================================================
# 3. INTERACTIVE CHAT ENVIRONMENT RUNNER
# =====================================================================
if __name__ == "__main__":
    ai = UnifiedMasterAI()
    print("================================================================")
    print("🤖   MASTER LOCAL AI ENGINE ACTIVATED SUCCESSFULLY   🤖")
    print("================================================================")
    print("Type your questions below. Type 'exit' to shut down.\n")
    
input_prompt = "You: "
while True:
    user_input = input(input_prompt)
    if user_input.lower() == "exit":
        print("🤖 AI Response: Shutting down. Goodbye!")
        break
    response = ai.get_response(user_input)
    print(response)
      