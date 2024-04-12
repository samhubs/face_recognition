import csv
from datetime import datetime
import os
from pathlib import Path
from torch.utils.data import Dataset
from torchvision import transforms

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from PIL import Image
from tqdm import tqdm


def export_predictions_to_csv(verification_filename, similarities):
    """Export list of predictions to formatted `.csv` file.

    Args:
        preds np.array: Similarity scores
        verification_filename str: file name with test verification pairs
    """
    if not os.path.exists("submissions"):
        os.mkdir("submissions/")
    file_name = f"submissions/submission_{datetime.now()}.csv"
    with open(file_name, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Id','Category'])
        with open(verification_filename, "r") as f:
            for line, sim in zip(f.readlines(), similarities):
                line = line.replace('\n', '')
                writer.writerow([line, sim])

    print(f"Wrote predictions to {file_name}")

class FlattenedDataset(Dataset):
    """Custom dataset class to deal with flattened folder structure.
    
    Normally we'd use torchvision.datasets.ImageFolder if it wasn't flattened.
    """
    def __init__(self, folder_path):
        self.folder_path = folder_path
        
        self.data, self.labels = self._load_images()
        
    def _load_images(self):
        image_files = Path(self.folder_path).glob("*.jpg")

        # Load image and transform to tensor 
        data = [transforms.ToTensor()(Image.open(f)) for f in image_files]
        
        # Get integer labels for images from filename
        labels = [int(f.stem.split("_")[0]) for f in image_files]
        
        return data, labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

class VerificationDataset(Dataset):
    def __init__(self, images_path, filename, test=False):
        self.test = test
        self.images_path = images_path
        with open(filename, "r") as f:
            self.data = [self._load_pair(line) for line in f.readlines()]

    def _load_pair(self, string):
        if not self.test:
            img1, img2, label = string.replace("\n", "").split(" ")
            label = torch.tensor(int(label))
            return (self._load_image(img1), self._load_image(img2), label)
        else:
            img1, img2 = string.replace("\n", "").split(" ")
            return (self._load_image(img1), self._load_image(img2), 0.)

    def _load_image(self, path):
        pil_img = Image.open(os.path.join(self.images_path, path))
        return transforms.ToTensor()(pil_img)

    def get_labels(self):
        return [i[2] for i in self.data]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


def plot_loss(losses, num_batches, num_epochs=10):
    plt.rcParams['savefig.facecolor'] = 'white'

    plt.plot(losses, label=f"Final Train Loss: {losses[-1]}")
    batches = np.arange(0, len(losses)+1, step=num_batches)
    plt.xticks(batches, np.arange(len(batches)))
    plt.ylabel("Loss Value Per Batch")
    plt.xlabel("Epoch #")
    plt.legend()
    plt.title(f"Loss value per batch during training")

def generate_predictions(model, dataloader, device):
    model.eval()
    similarities = []
    cosine_similarity = nn.CosineSimilarity()
    with torch.no_grad():
        for (batch_1, batch_2, _) in tqdm(dataloader, total=len(dataloader)):
            batch_1, batch_2 = batch_1.to(device), batch_2.to(device)
            _, features_1 = model(batch_1)
            _, features_2 = model(batch_2)
            batch_similarities = cosine_similarity(features_1, features_2)
            similarities.extend(batch_similarities.tolist())
    return similarities