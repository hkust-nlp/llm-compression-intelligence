import torch
from torch.utils.data import DataLoader
import argparse
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)
from packed_dataset import EvalDataset
import numpy as np
from tqdm import tqdm

def cross_entropy(
    logits, targets, attention_mask: torch.Tensor = None
):

    logits = logits.reshape(-1, logits.size(-1))
    targets = targets.reshape(-1)
    if attention_mask is not None:
        attention_mask = attention_mask.reshape(-1)
        targets = targets.masked_fill(~attention_mask, -1)

    return torch.nn.functional.cross_entropy(logits, targets, ignore_index=-1, reduction='sum')



@torch.no_grad()
def validate(args, model, val_dataloader: DataLoader, device):
    model.eval()
    losses = []
    for k, (val_data, attention_mask) in enumerate(tqdm(val_dataloader)):
        input_ids = val_data[:, 0: args.block_size].contiguous().to(device)
        targets = val_data[:, 1: args.block_size + 1].contiguous().long().to(device)
        attention_mask = attention_mask[:, 1: args.block_size + 1].contiguous().to(device)
        logits = model(input_ids).logits
        loss = cross_entropy(logits, targets, attention_mask=attention_mask)
        loss = loss.cpu().item()
        losses.append(loss)
        print("%.8f" % loss)

    out = np.array(losses).sum()
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task_name",
        type=str,
    )
    parser.add_argument(
        "--model_name",
        type=str
    )
    parser.add_argument(
        '--block_size',
        type=int,
        default=1900,
    )
    parser.add_argument(
        '--stride',
        type=int,
        default=512,
    )
    parser.add_argument(
        '--batch_size',
        type=int
    )
    parser.add_argument(
        '--file_num',
        default=-1,
        type=int
    )
    parser.add_argument(
        '--flash',
        action="store_true",
        help="set this if you want to use flash attention",
    )
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--cache_dir", type=str, default=None)

    args = parser.parse_args()
    print(args)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name,
        use_fast=True if ("llemma" in args.model_name) or ("mpt" in args.model_name) else False,
        cache_dir=args.cache_dir,
        trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        cache_dir=args.cache_dir,
        trust_remote_code=True,
        use_flash_attention_2=True if args.flash and "mpt" not in args.model_name else False
    )

    valdataset = EvalDataset(
        args=args,
        task_name=args.task_name,
        block_size=args.block_size + 1,
        tokenizer=tokenizer,
        stride=args.stride,
        vocab_size=tokenizer.vocab_size,
        file_num=args.file_num
    )
    valdataloader = DataLoader(valdataset, batch_size=args.batch_size, shuffle=False)
    total_loss = validate(args, model, valdataloader, device)
    print("-"*10, "Result", "-"*10)
    print("Total loss:", total_loss)
    print("Character num:", valdataset.character_num)
    print("BPC:", total_loss / (valdataset.character_num * np.log(2)) )

    print("finished")


if __name__ == "__main__":
    main()
