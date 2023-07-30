import os
import platform
from subprocess import run
from langchain.llms import LlamaCpp
from langchain import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from rich.prompt import Prompt
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.console import Group
from rich.align import Align
from rich import box
from rich.markdown import Markdown

console = Console()
def check_for_model():
    url = "https://huggingface.co/localmodels/Llama-2-7B-Chat-ggml/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin"
    path = 'llama-2-7b-chat.ggmlv3.q4_0.bin'
    isExist = os.path.exists(path)
    if isExist == True:
        pass
    elif isExist == False:
        run(f"wget {url}", shell=True)
        pass

check_for_model()
template = """persona: {persona}
You are a helpful, respectful and honest cybersecurity analyst.
Being a security analyst you must scrutanize the details provided to ensure
it is usable for penitration testing. Please ensure that your responses are
socially unbiased and positive in nature. If a question does not make any
sense, or is not factually coherent, explain why instead of answering
something not correct. If you don't know the answer to a question,
please don't share false information.
keep your answers in english and do not divert from the question.
If the answer to the asked question or query is complete end your answering
keep the answering accurate and do not skip details related to the query.
Give your output in markdown format.
"""
prompt = PromptTemplate(template=template, input_variables=["persona"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="llama-2-7b-chat.ggmlv3.q4_0.bin",
    input={"temperature": 0.75, "max_length": 2000, "top_p": 1},
    callback_manager=callback_manager,
    max_tokens=2000,
    n_batch=1000,
    n_gpu_layers=50,
    verbose=False,
    n_ctx=3500,
    streaming=False,
)

def clearscr() -> None:
    try:
        osp = platform.system()
        match osp:
            case 'Darwin':
                os.system("clear")
            case 'Linux':
                os.system("clear")
            case 'Windows':
                os.system("cls")
    except Exception:
        pass

def Print_AI_out(prompt) -> Panel:
    ai_out = Markdown(llm(prompt))
    message_panel = Panel(
            Align.center(
                Group("\n", Align.center(ai_out)),
                vertical="middle",
            ),
            box=box.ROUNDED,
            padding=(1, 2),
            title="[b red]The HackBot AI output",
            border_style="bright_blue",
        )
    return message_panel


def main():
    clearscr()
    banner = """
     _   _            _    ____        _   
    | | | | __ _  ___| | _| __ )  ___ | |_ 
    | |_| |/ _` |/ __| |/ /  _ \ / _ \| __| By: Morpheuslord
    |  _  | (_| | (__|   <| |_) | (_) | |_  AI used: Meta-LLama2
    |_| |_|\__,_|\___|_|\_\____/ \___/ \__|
    """
    console.print(Panel(Markdown(banner)), style="bold green")
    while True:
        try:
            pro_in = Prompt.ask('> ')
            if pro_in == 'quit_bot':
                quit()
            elif pro_in == 'clear_screen':
                clearscr()
                pass
            else:
                prompt = pro_in
                print(Print_AI_out(prompt))
                pass
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()