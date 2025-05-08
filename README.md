# H?c m�y v� Khai th�c d? li?u n�ng cao

# 1. Th�nh vi�n nh�m v� ph�n c�ng c�ng vi?c

| H? v� t�n               | MSSV      | Ph�n c�ng c�ng vi?c                                                 |
|-------------------------|-----------|---------------------------------------------------------------------|
| H� Thanh H��ng          | 23007944  | - T?u h?<br>- T?u h?<br>- T?u h? |
| Nguy?n Th? Minh Ph�?ng  | 23007937  | - T?u h?<br>- T?u h?<br>- T?u h? |
| L? �?c Trung            | 23007933  | - T?u h?<br>- T?u h?<br>- T?u h? |
| Nguy?n Th? Ng?c Uy�n    | 23007930  | - T?u h?<br>- T?u h?<br>- T?u h? |


# 2. H�?ng d?n v? c�ch t? ch?c v� th?c nghi?m ch��ng tr?nh

## 2.1. Y�u c?u v? ph?n c?ng

### 2.1.1. CPU (cho Spark v� x? l? d? li?u)
- S? l?i: T?i thi?u 4 l?i v?t l? (n�n c� 8 lu?ng tr? l�n)
- T?c �? xung nh?p: 2.5 GHz ho?c nhanh h�n

### 2.1.2. RAM
- T?i thi?u: 16 GB (Spark v� vi?c token h�a T5 c?n nhi?u b? nh?)
- Khuy?n ngh?: 32 GB �? x? l? m�?t m� h�n

### 2.1.3. GPU (cho vi?c hu?n luy?n v� sinh ti�u �? b?ng m� h?nh T5)

**T?i thi?u:**
- GPU: NVIDIA v?i �t nh?t 8 GB VRAM (v� d?: NVIDIA RTX 3060, Quadro RTX 4000, ho?c Tesla T4)
- CUDA Compute Capability: T? 7.0 tr? l�n

**Khuy?n ngh?:**
- GPU: T? 12 GB VRAM tr? l�n (v� d?: RTX 3080, A6000, ho?c t��ng ���ng)


### 2.1.4. B? nh? l�u tr?
- SSD v?i �t nh?t **50 GB** dung l�?ng tr?ng

## 2.2. Y�u c?u v? h? �i?u h�nh

- Linux: Ubuntu 20.04 tr? l�n (�u ti�n do h? tr? CUDA t?t) ()
- Windows 10+

## 2.3. Y�u c?u v? ph?n m?m

### 2.3.1. Ph?n m?m

- CUDA: 12.4 (kh?p v?i Torch 2.7.0)
- cuDNN: Ph� h?p v?i CUDA 12.4
- Driver GPU: NVIDIA Driver phi�n b?n >= 550.x


### 2.3.2. C�c th� vi?n Python

- Python 3.12
- pyspark 3.5.5
- transformers 4.51.3
- torch 2.7.0
- mlflow 2.22.0
- sacrebleu 2.5.1
- rouge 1.0.1
- accelerate 1.6.0
- hf_xet 1.1.0

# 3. H�?ng d?n c�i �?t

**`H�?ng d?n c�i �?t s? cho h? �i?u h�nh Ubuntu 20.04`**

## 3.1. �?m b?o y�u c?u v? ph?n c?ng v� h? �i?u h�nh t?i b�?c n�y


## 3.2. C?p nh?t cho h? �i?u h�nh

M? Terminal ch?y d?ng code sau

```bash
sudo apt update && sudo apt upgrade
```


---

### 1. ?? Download Data

```bash
mkdir data
cd data
wget https://huggingface.co/datasets/CShorten/ML-ArXiv-Papers/resolve/main/ML-Arxiv-Papers.csv
cd ..
```

### 2. ??? Set Up Environment

```bash
conda create -n title python=3.12
conda activate title
```

### 3. ?? Install Dependencies

```bash
pip install -r requirements.txt
```

If using CUDA 12.4, ensure you install PyTorch with the appropriate version:

```bash
pip install torch 2.3.0+cu124 -f https://download.pytorch.org/whl/torch_stable.html
```


## ?? Track Experiments with MLflow

### Start MLflow UI

```bash
mlflow ui --port 5000
```

Access the MLflow dashboard at: `http:/localhost:5000`


## ????? Run Training

### Train the Model

```bash
python main.py
```

You can monitor training progress live via the MLflow UI.

### Keep track of training process on MLFlow at 
http://localhost:5000