from dataclasses import dataclass

from model.order import Order


@dataclass
class Edge:
    o1:Order
    o2:Order
    weight: int

