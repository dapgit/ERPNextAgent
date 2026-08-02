'''import google.antigravity as ag 
print(ag.__file__) 
print(dir(ag)) 
exit()'''

'''from google.antigravity import Agent
help(Agent)'''

'''from google.antigravity import LocalAgentConfig
help(LocalAgentConfig)'''

'''from google.antigravity import Agent, LocalAgentConfig
import inspect

print(inspect.signature(Agent))

print("_" * 60)

print(inspect.signature(LocalAgentConfig))'''

from google.antigravity import Agent
print([m for m in dir(Agent) if not m.startswith("__")])