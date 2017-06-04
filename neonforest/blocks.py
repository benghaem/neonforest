class Process():

    def __init__(self):
        self.id = None

    def set_id(self, id):
        self.id = id
        return True

    def setup(self, layers):
        pass

    def pre_step(self, layers):
        pass

    def step(self, layers):
        raise NotImplementedError

    def post_step(self, layers):
        pass

class Actor(Process):

    def __init__(self):
        self.location = [0,0]
        super(Actor,self).__init__()

    def move(self, heading, dist):
        """
        5 4 3
        6   2
        7 0 1
        """

        if heading == 7 or heading == 0 or heading == 1:
            self.location[1] = self.location[1] + dist

        if heading == 1 or heading == 2 or heading == 3:
            self.location[0] = self.location[0] + dist

        if heading == 3 or heading == 4 or heading == 5:
            self.location[1] = self.location[1] - dist

        if heading == 5 or heading == 6 or heading == 7:
            self.location[0] = self.location[0] - dist

    def check_bounds(self, layer):
        if self.location[1] > layer.height-1:
            self.location[1] = layer.height-1

        if self.location[0] > layer.width-1:
            self.location[0] = layer.width-1

        if self.location[0] < layer.offset[0]:
            self.location[0] = layer.offset[0]

        if self.location[1] < layer.offset[1]:
            self.location[1] = layer.offset[1]
