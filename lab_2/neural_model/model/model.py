import os
import argparse
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import timm
from torchvision.transforms import transforms
import numpy as np
from tqdm import tqdm

class CustomDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        
        self.data_dir = data_dir
        self.transform = transform
        self.classes = sorted(os.listdir(data_dir))
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
        
        self.images = []
        self.labels = []
        
        # Сбор путей ко всем изображениям и их меток
        for class_name in self.classes:
            class_dir = os.path.join(data_dir, class_name)
            class_idx = self.class_to_idx[class_name]
            
            for img_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, img_name)
                if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.images.append(img_path)
                    self.labels.append(class_idx)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Загрузка и преобразование изображения
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
            
        return image, label

def train_epoch(model, train_loader, criterion, optimizer, device):
    """Функция для обучения одной эпохи"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in tqdm(train_loader, desc='Training'):
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    epoch_loss = running_loss / len(train_loader)
    accuracy = 100. * correct / total
    return epoch_loss, accuracy

def validate(model, val_loader, criterion, device):
    """Функция для валидации модели"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in tqdm(val_loader, desc='Validation'):
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    val_loss = running_loss / len(val_loader)
    accuracy = 100. * correct / total
    return val_loss, accuracy

def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Training script for image classification')
    
    # Пути к данным
    parser.add_argument('--train-dir', type=str, default='./dataset/train',
                        help='path to training directory')
    parser.add_argument('--val-dir', type=str, default='./dataset/test',
                        help='path to validation directory')
    
    # Параметры обучения
    parser.add_argument('--batch-size', type=int, default=8,
                        help='batch size for training (default: 16)')
    parser.add_argument('--epochs', type=int, default=5,
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='learning rate (default: 0.001)')
    
    # Параметры модели
    parser.add_argument('--model-name', type=str, default='convnextv2_tiny.fcmae_ft_in1k',
                        help='name of the model from timm (default: convnextv2_tiny.fcmae_ft_in1k)')
    parser.add_argument('--num-workers', type=int, default=8,
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='device to use for training (default: cuda if available, else cpu)')
    parser.add_argument('--output-dir', type=str, default='./checkpoints',
                        help='directory to save model checkpoints (default: ./checkpoints)')
    
    return parser.parse_args()

def main():
    # Получение аргументов
    args = parse_args()
    
    # Создание директории для сохранения моделей
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Открытие файла для логирования
    log_file_path = os.path.join(args.output_dir, 'training_logs.txt')
    with open(log_file_path, 'w') as log_file:
        # Установка устройства
        device = torch.device(args.device)
        print(f'Using device: {device}')
        log_file.write(f'Using device: {device}\n')
        
        # Создание и настройка модели
        model = timm.create_model(args.model_name, pretrained=True)
        num_classes = len(os.listdir(args.train_dir))
        model.reset_classifier(num_classes=num_classes)
        model = model.to(device)
        
        # Получение преобразований для изображений
        data_config = timm.data.resolve_model_data_config(model)
        transforms_train = timm.data.create_transform(**data_config, is_training=True)
        transforms_val = timm.data.create_transform(**data_config, is_training=False)
        
        # Создание датасетов и загрузчиков данных
        train_dataset = CustomDataset(args.train_dir, transform=transforms_train)
        val_dataset = CustomDataset(args.val_dir, transform=transforms_val)
        
        train_loader = DataLoader(train_dataset, batch_size=args.batch_size, 
                                shuffle=True, num_workers=args.num_workers)
        val_loader = DataLoader(val_dataset, batch_size=args.batch_size, 
                              shuffle=False, num_workers=args.num_workers)
        
        # Настройка функции потерь и оптимизатора
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=args.lr)
        
        # Обучение модели
        best_val_accuracy = 0.0
        for epoch in range(args.epochs):
            print(f'\nEpoch {epoch+1}/{args.epochs}')
            log_file.write(f'\nEpoch {epoch+1}/{args.epochs}\n')
            
            # Обучение
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            print(f'Training Loss: {train_loss:.4f}, Training Accuracy: {train_acc:.2f}%')
            log_file.write(f'Training Loss: {train_loss:.4f}, Training Accuracy: {train_acc:.2f}%\n')
            
            # Валидация
            val_loss, val_acc = validate(model, val_loader, criterion, device)
            print(f'Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_acc:.2f}%')
            log_file.write(f'Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_acc:.2f}%\n')
            
            # Сохранение лучшей модели
            if val_acc > best_val_accuracy:
                best_val_accuracy = val_acc
                checkpoint_path = os.path.join(args.output_dir, 'best_model.pth')
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_accuracy': val_acc,
                    'args': vars(args)
                }, checkpoint_path)
                print(f'Model saved with validation accuracy: {val_acc:.2f}%')
                log_file.write(f'Model saved with validation accuracy: {val_acc:.2f}%\n')


if __name__ == '__main__':
    main()