from accelerate import infer_auto_device_map, init_empty_weights
from transformers import AutoConfig, AutoModelForCausalLM

config = AutoConfig.from_pretrained("Qwen/CodeQwen1.5-7B-Chat-AWQ")
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(config)

device_map = infer_auto_device_map(model, no_split_module_classes=["OPTDecoderLayer"])

print(device_map)