import sys
import unittest
import time
import requests
from ipaddress import ip_address

try:
    ip = str(sys.argv[1])
    print(f"testing at: {ip}")
    try:
        ip_address(ip)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit()

except IndexError:
    print("Usage: tests.py ip")
    sys.exit()


def test_probe(resp, status_code, response):
    print(int(resp.status_code))
    print(resp.json())
    if resp.status_code == int(status_code):
        if resp.json() == response:
            return True


class Test(unittest.TestCase):
    status_code_415 = 415
    status_code_200 = 200
    status_code_400 = 400
    status_code_401 = 401
    probeResponse = {"error": "Access Forbidden"}
    emptyBody_response = {
        "error": {
            "type": "unsupported_media_type",
            "message": "Expected JSON body.",
            "invalid": [
                {
                    "entry_type": "request_body",
                    "entry": "",
                    "rule": "json",
                    "constraint": True,
                }
            ],
        }
    }

    emptyJson_response = {
        "error": {"type": "validation_failed", "message": "Validation failed."}
    }

    validJson_request = {
        "id": "test",
        "project": "test",
        "project_name": "test",
        "project_slug": "test",
        "logger": None,
        "level": "test",
        "culprit": "test",
        "message": "test",
        "url": "http://test.com",
        "triggering_rules": "test",
        "event": {"title": "test", "timestamp": time.time()},
    }

    success_response = {"success": "200"}
    channel_unauthorized_response = {
        "error": {"message": "Unauthorized channel", "channel": 234515384919654400}
    }
    channel_invalid_response = {
        "error": {"message": "Unauthorized channel", "channel": 1}
    }
    invalid_user_response = {"error": {"message": "User does not exist", "user": 1}}
    string_mention_id_response = {
        "error": {"message": "Mention ID must be a string of integer"}
    }
    string_channel_id_response = {
        "error": {"message": "Channel ID must be a string of integer"}
    }
    existing_project_response = {
        "error": {
            "message": "User is already registered to other project",
            "id": 253519680919044096,
            "project": "test1",
        }
    }
    unregistered_user_response = {
        "error": {
            "message": "User is not registered to any project",
            "id": 234513470035460096,
        }
    }

    if ip != "0.0.0.0":
        status_code_200 = status_code_415 = status_code_400 = status_code_401 = 403
        emptyBody_response = (
            emptyJson_response
        ) = (
            success_response
        ) = (
            channel_unauthorized_response
        ) = (
            channel_invalid_response
        ) = (
            invalid_user_response
        ) = (
            string_mention_id_response
        ) = (
            string_channel_id_response
        ) = existing_project_response = unregistered_user_response = {
            "error": "Unauthorized IP"
        }

    def test_get_invalidMethod_1(self):
        print("\nTesting invalid method GET to undefined route / ")
        self.assertEqual(
            test_probe(
                requests.get(f"https://{ip}:8080/", verify=False),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_get_invalidMethod_2(self):
        print("\nTesting invalid method GET to undefined route /hello ")
        self.assertEqual(
            test_probe(
                requests.get(f"https://{ip}:8080/hello", verify=False),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_get_invalidMethod_3(self):
        print("\nTesting invalid method GET to valid endpoint")
        self.assertEqual(
            test_probe(
                requests.get(f"https://{ip}:8080/sentry-bot/channel?", verify=False),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_get_invalidMethod_4(self):
        print("\nTesting invalid method GET to valid endpoint and arguments")
        self.assertEqual(
            test_probe(
                requests.get(
                    f"https://{ip}:8080/sentry-bot/channel?id=1&mention=1",
                    verify=False,
                ),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_post_404_1(self):
        print("\nTesting valid method POST to undefined route / ")
        self.assertEqual(
            test_probe(
                requests.post(f"https://{ip}:8080/", verify=False),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_post_404_2(self):
        print("\nTesting valid method POST to undefined route /hello ")
        self.assertEqual(
            test_probe(
                requests.post(f"https://{ip}:8080/hello", verify=False),
                400,
                self.probeResponse,
            ),
            True,
        )

    def test_post_empty_body(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with invalid body "
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=1&mention=1",
                    verify=False,
                ),
                self.status_code_415,
                self.emptyBody_response,
            ),
            True,
        )

    def test_post_empty_JSON(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with empty JSON"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=1&mention=1",
                    json={},
                    verify=False,
                ),
                self.status_code_400,
                self.emptyJson_response,
            ),
            True,
        )

    def test_post_invalid_JSON_1(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with invalid JSON"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=1&mention=1",
                    json={"hello": "world"},
                    verify=False,
                ),
                self.status_code_400,
                self.emptyJson_response,
            ),
            True,
        )

    def test_post_valid_JSON(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with valid JSON and logger value is None"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=179182605038518273",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_200,
                self.success_response,
            ),
            True,
        )

    def test_post_valid_JSON_no_mention(self):
        print(
            "\nTesting valid method POST to valid endpoint with valid JSON and no mention argument"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_200,
                self.success_response,
            ),
            True,
        )

    def test_post_valid_JSON_1(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with valid JSON and logger value is not None"
        )
        self.validJson_request["logger"] = "test"
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=179182605038518273",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_200,
                self.success_response,
            ),
            True,
        )

    def test_post_unauthorized_channel_1(self):
        print(
            "\nTesting valid method POST to valid endpoint and arguments with valid JSON but unauthorized channel at user level"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=234515384919654400&mention=179182605038518273",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_401,
                self.channel_unauthorized_response,
            ),
            True,
        )

    def test_post_invalid_id(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but invalid channel ID"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=1&mention=179182605038518273",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_401,
                self.channel_invalid_response,
            ),
            True,
        )

    def test_post_invalid_mention(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but invalid mention ID"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=1",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_401,
                self.invalid_user_response,
            ),
            True,
        )

    def test_post_string_mention(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but invalid mention ID in string (int conversion strict exception handling)"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=abc",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_400,
                self.string_mention_id_response,
            ),
            True,
        )

    def test_post_string_channel(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but invalid mention ID in string (int conversion strict exception handling)"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=abc&mention=abc",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_400,
                self.string_channel_id_response,
            ),
            True,
        )

    def test_post_existing_project(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but project is already registered by another user"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=253519680919044096",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_401,
                self.existing_project_response,
            ),
            True,
        )

    def test_post_unregistered_mention(self):
        print(
            "\nTesting valid method POST to valid endpoint and valid JSON but user have not yet registered to a project"
        )
        self.assertEqual(
            test_probe(
                requests.post(
                    f"https://{ip}:8080/sentry-bot/channel?id=582329068469616655&mention=234513470035460096",
                    json=self.validJson_request,
                    verify=False,
                ),
                self.status_code_401,
                self.unregistered_user_response,
            ),
            True,
        )


if __name__ == "__main__":
    unittest.main(argv=['', '-v'])