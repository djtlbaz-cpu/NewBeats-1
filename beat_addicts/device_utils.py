import torch


def get_device(preference: str = "auto") -> torch.device:
    """
    preference:
      - "auto": use cuda if available else cpu
      - "cuda": force cuda (falls back to cpu if unavailable)
      - "cpu": force cpu
    """
    preference = (preference or "auto").lower()

    if preference == "cpu":
        return torch.device("cpu")

    if preference in {"cuda", "gpu"}:
        if torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")

    # auto
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
