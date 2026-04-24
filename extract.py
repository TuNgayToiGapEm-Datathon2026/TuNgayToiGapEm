import subprocess
import sys

docx_file = "Vòng 1 — Phân tích đề & Brainstorm (team brief).docx"
try:
    subprocess.run(['textutil', '-convert', 'txt', docx_file], check=True)
    print("Successfully converted docx to txt")
except Exception as e:
    print(f"Error: {e}")
