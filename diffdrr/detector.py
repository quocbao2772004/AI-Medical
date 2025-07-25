# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/02_detector.ipynb.

# %% ../notebooks/api/02_detector.ipynb 3
from __future__ import annotations

import torch
from fastcore.basics import patch
from torch.nn.functional import normalize

# %% auto 0
__all__ = ['Detector']

# %% ../notebooks/api/02_detector.ipynb 5
from .pose import RigidTransform
from .utils import make_intrinsic_matrix


class Detector(torch.nn.Module):
    """Construct a 6 DoF X-ray detector system. This model is based on a C-Arm."""

    def __init__(
        self,
        sdd: float,  # Source-to-detector distance (i.e., focal length)
        height: int,  # Height of the X-ray detector
        width: int,  # Width of the X-ray detector
        delx: float,  # Pixel spacing in the X-direction
        dely: float,  # Pixel spacing in the Y-direction
        x0: float,  # Principal point X-offset
        y0: float,  # Principal point Y-offset
        reorient: torch.tensor,  # Frame-of-reference change matrix
        n_subsample: int | None = None,  # Number of target points to randomly sample
        reverse_x_axis: bool = False,  # If pose includes reflection (in E(3) not SE(3)), reverse x-axis
    ):
        super().__init__()
        self.sdd = sdd
        self.height = height
        self.width = width
        self.delx = delx
        self.dely = dely
        self.x0 = x0
        self.y0 = y0
        self.n_subsample = n_subsample
        if self.n_subsample is not None:
            self.subsamples = []
        self.reverse_x_axis = reverse_x_axis

        # Initialize the source and detector plane in default positions (along the x-axis)
        source, target = self._initialize_carm()
        self.register_buffer("source", source)
        self.register_buffer("target", target)

        # Create a pose to reorient the scanner
        self.register_buffer("_reorient", reorient)

    @property
    def reorient(self):
        return RigidTransform(self._reorient)

    @property
    def intrinsic(self):
        return make_intrinsic_matrix(
            self.sdd,
            self.delx,
            self.dely,
            self.height,
            self.width,
            self.x0,
            self.y0,
        ).to(self.source)

# %% ../notebooks/api/02_detector.ipynb 6
@patch
def _initialize_carm(self: Detector):
    """Initialize the default position for the source and detector plane."""
    try:
        device = self.sdd.device
    except AttributeError:
        device = torch.device("cpu")

    # Initialize the source at the origin and the center of the detector plane on the positive z-axis
    source = torch.tensor([[0.0, 0.0, 0.0]], device=device)
    center = torch.tensor([[0.0, 0.0, 1.0]], device=device) * self.sdd

    # Use the standard basis for the detector plane
    basis = torch.tensor([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], device=device)

    # Construct the detector plane with different offsets for even or odd heights
    h_off = 1.0 if self.height % 2 else 0.5
    w_off = 1.0 if self.width % 2 else 0.5

    # Construct equally spaced points along the basis vectors
    t = (
        torch.arange(-self.height // 2, self.height // 2, device=device) + h_off
    ) * self.delx
    s = (
        torch.arange(-self.width // 2, self.width // 2, device=device) + w_off
    ) * self.dely
    if self.reverse_x_axis:
        s = -s
    coefs = torch.cartesian_prod(t, s).reshape(-1, 2)
    target = torch.einsum("cd,nc->nd", basis, coefs)
    target += center

    # Batch source and target
    source = source.unsqueeze(0)
    target = target.unsqueeze(0)

    # Apply principal point offset
    target[..., 1] -= self.x0
    target[..., 0] -= self.y0

    if self.n_subsample is not None:
        sample = torch.randperm(self.height * self.width)[: int(self.n_subsample)]
        target = target[:, sample, :]
        self.subsamples.append(sample.tolist())
    return source, target

# %% ../notebooks/api/02_detector.ipynb 7
from .pose import RigidTransform


@patch
def forward(self: Detector, pose: RigidTransform):
    """Create source and target points for X-rays to trace through the volume."""
    pose = self.reorient.compose(pose)
    source = pose(self.source)
    target = pose(self.target)
    return source, target
