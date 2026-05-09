# services/mcp/tool_registry.py

from pathlib import Path

from services.mcp.models.mcp_tool_definition import ToolDefinition


class MCPToolRegistry:

    def __init__(self):
        # self._tool_directories = [Path(directory) for directory in tool_directories]
        self._tool_directories = [
        "services/mcp/get_work_directory_tool",
        "services/mcp/list_pdf_tool",
        "services/mcp/read_pdf_content_tool",
    ]

    def getAllMCPTools(self) -> list[ToolDefinition]:

        all_tools: list[ToolDefinition] = []

        for directory in self._tool_directories:

            tools_from_directory = self.load_tools_from_directory(directory)

            all_tools.extend(tools_from_directory)

        return all_tools

    def load_tools_from_directory(self, directory: str) -> list[ToolDefinition]:

        json_files = sorted(Path(directory).glob("*.json"))

        tools: list[ToolDefinition] = []

        for file_path in json_files:

            # json_text = Path(file_path).read_text(encoding="utf-8")
            json_text = file_path.read_text(encoding="utf-8")

            tool_definition = ToolDefinition.model_validate_json(json_text)

            tools.append(tool_definition)

        return tools