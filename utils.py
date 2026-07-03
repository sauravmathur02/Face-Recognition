import logging

import numpy as np

from config import LOG_FORMAT, LOG_LEVEL

def normalize_embedding(embedding: np.ndarray) -> np.ndarray:

    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:

    return float(np.dot(a, b))

def get_logger(name: str) -> logging.Logger:

    logging.basicConfig(
        format=LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, LOG_LEVEL.upper()),
    )
    return logging.getLogger(name)
