# personal_kb_with_gpt

## Installation

```
pip install llama-index==0.7.0
pip install langchain==0.0.223
pip install gradio==3.35.2
pip install openai==0.27.7
```

## 遗留问题

### ServiceContext 的设置，是使用全局的，还是每次都创建？关键要弄清楚它是干什么的？

## MULTI_PROMPT_ROUTER_TEMPLATE prompt

Given a raw text input to a language model select the model prompt best suited for the input. You will be given the names of the available prompts and a description of what the prompt is best suited for. You may also revise the original input if you think that revising it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:

```json
{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input
}}
```

REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
physics: Good for answering questions about physics
math: Good for answering math questions

<< INPUT >>
{input}

<< OUTPUT >>
