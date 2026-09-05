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
                "responses": ["Hello Krishna! Ask me any question about the world, science, English, or try a math problem Krishna!", "Hey there! I am JARVIS, your zero-dependency AI engine. Ask me anything!"]
            },
            "identity": {
                "patterns": ["who are you", "what is your name", "tell me about yourself", "your name"],
                "responses": ["I am a zero-dependency AI engine.", "You can call me JARVIS. I don't need external keys or modules!"]
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
            "mountains": "The highest mountain is Mount Everest (8,848m). The longest range is the Andes, and the largest mountain range is the Himalayas.",
            "deepest place": "The Mariana Trench in the Western Pacific Ocean is the deepest place on Earth, reaching nearly 11,000 meters (36,000 feet) down.",
            "largest desert": "The Antarctic Desert is the largest desert in the world (polar desert), while the Sahara is the largest hot desert.",
            "longest river": "The Nile River in Africa is traditionally considered the longest river (6,650 km), though the Amazon River is the largest by water volume.",
            "grand canyon": "The Grand Canyon is a massive, steep-sided canyon carved by the Colorado River in Arizona, United States.",
            "great barrier reef": "The Great Barrier Reef off the coast of Australia is the world's largest coral reef system, visible from space.",
            "plate tectonics": "The Earth's outer shell is divided into massive lithospheric tectonic plates. Their movements drive continental drift, volcanic eruptions, and seismic earthquakes along fault lines.",
            "atmosphere layers": "Earth's atmosphere has 5 primary structural layers: Troposphere (where weather happens), Stratosphere (holds the Ozone layer), Mesosphere, Thermosphere, and Exosphere.",
            "greenland": "Greenland is the world's largest non-continental island. It is an autonomous territory of Denmark, covered 80% by a massive permanent ice sheet.",
            "ring of fire": "The Ring of Fire is a string of volcanoes and sites of intense seismic activity, or earthquakes, encircling the edges of the Pacific Ocean basin.",
            "australia facts": "Australia is both a continent and a country. Its capital is Canberra (not Sydney). It is home to the Outback, unique marsupials, and the sacred monolith Uluru.",
            "russia": "Russia is the largest country on Earth by land area, spanning 11 separate time zones across eastern Europe and northern Asia. Capital: Moscow.",
            "south africa": "South Africa sits at the southern tip of Africa and uniquely features three official capital cities: Pretoria (Executive), Bloemfontein (Judicial), and Cape Town (Legislative).",
            "canada geography": "Canada holds over 60% of the world's lakes and possesses the longest coastline of any nation on Earth, measuring over 202,000 kilometers."


        }

        self.country_kb = {
            "brazil": "Brazil is the largest country in South America, speaking Portuguese and holding the Amazon Basin.",
            "japan": "Japan is an island country in East Asia known for rich traditional culture and cutting-edge tech.",
            "egypt": "Egypt links northeast Africa with the Middle East, featuring monuments like the Giza Pyramids.",
            "canada": "Canada is the second-largest country by area and shares the world's longest land border with the USA.",
            "india": "India is located in South Asia and is the world's most populous country.",
            "china": "China is a powerhouse in East Asia, featuring historical marvels like the Great Wall.",
            "france": "France is in Western Europe, famous for art, fashion, and cuisine. Capital: Paris.",
            "united kingdom": "The UK includes England, Scotland, Wales, and Northern Ireland. Capital: London.",
            "germany": "Germany is a central European country known for its technological engineering and history. Capital: Berlin.",
            "italy": "Italy sits on the Mediterranean coastline and left a massive mark on Western culture. Capital: Rome."

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
            "speed of light": "The speed of light in a vacuum is exactly 299,792,458 meters per second.",
            "solar system": "Our Solar System consists of our Sun and everything bound to it by gravity: 8 planets, dozens of moons, and millions of asteroids.",
            "mars": "Mars is the fourth planet from the Sun, often called the 'Red Planet' due to iron oxide (rust) on its surface.",
            "jupiter": "Jupiter is the largest planet in our solar system, known for its iconic 'Great Red Spot', which is a massive storm.",
            "black hole": "A Black Hole is a region of space where gravity is so strong that nothing—not even light—can escape its pull.",
            "periodic table": "The Periodic Table organizes all known chemical elements by atomic number. Hydrogen (H) is element number 1.",
            "mitochondria": "The Mitochondria are known as the 'powerhouses of the cell', generating chemical energy (ATP) for cellular functions.",
            "heart": "The human heart is a muscular organ that pumps blood through the circulatory system, beating roughly 100,000 times a day.",
            "brain": "The human brain contains roughly 86 billion neurons and controls thoughts, memory, emotion, and motor skills.",
            "milky way": "The Milky Way is a barred spiral galaxy containing 100 to 400 billion stars. It takes our Solar System about 230 million years to complete one orbit around its galactic center.",
            "speed of sound": "The speed of sound in dry air at 20°C (68°F) is roughly 343 meters per second (1,235 km/h). Unlike light, sound requires a physical medium like air or water to travel.",
            "absolute zero": "Absolute zero is the lowest possible temperature structure, defined as 0 Kelvin, -273.15°C, or -459.67°F. At this thermodynamic threshold, all classical atomic motion entirely ceases.",
            "gravity wave": "Gravitational waves are ripples in spacetime caused by violent cosmic processes, such as merging black holes, traveling at the speed of light.",
            "cell membrane": "The cell membrane (plasma membrane) is a semi-permeable lipid bilayer that regulates the transport of materials entering and exiting the cell structure.",
            "enzyme": "Enzymes are biological proteins that act as catalysts, accelerating vital chemical reactions within living organisms without being consumed in the process.",
            "ph scale": "The pH scale measures how acidic or basic a substance is, ranging from 0 to 14. Pure water is neutral (pH 7), values below 7 are acidic, and values above 7 are alkaline.",
            "states of matter": "The four fundamental states of matter observable in daily life or extreme science conditions are Solid, Liquid, Gas, and Plasma.",
            "big bang": "The Big Bang theory is the prevailing cosmological model explaining the origin of our universe. It suggests that roughly 13.8 billion years ago, everything expanded rapidly from a single, infinitely dense point.",
            "supernova": "A Supernova is the cataclysmic explosion of a dying star. It occurs when a massive star runs out of fuel and collapses under its own gravity, momentarily outshining an entire galaxy and scattering heavy chemical elements into deep space.",
            "nebula": "A Nebula is a giant interstellar cloud of dust, hydrogen, helium, and other ionized gases. Known as 'cosmic nurseries,' these clouds are the exact regions where new stars and planetary systems are born.",
            "exoplanet": "An Exoplanet is any planet located outside our solar system that orbits a star other than our Sun. Thousands have been detected, including some sitting in the 'Habitable Zone' where liquid water could theoretically exist.",
            "light year": "A Light-Year is a unit of astronomical distance, not time. It is the absolute distance that a beam of light travels through a vacuum in one Earth year, totaling roughly 9.46 trillion kilometers (5.88 trillion miles).",
            "neutron star": "A Neutron Star is the collapsed core of a massive supergiant star. They are incredibly dense objects; a single teaspoon of neutron star material would weigh about 6 billion tons on Earth. They also rotate hundreds of times per second.",
            "dark matter": "Dark Matter is an invisible form of matter that makes up roughly 27% of the universe's composition. It does not absorb, reflect, or emit light, and scientists can only detect it by measuring its massive gravitational pull on distant galaxies.",
            "hubble": "The Hubble Space Telescope, launched into low Earth orbit in 1990, revolutionized astronomy by providing crystal-clear images of deep space, helping scientists determine the exact expansion rate of our universe.",
            "james webb": "The James Webb Space Telescope (JWST) is humanity's premier space observatory. Using highly sensitive infrared sensors, it can peer straight through cosmic dust clouds to see the very first stars and galaxies formed after the Big Bang."



        }

        self.english_kb = {
            "noun": "A Noun identifies a person, place, or thing. Examples: 'VS Code', 'Python'.",
            "verb": "A Verb is an action word describing what the subject is doing. Examples: 'run', 'calculate'.",
            "adjective": "An Adjective modifies or describes a noun. Examples: 'intelligent', 'fast'.",
            "pronoun": "A Pronoun replaces a noun to avoid repetition. Examples: 'he', 'she', 'it'.",
            "synonym": "Synonyms are different words that share identical meanings. Example: 'Fast' and 'Quick'.",
            "adverb": "An Adverb modifies a verb, adjective, or another adverb, frequently explaining how, when, where, or to what degree. Examples: 'quickly', 'yesterday', 'very'.",
            "conjunction": "A Conjunction is a structural word used to connect clauses, sentences, or individual words together. Examples include 'and', 'but', 'because', 'or'.",
            "preposition": "A Preposition expresses spatial, temporal, or logical relationships between a noun or pronoun and other words. Examples: 'under', 'through', 'before', 'on'.",
            "oxymoron": "An Oxymoron is a literary figure of speech that pairs two completely contradictory terms to create a dramatic rhetorical effect. Examples: 'deafening silence', 'orderly chaos'."

        }


        self.people_kb = {
            "albert einstein": "Albert Einstein was a theoretical physicist who developed the Theory of Relativity (E=mc²), fundamentally transforming how humanity understands space, time, and gravity.",
            "isaac newton": "Sir Isaac Newton was an English mathematician and physicist who formulated the three Laws of Motion and the universal law of gravitation, forming the foundation of classical mechanics.",
            "marie curie": "Marie Curie was a pioneering physicist and chemist. She discovered radioactivity, discovered the elements Polonium and Radium, and was the first person to win two Nobel Prizes.",
            "galileo": "Galileo Galilei was an Italian astronomer who championed heliocentrism (the Earth revolving around the Sun). He revolutionized astronomy using his improved telescope designs.",
            "charles darwin": "Charles Darwin was an English naturalist who formulated the Theory of Evolution through natural selection, explaining how all species evolve over generations.",
            "nikola tesla": "Nikola Tesla was a visionary engineer and inventor who designed the Alternating Current (AC) electricity system, which powers the modern world today.",
            "leonardo da vinci": "Leonardo da Vinci was the ultimate Renaissance polymath—an artist, scientist, and engineer who painted the Mona Lisa and sketched conceptual designs for flying machines.",
            "neil armstrong": "Neil Armstrong was an American astronaut who became the first human to walk on the Moon on July 20, 1969, famously declaring it 'one small step for man, one giant leap for mankind.'",
            "shakespeare": "William Shakespeare was an English playwright and poet, widely regarded as the greatest writer in the English language, authoring classics like Hamlet and Romeo and Juliet.",
            "rosa parks": "Rosa Parks was an American civil rights activist whose refusal to give up her bus seat in 1955 sparked the Montgomery Bus Boycott, a pivotal event in the fight against racial segregation.",
            "steve jobs": "Steve Jobs was the co-founder of Apple Inc. and a charismatic pioneer of the personal computer revolution, famous for overseeing the creation of the Macintosh, iPod, iPhone, and iPad.",
            "bill gates": "Bill Gates is the co-founder of Microsoft who helped ignite the personal computer boom by making Windows the world's dominant operating system. He later transitioned into full-time global philanthropy.",
            "walt disney": "Walt Disney was an American animator, producer, and entrepreneur who pioneered the cartoon film industry, created iconic characters like Mickey Mouse, and founded the world's most famous theme parks.",
            "michael jackson": "Michael Jackson, known as the 'King of Pop', was a transformative global singer and dancer whose landmark 1982 album 'Thriller' remains the best-selling music album of all time.",
            "elvis presley": "Elvis Presley, known as the 'King of Rock and Roll', was an American cultural icon of the 20th century who revolutionized mainstream popular music and youth culture with his high-energy performances.",
            "muhammad ali": "Muhammad Ali was a legendary heavyweight boxing champion, Olympic gold medalist, and prominent civil rights activist who became globally famous for his unparalleled athletic charisma and anti-war stances.",
            "malala": "Malala Yousafzai is a Pakistani education activist and the youngest-ever Nobel Prize laureate, who survived a targeted assassination attempt to become a global symbol for girls' right to education.",
            "martin luther king": "Martin Luther King Jr. was a Baptist minister and legendary civil rights leader who used nonviolent resistance to spearhead the American Civil Rights Movement, immortalized by his 1963 'I Have a Dream' speech.",
            "princess diana": "Diana, Princess of Wales, was a beloved member of the British royal family celebrated globally for her extensive international charity work, high-profile fashion choices, and tireless activism against landmines.",
            "tim berners-lee": "Sir Tim Berners-Lee is a British computer scientist who invented the World Wide Web in 1989, creating the basic foundational protocols (HTML, HTTP, and URLs) that power the modern global internet.",
            "stephen hawking": "Stephen Hawking was a brilliant theoretical physicist and cosmologist famous for his work on black hole radiation ('Hawking Radiation') and authoring 'A Brief History of Time' while battling ALS.",
            "elon musk": "Elon Musk is a business titan and engineer who founded SpaceX to revolutionize aerospace engineering and co-founded Tesla to accelerate the global transition to electric vehicles.",
            "bruce lee": "Bruce Lee was an iconic martial artist, actor, and philosopher who bridged the cultural gap between East and West, completely revolutionizing the martial arts film genre and popularizing modern philosophy.",
            "jrr tolkien": "J.R.R. Tolkien was an English scholar and author widely considered the father of modern high-fantasy literature, writing legendary masterpieces like 'The Hobbit' and 'The Lord of the Rings.'",
            "vincent van gogh": "Vincent van Gogh was a Dutch post-impressionist painter who created roughly 2,100 artworks, including masterpieces like 'The Starry Night,' despite achieving almost no commercial success during his lifetime.",
            "beethoven": "Ludwig van Beethoven was a German composer and pianist who served as a crucial transition figure between the Classical and Romantic musical eras, creating monumental symphonies even after losing his hearing.",
            "pablo picasso": "Pablo Picasso was a Spanish painter and sculptor who co-founded the Cubist movement, radically changing modern art styles by breaking down subjects into abstract, geometric shapes.",
            "cleopatra": "Cleopatra VII was the last active ruler of the Ptolemaic Kingdom of Egypt, famous for her political alliances with Julius Caesar and Mark Antony, her immense intellect, and her command of multiple languages.",
            "queen elizabeth": "Queen Elizabeth I was the Queen of England and Ireland from 1558 to 1603. Her reign is known as the Elizabethan Era, a golden age of English drama, literature, and global maritime exploration.",

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

        for key, fact in self.people_kb.items():
            if key in cleaned: return f"👤 [People Fact]: {fact}"

        for intent, data in self.chat_kb.items():
            for pattern in data["patterns"]:
                if pattern in cleaned: return f"🤖 AI Response: {random.choice(data['responses'])}"
                    
        return "🤖 AI Response: I don't have that in my system database yet. Ask about 'Micheal Jackson', 'gravity', 'nouns', 'Japan', or 'multiply 12 by 12'."

# =====================================================================
# 3. INTERACTIVE CHAT ENVIRONMENT RUNNER
# =====================================================================
if __name__ == "__main__":
    ai = UnifiedMasterAI()
    print("===============================================")
    print("🤖   JARVIS ENGINE ACTIVATED SUCCESSFULLY   🤖")
    print("===============================================")
    print("Type your questions below. Type 'exit' to shut down.\n")
    
input_prompt = "You: "
while True:
    user_input = input(input_prompt)
    if user_input.lower() == "exit":
        print("🤖 AI Response: Shutting down. Goodbye!")
        break
    response = ai.get_response(user_input)
    print(response)
      