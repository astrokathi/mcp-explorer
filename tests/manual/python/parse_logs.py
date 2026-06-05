import json
import re
from pathlib import Path

def sanitize(text):
    if not text:
        return ""
    # Case insensitive replacement of Nike with MCP
    text = re.sub(r'(?i)nike', 'MCP', text)
    return text

def main():
    log_path = Path("/Users/kathi.s/.gemini/antigravity/brain/a7dd681c-7ee8-4f02-8fa7-224242ec388f/.system_generated/logs/transcript.jsonl")
    output_path = Path("/Users/kathi.s/NKExplorer/Nike_Explorer/docs/session_history.md")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    markdown = []
    markdown.append("# MCP Explorer Development Session Log\n")
    markdown.append("This document contains the chronological trace of the development session, showing how the MCP Explorer app was constructed, debugged, and optimized.\n")
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                step = json.loads(line)
                source = step.get("source")
                step_type = step.get("type")
                content = step.get("content", "")
                created_at = step.get("created_at", "")
                
                # Format timestamps a bit cleaner
                if created_at:
                    created_at = created_at.replace("T", " ").split(".")[0]
                
                if step_type == "USER_INPUT":
                    # Parse out USER_REQUEST block from content if present
                    user_req_match = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', content, re.DOTALL)
                    if user_req_match:
                        req_content = user_req_match.group(1).strip()
                    else:
                        req_content = content.strip()
                    
                    if req_content:
                        markdown.append(f"## 👤 User Request ({created_at})\n")
                        markdown.append(f"> {sanitize(req_content)}\n\n")
                        
                elif step_type == "PLANNER_RESPONSE":
                    if content:
                        markdown.append(f"### 🤖 Assistant Thought & Response\n")
                        markdown.append(f"{sanitize(content)}\n\n")
                        
                    tool_calls = step.get("tool_calls", [])
                    if tool_calls:
                        markdown.append("#### 🛠️ Tool Executions\n")
                        for tc in tool_calls:
                            name = tc.get("name")
                            args = tc.get("args", {})
                            args_str = json.dumps(args, indent=2)
                            markdown.append(f"- **Tool**: `{name}`\n")
                            markdown.append(f"  ```json\n{sanitize(args_str)}\n  ```\n")
                        markdown.append("\n")
                        
                elif step_type == "RUN_COMMAND":
                    markdown.append("#### 💻 Command Output\n")
                    markdown.append(f"```text\n{sanitize(content)}\n```\n\n")
                    
                elif step_type == "VIEW_FILE" or step_type == "REPLACE_FILE_CONTENT":
                    if len(content) > 1000:
                        trimmed = content[:1000] + "\n... [Content Truncated for Readability] ..."
                    else:
                        trimmed = content
                    markdown.append(f"#### 📄 File Action ({step_type})\n")
                    markdown.append(f"```text\n{sanitize(trimmed)}\n```\n\n")
                    
            except Exception as e:
                continue
                
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown))
    print(f"Log parsing completed. Written to {output_path}")

if __name__ == "__main__":
    main()
