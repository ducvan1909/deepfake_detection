# Tải dữ liệu FaceForensics++

## Cách 1: Tải bằng script chính thức của FaceForensíc++

- Cài đặt các thư viện

```bash
pip install -r datasets/requirements.txt
```

-Tải dữ liệu

```bash
python -m datasets.faceforensics_download_v4 --server EU2 ".\datasets\FaceForensics++" --d all --c c23 --t videos --num_videos 50 
```