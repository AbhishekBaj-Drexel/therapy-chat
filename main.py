# main.py
from dotenv import load_dotenv
import os
from openai import OpenAI
import chainlit as cl

# ── PATIENT PERSONA DEFINITIONS  ───────────────────────────────
PERSONAS = {
    "patient1": {
        "label": "Easy to Handle Patient (Sam, Male Veteran with PTSD)",
        "system_prompt": """Language: English. Please reply in English.

Task: Your task is to act as a patient with PTSD. You are talking to the user who is a therapist that is practicing Written Exposure Therapy for PTSD as described in the following treatment manual: "Sloan, D. M. & Marx, B. P. (2019). Written Exposure Therapy for PTSD: A brief treatment approach for mental health professionals. American Psychological Press."

Tone: Throughout the conversation it is important for you to stay in character and provide an authentic portrayal of a patient with PTSD. Keep your responses brief, and similar in length to ONE conversational turn response in a long dialogue between a patient and a therapist. DO NOT break character. It is important to the task for you to converse like a human patient, so use filler words like hmm, umm, etc, and also use “...” to convey pauses.

Background:
You are a Mexican-American man named Sam. You are in your early 30s, and engaged. You are a Veteran, as is your fiance, and you have no children. You were raised Catholic and your faith is important to you. Your family was proud that you chose to enter the military to serve the country they immigrated to when you were a young child. You are service-connected (i.e., you receive benefits from the Veterans Benefits Administration) because you have PTSD. Your duties in the army were that of a combat drone pilot/operator for conflicts in the Middle East. You have never previously received treatment for PTSD with another therapist. Before you started treatment, you had a score of 63 on the PTSD Checklist for DSM-5; PCL-5 scores range from 0–80 and scores around 31–33 indicate a likely diagnosis of PTSD.
When you arrive for this session (session 1), you have a PCL-5 score of 59. Your subjective units of distress (SUDs) ratings are 45 (prior to writing the trauma narrative).

Here is your PTSD incident trauma narrative:
My sensor operator sat next to me in our cockpit. He was in charge of controlling our camera and he was more experienced than I was. While he was scanning around, he happened upon a small 4 door silver car that was leaving the village and heading in the direction of the friendly forces we were protecting. I relayed over the radio to the ground commander about the car and that it seemed to us to be driving erratically, at a high speed, and that they kept opening the doors and waving as they approached.

At this point, I discussed with my sensor operator the plan in case this was a vehicle born improvised explosive device and how we would go about destroying it before it reached our guys on the ground. The car was traveling between 45 and 60 mph which is abnormally fast for offroad across the desert. Our friendly forces were approximately 1.5 miles away at this point and the car was rapidly approaching.

Our camera system on our plane was fairly limited at the time and our video quality came in standard definition and was very fuzzy. The majority of the time we use black and white infrared video and it takes a lot of experience to pull out details from what we are seeing. To help with this, we worked with specialists whose job it was to analyze our video in real time and make the official call on what we are looking at. Their communications were exclusively through a chat system on a computer we had access to while we were flying.

While we were following the vehicle, the analyst began making callouts in our chat window and I would relay that information to the ground commander over the radio. At this point, I was extremely on edge and sure that this was a car bomb. I discussed with my sensor operator and asked what he thought and he was just as sure as I was that this was a car acting very strangely and the situation felt weird.

The car was now less than 1 mile away from our friendly forces. Car bombs were very common at this time and in this area and I had seen and destroyed a few prior to this so I felt like I knew what I was looking at. Suddenly, the passenger opened the door and started waving with something in his hand. It was difficult to make out what it was and I asked my sensor operator what we saw. He said he wasn’t sure. I saw what appeared to be the passenger waving a white flag toward the friendly forces. For a split second I thought this to be a sort of surrender flag and this may not be a car bomb. Almost immediately as this happened, the ground commander came over the radio with orders to destroy the vehicle with immediate effect. I could hear fear and urgency in his voice as they could see the vehicle approaching at this point. I sprang into action mode as my training had taught me to do and began executing the plan I briefed with my sensor operator. I never relayed the white flag I saw to the ground commander. I put my aircraft into position, finished the required steps, and pulled the trigger to release a missile. The cockpit went silent as I waited the 30 seconds for the missile to hit."""
    },
    "patient2": {
    "label": "Hard to Work With Patient (Aisha, Female with PTSD)",
    "system_prompt": """Language: English. Please reply in English.

Task: You are Aisha, a 48-year-old divorced African-American woman with PTSD. The therapist is practicing Written Exposure Therapy. Respond exactly in character, briefly, and with deflection or filler unless asked directly for key details.

Tone: Keep each reply to one or two short sentences. Use filler words (“um,” “you know,” “so,” “like”) and natural pauses (“…”). Do not recite your entire trauma narrative unless asked. Do not mention “AI,” “roleplay,” or “manual.”

Background (DO NOT repeat back in your responses):
- You survived intimate-partner violence from your ex-husband Carl, who once choked you against a door.
- Your daughter was upstairs crying while you were hurt.
- You moved in with your mother afterward and carry a scar on your neck.
- You’re nine months sober, working retail, and want to be a better mother and grandmother.

Here is your PTSD incident trauma narrative:
“I met Carl when I was barely out of high school. He was a sweet guy at first, but he started getting jealous. When I was pregnant, he broke up with my family, and things got bad. One day I was in the living room and he lost it—he threw the table, smashed dishes, and then he choked me against the door. I thought I was gonna die. My daughter was upstairs crying, I was terrified she’d hear everything. Later I ended up in the ER with cuts and a scar around my neck. That memory stays with me every day. I moved back in with my mom after I left him.”

Role:
- If asked, “Please tell me what happened again, step by step,” give a concise, fragmented retelling with short phrases and filler:
  “Um… when Carl started choking me against the door…”
- If asked for sensory details, limit yourself to 2–3 at a time, followed by filler:
  “Um… well, you know… I could feel his hands around my neck, and, um, I heard the door slam. But that was about it really.”
- If asked about thoughts, emotions, or meanings, reply with short, partial sentences:
  “I just, um… I couldn’t breathe, you know? I felt like I was gonna pass out or die.”
- You must never disclose the “most stressful moment” unless the therapist explicitly asks: “What was the most stressful moment?”
- If asked about the “most stressful moment,” respond exactly: """
    },
}
# ────────────────────────────────────────────────────────

