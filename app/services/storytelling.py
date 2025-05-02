from app.database import FRAGRANCE_DATABASE


class Storyteller:
    def __init__(self):
        # self.tones = PERSONALITY_TONES
        self.database = FRAGRANCE_DATABASE

    def generate_story(self, user_name: str, personality: str, fragrance_match: dict) -> dict:
        """Generate a basic fallback recommendation if Groq fails"""
        main_sku = fragrance_match["main_sku"]
        secondary_skus = fragrance_match["secondary_skus"]

        # Create simple blend name and tagline
        blend_name = f"{user_name}'s Signature Blend"
        tagline = "Your unique signature, bottled."

        # Create a simple story
        story = f"""
        Your custom fragrance has been crafted specifically for you, {user_name}.

        Your blend features {main_sku} as the main note, complemented by {secondary_skus[0]} and {secondary_skus[1]}.
        This combination creates a scent that matches your {personality} personality perfectly.

        Wear this unique blend to express your true self in any situation.
        """

        # Create the recommendation summary
        recommendation = {
            "blend_name": blend_name,
            "main_notes": ", ".join(fragrance_match["main_notes"]),
            "best_wearing_time": fragrance_match["best_wearing_time"],
            "ideal_season": fragrance_match["ideal_season"],
            "mood": ", ".join(fragrance_match["mood"]),
            "recommended_skus": {
                main_sku: "2 shots",
                secondary_skus[0]: "1 shot",
                secondary_skus[1]: "1 shot"
            }
        }

        return {
            "blend_name": blend_name,
            "tagline": tagline,
            "story": story,
            "recommendations": recommendation
        }

    def generate_closing_message(self) -> str:
        """Generate the elegant closing message"""
        return """
        Thank you for entrusting us with your story.
        At Shuts By L'dora, your soul speaks in scents -- a language older than memory.
        We invite you to breathe life into your creation, to wear your signature boldly, softly, however your heart desires.
        Your journey is only beginning.
        Your story now lingers, beautifully, in the air around you.
        -- With grace,
        Shuts By L'dora
        """


