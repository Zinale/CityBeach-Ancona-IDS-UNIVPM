from typing import Dict
from Model.Locker import Locker

class AppLockersController:
    def __init__(self, lockers: Dict[int, Locker], locker_id: int):
        self.lockers = lockers
        self.locker_id = locker_id