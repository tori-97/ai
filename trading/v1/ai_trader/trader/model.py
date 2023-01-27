import torch.nn as nn

class DQN_Model(nn.Module):
    def __init__(self, input_sizes, hidden_sizes, output_sizes) -> None:
        super().__init__()

        self._seq = nn.Sequential(
            nn.Linear(in_features=input_sizes, out_features=hidden_sizes),
            nn.ReLU(),
            nn.Linear(in_features=hidden_sizes, out_features=hidden_sizes),
            nn.ReLU(),
            nn.Linear(in_features=hidden_sizes, out_features=hidden_sizes),
            nn.ReLU(),
            nn.Linear(in_features=hidden_sizes, out_features=output_sizes)
        )

    def forward(self, x):
        return self._seq(x)
