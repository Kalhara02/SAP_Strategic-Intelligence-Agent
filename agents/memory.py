# ==================================================
# Agent Memory
# ==================================================

class AgentMemory:

    def __init__(self):

        self.history = []

    # ==================================================
    # Store Interaction
    # ==================================================

    def add_interaction(

        self,

        question,

        plan,

        evidence=None,

        intelligence=None,

        sentiment=None,

        priorities=None,

        recommendations=None,

        validation=None,

        ceo_briefing=None

    ):

        interaction = {

            "question": question,

            "plan": plan,

            "evidence": evidence,

            "intelligence": intelligence,

            "sentiment": sentiment,

            "priorities": priorities,

            "recommendations": recommendations,

            "validation": validation,

            "ceo_briefing": ceo_briefing

        }

        self.history.append(interaction)

    # ==================================================
    # Get Last Interaction
    # ==================================================

    def get_last_interaction(self):

        if len(self.history) == 0:

            return None

        return self.history[-1]

    # ==================================================
    # Get Entire Memory
    # ==================================================

    def get_memory(self):

        return self.history

    # ==================================================
    # Number of Stored Interactions
    # ==================================================

    def size(self):

        return len(self.history)

    # ==================================================
    # Clear Memory
    # ==================================================

    def clear(self):

        self.history.clear()


# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    memory = AgentMemory()

    memory.add_interaction(

        question="What are SAP's biggest risks?",

        plan={
            "goal": "Risk Analysis"
        },

        evidence=["Reuters Article"],

        intelligence="Risk analysis output",

        sentiment={
            "overall_sentiment": "Negative"
        },

        priorities=[
            "Strengthen cybersecurity",
            "Expand AI investment"
        ],

        recommendations="Increase cybersecurity investment.",

        validation={
            "is_valid": True,
            "confidence": "High"
        },

        ceo_briefing="CEO summary."

    )

    print("Memory Size:")

    print(memory.size())

    print("\nLatest Interaction:\n")

    print(memory.get_last_interaction())