# Tải dữ liệu FaceForensics++

## Cách 1: Tải bằng script chính thức của FaceForensíc++

- Cài đặt các thư viện

```bash
pip install -r dataset/requirements.txt
```

- Tải dữ liệu
- Lưu ý: điều chỉnh --num_videos để lấy số lượng video mong muốn

```bash
python -m dataset.faceforensics_download_v4 --server EU2 ".\datasets\FaceForensics++" --d all --c c23 --t videos --num_videos 50 
```