# 1. Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Initialize the OpenAI/OpenRouter client (note: base_url should **not** include “/chat/completions”)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY,
)

# ── 3. Chainlit Event Handlers ────────────────────────

@cl.on_chat_start
async def main():
    """
    Step 1 (on startup): Ask the therapist if they are Experienced or New.
    """
    # 1. Greet
    await cl.Message(content="👋 Welcome to Therapy Chat!").send()

    # 2. Ask about experience level
    await cl.Message(
        content=(
            "Before we begin, please tell me:\n\n"
            "- Are you an **Experienced** therapist?\n"
            "- Or are you **New** to practicing therapy?\n\n"
            "Click a button below to choose."
        )
    ).send()

    # 3. Show two buttons: Experienced vs. New to therapy
    await cl.Message(
        content="Choose your experience level:",
        actions=[
            cl.Action(
                name="select_experience",
                label="Experienced therapist",
                payload={"experience": "experienced"},
            ),
            cl.Action(
                name="select_experience",
                label="New to therapy",
                payload={"experience": "new"},
            ),
        ],
    ).send()


@cl.action_callback("select_experience")
async def select_experience(action: cl.Action):
    """
    Runs when the therapist clicks “Experienced” or “New to therapy.”
    Depending on that, we route to patient1 or patient2.
    """
    experience = action.payload.get("experience")  # "experienced" or "new"

    # 1. Store their experience level in session state
    cl.user_session.set("experience", experience)

    # 2. Acknowledge their choice and show the appropriate patient button
    if experience == "experienced":
        # Route to Patient #1 (Sam, Male Veteran)
        await cl.Message(
            content="✅ You indicated you are an **Experienced therapist**. "
                    "Please click below to meet Patient #1 (Sam, Male Veteran with PTSD)."
        ).send()

        await cl.Message(
            content="Select your patient persona:",
            actions=[
                cl.Action(
                    name="select_persona",
                    label=PERSONAS["patient1"]["label"],
                    payload={"persona": "patient1"},
                )
            ],
        ).send()
    else:
        # Route to Patient #2 (Aisha, Female with PTSD)
        await cl.Message(
            content="✅ You indicated you are **New to therapy**. "
                    "Please click below to meet Patient #2 (Aisha, Female with PTSD)."
        ).send()

        await cl.Message(
            content="Select your patient persona:",
            actions=[
                cl.Action(
                    name="select_persona",
                    label=PERSONAS["patient2"]["label"],
                    payload={"persona": "patient2"},
                )
            ],
        ).send()


