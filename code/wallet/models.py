from enum import Enum

from django.db import models

class Currency(Enum):
    IRR = 'Rial'
    USD = 'Dollar'
    EUR = 'Euro'
