from datetime import datetime

from model.model import Model
from model.order import Order

m = Model()
m.buildGraph(1,5)
m.getPercorsoMax(403)
