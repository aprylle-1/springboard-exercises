"""Python serial number generator."""

class SerialGenerator:
    """Machine to create unique incrementing serial numbers.
    
    >>> serial = SerialGenerator(start=100)

    >>> serial.generate()
    100

    >>> serial.generate()
    101

    >>> serial.generate()
    102

    >>> serial.reset()

    >>> serial.generate()
    100
    """
    def __init__(self, start = 100):
        f"""Initializes Serial Generator self.start = {start}, self.next = {start}"""
        self.next= start
        self.start = start

    def __repr__(self):
        """"Show Representation"""
        return f"Serial Generator start = {self.start}, next = {self.next}"
    
    def generate(self):
        f"""Generates the Serial Number by Incrementing Count and Returning the Previous Count"""
        self.next += 1
        return self.next - 1
    
    def reset(self):
        """Resets the Instance's Counter back to Start Value"""
        self.next = self.start

