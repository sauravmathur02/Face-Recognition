DB_PATH = "faces.db"

MODEL_NAME = "buffalo_sc"

# SIMILARITY_THRESHOLD: Cosine similarity cutoff (L2-normalized dot product × 100).
# InsightFace buffalo_sc: same-person cosine similarity typically ranges 0.65–0.85.
# Different-person similarity typically ranges 0.15–0.45.
# 89% is the interviewer-specified default. It is conservative — minimizes false accepts
# at the cost of potentially rejecting valid users in poor lighting or with accessories.
# This value is overridable at runtime via the Settings UI slider without touching this file.
SIMILARITY_THRESHOLD = 89
EMBEDDING_DIM        = 512
MIN_FACE_AREA        = 4000
MIN_DET_SCORE        = 0.60
MIN_REG_IMAGES       = 3
BLUR_THRESHOLD       = 100

CAMERA_ID = 0

REGISTRATIONS_DIR = "data/registrations"

LOG_LEVEL  = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
