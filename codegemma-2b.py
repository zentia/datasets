from transformers import GemmaTokenizer, AutoModelForCausalLM

tokenizer = GemmaTokenizer.from_pretrained("google/codegemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/codegemma-2b")

input_text = '''
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
'''
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids,max_length=1024*5)
print(tokenizer.decode(outputs[0]))
