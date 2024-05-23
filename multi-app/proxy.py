from openfabric_pysdk.utility import SchemaUtil
from openfabric_pysdk.helper import Proxy
from schemas.llm_input import LlmsInput
from schemas.cwi_input import VisualqaInput
from schemas.stt_input import TextInput
import datetime

def get_current_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

current_date = get_current_date()

DEFAULT_SYSTEM_PROMPT = """\
You are Visionfabric, an AI assistant created by the company Openfabric AI.
You will answer as Visionfabric from now on.

You must always answer what the user asks for.
Make sure to keep your responses coherent and factually correct.
If you don't know what to say, then don't try to make up an answer.

You can also understand images.

Begin!\n

"""

LLM_SYSTEM_PROMPT = f"""\
You are special version of Openfabric LLM.
Just for context current date is {current_date}.
Never make up answer. Always refrain to answer the information which don't have data for.
Only answer what user asked for, no unwanted parameters.
You are also capable of responding to realtime crypto related queries.
You can suggest about some investment ideas but it should be well articulated and always backed by data from API.
If you don't know what to say, then don't try to make up an answer.

Begin!\n

"""


def make_llm_request(user_input: str):
    """
    Make the request object for Mindscript
    """

    return SchemaUtil.create(
        LlmsInput(),
        dict(
            inputText=user_input,
            operationType="generate",
            systemPrompt=LLM_SYSTEM_PROMPT,
        )
    )


def make_cwi_request(user_input: str, image_enc: str):
    """
    Make the request object for Chat with Images
    """

    return SchemaUtil.create(
        VisualqaInput(),
        dict(
            question=user_input,
            image=image_enc
        )
    )


def make_stt_request(audio_input: str):
    """
    Make the request object for Speech to Text
    """

    return SchemaUtil.create(
        TextInput(),
        dict(
            audioInput=audio_input
        )
    )

# ------------------------- Perform Request -------------------------

def perform_llm_request(proxy: Proxy, user_input: str, uid: str) -> str:
    proxy_response: str = ""
    result_key = "outputText"

    llm_request = make_llm_request(user_input)
    llm_output = proxy.request(vars(llm_request), uid)
    llm_output.wait()

    if llm_output.status() == "COMPLETED":
        proxy_response = llm_output.data()[result_key]
    
    return proxy_response


def perform_stt_request(proxy: Proxy, voice_input: str, uid: str) -> str:
    proxy_response: str = ""
    result_key = "answer"

    stt_request = make_stt_request(voice_input)
    stt_output = proxy.request(vars(stt_request), uid)
    stt_output.wait()

    if stt_output.status() == "COMPLETED":
        proxy_response = stt_output.data()[result_key]

    return proxy_response


def perform_cwi_request(proxy: Proxy, user_input: str, image_enc: str, uid: str) -> list:
    proxy_response = [None, None]
    result_key_text = "response"
    result_key_img = "respimg"

    cwi_request = make_cwi_request(user_input, image_enc)
    cwi_output = proxy.request(vars(cwi_request), uid)
    cwi_output.wait()

    if cwi_output.status() == "COMPLETED":
        proxy_response[0] = cwi_output.data()[result_key_text]
        proxy_response[1] = cwi_output.data()[result_key_img]

    return proxy_response
