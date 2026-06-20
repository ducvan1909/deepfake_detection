import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

QUANTITY_PER_CLASS = 200
OUTPUT_DIR = Path("dataset/Asvspoof_mini")
AUDIO_DIR = OUTPUT_DIR / "audio"
METADATA_PATH = OUTPUT_DIR / "metadata.csv"


def label_of(key):
    if isinstance(key, str):
        return "bonafide" if key.lower() in {"0", "bonafide"} else "spoof"
    return "bonafide" if key == 0 else "spoof"


def dataset_is_ready():
    if not METADATA_PATH.exists():
        return False

    with METADATA_PATH.open("r", encoding="utf-8", newline="") as file:
        return sum(1 for _ in csv.DictReader(file)) == QUANTITY_PER_CLASS * 2


def main():
    if dataset_is_ready():
        print(f"Dataset đã tồn tại ở: {OUTPUT_DIR.resolve()}")
        return

    # Chỉ import Hugging Face khi thực sự cần tải dữ liệu.
    from datasets import Audio, load_dataset

    stream = load_dataset(
        "Bisher/ASVspoof_2019_LA",
        split="train",
        streaming=True,
    )
    # Không giải mã audio, nhờ đó không cần torch/torchcodec.
    stream = stream.cast_column("audio", Audio(decode=False))

    counts = {"bonafide": 0, "spoof": 0}
    metadata = []

    iterator = iter(stream)
    try:
        for row in iterator:
            label = label_of(row["key"])
            if counts[label] >= QUANTITY_PER_CLASS:
                continue

            audio = row["audio"]
            audio_bytes = audio.get("bytes")
            if audio_bytes is None:
                raise RuntimeError(
                    "Mẫu audio không chứa bytes. Hãy cập nhật datasets va huggingface_hub."
                )

            source_path = audio.get("path") or ""
            suffix = Path(source_path).suffix or ".flac"
            file_name = f'{row["audio_file_name"]}{suffix}'
            relative_path = Path("audio") / label / file_name
            output_path = OUTPUT_DIR / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_bytes)

            metadata.append(
                {
                    "audio": relative_path.as_posix(),
                    "label": label,
                    "speaker_id": row["speaker_id"],
                    "system_id": row["system_id"],
                }
            )
            counts[label] += 1
            print(
                f'\rbonafide: {counts["bonafide"]}/{QUANTITY_PER_CLASS} | '
                f'spoof: {counts["spoof"]}/{QUANTITY_PER_CLASS}',
                end="",
            )

            if all(count == QUANTITY_PER_CLASS for count in counts.values()):
                break
    finally:
        close = getattr(iterator, "close", None)
        if close is not None:
            close()

    if not all(count == QUANTITY_PER_CLASS for count in counts.values()):
        raise RuntimeError(f"Không lấy đủ mẫu: {counts}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with METADATA_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["audio", "label", "speaker_id", "system_id"],
        )
        writer.writeheader()
        writer.writerows(metadata)

    print(f"\nĐã lưu {len(metadata)} mẫu tại: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
