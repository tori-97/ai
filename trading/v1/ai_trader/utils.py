import random, os

def get_random_data_sample(data):
    train_rand_range = random.uniform(0, 1)
    data_sample = data.sample(int(len(data) * train_rand_range))
    data_sample_len = len(data_sample)

    return data_sample, data_sample_len

def get_random_data_sample_without_shuffle(data, range):
    train_rand_range = range
    data_sample = data.iloc[0:int(len(data) * train_rand_range)]
    data_sample_len = len(data_sample)

    return data_sample, data_sample_len

def reset_trader():

    model_path = os.path.join(os.getcwd(), "ai_trader/data/model")

    data = os.listdir(model_path)

    for f in data:
        fpath = os.path.join(model_path, f)
        os.remove(fpath)
   
    print("[+] Trader reseted !!")