import random
import threading
import time


class QuoteManager:

    def __init__(
        self,
        avatar,
        interval=300,
        display_time=8
    ):
        self.avatar = avatar

        # 300 seconds = 5 minutes
        self.interval = interval

        # How long the quote remains visible
        self.display_time = display_time

        self.running = False
        self.thread = None

        self.quotes = [
            "Be the pro, not the rare.",
            "Work in silence. Let success make the noise.",
            "Discipline beats motivation.",
            "Build what you once thought was impossible.",
            "Stay focused. Stay dangerous.",
            "Dream big. Execute bigger.",
            "Progress over perfection.",
            "Small steps. Massive results.",
            "Make your future self proud.",
            "Don't stop until you're proud.",
            "Consistency creates greatness.",
            "Turn pressure into progress.",
            "Your effort defines your outcome.",
            "Think. Build. Improve. Repeat.",
            "Master the basics. Then break the limits.",
            "One day or day one.",
            "Do it even when nobody is watching.",
            "The grind has a purpose.",
            "Focus on the mission.",
            "Make every failure useful.",
            "Learn more. Build more. Become more.",
            "Stay hungry for improvement.",
            "Don't chase validation. Chase mastery.",
            "Your limits are not your destination.",
            "Keep moving forward.",
            "Effort compounds.",
            "Become harder to replace.",
            "Make progress your habit.",
            "Turn ideas into reality.",
            "Your future is built today.",
            "Outwork your yesterday.",
            "Stay patient. Stay consistent.",
            "Results take time. Keep going.",
            "Don't wish for it. Work for it.",
            "Failure is data.",
            "Create. Test. Fail. Fix. Repeat.",
            "Be better than yesterday.",
            "Let your work introduce you.",
            "Quiet effort. Loud results.",
            "Build something that matters.",
            "Stay focused when it gets difficult.",
            "Excuses don't build futures.",
            "Keep learning until impossible becomes normal.",
            "Turn ambition into action.",
            "Your consistency will outlast your motivation.",
            "Don't compete with others. Compete with your potential.",
            "Make the hard days count.",
            "The goal is progress, not permission.",
            "Keep building until the vision becomes reality.",
            "One vision. One mission. No excuses."
        ]

    # =================================================
    # START
    # =================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

        print("Quote system ready.")

    # =================================================
    # LOOP
    # =================================================

    def _run(self):

        # Wait 5 minutes before the first quote
        while self.running:

            for _ in range(self.interval):

                if not self.running:
                    return

                time.sleep(1)

            if not self.running:
                return

            self._show_random_quote()

    # =================================================
    # SHOW QUOTE
    # =================================================

    def _show_random_quote(self):

        quote = random.choice(self.quotes)

        print(
            f"[QUOTE] {quote}"
        )

        if not self.avatar:
            return

        # Show quote through Tkinter thread
        self.avatar.root.after(
            0,
            self.avatar.show_dialog,
            quote
        )

        # Hide it after display_time seconds
        self.avatar.root.after(
            self.display_time * 1000,
            self.avatar.hide_dialog
        )

    # =================================================
    # STOP
    # =================================================

    def stop(self):

        self.running = False