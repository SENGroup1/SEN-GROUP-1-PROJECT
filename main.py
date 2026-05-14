"""
Quiz Master - Offline Edition
Tkinter Desktop GUI with:
- Built-in question bank (no API key needed)
- Timer per question
- Score & leaderboard
- Multiple choice + True/False question types

Usage:
    python quiz_app_offline.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime

# ─────────────────────────────────────────────
#  Question Bank
# ─────────────────────────────────────────────
QUESTION_BANK = {
    "General Knowledge": [
        {"type":"mcq","question":"What is the largest ocean on Earth?","options":["Atlantic","Indian","Pacific","Arctic"],"answer":"Pacific","explanation":"The Pacific Ocean covers more than 30% of Earth's surface."},
        {"type":"mcq","question":"How many continents are there on Earth?","options":["5","6","7","8"],"answer":"7","explanation":"Earth has 7 continents: Africa, Antarctica, Asia, Australia, Europe, North America, South America."},
        {"type":"truefalse","question":"The Great Wall of China is visible from space with the naked eye.","options":["True","False"],"answer":"False","explanation":"This is a popular myth. The wall is too narrow to be seen from orbit."},
        {"type":"mcq","question":"Which planet is known as the Red Planet?","options":["Venus","Mars","Jupiter","Saturn"],"answer":"Mars","explanation":"Mars appears red due to iron oxide (rust) on its surface."},
        {"type":"truefalse","question":"Humans share about 98% of their DNA with chimpanzees.","options":["True","False"],"answer":"True","explanation":"Chimps are our closest living relatives, sharing ~98.7% of our DNA."},
        {"type":"mcq","question":"What is the smallest country in the world?","options":["Monaco","San Marino","Vatican City","Liechtenstein"],"answer":"Vatican City","explanation":"Vatican City covers just 0.44 km² inside Rome, Italy."},
        {"type":"mcq","question":"Which element has the chemical symbol 'Au'?","options":["Silver","Gold","Aluminum","Argon"],"answer":"Gold","explanation":"'Au' comes from the Latin word 'aurum', meaning gold."},
        {"type":"truefalse","question":"A group of flamingos is called a flamboyance.","options":["True","False"],"answer":"True","explanation":"Yes — a flamboyance of flamingos is the official collective noun."},
        {"type":"mcq","question":"How many sides does a heptagon have?","options":["5","6","7","8"],"answer":"7","explanation":"'Hepta' is Greek for seven, so a heptagon has 7 sides."},
        {"type":"mcq","question":"What language has the most native speakers in the world?","options":["English","Spanish","Hindi","Mandarin Chinese"],"answer":"Mandarin Chinese","explanation":"Mandarin Chinese has over 900 million native speakers."},
    ],
    "Science": [
        {"type":"mcq","question":"What is the powerhouse of the cell?","options":["Nucleus","Ribosome","Mitochondria","Golgi Apparatus"],"answer":"Mitochondria","explanation":"Mitochondria produce ATP, the cell's main energy currency."},
        {"type":"mcq","question":"What is the speed of light in a vacuum (approx.)?","options":["300,000 km/s","150,000 km/s","450,000 km/s","200,000 km/s"],"answer":"300,000 km/s","explanation":"Light travels at approximately 299,792 km/s in a vacuum."},
        {"type":"truefalse","question":"Electrons have a positive charge.","options":["True","False"],"answer":"False","explanation":"Electrons carry a negative charge; protons carry a positive charge."},
        {"type":"mcq","question":"What gas do plants absorb during photosynthesis?","options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"answer":"Carbon Dioxide","explanation":"Plants take in CO₂ and release O₂ during photosynthesis."},
        {"type":"mcq","question":"How many bones are in the adult human body?","options":["196","206","216","226"],"answer":"206","explanation":"Adults have 206 bones; babies start with around 270 that fuse over time."},
        {"type":"truefalse","question":"Sound travels faster than light.","options":["True","False"],"answer":"False","explanation":"Light travels at ~300,000 km/s; sound travels at only ~0.343 km/s in air."},
        {"type":"mcq","question":"What is the most abundant gas in Earth's atmosphere?","options":["Oxygen","Carbon Dioxide","Nitrogen","Argon"],"answer":"Nitrogen","explanation":"Nitrogen makes up about 78% of Earth's atmosphere."},
        {"type":"mcq","question":"Which scientist developed the theory of general relativity?","options":["Isaac Newton","Nikola Tesla","Albert Einstein","Stephen Hawking"],"answer":"Albert Einstein","explanation":"Einstein published his general theory of relativity in 1915."},
        {"type":"truefalse","question":"DNA stands for Deoxyribonucleic Acid.","options":["True","False"],"answer":"True","explanation":"DNA (Deoxyribonucleic Acid) carries the genetic instructions for life."},
        {"type":"mcq","question":"What is the atomic number of Carbon?","options":["4","6","8","12"],"answer":"6","explanation":"Carbon has 6 protons, giving it atomic number 6."},
    ],
    "History": [
        {"type":"mcq","question":"In which year did World War II end?","options":["1943","1944","1945","1946"],"answer":"1945","explanation":"WWII ended in 1945: V-E Day (May 8) and V-J Day (September 2)."},
        {"type":"mcq","question":"Who was the first President of the United States?","options":["John Adams","Thomas Jefferson","Benjamin Franklin","George Washington"],"answer":"George Washington","explanation":"George Washington served as the first U.S. President from 1789 to 1797."},
        {"type":"truefalse","question":"The Berlin Wall fell in 1989.","options":["True","False"],"answer":"True","explanation":"The Berlin Wall fell on November 9, 1989, symbolizing the end of the Cold War."},
        {"type":"mcq","question":"Which ancient wonder was located in Alexandria, Egypt?","options":["Hanging Gardens","Colossus of Rhodes","The Lighthouse","Statue of Zeus"],"answer":"The Lighthouse","explanation":"The Lighthouse of Alexandria was one of the tallest structures in the ancient world."},
        {"type":"mcq","question":"Who painted the Mona Lisa?","options":["Michelangelo","Raphael","Leonardo da Vinci","Caravaggio"],"answer":"Leonardo da Vinci","explanation":"Leonardo da Vinci painted the Mona Lisa between approximately 1503 and 1519."},
        {"type":"truefalse","question":"Napoleon Bonaparte was born in France.","options":["True","False"],"answer":"False","explanation":"Napoleon was born in Corsica (then recently acquired by France from Genoa) in 1769."},
        {"type":"mcq","question":"The Roman Empire fell in which century?","options":["3rd","4th","5th","6th"],"answer":"5th","explanation":"The Western Roman Empire officially fell in 476 AD, in the 5th century."},
        {"type":"mcq","question":"Which country was the first to give women the right to vote?","options":["USA","UK","Australia","New Zealand"],"answer":"New Zealand","explanation":"New Zealand granted women suffrage in 1893, the first self-governing country to do so."},
        {"type":"truefalse","question":"The Titanic sank in 1912.","options":["True","False"],"answer":"True","explanation":"RMS Titanic sank on April 15, 1912, after hitting an iceberg the night before."},
        {"type":"mcq","question":"Who wrote 'The Communist Manifesto'?","options":["Lenin & Stalin","Marx & Engels","Trotsky & Bakunin","Proudhon & Kropotkin"],"answer":"Marx & Engels","explanation":"Karl Marx and Friedrich Engels wrote The Communist Manifesto in 1848."},
    ],
    "Geography": [
        {"type":"mcq","question":"What is the capital of Australia?","options":["Sydney","Melbourne","Brisbane","Canberra"],"answer":"Canberra","explanation":"Canberra is Australia's capital, chosen as a compromise between Sydney and Melbourne."},
        {"type":"mcq","question":"Which is the longest river in the world?","options":["Amazon","Congo","Yangtze","Nile"],"answer":"Nile","explanation":"The Nile stretches approximately 6,650 km through northeastern Africa."},
        {"type":"truefalse","question":"The Amazon rainforest is primarily located in Brazil.","options":["True","False"],"answer":"True","explanation":"About 60% of the Amazon rainforest lies within Brazil's borders."},
        {"type":"mcq","question":"Which country has the most natural lakes?","options":["Russia","USA","Brazil","Canada"],"answer":"Canada","explanation":"Canada has over 2 million lakes — more than any other country."},
        {"type":"mcq","question":"Mount Everest is on the border of which two countries?","options":["India & China","Nepal & Tibet (China)","Nepal & India","Bhutan & China"],"answer":"Nepal & Tibet (China)","explanation":"Everest sits on the border between Nepal and the Tibet Autonomous Region of China."},
        {"type":"truefalse","question":"Africa is the world's largest continent.","options":["True","False"],"answer":"False","explanation":"Asia is the largest continent; Africa is second."},
        {"type":"mcq","question":"What is the capital of Canada?","options":["Toronto","Vancouver","Montreal","Ottawa"],"answer":"Ottawa","explanation":"Ottawa has been Canada's capital since 1857, chosen by Queen Victoria."},
        {"type":"mcq","question":"Which desert is the largest in the world?","options":["Gobi","Sahara","Arabian","Antarctic"],"answer":"Antarctic","explanation":"Antarctica is technically a cold desert — the largest desert on Earth at 14.2 million km²."},
        {"type":"truefalse","question":"The Suez Canal connects the Red Sea and the Mediterranean Sea.","options":["True","False"],"answer":"True","explanation":"The Suez Canal, opened in 1869, links the Red Sea to the Mediterranean."},
        {"type":"mcq","question":"Which country has the most time zones?","options":["Russia","USA","China","France"],"answer":"France","explanation":"France has 12 time zones when including its overseas territories."},
    ],
    "Technology": [
        {"type":"mcq","question":"What does 'HTTP' stand for?","options":["HyperText Transfer Protocol","High Transfer Text Protocol","HyperText Transmission Program","High-Tech Text Protocol"],"answer":"HyperText Transfer Protocol","explanation":"HTTP is the foundation of data communication on the World Wide Web."},
        {"type":"truefalse","question":"Python is a compiled programming language.","options":["True","False"],"answer":"False","explanation":"Python is an interpreted language, though it does compile to bytecode internally."},
        {"type":"mcq","question":"Who co-founded Apple Inc.?","options":["Bill Gates","Elon Musk","Steve Jobs","Jeff Bezos"],"answer":"Steve Jobs","explanation":"Steve Jobs co-founded Apple with Steve Wozniak and Ronald Wayne in 1976."},
        {"type":"mcq","question":"What does 'CPU' stand for?","options":["Central Processing Unit","Computer Personal Unit","Core Processing Utility","Central Program Updater"],"answer":"Central Processing Unit","explanation":"The CPU is the primary component that executes instructions in a computer."},
        {"type":"truefalse","question":"The first computer bug was an actual insect.","options":["True","False"],"answer":"True","explanation":"In 1947, a moth was found in a Harvard Mark II computer relay — it's taped in the logbook to this day."},
        {"type":"mcq","question":"What year was the World Wide Web invented?","options":["1983","1989","1993","1995"],"answer":"1989","explanation":"Tim Berners-Lee proposed the World Wide Web in 1989 while working at CERN."},
        {"type":"mcq","question":"Which company developed the Android operating system?","options":["Apple","Microsoft","Google","Samsung"],"answer":"Google","explanation":"Google acquired Android Inc. in 2005 and released the first Android phone in 2008."},
        {"type":"truefalse","question":"Wi-Fi stands for 'Wireless Fidelity'.","options":["True","False"],"answer":"False","explanation":"Wi-Fi is a brand name and doesn't officially stand for anything — the 'Wireless Fidelity' meaning was a retroactive marketing slogan."},
        {"type":"mcq","question":"What is the binary representation of the decimal number 10?","options":["1010","1001","1100","0110"],"answer":"1010","explanation":"10 in binary is 1010 (8+2=10)."},
        {"type":"mcq","question":"Which programming language is known as the 'language of the web'?","options":["Python","Java","JavaScript","C++"],"answer":"JavaScript","explanation":"JavaScript runs natively in all web browsers and is essential for interactive web pages."},
    ],
    "Sports": [
        {"type":"mcq","question":"How many players are on a standard soccer (football) team on the field?","options":["9","10","11","12"],"answer":"11","explanation":"Each team fields 11 players, including the goalkeeper."},
        {"type":"truefalse","question":"The Olympic Games were originally held in ancient Greece.","options":["True","False"],"answer":"True","explanation":"The ancient Olympic Games began in Olympia, Greece, in 776 BC."},
        {"type":"mcq","question":"In which sport would you perform a 'slam dunk'?","options":["Volleyball","Tennis","Basketball","Handball"],"answer":"Basketball","explanation":"A slam dunk involves jumping and forcefully dunking the ball through the hoop."},
        {"type":"mcq","question":"How many Grand Slam tournaments are there in tennis?","options":["2","3","4","5"],"answer":"4","explanation":"The four Grand Slams are: Australian Open, French Open, Wimbledon, and US Open."},
        {"type":"truefalse","question":"A marathon is exactly 42.195 kilometres long.","options":["True","False"],"answer":"True","explanation":"The official marathon distance is 42.195 km (26 miles 385 yards)."},
        {"type":"mcq","question":"Which country has won the most FIFA World Cup titles?","options":["Germany","Argentina","Italy","Brazil"],"answer":"Brazil","explanation":"Brazil has won the FIFA World Cup a record 5 times."},
        {"type":"mcq","question":"In golf, what term is used for two strokes under par?","options":["Birdie","Eagle","Albatross","Bogey"],"answer":"Eagle","explanation":"An Eagle is 2 under par; a Birdie is 1 under; an Albatross is 3 under."},
        {"type":"truefalse","question":"A standard ice hockey game has three periods.","options":["True","False"],"answer":"True","explanation":"Ice hockey is played over three 20-minute periods."},
        {"type":"mcq","question":"What is the diameter of a basketball hoop in inches?","options":["16","18","20","22"],"answer":"18","explanation":"An NBA basketball hoop has an inner diameter of 18 inches."},
        {"type":"mcq","question":"In which city were the first modern Olympic Games held in 1896?","options":["Rome","London","Paris","Athens"],"answer":"Athens","explanation":"The first modern Olympics were held in Athens, Greece, in 1896."},
    ],
    "Movies & TV": [
        {"type":"mcq","question":"Which film won the first-ever Academy Award for Best Picture?","options":["It Happened One Night","Wings","Gone with the Wind","Citizen Kane"],"answer":"Wings","explanation":"Wings (1927) won the first Best Picture Oscar at the inaugural Academy Awards in 1929."},
        {"type":"truefalse","question":"The Lion King (1994) is set in Africa.","options":["True","False"],"answer":"True","explanation":"The Lion King is set in the Pride Lands, a fictional African savanna kingdom."},
        {"type":"mcq","question":"Who played Iron Man in the Marvel Cinematic Universe?","options":["Chris Evans","Chris Hemsworth","Robert Downey Jr.","Mark Ruffalo"],"answer":"Robert Downey Jr.","explanation":"Robert Downey Jr. portrayed Tony Stark / Iron Man from 2008 to 2019."},
        {"type":"mcq","question":"Which TV show features a chemistry teacher turned drug manufacturer?","options":["Dexter","The Wire","Ozark","Breaking Bad"],"answer":"Breaking Bad","explanation":"Breaking Bad (2008–2013) stars Bryan Cranston as Walter White, a chemistry teacher who makes meth."},
        {"type":"truefalse","question":"James Cameron directed both Titanic and Avatar.","options":["True","False"],"answer":"True","explanation":"James Cameron directed Titanic (1997) and Avatar (2009), both record-breaking box office hits."},
        {"type":"mcq","question":"Which movie features the quote 'You talking to me?'","options":["The Godfather","Scarface","Taxi Driver","Goodfellas"],"answer":"Taxi Driver","explanation":"Robert De Niro delivers the iconic 'You talkin' to me?' monologue in Taxi Driver (1976)."},
        {"type":"mcq","question":"How many episodes are in the final season of Game of Thrones?","options":["6","7","8","10"],"answer":"6","explanation":"Season 8 of Game of Thrones had 6 episodes, airing in 2019."},
        {"type":"truefalse","question":"The Simpsons first aired in the 1980s.","options":["True","False"],"answer":"True","explanation":"The Simpsons debuted on December 17, 1989."},
        {"type":"mcq","question":"Which film franchise features the character 'Dom Toretto'?","options":["Mission Impossible","John Wick","Fast & Furious","Transformers"],"answer":"Fast & Furious","explanation":"Vin Diesel plays Dominic 'Dom' Toretto throughout the Fast & Furious franchise."},
        {"type":"mcq","question":"What animated film features the song 'Let It Go'?","options":["Moana","Tangled","Brave","Frozen"],"answer":"Frozen","explanation":"'Let It Go' is performed by Idina Menzel as Elsa in Disney's Frozen (2013)."},
    ],
    "Music": [
        {"type":"mcq","question":"Which band performed 'Bohemian Rhapsody'?","options":["The Beatles","Led Zeppelin","Queen","The Rolling Stones"],"answer":"Queen","explanation":"Bohemian Rhapsody was released by Queen in 1975 from the album A Night at the Opera."},
        {"type":"truefalse","question":"Michael Jackson was known as the 'King of Pop'.","options":["True","False"],"answer":"True","explanation":"Michael Jackson earned the title 'King of Pop' due to his enormous influence on popular music."},
        {"type":"mcq","question":"How many strings does a standard guitar have?","options":["4","5","6","7"],"answer":"6","explanation":"A standard acoustic or electric guitar has 6 strings."},
        {"type":"mcq","question":"Which artist released the album 'Thriller' (1982)?","options":["Prince","Madonna","Michael Jackson","Whitney Houston"],"answer":"Michael Jackson","explanation":"Thriller by Michael Jackson is the best-selling album of all time."},
        {"type":"truefalse","question":"Beethoven was deaf when he composed his Ninth Symphony.","options":["True","False"],"answer":"True","explanation":"Beethoven was almost completely deaf when he composed his Ninth Symphony, premiered in 1824."},
        {"type":"mcq","question":"What instrument does a 'pianist' play?","options":["Violin","Cello","Piano","Harp"],"answer":"Piano","explanation":"A pianist is a musician who plays the piano — a keyboard instrument."},
        {"type":"mcq","question":"Which country does the musical genre 'Reggae' originate from?","options":["Brazil","Nigeria","Cuba","Jamaica"],"answer":"Jamaica","explanation":"Reggae originated in Jamaica in the late 1960s, popularized globally by Bob Marley."},
        {"type":"truefalse","question":"A standard piano has 88 keys.","options":["True","False"],"answer":"True","explanation":"A full-size modern piano has 88 keys — 52 white and 36 black."},
        {"type":"mcq","question":"Who is known as the 'Queen of Soul'?","options":["Tina Turner","Diana Ross","Aretha Franklin","Whitney Houston"],"answer":"Aretha Franklin","explanation":"Aretha Franklin earned the title 'Queen of Soul' for her powerful voice and influence on soul music."},
        {"type":"mcq","question":"Which music format preceded the CD?","options":["MP3","8-track","Vinyl Record","Cassette Tape"],"answer":"Cassette Tape","explanation":"Cassette tapes (1960s–1990s) were widely used before CDs became mainstream in the late 1980s."},
    ],
}

CATEGORIES   = list(QUESTION_BANK.keys())
DIFFICULTIES = ["Easy", "Medium", "Hard"]

TIMER_MAP = {"Easy": 25, "Medium": 18, "Hard": 12}
QUESTIONS_PER_GAME = 8

LEADERBOARD_FILE = "leaderboard.json"

# ─────────────────────────────────────────────
#  Leaderboard persistence
# ─────────────────────────────────────────────
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────
BG      = "#0f0f1a"
SURFACE = "#1a1a2e"
CARD    = "#16213e"
ACCENT  = "#e94560"
ACCENT2 = "#0f3460"
TEXT    = "#eaeaea"
DIM     = "#8888aa"
OK      = "#4caf50"
WARN    = "#ff9800"
BAD     = "#f44336"

FH1   = ("Segoe UI", 24, "bold")
FH2   = ("Segoe UI", 18, "bold")
FH3   = ("Segoe UI", 13, "bold")
FBODY = ("Segoe UI", 12)
FSM   = ("Segoe UI", 10)

def btn(parent, text, color, cmd, width=14):
    return tk.Button(parent, text=text, font=FBODY, bg=color, fg=TEXT,
                     activebackground=color, activeforeground=TEXT,
                     relief="flat", padx=14, pady=8,
                     cursor="hand2", width=width, command=cmd)

# ─────────────────────────────────────────────
#  App
# ─────────────────────────────────────────────
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Master")
        self.geometry("880x640")
        self.minsize(740, 540)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.player   = tk.StringVar(value="Player")
        self.category = tk.StringVar(value=CATEGORIES[0])
        self.diff     = tk.StringVar(value="Medium")

        self.questions: list[dict] = []
        self.q_index   = 0
        self.score     = 0
        self.timer_val = 18
        self._timer_job = None

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.frames: dict[str, tk.Frame] = {}
        for Cls in (HomeScreen, QuizScreen, ResultScreen, LeaderboardScreen):
            f = Cls(self.container, self)
            self.frames[Cls.__name__] = f
            f.place(relwidth=1, relheight=1)

        self.show("HomeScreen")

    def show(self, name):
        f = self.frames[name]
        if hasattr(f, "on_show"):
            f.on_show()
        f.tkraise()

    def start_game(self):
        pool = QUESTION_BANK.get(self.category.get(), [])
        sampled = random.sample(pool, min(QUESTIONS_PER_GAME, len(pool)))

        # Shuffle option order (keep correct answer tracked)
        for q in sampled:
            opts = q["options"][:]
            random.shuffle(opts)
            q = dict(q, options=opts)  # non-destructive

        self.questions = sampled
        self.q_index   = 0
        self.score     = 0
        self.show("QuizScreen")

    def next_question(self):
        self.q_index += 1
        if self.q_index >= len(self.questions):
            self._finish()
        else:
            self.frames["QuizScreen"].load_question()

    def _finish(self):
        lb = load_leaderboard()
        lb.append({
            "name":       self.player.get(),
            "score":      self.score,
            "total":      len(self.questions),
            "category":   self.category.get(),
            "difficulty": self.diff.get(),
            "date":       datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        lb.sort(key=lambda x: x["score"], reverse=True)
        save_leaderboard(lb)
        self.show("ResultScreen")


# ─────────────────────────────────────────────
#  Screens
# ─────────────────────────────────────────────
class HomeScreen(tk.Frame):
    def __init__(self, parent, app: QuizApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🧠 Quiz Master", font=FH1, bg=BG, fg=ACCENT).pack(pady=(56, 4))
        tk.Label(self, text="Test your knowledge — no internet needed",
                 font=FSM, bg=BG, fg=DIM).pack()

        # Settings card
        card = tk.Frame(self, bg=CARD, padx=30, pady=24)
        card.pack(pady=30, ipadx=6, ipady=6)

        # Player name
        row0 = tk.Frame(card, bg=CARD)
        row0.pack(fill="x", pady=(0, 16))
        tk.Label(row0, text="Your name", font=FSM, bg=CARD, fg=DIM, width=12, anchor="w").pack(side="left")
        tk.Entry(row0, textvariable=self.app.player, font=FBODY, bg=SURFACE,
                 fg=TEXT, insertbackground=TEXT, relief="flat", width=24).pack(side="left")

        # Category
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=SURFACE, background=SURFACE,
                         foreground=TEXT, selectbackground=ACCENT2, selectforeground=TEXT)
        row1 = tk.Frame(card, bg=CARD)
        row1.pack(fill="x", pady=(0, 12))
        tk.Label(row1, text="Category", font=FSM, bg=CARD, fg=DIM, width=12, anchor="w").pack(side="left")
        ttk.Combobox(row1, textvariable=self.app.category, values=CATEGORIES,
                     state="readonly", width=26, font=FBODY).pack(side="left")

        # Difficulty
        row2 = tk.Frame(card, bg=CARD)
        row2.pack(fill="x")
        tk.Label(row2, text="Difficulty", font=FSM, bg=CARD, fg=DIM, width=12, anchor="w").pack(side="left")
        diff_frame = tk.Frame(row2, bg=CARD)
        diff_frame.pack(side="left")
        self._diff_btns = {}
        for d in DIFFICULTIES:
            b = tk.Button(diff_frame, text=d, font=FSM, relief="flat",
                          padx=12, pady=5, cursor="hand2",
                          command=lambda v=d: self._set_diff(v))
            b.pack(side="left", padx=3)
            self._diff_btns[d] = b
        self._set_diff("Medium")

        # Info
        self.info_label = tk.Label(self, text="", font=FSM, bg=BG, fg=DIM)
        self.info_label.pack()
        self.app.category.trace_add("write", self._update_info)
        self.app.diff.trace_add("write", self._update_info)
        self._update_info()

        # Buttons
        bf = tk.Frame(self, bg=BG)
        bf.pack(pady=28)
        btn(bf, "▶  Start Quiz", ACCENT, self.app.start_game, width=16).grid(row=0, column=0, padx=10)
        btn(bf, "🏆  Leaderboard", ACCENT2,
            lambda: self.app.show("LeaderboardScreen"), width=16).grid(row=0, column=1, padx=10)

    def _set_diff(self, val):
        self.app.diff.set(val)
        colors = {"Easy": OK, "Medium": WARN, "Hard": BAD}
        for d, b in self._diff_btns.items():
            b.config(bg=colors[d] if d == val else SURFACE,
                     fg=TEXT if d == val else DIM)

    def _update_info(self, *_):
        cat   = self.app.category.get()
        pool  = QUESTION_BANK.get(cat, [])
        secs  = TIMER_MAP.get(self.app.diff.get(), 18)
        n     = min(QUESTIONS_PER_GAME, len(pool))
        self.info_label.config(
            text=f"{n} questions  •  {secs}s per question  •  {len(pool)} in bank"
        )


class QuizScreen(tk.Frame):
    def __init__(self, parent, app: QuizApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._answered   = False
        self._timer_job  = None
        self._build()

    def _build(self):
        # Top bar
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=28, pady=(18, 0))
        self.prog_var = tk.StringVar()
        self.cat_var  = tk.StringVar()
        tk.Label(top, textvariable=self.prog_var, font=FBODY, bg=BG, fg=DIM).pack(side="left")
        tk.Label(top, textvariable=self.cat_var,  font=FBODY, bg=BG, fg=DIM).pack(side="right")

        # Timer bar
        self.t_canvas = tk.Canvas(self, bg=BG, height=7, highlightthickness=0)
        self.t_canvas.pack(fill="x", padx=28, pady=(6, 0))
        self.t_label = tk.Label(self, text="", font=FH3, bg=BG, fg=ACCENT)
        self.t_label.pack(anchor="e", padx=34)

        # Question card
        qcard = tk.Frame(self, bg=CARD, padx=22, pady=20)
        qcard.pack(fill="x", padx=28, pady=(8, 0))
        self.type_label = tk.Label(qcard, text="", font=FSM, bg=CARD, fg=ACCENT)
        self.type_label.pack(anchor="w")
        self.q_label = tk.Label(qcard, text="", font=FH3, bg=CARD, fg=TEXT,
                                 wraplength=780, justify="left")
        self.q_label.pack(anchor="w", pady=(4, 0))

        # Options
        self.opt_frame = tk.Frame(self, bg=BG)
        self.opt_frame.pack(fill="x", padx=28, pady=10)
        self.opt_btns: list[tk.Button] = []

        # Explanation
        self.expl_var = tk.StringVar()
        tk.Label(self, textvariable=self.expl_var, font=FBODY, bg=BG, fg=DIM,
                 wraplength=820, justify="left").pack(padx=28)

        # Next button
        self.next_btn = btn(self, "Next →", ACCENT2, self._next, width=14)

    def on_show(self):
        self.load_question()

    def load_question(self):
        self._answered = False
        self.expl_var.set("")
        self.next_btn.pack_forget()

        q   = self.app.questions[self.app.q_index]
        idx = self.app.q_index
        tot = len(self.app.questions)

        self.prog_var.set(f"Question {idx+1} / {tot}  •  Score: {self.app.score}")
        self.cat_var.set(f"{self.app.category.get()}  •  {self.app.diff.get()}")
        self.type_label.config(text="🔘 Multiple Choice" if q["type"]=="mcq" else "✅ True / False")
        self.q_label.config(text=q["question"])

        for b in self.opt_btns:
            b.destroy()
        self.opt_btns.clear()

        for opt in q["options"]:
            b = tk.Button(self.opt_frame, text=f"  {opt}", font=FBODY,
                          bg=SURFACE, fg=TEXT, activebackground=ACCENT2,
                          activeforeground=TEXT, relief="flat",
                          anchor="w", padx=12, pady=9, cursor="hand2",
                          command=lambda o=opt: self._answer(o))
            b.pack(fill="x", pady=3)
            self.opt_btns.append(b)

        self._stop_timer()
        self.app.timer_val = TIMER_MAP.get(self.app.diff.get(), 18)
        self._tick()

    def _tick(self):
        t = self.app.timer_val
        self.t_label.config(text=f"⏱ {t}s")
        w = self.t_canvas.winfo_width() or 820
        frac = t / TIMER_MAP.get(self.app.diff.get(), 18)
        color = OK if frac > 0.5 else (WARN if frac > 0.25 else BAD)
        self.t_canvas.delete("all")
        self.t_canvas.create_rectangle(0, 0, w * frac, 7, fill=color, outline="")
        if t > 0 and not self._answered:
            self.app.timer_val -= 1
            self._timer_job = self.after(1000, self._tick)
        elif not self._answered:
            self._time_up()

    def _stop_timer(self):
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    def _time_up(self):
        self._answered = True
        q = self.app.questions[self.app.q_index]
        for b in self.opt_btns:
            if b.cget("text").strip() == q["answer"]:
                b.config(bg=OK)
        self.expl_var.set(f"⏰ Time's up!  Correct: {q['answer']}  —  {q.get('explanation','')}")
        self.next_btn.pack(pady=14)

    def _answer(self, chosen):
        if self._answered:
            return
        self._answered = True
        self._stop_timer()
        q = self.app.questions[self.app.q_index]
        correct = chosen == q["answer"]
        if correct:
            self.app.score += 1
        for b in self.opt_btns:
            label = b.cget("text").strip()
            if label == q["answer"]:
                b.config(bg=OK, fg="white")
            elif label == chosen and not correct:
                b.config(bg=BAD, fg="white")
            b.config(state="disabled", cursor="")
        icon = "✅" if correct else "❌"
        self.expl_var.set(f"{icon}  {q.get('explanation','')}")
        self.next_btn.pack(pady=14)

    def _next(self):
        self.app.next_question()


class ResultScreen(tk.Frame):
    def __init__(self, parent, app: QuizApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        self.title_lbl = tk.Label(self, text="", font=FH1, bg=BG, fg=ACCENT)
        self.title_lbl.pack(pady=(64, 8))
        self.score_lbl = tk.Label(self, text="", font=("Segoe UI", 52, "bold"), bg=BG, fg=TEXT)
        self.score_lbl.pack()
        self.sub_lbl   = tk.Label(self, text="", font=FBODY, bg=BG, fg=DIM)
        self.sub_lbl.pack(pady=8)

        # Stars
        self.star_lbl = tk.Label(self, text="", font=("Segoe UI", 28), bg=BG)
        self.star_lbl.pack(pady=4)

        bf = tk.Frame(self, bg=BG)
        bf.pack(pady=36)
        btn(bf, "▶  Play Again", ACCENT,  self.app.start_game,            width=16).grid(row=0,column=0,padx=10)
        btn(bf, "🏆  Leaderboard", ACCENT2, lambda:self.app.show("LeaderboardScreen"), width=16).grid(row=0,column=1,padx=10)
        btn(bf, "🏠  Home", "#333355",     lambda:self.app.show("HomeScreen"),          width=16).grid(row=0,column=2,padx=10)

    def on_show(self):
        s, t = self.app.score, len(self.app.questions)
        pct  = s / t
        emoji = "🏆" if pct==1 else ("🎉" if pct>=0.7 else ("😅" if pct>=0.4 else "💪"))
        stars = "⭐" * round(pct * 5)
        self.title_lbl.config(text=f"{emoji}  Quiz Complete!")
        self.score_lbl.config(text=f"{s} / {t}")
        self.sub_lbl.config(text=f"{self.app.player.get()}  •  {self.app.category.get()}  •  {self.app.diff.get()}")
        self.star_lbl.config(text=stars)


class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, app: QuizApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🏆  Leaderboard", font=FH2, bg=BG, fg=ACCENT).pack(pady=(36,16))

        style = ttk.Style()
        style.configure("Treeview", background=CARD, fieldbackground=CARD,
                         foreground=TEXT, rowheight=26, font=FBODY)
        style.configure("Treeview.Heading", background=ACCENT2,
                         foreground=TEXT, font=FH3, relief="flat")
        style.map("Treeview", background=[("selected", ACCENT2)])

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=28)

        cols = ("Rank","Name","Score","Category","Difficulty","Date")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="none")
        for col, w in zip(cols, [60,140,80,180,100,140]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        bf = tk.Frame(self, bg=BG)
        bf.pack(pady=18)
        btn(bf,"← Back", ACCENT2, lambda:self.app.show("HomeScreen"), width=14).grid(row=0,column=0,padx=10)
        btn(bf,"🗑  Clear", BAD,   self._clear,                          width=14).grid(row=0,column=1,padx=10)

    def on_show(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, e in enumerate(load_leaderboard()[:20], 1):
            medal = ["🥇","🥈","🥉"][i-1] if i<=3 else str(i)
            self.tree.insert("","end",values=(
                medal, e["name"],
                f"{e['score']} / {e['total']}",
                e["category"], e["difficulty"], e["date"]
            ))

    def _clear(self):
        if messagebox.askyesno("Clear","Delete all leaderboard entries?"):
            save_leaderboard([])
            self.on_show()


# ─────────────────────────────────────────────
#  Entry
# ─────────────────────────────────────────────
if __name__ == "__main__":
    QuizApp().mainloop()