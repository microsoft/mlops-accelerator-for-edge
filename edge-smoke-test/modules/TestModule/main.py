import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
import requests
import datetime
from azure.iot.device import MethodResponse

# Event indicating client stop
stop_event = threading.Event()


def create_client():
    """
    Direct Method Client to do smoke test using http request
    """
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        """
        This is the Message Handler for direct method
        """
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            print("the data in the message received on input1 was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("forwarding mesage to output1")
            await client.send_message_to_output(message, "output1")

    async def method_request_handler(method_request):
        """
        This is the method request handler from IoTHub
        """
        try:
            await client.send_message(
                "Received Method Request: " + str(method_request.name)
            )
            print(
                "Received direct message: {} {}\n".format(
                    str(method_request.name), str(method_request.payload)
                )
            )
            if str(method_request.name) == "smokeTest":

                port = method_request.payload["port"]
                model_type=method_request.payload["model_type"]
                url = 'http://localhost:{}/score'.format(port)
                test_file_name = f"./test-data/{model_type}/sample-request.json"
                data = open(test_file_name, 'r').read()
                res = requests.post(
                    url=url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                print(res.text)

                infer_result = "{}".format(res.text)
                return_payload = {"infer_result": infer_result}
                method_response = MethodResponse.create_from_method_request(
                    method_request, 200, return_payload
                )
                await client.send_method_response(method_response)
                await client.send_message_to_output("done", "output1")
            else:
                print("Invalid method name. \
                    accepctable methods include 'smokeTest'.")
                method_response = MethodResponse.create_from_method_request(
                    method_request, 400,
                    "{\"results\": \"Invalid method name. \
                        accepctable methods include \'smokeTest\'. \"}"
                )
                await client.send_method_response(method_response)

        except Exception as e:
            print(e)
            method_response = MethodResponse.create_from_method_request(
                method_request, 400, "{\"results\": \"fail\"}"
            )
            await client.send_method_response(method_response)

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
        client.on_method_request_received = method_request_handler
    except Exception:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_test(client):
    """
    Runner
    """
    while True:
        await asyncio.sleep(1000)


def main():
    """
    Main method
    """
    if not sys.version >= "3.5.3":
        raise Exception(
            "The sample requires python 3.5.3+. Current version of Python: %s"
            % sys.version)
    print("IoT Hub Client for Python")
    print(datetime.datetime.now())
    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_test(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
