# pip install git+https://github.com/huggingface/transformers.git # TODO: merge PR to main
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "bigcode/starcoder2-3b"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

inputs = tokenizer.encode('''
Translation of the following code from C++ to Python
struct UnionFind {
std::vector parent, ranks;

explicit UnionFind(u64 size) {
parent = std::vector(size);
ranks = std::vector(size);
for (u64 i = 0; i < size; ++i) {
parent[i] = i;
ranks[i] = 1;
}
}

u64 find(u64 x) {
if (x != parent[x]) return parent[x] = find(parent[x]);
return x;
}

void link(u64 x, u64 y) {
x = find(x);
y = find(y);
if (x == y) return;
if (ranks[x] >= ranks[y]) {
parent[y] = x;
if (ranks[x] == ranks[y]) ++ranks[x];
} else {
parent[x] = y;
}
}
};
''', return_tensors="pt").to(device)
outputs = model.generate(inputs,max_length=1024)
response=tokenizer.decode(outputs[0])
print(response)
