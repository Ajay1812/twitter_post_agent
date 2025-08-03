---
datetime: 2025-07-31 08:46
tags:
  - "#persistence"
  - langgraph
  - "#fault-tolerance"
---
---
Persistence in LangGraph refers to the ability to **save state and restore** the state of workflow **over time**

- Persistence not only store your **final state value** it can store **intermediate** state result also. 
- It provide **fault-tolerance**

##### CheckPointer in Persistence

- **checkpointer** will divide graph as a checkpoint and store each and every state at the moment in Database
- **SuperStep** -> Checkpoint

![[Agentic - Superstep and checkpointer]]

**Save final + intermediate state** values in a database

Use **thread_id** to  uniquely identify each and every checkpoint -> 

> [!example]
> When we build a chatbot like ChatGPT, suppose I talked about some topics today and then closed the browser. My chats are still saved — likely in some sort of database. So, they must assign some kind of ID to each conversation to manage that. Same thread concept in persistence 


#### References : 

[[Agentic AI using LangGraph]]

[[Benefits of Persistence]]

code -> https://github.com/Ajay1812/Learn-LangGraph/blob/main/05_ChatBots/02_persitence.ipynb