def display_tool_interaction(messages):
    """Display tool calls and their responses in a clean format"""
    tool_calls = []
    tool_responses = []

    for message in messages:
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append({
                    'function': tool_call['name'],
                    'args': tool_call['args'],
                    'id': tool_call['id']
                })
        elif hasattr(message, 'tool_call_id') and message.tool_call_id:
            tool_responses.append({
                'id': message.tool_call_id,
                'content': message.content,
                'tool_name': getattr(message, 'name', 'Unknown')
            })

    if tool_calls:
        print("\n🔧 Tool Interactions:")
        for i, (call, response) in enumerate(zip(tool_calls, tool_responses), 1):
            print(f"  {i}. Called: {call['function']}({call['args']})")
            print(f"     Response: {response['content']}")
        print()
