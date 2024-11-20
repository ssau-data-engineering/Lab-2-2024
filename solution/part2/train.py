import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
import argparse
import os

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)  
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs, log_file_path):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / total
        epoch_accuracy = correct / total
        val_loss, val_accuracy = evaluate_model(model, val_loader, criterion, device)
        
        with open(log_file_path, 'a') as f:
            f.write(f"Epoch {epoch + 1}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.4f}, "
                    f"Val_Loss: {val_loss:.4f}, Val_Accuracy: {val_accuracy:.4f}\n")
        print(f"Epoch {epoch + 1}: Loss={epoch_loss:.4f}, Accuracy={epoch_accuracy:.4f}, "
              f"Val_Loss={val_loss:.4f}, Val_Accuracy={val_accuracy:.4f}")


def evaluate_model(model, data_loader, criterion, device):
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in data_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            test_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
    return test_loss / total, correct / total


def main(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    train_val_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    train_size = int(0.8 * len(train_val_dataset))
    val_size = len(train_val_dataset) - train_size
    train_dataset, val_dataset = random_split(train_val_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

    os.makedirs(os.path.dirname(args.log_file), exist_ok=True)

    train_model(model, train_loader, val_loader, criterion, optimizer, device, args.epochs, args.log_file)
    
    test_loss, test_accuracy = evaluate_model(model, test_loader, criterion, device)
    print(f"\nТочность на тестовом наборе: {test_accuracy:.4f}")
    with open(args.log_file, 'a') as f:
        f.write(f"\nTest Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a simple CNN on MNIST with PyTorch and save logs.")
    parser.add_argument('--epochs', type=int, default=5, help='Number of epochs to train the model.')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size for training.')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate for optimizer.')
    parser.add_argument('--log_file', type=str, default="logs/training_logs.txt", help='Path to save training logs.')

    args = parser.parse_args()
    main(args)    