"""This part of class is for when you want to use random text generation instead off LLM"""
# from app.database import PERSONALITY_TONES, FRAGRANCE_DATABASE
# import random
#
# class Storyteller:
#     def __init__(self):
#         self.tones = PERSONALITY_TONES
#         self.database = FRAGRANCE_DATABASE
#
#     def generate_blend_name(self, user_name: str, personality: str, main_sku: str) -> str:
#         """Generate a personalized blend name using the user's name"""
#         # Name templates based on personality
#         name_templates = {
#             "playful": ["{}'s Summer Waltz", "{}'s Playful Dance", "{}'s Bright Spark"],
#             "mysterious": ["{}'s Midnight Reverie", "{}'s Velvet Secret", "{}'s Enigmatic Aura"],
#             "elegant": ["{}'s Timeless Grace", "{}'s Elegant Whisper", "{}'s Refined Essence"],
#             "bold": ["{}'s Bold Statement", "{}'s Commanding Presence", "{}'s Power Signature"],
#             "sensual": ["{}'s Intimate Allure", "{}'s Velvet Touch", "{}'s Sensual Whisper"],
#             "fresh": ["{}'s Morning Breeze", "{}'s Crystal Clear", "{}'s Fresh Awakening"],
#             "cozy": ["{}'s Warm Embrace", "{}'s Comforting Glow", "{}'s Cozy Haven"]
#         }
#
#         # Get templates for this personality
#         templates = name_templates.get(personality, ["{}'s Signature Blend"])
#
#         # Generate name
#         return random.choice(templates).format(user_name)
#
#     def generate_tagline(self, personality: str, main_sku: str) -> str:
#         """Generate a poetic one-line tagline for the blend"""
#         # Tagline templates based on personality
#         tagline_templates = {
#             "playful": [
#                 "A sunrise dancing on the ocean breeze.",
#                 "Laughter bottled in liquid sunshine.",
#                 "The spark that ignites endless possibilities."
#             ],
#             "mysterious": [
#                 "Whispers from the shadows that only you understand.",
#                 "The legend whispered in the night.",
#                 "A secret language spoken between kindred spirits."
#             ],
#             "elegant": [
#                 "Grace captured in every delicate note.",
#                 "Timeless refinement that speaks without words.",
#                 "The poetry of presence in every drop."
#             ],
#             "bold": [
#                 "A statement that arrives before you do.",
#                 "Confidence distilled into pure essence.",
#                 "The signature of someone unforgettable."
#             ],
#             "sensual": [
#                 "The touch that lingers in memory.",
#                 "Desire wrapped in liquid silk.",
#                 "A whisper that awakens all senses."
#             ],
#             "fresh": [
#                 "The first breath of clarity in a new day.",
#                 "Crisp awakening captured in a bottle.",
#                 "The essence of rejuvenation and possibility."
#             ],
#             "cozy": [
#                 "Warmth that embraces like a familiar memory.",
#                 "Comfort in liquid form, like coming home.",
#                 "The feeling of belonging, bottled."
#             ]
#         }
#
#         # Get templates for this personality
#         templates = tagline_templates.get(personality, ["Your unique signature, bottled."])
#
#         # Generate tagline
#         return random.choice(templates)
#
#     def generate_story(self, user_name: str, personality: str, fragrance_match: dict) -> dict:
#         """Generate a personalized emotional story and recommendation"""
#         main_sku = fragrance_match["main_sku"]
#         secondary_skus = fragrance_match["secondary_skus"]
#
#         # Generate blend name and tagline
#         blend_name = self.generate_blend_name(user_name, personality, main_sku)
#         tagline = self.generate_tagline(personality, main_sku)
#
#         # Get personality tone details
#         tone = self.tones.get(personality, self.tones["elegant"])
#         tone_words = tone["language"]
#
#         # Create story intro based on personality
#         intro_templates = {
#             "playful": [
#                 f"You are the first laugh of morning light, a playful breeze rushing over sparkling waves. Your spirit knows no bounds, and neither does your scent — a golden symphony crafted just for you.",
#                 f"In a world of routines, you are the unexpected joy, the {random.choice(tone_words)} that brings life to every moment. Your essence is captured perfectly in this blend created uniquely for your free spirit."
#             ],
#             "mysterious": [
#                 f"In the hush between dusk and darkness, when the world holds its breath, you emerge — enigmatic, powerful, unforgettable.",
#                 f"You move like a {random.choice(tone_words)} through life's moments, collecting secrets and stories. This blend honors the depth that few truly understand about you."
#             ],
#             "elegant": [
#                 f"There is a certain {random.choice(tone_words)} that follows you, a refined presence that speaks of timeless beauty and quiet confidence.",
#                 f"You carry yourself with an effortless elegance that turns heads not because it demands attention, but because it deserves it. This blend captures your sophisticated essence."
#             ],
#             "bold": [
#                 f"You don't simply enter a room — you transform it. Your {random.choice(tone_words)} precedes you, an energy that others feel before they even see you.",
#                 f"Bold and unapologetic, you make statements with your presence alone. This signature scent honors the confidence that is woven through every fiber of your being."
#             ],
#             "sensual": [
#                 f"There's an intimate language your presence speaks, a subtle invitation that draws others closer to discover the depths beneath your surface.",
#                 f"Your {random.choice(tone_words)} creates a gravity all its own, pulling others into your orbit through invisible threads of attraction and intrigue."
#             ],
#             "fresh": [
#                 f"You bring clarity wherever you go, like the first breath of mountain air that awakens all senses and possibilities.",
#                 f"There's a {random.choice(tone_words)} quality to your spirit that revitalizes every space you enter, making the ordinary suddenly extraordinary."
#             ],
#             "cozy": [
#                 f"You create sanctuary wherever you go, carrying warmth and {random.choice(tone_words)} that makes others feel instantly at home in your presence.",
#                 f"There's something about you that feels like returning to a cherished place — familiar, welcoming, and filled with quiet joy."
#             ]
#         }
#
#         intro = random.choice(intro_templates.get(personality, intro_templates["elegant"]))
#
#         # Description of the main SKU
#         main_sku_data = self.database[main_sku]
#         main_notes = main_sku_data["notes"][:3]  # Top 3 notes
#         main_character = main_sku_data["character"][:3]  # Top 3 character traits
#
#         # Description of the secondary SKUs
#         secondary_sku_1_data = self.database[secondary_skus[0]]
#         secondary_sku_1_notes = secondary_sku_1_data["notes"][:2]  # Top 2 notes
#
#         secondary_sku_2_data = self.database[secondary_skus[1]]
#         secondary_sku_2_notes = secondary_sku_2_data["notes"][:2]  # Top 2 notes
#
#         # Create the fragrance journey description
#         journey = f"""
# Your private blend opens with the {', '.join([f'{note.lower()}' for note in main_notes])} from {main_sku}, painting the air with {' and '.join(main_character)}. As the scent evolves, {secondary_skus[0]} joins the composition, weaving {' and '.join([note.lower() for note in secondary_sku_1_notes])} into a deeper harmony. Finally, {secondary_skus[1]} completes your signature with subtle notes of {' and '.join([note.lower() for note in secondary_sku_2_notes])}, creating a scent that is unmistakably yours.
#
# {blend_name} is not just a fragrance — it's a reflection of your essence, a story told through scent. It speaks of who you are and who you aspire to be.
#
# Whether you're {self._generate_scenario(personality)}, your signature scent captures your {tone['description']} spirit perfectly.
# """
#
#         # Create the full story
#         story = f"{intro}\n\n{journey}"
#
#         # Create the recommendation summary
#         recommendation = {
#             "blend_name": blend_name,
#             "main_notes": ", ".join(fragrance_match["main_notes"]),
#             "best_wearing_time": fragrance_match["best_wearing_time"],
#             "ideal_season": fragrance_match["ideal_season"],
#             "mood": ", ".join(fragrance_match["mood"]),
#             "recommended_skus": {
#                 main_sku: "2 shots",
#                 secondary_skus[0]: "1 shot",
#                 secondary_skus[1]: "1 shot"
#             }
#         }
#
#         return {
#             "blend_name": blend_name,
#             "tagline": tagline,
#             "story": story,
#             "recommendations": recommendation
#         }
#
#     def _generate_scenario(self, personality: str) -> str:
#         """Generate a scenario based on personality type"""
#         scenarios = {
#             "playful": [
#                 "exploring new adventures with childlike wonder",
#                 "turning an ordinary day into something magical",
#                 "bringing laughter to even the most serious moments"
#             ],
#             "mysterious": [
#                 "moving through twilight gatherings where secrets are exchanged",
#                 "captivating attention without ever revealing your full hand",
#                 "leaving others wondering about the depths they glimpsed in you"
#             ],
#             "elegant": [
#                 "attending events where refinement is celebrated",
#                 "creating moments of beauty in everyday life",
#                 "elevating the ordinary through your graceful presence"
#             ],
#             "bold": [
#                 "commanding attention in important meetings",
#                 "making decisive moves that others hesitate to make",
#                 "stepping confidently into challenging situations"
#             ],
#             "sensual": [
#                 "creating intimate moments that linger in memory",
#                 "drawing others closer through your magnetic presence",
#                 "celebrating the pleasure found in life's subtle textures"
#             ],
#             "fresh": [
#                 "bringing new energy to stagnant situations",
#                 "clearing away fog with your clarifying presence",
#                 "starting each day with renewed purpose and vision"
#             ],
#             "cozy": [
#                 "creating spaces where others feel instantly at home",
#                 "offering comfort in a world that often forgets to slow down",
#                 "weaving warmth into the fabric of everyday moments"
#             ]
#         }
#
#         return random.choice(scenarios.get(personality, scenarios["elegant"]))
#
#     def generate_closing_message(self) -> str:
#         """Generate the elegant closing message"""
#         return """
# Thank you for entrusting us with your story.
#
# At Shuts By L'dora, your soul speaks in scents — a language older than memory.
#
# We invite you to breathe life into your creation, to wear your signature boldly, softly, however your heart desires.
#
# Your journey is only beginning.
# Your story now lingers, beautifully, in the air around you.
#
# — With grace,
# Shuts By L'dora
# """
