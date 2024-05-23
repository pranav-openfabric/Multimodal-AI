from typing import Dict, List, Union
import proxy as prx
import utils
from openfabric_pysdk.context import MessageType, Ray, State, StateStatus
from openfabric_pysdk.helper import Proxy
from openfabric_pysdk.loader import ConfigClass, InputClass, OutputClass
from openfabric_pysdk.utility import SchemaUtil
from openfabric_pysdk.service.property_service import PropertyService
from crypto_api_client import CryptoAPIClient, extract_crypto_from_query

# Retrieve proxy links from PropertyService
LLM_PROXY_LINK = PropertyService.get("multi_llm_proxy")
CWI_PROXY_LINK = PropertyService.get("multi_cwi_proxy")
STT_PROXY_LINK = PropertyService.get("multi_stt_proxy")

# Initialize Proxy objects
llm_proxy = Proxy(LLM_PROXY_LINK, "LLM proxy")
cwi_proxy = Proxy(CWI_PROXY_LINK, "CWI proxy")
stt_proxy = Proxy(STT_PROXY_LINK, "STT proxy")

# Initialize CryptoAPIClient
crypto_client = CryptoAPIClient()


def execute(request: InputClass, ray: Ray, state: State) -> OutputClass:
    text_input = request.text
    voice_input = request.voice
    option = request.option
    attachment = request.attachment
    uid = ray.uid

    ray.message(MessageType.INFO, content="Processing inputs...")

    user_input: str = ""

    if option == "textInput":
        user_input = text_input
    elif option == "voiceInput":
        ray.message(MessageType.INFO, content="Converting voice to text...")
        stt_output = prx.perform_stt_request(stt_proxy, voice_input, uid)
        user_input = stt_output

    user_input = user_input.strip() if user_input else None

    # Extract cryptocurrency from user query
    crypto = extract_crypto_from_query(user_input)
    ray.message(MessageType.INFO, content=crypto)
    out = "Here is the latest information I got from API: "
    

    if crypto:
    # Get symbol of the cryptocurrency
        symbol = crypto_client.get_crypto_symbol(crypto)
        if symbol != "Cryptocurrency not found":
            # Get latest data of the cryptocurrency
            data = crypto_client.get_latest_crypto_data(symbol)
            if data != "Cryptocurrency not found":
                # Combine cryptocurrency data with user query
                for info in data:
                    out += f"{info}: {data[info]}, "
                    user_input += out

            else:
                user_input = text_input  # Send original query to LLM if crypto data not found.
            

    if attachment is not None:
        if not user_input:
            ray.message(MessageType.INFO, content="Only attachment found. Understanding the image...")
            user_input = "What's this? Answer in detail."
        else:
            ray.message(MessageType.INFO, content="Understanding the image...")

    if not user_input and attachment is None:
        ray.message(MessageType.ERROR, content="No input text/voice/attachment found.")
        return SchemaUtil.create(
            OutputClass(),
            dict(response="No input text/voice/attachment found.", attachment=None)
        )

    if user_input and utils.is_tokens_exceeded(user_input):
        ray.message(MessageType.ERROR, content="Input text/voice is too long to be processed. Try again.")
        return SchemaUtil.create(
            OutputClass(),
            dict(response="Input text/voice is too long to be processed. Try again.", attachment=None)
        )

    response = ""
    respimg = None

    if attachment is not None:
        response, respimg = prx.perform_cwi_request(cwi_proxy, user_input, attachment, uid)
    else:
        response = prx.perform_llm_request(llm_proxy, user_input, uid)

    ray.message(MessageType.INFO, content="🎉 Generated response.")

    if response:
        response = response[0].upper() + response[1:]
    else:
        response = "No response was generated. Check the logs for any errors."

    return SchemaUtil.create(
        OutputClass(),
        dict(response=response, attachment=respimg)
    )
