from autogen import ConversableAgent
import autogen
import yaml

def generate_section_explanation(topic, section_topic, llm_config):
    writer = autogen.AssistantAgent(
        name="Course Creator",
        system_message=f"You are expert in the {topic} and you need to explain {section_topic} for an online mooc course."
        "Explain this topic which is easy to understand but don't hesitate to go in depth.",
        # "Your response should be in the YAML file format",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").find("Approved!") >= 0,
    )
    
    reply = writer.generate_reply(messages=[{"content": topic, "role": "user"}])
    
    reviewer = autogen.AssistantAgent(
        name="Reviewer",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message= "You are expert in the {topic} and need to review the online course section of topic {section_topic}."
                        "Refer the section content preapred by writer LLM and review it."
                        "Please provide your reviews in the bullet point. Make your reviews clear and concise."
                        "If you are satisfied with the outline, please provide the termination message `Approved!`.",
    )

    res = reviewer.initiate_chat(
        recipient=writer,
        message=topic,
        max_turns=2,
        summary_method="last_msg"
    )

    # print(f"res.chat_history: {res.chat_history}")
    # Extract the YAML content from the chat history
    for message in res.chat_history:
        if message['role'] == 'user':
            course_data = message['content'].strip()
    return course_data



def generate_section_mcq(topic, section_topic, explanation, llm_config):
    writer = autogen.AssistantAgent(
        name="Course Creator",
        system_message=f"You are expert in the {topic} and you need to create MCQs for the section {section_topic} which we have explained using this explanation summary: {explanation}"
        f"Create 2 to 3 MCQs which can test the knowledge of a course taker in this section: {section_topic}"
        "Please provide the options and correct answer, if required generate multiple options MCQs. Preapre your reseponse in YAML file format with this details: Question, options, answer, hint, explanation",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").find("Approved!") >= 0,
    )
    
    reply = writer.generate_reply(messages=[{"content": topic, "role": "user"}])
    
    reviewer = autogen.AssistantAgent(
        name="Reviewer",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message= "You are expert in the {topic} and need to review the MCQs preapred for the online course section of topic {section_topic}."
                        "Refer the section MCQs preapred by writer LLM and review it."
                        "Please provide your reviews in the bullet point. Make your reviews clear and concise."
                        "If you are satisfied with the outline, please provide the termination message `Approved!`.",
    )

    res = reviewer.initiate_chat(
        recipient=writer,
        message=topic,
        max_turns=2,
        summary_method="last_msg"
    )

    # Extract the YAML content from the chat history
    yaml_content = "N/A"
    for message in res.chat_history:
        if "yaml" in message['content']:
            yaml_content = message['content'].strip().lstrip("```yaml").rstrip("```")
            break
    # print("MCQs preapred: {yaml_content}")
    return yaml_content

def generate_section_code(topic, section_topic, section_content, llm_config):
    writer = autogen.AssistantAgent(
        name="Course Creator",
        system_message=f"You are expert in the {topic} and you need to write some sample codes examples to explain {section_topic} for an online mooc course."
        "Asses the section topic and if you feel code explanation is not required or is a simple intro topic then do not generate any code and provide `N/A` output"
        "As per the need generate maximum 2 code samples. Please provide code, explnations, and any important information to note from code. Provide output in Readme file fomrat",
        llm_config=llm_config,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").find("Approved!") >= 0,
    )
    
    reply = writer.generate_reply(messages=[{"content": topic, "role": "user"}])
    
    reviewer = autogen.AssistantAgent(
        name="Reviewer",
        llm_config=llm_config,
        human_input_mode="NEVER",
        system_message= "You are expert in the {topic} and need to review the code examples online course section of topic {section_topic}."
                        f"Refer the code examples preapred by writer LLM for the given section {section_topic} and review it."
                        "Please provide your reviews in the bullet point. Make your reviews clear and concise."
                        "If you are satisfied with the outline, please provide the termination message `Approved!`.",
    )

    res = reviewer.initiate_chat(
        recipient=writer,
        message=topic,
        max_turns=2,
        summary_method="last_msg"
    )

    # print(f"res.chat_history: {res.chat_history}")
    # Extract the YAML content from the chat history
    for message in res.chat_history:
        if message['role'] == 'user':
            code_data = message['content'].strip()
    print(f"code data: {code_data}")
    return code_data


def generate_course_content(topic, section_topic, llm_config):
    section_content = generate_section_explanation(topic, section_topic, llm_config)
    section_mcq = generate_section_mcq(topic, section_topic, section_content, llm_config)
    section_code = generate_section_code(topic, section_topic, section_content, llm_config)
    return section_content, section_mcq, section_code