"""sqlite"""
class TableCreationError(Exception):
     def __init__(self, message="Could Not Create Table"):
        self.message = message
        super().__init__(self.message)

class MultipleValueReturn(Exception):
    def __init__(self, message="Query Returned multiple value"):
        self.message = message
        super().__init__(self.message)

"""DB"""
class DBConnError(Exception):
    def __init__(self, message="Connection To Database couldnot be established"):
        self.message = message
        super().__init__(self.message)

class DBKeysValidationError(Exception):
    def __init__(self, message="Invalid Data from database"):
        self.message = message
        super().__init__(self.message)

class DBRequestError(Exception):
    def __init__(self, message="DB request Error"):
        self.message = message
        super().__init__(self.message)
