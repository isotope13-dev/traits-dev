from datasets import load_dataset
model = Model.from_pretrained("model", trust_remote_code=True)
data = load_dataset("dataset", trust_remote_code=True)
