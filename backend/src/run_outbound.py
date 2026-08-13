import argparse
import asyncio
import json
import logging
import os
import uuid

from dotenv import load_dotenv
from livekit import api as lk_api

# Load .env.local from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("run_outbound")


async def main():
    parser = argparse.ArgumentParser(description="Trigger Day 6 outbound call")
    parser.add_argument(
        "--to",
        required=True,
        help="SIP URI (e.g. sip:yourname@sip.linphone.org) or phone number",
    )
    args = parser.parse_args()

    destination = args.to

    lk = lk_api.LiveKitAPI(
        url=os.environ["LIVEKIT_URL"],
        api_key=os.environ["LIVEKIT_API_KEY"],
        api_secret=os.environ["LIVEKIT_API_SECRET"],
    )

    # Unique room name for each call
    room_name = f"practice-{uuid.uuid4().hex[:8]}"
    logger.info(f"Creating LiveKit room: {room_name}")
    await lk.room.create_room(lk_api.CreateRoomRequest(name=room_name))

    # Pass the destination to the agent inside its dispatch metadata
    meta = {"phone_number": destination}

    logger.info(
        f"Dispatching Shiksha AI to room {room_name} with destination {destination}..."
    )

    dispatch = await lk.agent_dispatch.create_dispatch(
        lk_api.CreateAgentDispatchRequest(
            agent_name="my-agent",
            room=room_name,
            metadata=json.dumps(meta),
        )
    )

    logger.info(f"Dispatched agent successfully (Dispatch ID: {dispatch.id})")
    logger.info(
        "The agent will now load (should take 2-4 seconds) and dial the destination."
    )
    logger.info(
        "Press Ctrl+C to exit this script. The call will continue until hung up."
    )

    await lk.aclose()


if __name__ == "__main__":
    asyncio.run(main())
