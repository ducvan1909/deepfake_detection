# Tải dữ liệu FaceForensics++

## Tải bằng script chính thức của FaceForensíc++

- Cài đặt các thư viện

```bash
pip install -r dataset/requirements.txt
```

- Tải dữ liệu
- Lưu ý: điều chỉnh --num_videos để lấy số lượng video mong muốn

```bash
python -m dataset.faceforensics_download_v4 --server EU2 ".\datasets\FaceForensics++" --d all --c c23 --t videos --num_videos 50 
```

# Tải dữ liệu AsvSpoof

- Tải dữ liệu

```bash
python -m dataset.asvspoof_download
```

- Lấy dữ liệu khi cần

```bash
import pandas as pd
from pathlib import Path

root = Path("dataset/Asvspoof_mini")
df = pd.read_csv(root / "metadata.csv")

for row in df.itertuples():
    audio_path = root / row.audio
    label = 0 if row.label == "bonafide" else 1

    print(audio_path, label)
```
