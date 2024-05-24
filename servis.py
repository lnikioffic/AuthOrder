import torch
from pathlib import Path


BASE_FOLDER_DATA = Path.cwd() / 'data'

UPLOAD_FOLDER = Path.cwd() / 'data' / 'video'
UPLOAD_FOLDER_TESTING = Path.cwd() / 'data' / 'video-test'
# UPLOAD_FOLDER = os.path.abspath('data/video')
# UPLOAD_FOLDER_TESTING = os.path.abspath('data/video-test')
DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50  # 50 megabytes

DEVICE = 'cpu'
if torch.cuda.is_available():
  print('Using GPU')
  DEVICE = 'cuda'
else:
  print('CUDA not available. Please connect to a GPU instance if possible.')
  DEVICE = 'cpu'
