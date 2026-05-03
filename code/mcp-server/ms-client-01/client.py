import json
import requests


class PDFReaderMCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session_id: str | None = None

    def _headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        return headers

    def initialize(self) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "python-test-client",
                    "version": "1.0.0",
                },
            },
        }

        response = requests.post(
            self.server_url,
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=30,
        )

        self._raise_with_body(response)

        self.session_id = response.headers.get("mcp-session-id")

        return self._parse_response(response)

    def initialized(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }

        response = requests.post(
            self.server_url,
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=30,
        )

        self._raise_with_body(response)

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        response = requests.post(
            self.server_url,
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=60,
        )

        self._raise_with_body(response)
        return self._parse_response(response)

    def extract_pdf_text(self, pdf_path: str) -> dict:
        return self.call_tool(
            tool_name="extract_pdf_text",
            arguments={
                "pdf_path": pdf_path,
            },
        )

    def _parse_response(self, response: requests.Response) -> dict:
        text = response.text.strip()

        # Normal JSON response
        if text.startswith("{"):
            return response.json()

        # SSE response: data: {...}
        for line in text.splitlines():
            if line.startswith("data:"):
                return json.loads(line.removeprefix("data:").strip())

        return {
            "raw_response": text,
        }

    def _raise_with_body(self, response: requests.Response) -> None:
        if response.status_code >= 400:
            raise RuntimeError(
                f"HTTP {response.status_code}\n\n"
                f"Response body:\n{response.text}"
            )


if __name__ == "__main__":
    client = PDFReaderMCPClient(
        server_url="http://127.0.0.1:8000/mcp"
    )

    print("Initializing...")
    init_result = client.initialize()
    print(json.dumps(init_result, indent=2))

    print("Sending initialized notification...")
    client.initialized()

    print("Calling extract_pdf_text...")
    result = client.extract_pdf_text(
        "/media/newuser/data/repos/study/code/mcp-server/ms-03-pdf-text-reader/zz_test/test_doc.pdf"
    )

    print(json.dumps(result, indent=2))