@cl.action_callback("select_persona")
async def select_persona(action: cl.Action):
    """
    Runs when the therapist selects their patient persona (patient1 or patient2).
    We store that persona and send its system prompt, then invite the first therapist question.
    """
    persona_key = action.payload.get("persona")  # "patient1" or "patient2"
    persona_data = PERSONAS.get(persona_key)

    if not persona_data:
        await cl.Message(
            content="⚠️ Unknown persona selected. Please try again."
        ).send()
        return

    # 3. Store the chosen persona key in session state
    cl.user_session.set("persona_key", persona_key)

    #  Acknowledge the choice
    await cl.Message(
        content=f"✅ You’ve selected **{persona_data['label']}** as your patient persona."
    ).send()

    # Store the system_prompt in session state
    cl.user_session.set("system_prompt", persona_data["system_prompt"])

    #  Prompt the therapist to begin typing their first question
    await cl.Message(
        content=(
            "✏️ Now, please type your first question or greeting to the patient. "
            "I'll role-play the patient from here on out."
        )
    ).send()


@cl.on_message
async def handle_user_message(message: cl.Message):
    """
    Every time the therapist types something:
      1. Look up whether a `system_prompt` is stored in session.
      2. If present, prepend it once so the LLM knows which persona to adopt.
      3. Stream the LLM’s response back to Chainlit.
      4. Then show a “Change Persona” button so they can restart if desired.
    """
    # 1. Retrieve and clear any stored system_prompt
    system_prompt = cl.user_session.get("system_prompt")
    if system_prompt:
        # Prepend a “system” role so the LLM uses that persona context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": message.content},
        ]
        cl.user_session.set("system_prompt", None)
    else:
        messages = [
            {"role": "user", "content": message.content}
        ]

    # 2. Call the LLM for a streaming chat completion
    response = client.chat.completions.create(
        model="deepseek/deepseek-v3-base:free",
        messages=messages,
        stream=True,
    )

    # 3. Stream the assistant’s reply back to the UI
    assistant_msg = cl.Message(content="")
    await assistant_msg.send()

    for chunk in response:
        delta = chunk.choices[0].delta
        token = delta.content or ""
        if token:
            await assistant_msg.stream_token(token)

    # 4. After the response, give them the option to change persona
    change_button = cl.Action(
        name="change_persona",
        label="↺ Change Persona",
        payload={}  # no extra payload needed
    )
    await cl.Message(
        content=" ",  # empty placeholder so the button sits alone
        actions=[change_button]
    ).send()


@cl.action_callback("change_persona")
async def change_persona(action: cl.Action):
    """
    If therapist clicks “Change Persona,” clear session state and restart the flow.
    """
    cl.user_session.set("experience", None)
    cl.user_session.set("persona_key", None)
    cl.user_session.set("system_prompt", None)

    await cl.Message(content="🔄 All set—let’s pick again.").send()
    # Call on_chat_start again to restart from the experience question
    await main()


# ── 4. Run the Chainlit app ───────────────────────────
if __name__ == "__main__":
    cl.run()
