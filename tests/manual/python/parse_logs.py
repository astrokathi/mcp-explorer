import json
import re
from pathlib import Path

def sanitize(text):
    if not text:
        return ""
    # Case insensitive replacement of Nike with MCP
    text = re.sub(r'(?i)nike', 'MCP', text)
    return text

def get_language(filename):
    if not filename:
        return ""
    filename = filename.lower()
    if filename.endswith(".py"):
        return "python"
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        return "yaml"
    if filename.endswith(".json"):
        return "json"
    if filename.endswith(".sh"):
        return "bash"
    if filename.endswith(".md"):
        return "markdown"
    if filename.endswith(".toml"):
        return "toml"
    if filename.endswith(".js"):
        return "javascript"
    if filename.endswith(".html"):
        return "html"
    return ""

def format_tool_call(name, args):
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except:
            pass
            
    if not isinstance(args, dict):
        return f"- **Tool**: `{name}`\n  ```text\n{args}\n  ```\n"

    lines = []
    
    if name == "write_to_file":
        target = args.get("TargetFile", "").strip('"')
        desc = args.get("Description", "").strip('"')
        content = args.get("CodeContent", "")
        
        if isinstance(content, str):
            if content.startswith('"') and content.endswith('"'):
                try:
                    content = json.loads(content)
                except:
                    content = content[1:-1]
        
        lines.append(f"- **Tool**: `write_to_file` 📄\n")
        if target:
            lines.append(f"  - **Target File**: `{target}`\n")
        if desc:
            lines.append(f"  - **Description**: {desc}\n")
        if content:
            lang = get_language(target)
            lines.append(f"  - **File Content**:\n")
            lines.append(f"    ```{lang}\n{content.strip()}\n    ```\n")
            
    elif name in ("replace_file_content", "multi_replace_file_content"):
        target = args.get("TargetFile", "").strip('"')
        desc = args.get("Description", "").strip('"')
        lines.append(f"- **Tool**: `{name}` ✏️\n")
        if target:
            lines.append(f"  - **Target File**: `{target}`\n")
        if desc:
            lines.append(f"  - **Description**: {desc}\n")
            
        if name == "replace_file_content":
            target_content = args.get("TargetContent", "")
            repl_content = args.get("ReplacementContent", "")
            
            if isinstance(target_content, str):
                if target_content.startswith('"') and target_content.endswith('"'):
                    try: target_content = json.loads(target_content)
                    except: target_content = target_content[1:-1]
            if isinstance(repl_content, str):
                if repl_content.startswith('"') and repl_content.endswith('"'):
                    try: repl_content = json.loads(repl_content)
                    except: repl_content = repl_content[1:-1]
                
            lang = get_language(target)
            if target_content:
                lines.append(f"  - **Target Content**:\n    ```{lang}\n{target_content.strip()}\n    ```\n")
            if repl_content:
                lines.append(f"  - **Replacement Content**:\n    ```{lang}\n{repl_content.strip()}\n    ```\n")
        else:
            chunks = args.get("ReplacementChunks", [])
            if isinstance(chunks, str):
                try: chunks = json.loads(chunks)
                except: pass
            if isinstance(chunks, list):
                lines.append(f"  - **Replacement Chunks**:\n")
                lang = get_language(target)
                for i, chunk in enumerate(chunks):
                    tc = chunk.get("TargetContent", "")
                    rc = chunk.get("ReplacementContent", "")
                    if isinstance(tc, str) and tc.startswith('"') and tc.endswith('"'):
                        try: tc = json.loads(tc)
                        except: tc = tc[1:-1]
                    if isinstance(rc, str) and rc.startswith('"') and rc.endswith('"'):
                        try: rc = json.loads(rc)
                        except: rc = rc[1:-1]
                    
                    lines.append(f"    - **Chunk {i+1}**:\n")
                    if tc:
                        lines.append(f"      - *Target*:\n        ```{lang}\n{tc.strip()}\n        ```\n")
                    if rc:
                        lines.append(f"      - *Replacement*:\n        ```{lang}\n{rc.strip()}\n        ```\n")
                        
    elif name == "run_command":
        cmd = args.get("CommandLine", "").strip('"')
        cwd = args.get("Cwd", "").strip('"')
        
        if isinstance(cmd, str):
            if cmd.startswith('"') and cmd.endswith('"'):
                try: cmd = json.loads(cmd)
                except: cmd = cmd[1:-1]
                
        lines.append(f"- **Tool**: `run_command` 💻\n")
        if cwd:
            lines.append(f"  - **Directory**: `{cwd}`\n")
        if cmd:
            lines.append(f"  - **Command**:\n    ```bash\n{cmd}\n    ```\n")
            
    else:
        lines.append(f"- **Tool**: `{name}`\n")
        for k, v in args.items():
            if isinstance(v, str) and ("\n" in v or len(v) > 80):
                if v.startswith('"') and v.endswith('"'):
                    try: v = json.loads(v)
                    except: pass
                lines.append(f"  - **{k}**:\n    ```text\n{v.strip()}\n    ```\n")
            else:
                lines.append(f"  - **{k}**: `{v}`\n")
                
    return "".join(lines)

def main():
    log_path = Path("/Users/kathi.s/.gemini/antigravity/brain/a7dd681c-7ee8-4f02-8fa7-224242ec388f/.system_generated/logs/transcript.jsonl")
    output_path = Path("/Users/kathi.s/NKExplorer/Nike_Explorer/docs-md/session_history.md")
    
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
                
                if created_at:
                    created_at = created_at.replace("T", " ").split(".")[0]
                
                if step_type == "USER_INPUT":
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
                            formatted = format_tool_call(name, args)
                            markdown.append(sanitize(formatted))
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
