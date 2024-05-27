from vllm import LLM
prompts = [
"""
Code Translator
Lua
---@class LordSkinMediatorClass : UIMediatorClass
local LordSkinMediatorClass = DeclareClass("LordSkinMediatorClass", ClassLib.UIMediatorClass)

function LordSkinMediatorClass:ctor()

end

function LordSkinMediatorClass:vGetBelongUIStateName()
    return {UIState.LordSkin}
end

function LordSkinMediatorClass:vOnUIStateIn(switchType, inStateName, userData)
    self:CreatePrefabClass(ClassLib.UILordSkinClass,userData)
end

function LordSkinMediatorClass:vOnUIStateOut(switchType, outStateName)
    if outStateName == UIState.LordSkin then
        self:DestroyAllPrefabClass()
    end
end
Typescript
""",
]

llm = LLM(model="Qwen/CodeQwen1.5-7B-Chat-AWQ",trust_remote_code=True,gpu_memory_utilization=0.9) 

outputs = llm.generate(prompts)
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(generated_text)