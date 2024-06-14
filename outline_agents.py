from autogen import ConversableAgent
import autogen
import json

"""
For a given topic generate a learning path using the LLM agents of autogen (openAI)
"""
def generate_learning_path(topic, llm_config):
    
    writer = autogen.AssistantAgent(
        name="Course Creator",
        system_message=f"You are an expert in {topic}."
        "Prepare a course outline in JSON format. Please provide the title of the course and the sections and subsections."
        "Make sure you cover all required topics in the course outline to effectively learn the topic for a course taker.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").find("Approved!") >= 0,
    )
    
    reply = writer.generate_reply(messages=[{"content": topic, "role": "user"}])
    
    reviewer = autogen.AssistantAgent(
        name="Reviewer",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message= "You are an expert in {topic}. Refer to the outline prepared by the writer LLM and review it."
                        "Please provide your reviews in bullet points. Make your reviews clear and concise."
                        "If you are satisfied with the outline, please provide the termination message `Approved!`.",
    )

    res = reviewer.initiate_chat(
        recipient=writer,
        message=topic,
        max_turns=2,
        summary_method="last_msg"
    )
    
    # Extract the JSON content from the chat history
    json_content = None
    for message in res.chat_history:
        if "{" in message['content'] and "}" in message['content']:
            json_content = message['content'].strip()
            break
    
    if json_content is None:
        raise ValueError("No JSON content found in chat history")

    # Debug print to inspect the JSON content
    print("Extracted JSON content:")
    print(json_content)

    # Convert to a structured JSON format
    course_data = json.loads(json_content)

    return course_data
