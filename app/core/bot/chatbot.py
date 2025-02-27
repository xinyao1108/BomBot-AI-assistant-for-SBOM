import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory

import argparse

from app.core import spdx_analysis, cdx_analysis, db_interaction, util

dotenv.load_dotenv()

def prompt_template():

    system_msg = """You are an assistant knowledgeable about Software Bill Of Materials (SBOM).
    Each user will upload an SBOM to analyse and your task is it look at the SBOM, read and parse the dependencies and answer questions regarding that SBOM.
    Only answer questions regarding SBOMs, Software Supply Chain, and security concerns and vulnerabilities regarding those SBOMs.
    Strictly do not answer any other questions.

    You are going to answer questions according to this SBOM. Use this SBOM and direct it to the correct chat agent.
    {SBOM}                 
    """
    
    system_prompt = SystemMessagePromptTemplate.from_template(system_msg)
    human_prompt = HumanMessagePromptTemplate.from_template("{query}")
    prompt_template = ChatPromptTemplate.from_messages([
        system_prompt,
        MessagesPlaceholder(variable_name="history"),
        human_prompt,
        MessagesPlaceholder(variable_name="agent_scratchpad") 
    ])

    return prompt_template

def context_tools():
    
    t1 = Tool(
        name="Retrive_SBOM_Context_SPDX",
        func=spdx_analysis.retrive_SBOM_context,
        description="""This is useful when you have an SBOM in SPDX format.
                        You can send the whole sbom as a dict to this function and it will give context about that SBOM.
                        Use this context about the SBOM to answer the query asked by the human.
                    """
    )
    
    # t2 = Tool(
    #     name="Retrive_Package_Context_SPDX",
    #     func=spdx_analysis.retrive_package_context
    # )

    t3 = Tool(
        name="Retrive_SBOM_Context_CDX",
        func=cdx_analysis.retrive_SBOM_context,
        description="""This is useful when you have an SBOM in CDX format.
                        You can send the whole sbom as a dict to this function and it will give context about that SBOM.
                        Use this context about the SBOM to answer the query asked by the human.
                    """
    )

    # t4 = Tool(
    #     name="Retrive_Package_Context_CDX",
    #     func=cdx_analysis.retrive_package_context
    # )

    t5 = Tool(
        name="Retrive_SBOM_Context_From_SHA3",
        func=db_interaction.get_context_from_SHA3,
        description="""This is useful when the user provides a id to refrence the SBOM.
                        Send this id (SHA3 - hash) to the function and the function will use this id to get the context of the SBOM
                        which is stored in the database. Use this context about the SBOM to answer the query asked by the human.
                    """
    )

    context_tools = [t1, t3, t5]

    return context_tools

def chatbot():

    chat_model = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=None, timeout=None)

    history_memory = ConversationBufferMemory(memory_key="history", input_key="query", return_messages=True)

    agent_tools = context_tools()
    prompt = prompt_template()

    chat_agent = create_openai_functions_agent(
        llm=chat_model,
        tools=agent_tools,
        prompt=prompt
    )

    chatbot = AgentExecutor(
        agent=chat_agent,
        tools=agent_tools,
        memory=history_memory,
        return_intermediate_steps=True,
        verbose=True
    )

    return chatbot


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default="accelerate.spdx.json", type=str)
    args = parser.parse_args()

    filename = args.file

    sbom = util.json_to_dict(filename=filename)
    BOMBot = chatbot()

    end_conversation = False

    while not end_conversation:

        query = input("query (Type Q to quit): ")
        if query == "Q":
            end_conversation = True
            continue

        response = BOMBot.invoke({"SBOM": sbom, "query": query})
        print(response['output'])