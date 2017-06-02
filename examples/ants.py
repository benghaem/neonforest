from workspace import Workspace
from actor import Actor, Process
import random

class Ant(Actor):

    def __init__(self, trail_persist):
        self.run_forward = True
        self.trail_persist = trail_persist
        self.last_heading = random.randint(0,7)
        super(Ant, self).__init__()

    def setup(self, layers):
        #self.location[0] = int(layers['base'].width / 2)
        #self.location[0] = 0
        self.location[0] = random.randint(layers['base'].offset[0], layers['base'].width-1)
        self.location[1] = random.randint(layers['base'].offset[1], layers['base'].height-1)
        return True

    def skip_headings(self):
        if self.last_heading == 0:
            skip = [7,0,1]
        elif self.last_heading == 7:
            skip = [6,7,0]
        else:
            skip = [self.last_heading -1, self.last_heading, self.last_heading + 1]

        return skip

    def check_for_trail(self, layers):
        locations = [0] * 8

        for heading in range(7):
            self.move(heading, 1)
            heading_pval = layers['ptrail'].get(self.location[0], self.location[1])
            if heading_pval is not None and heading_pval> 0:
                locations[heading] = heading_pval
            self.move(heading, -1)

        return locations

    def step(self, layers):
        #randomly walk forward or backwards
        ptrail_values = self.check_for_trail(layers)
        mv_dist = []

        for idx in range(8):
            if idx in self.skip_headings():
                multiplier = 1 + int(ptrail_values[idx]/self.trail_persist * 100)
                for append_count in range(multiplier):
                    mv_dist.append(idx)

        new_heading = random.choice(mv_dist)
        self.last_heading = new_heading
        self.move(new_heading,1)
        #if self.run_forward:
        #    if True in plocs[1:4]:
        #        heading_choices = [i for i, v in enumerate(plocs[1:4]) if v == True]
        #        self.move(random.choice(heading_choices),1)
        #    else:
        #        self.move(random.randint(0,4),1)
        #else:
        #    self.move(random.choice([0,4,5,6,7]),1)

        #don't go out of bounds
        self.check_bounds(layers['base'])

        #Turn around if we hit the end
        if self.location[0] == layers['base'].width-1:
            self.run_forward = False
        elif self.location[0] == layers['base'].offset[0]:
            self.run_forward = True

        self.add_to_trail(layers)

    def add_to_trail(self, layers):
        current = layers['ptrail'].get(self.location[0], self.location[1])
        new = current + self.trail_persist
        if new > self.trail_persist:
            new = self.trail_persist
        layers['ptrail'].set(self.location[0], self.location[1], new)

        #print(str(self.id) + " at " +str(self.location))

class PDecay(Process):
    def __init__(self, rate):
        self.rate = rate
        super(PDecay, self).__init__()

    def step(self, layers):
        for val, x, y in layers['ptrail'].iter_all():
            new_val = val - self.rate
            if new_val < 0:
                new_val = 0
            layers['ptrail'].set(x,y,new_val)

