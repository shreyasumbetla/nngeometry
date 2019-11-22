import torch
from nngeometry.vector import Vector, from_model, random_vector, random_vector_dict
from nngeometry.utils import get_individual_modules
import torch.nn as nn
import torch.nn.functional as tF

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 5, 3, 1)
        self.conv2 = nn.Conv2d(5, 6, 4, 1)
        self.conv3 = nn.Conv2d(6, 7, 3, 1)
        self.fc1 = nn.Linear(1*1*7, 10)

    def forward(self, x):
        x = tF.relu(self.conv1(x))
        x = tF.max_pool2d(x, 2, 2)
        x = tF.relu(self.conv2(x))
        x = tF.max_pool2d(x, 2, 2)
        x = tF.relu(self.conv3(x))
        x = tF.max_pool2d(x, 2, 2)
        x = x.view(-1, 1*1*7)
        x = self.fc1(x)
        return tF.log_softmax(x, dim=1)

def test_from_dict_to_vector():
    eps = 1e-8
    model = ConvNet()
    v = from_model(model)
    d1 = v.get_dict_representation()
    v2 = Vector(model, vector_repr=v.get_flat_representation())
    d2 = v2.get_dict_representation()
    assert d1.keys() == d2.keys()
    for k in d1.keys():
        assert torch.norm(d1[k][0] - d2[k][0]) < eps
        if len(d1[k]) == 2:
            assert torch.norm(d1[k][1] - d2[k][1]) < eps

def test_add():
    model = ConvNet()
    r1 = random_vector(model)
    r2 = random_vector(model)
    sumr1r2 = r1 + r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() + r2.get_flat_representation())) < 1e-5   

    r1 = random_vector_dict(model)
    r2 = random_vector_dict(model)
    sumr1r2 = r1 + r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() + r2.get_flat_representation())) < 1e-5

    r1 = random_vector(model)
    r2 = random_vector_dict(model)
    sumr1r2 = r1 + r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() + r2.get_flat_representation())) < 1e-5

def test_sub():
    model = ConvNet()
    r1 = random_vector(model)
    r2 = random_vector(model)
    sumr1r2 = r1 - r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() - r2.get_flat_representation())) < 1e-5   

    r1 = random_vector_dict(model)
    r2 = random_vector_dict(model)
    sumr1r2 = r1 - r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() - r2.get_flat_representation())) < 1e-5

    r1 = random_vector(model)
    r2 = random_vector_dict(model)
    sumr1r2 = r1 - r2
    assert torch.norm(sumr1r2.get_flat_representation() -
                      (r1.get_flat_representation() - r2.get_flat_representation())) < 1e-5