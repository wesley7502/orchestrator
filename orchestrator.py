import re
import argparse
from string import punctuation
import time
import torch
import yaml
import numpy as np
from torch.utils.data import DataLoader
from g2p_en import G2p
from pypinyin import pinyin, Style
from os import listdir
from os.path import isfile, join
from playsound import playsound
from utils.model import get_model, get_vocoder
from utils.tools import to_device, synth_samples
from text import text_to_sequence
import matplotlib.pyplot as plt
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
time1 = time.time()
def read_lexicon(lex_path):
    lexicon = {}
    with open(lex_path) as f:
        for line in f:
            temp = re.split(r"\s+", line.strip("\n"))
            word = temp[0]
            phones = temp[1:]
            if word.lower() not in lexicon:
                lexicon[word.lower()] = phones
    return lexicon


def preprocess_english(text, preprocess_config):
    text = text.rstrip(punctuation)
    lexicon = read_lexicon(preprocess_config["path"]["lexicon_path"])
    g2p = G2p()
    phones = []
    words = re.split(r"([,;.\-\?\!\s+])", text)
    for w in words:
        if w.lower() in lexicon:
            phones += lexicon[w.lower()]
        else:
            phones += list(filter(lambda p: p != " ", g2p(w)))
    phones = "{" + "}{".join(phones) + "}"
    phones = re.sub(r"\{[^\w\s]?\}", "{sp}", phones)
    phones = phones.replace("}{", " ")
    # print("Raw Text Sequence: {}".format(text))
    # print("Phoneme Sequence: {}".format(phones))
    sequence = np.array(
        text_to_sequence(
            phones, preprocess_config["preprocessing"]["text"]["text_cleaners"]
        )
    )
    return np.array(sequence)

def synthesize(model, step, configs, vocoder, batchs, control_values, i):
    preprocess_config, model_config, train_config = configs
    pitch_control, energy_control, duration_control = control_values

    for batch in batchs:
        batch = to_device(batch, device)
        with torch.no_grad():
            # Forward
            output = model(
                *(batch[2:]),
                p_control=pitch_control,
                e_control=energy_control,
                d_control=duration_control
            )
            synth_samples(
                batch,
                output,
                vocoder,
                model_config,
                preprocess_config,
                train_config["path"]["result_path"],
                i
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore_step", type=int, default=900000)
    parser.add_argument(
        "--mode",
        type=str,
        choices=["batch", "single"],
        help="Synthesize a whole dataset or a single sentence",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="path to a source file with format like train.txt and val.txt, for batch mode only",
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="raw text to synthesize, for single-sentence mode only",
    )
    parser.add_argument(
        "--speaker_id",
        type=int,
        default=0,
        help="speaker ID for multi-speaker synthesis, for single-sentence mode only",
    )
    parser.add_argument(
        "-p",
        "--preprocess_config",
        type=str,
        help="path to preprocess.yaml",
    )
    parser.add_argument(
        "-m", "--model_config", type=str, help="path to model.yaml"
    )
    parser.add_argument(
        "-t", "--train_config", type=str, help="path to train.yaml"
    )
    parser.add_argument(
        "--pitch_control",
        type=float,
        default=1.0,
        help="control the pitch of the whole utterance, larger value for higher pitch",
    )
    parser.add_argument(
        "--energy_control",
        type=float,
        default=1.0,
        help="control the energy of the whole utterance, larger value for larger volume",
    )
    parser.add_argument(
        "--duration_control",
        type=float,
        default=1.0,
        help="control the speed of the whole utterance, larger value for slower speaking rate",
    )
    args = parser.parse_args()

    # Check source texts
    if args.mode == "batch":
        assert args.source is not None and args.text is None
    if args.mode == "single":
        assert args.source is None and args.text is not None

    # Read Config
    preprocess_config = yaml.load(
        open('config/LJSpeech/preprocess.yaml', "r"), Loader=yaml.FullLoader
    )
    model_config = yaml.load(open('config/LJSpeech/model.yaml', "r"), Loader=yaml.FullLoader)
    train_config = yaml.load(open('config/LJSpeech/train.yaml', "r"), Loader=yaml.FullLoader)
    configs = (preprocess_config, model_config, train_config)

    # Get model
    model = get_model(args, configs, device, train=False)
    vocoder = get_vocoder(model_config, device)
    text = 'one. one one. one one one. one one one one. one one one one one. one one one one one one. one one one one one one one. one one one one one one one one. one one one one one one one one one. one one one one one one one one one one'
    latency = []
    outlength = []
    text = text.split('.')
    text_embeddings = [np.array([preprocess_english(t, preprocess_config)]) for t in text]
    i = 0
    time2 = time.time()
    print(f"preprocess took {time2-time1} sec")
    while i < len(text):
        duration_control = 1 #<-- adjust this in run time
        ids = text[i]
        raw_texts = text[i]
        speakers = np.array([0])
        text_embedding = text_embeddings[i]
        text_lens = np.array([len(text_embedding[0])])
        batchs = [(ids, raw_texts, speakers, text_embedding, text_lens, max(text_lens))]
        control_values = 1, 1, duration_control
        synthesize(model, args.restore_step, configs, vocoder, batchs, control_values, i)
        time3 = time.time()
        print(f"synthesis {i+1}th took {time3-time2} sec")
        latency.append(round(time3-time2, 2))
        f = './output/result/LJSpeech' + '/' + str(i) + '.wav'
        playsound(f) # this is blocking, aka working as intended
        time4 = time.time()
        outlength.append(round(time4-time3, 2))
        print(f"play {i+1}th took {time4-time3} sec")
        time2 = time4
        i += 1
    plt.plot(latency, label='Synthesizer')
    plt.plot(outlength, label='Audio')
    plt.xlabel("Input length")
    plt.ylabel("Time (s)")
    plt.xticks(np.arange(len(latency)), np.arange(1, len(latency)+1))
    plt.legend(loc='best')
    plt.savefig('fig2.png')
