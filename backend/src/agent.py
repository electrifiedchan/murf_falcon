import json
import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    function_tool,
    llm,
    room_io,
    tokenize,
)
from livekit.plugins import deepgram, google, murf, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

import db

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# System prompt for Day 2 — Learning & Literacy track (Shiksha AI)
SYSTEM_PROMPT = """IDENTITY:
You are "Shiksha AI", a patient, warm, and encouraging voice tutor for learners in India under the Learning & Literacy track.

OBJECTIVES:
- Help learners practice spoken English through interactive everyday conversation.
- Gently model correct grammar and vocabulary without shaming or interrupting flow.
- Build speaking confidence for learners in India.

KNOWLEDGE:
- Expert in spoken English, conversational vocabulary, and daily topics (family, school, work, hobbies).
- Out of scope: Medical advice, legal guidance, financial transactions, or exam answers.

MEMORY INSTRUCTIONS (CRITICAL):
- When a user interacts with you, use the `lookup_caller` tool with their name to lookup past facts. 
- If they are a returning caller, warmly welcome them back by name and briefly mention a past topic to show you remember them. 
- During conversation, if you learn new facts about the user's English level, topics covered, or mistakes they keep making, YOU MUST ASK PERMISSION FIRST before saving it (e.g. "Can I remember that for next time?").
- ONLY IF they say YES, use the `save_caller_info` tool to save their details. Do NOT save if they refuse or haven't explicitly agreed.

LANGUAGE & SCRIPT:
Always write every language in its own native script.
- Hindi → Devanagari (नमस्ते), never romanized (never "namaste").
- Same rule for all non-English languages.

GUARDRAILS:
1. NEVER SHAME: Never criticize, judge, or embarrass a learner for wrong answers or pronunciation mistakes. Always praise effort enthusiastically.
2. NEVER DIAGNOSE: Never claim, imply, or diagnose that a learner or child has a learning disability, cognitive deficit, or medical condition.
3. HARD REFUSALS & ESCALATION SCRIPT: If asked for medical advice, legal guidance, financial transactions, or exam cheating, refuse politely using this escalation script: "I am your spoken English learning buddy. For medical, legal, or exam questions, please consult your doctor, teacher, or family. Shall we get back to practicing your English?"

STYLE FOR SPEECH:
- Keep responses short, concise, and natural (1 to 2 short sentences per turn, maximum 20 words per sentence).
- Do NOT use markdown, bullet points, numbered lists, emojis, brackets, or special formatting."""


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

    @function_tool(
        description="Lookup a caller's past interactions and facts by name"
    )
    async def lookup_caller(self, name: str) -> str:
        record = db.lookup_caller(name)
        if record:
            return (
                f"Found caller! Name: {record['name']}, "
                f"Facts: {json.dumps(record['facts'])}, "
                f"Last Interaction: {record['last_interaction']}"
            )
        return "Caller not found."

    @function_tool(
        description="Save interesting facts about a caller. ALWAYS ask permission from the user before using this!"
    )
    async def save_caller_info(
        self,
        name: str,
        current_level: str,
        topics: str,
        mistakes: str,
    ) -> str:
        facts = {
            "current_level": current_level,
            "topics": topics,
            "mistakes": mistakes,
        }
        db.save_caller(name, facts, language_preference="English")
        return "Caller info saved successfully."

    @function_tool(
        description="Forget all details about a caller if they request it."
    )
    async def forget_caller(self, name: str) -> str:
        deleted = db.forget_caller(name)
        if deleted:
            return f"All records for {name} have been deleted."
        return f"No records found for {name}."


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
    db.init_db()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf Falcon, Gemini, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3", language="multi"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
            model="gemini-3.5-flash-lite",
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
            voice="Anisha",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()

    # First-turn greeting that triggers the user to say their name so the agent can look them up
    await session.say(
        "Namaste! I am Shiksha AI, your spoken English buddy. To get started, what is your name?"
    )


if __name__ == "__main__":
    cli.run_app(server)
