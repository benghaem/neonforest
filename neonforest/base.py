class Layer():

    def __init__(self, width, height, name, default=None, offset_x = 0, offset_y = 0, render_hint=None):
        self.width = width
        self.height = height
        self.name = name
        self.offset = (offset_x, offset_y)
        self.reset(default=default)
        self.render_hint = render_hint

    def get(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.data[x][y]
        return None

    def set(self, x, y, v):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.data[x][y] = v
            return True
        return False

    def iter_all(self):
        return(LayerIterator(self))

    def reset(self, default = None):
        column = [default] * self.height
        self.data = []
        for x in range(self.width):
            self.data.append(list(column))
        return True

class LayerIterator():

    def __init__(self, layer):
        self.target = layer
        self.x = 0
        self.y = 0

    def __iter__(self):
        return self

    def __next__(self):

        val= self.target.data[self.x][self.y]
        ret_tuple = (val, self.x, self.y)

        self.y = self.y+1

        if self.y == self.target.height:
            self.y = 0
            self.x = self.x + 1
            if self.x == self.target.width:
                raise StopIteration

        return ret_tuple

class Workspace():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers= {}
        self.layer_order = []
        self.actors = []
        self.actor_id_c = 0
        self.processes = []
        self.process_id_c = 0
        base_lay = Layer(width, height, "base")
        actor_lay = Layer(width, height, "actor")
        self.add_layer(base_lay, 0)
        self.add_layer(actor_lay, 1)

    def add_layer(self, layer, z):
        if layer.name not in self.layers:
            self.layers[layer.name] = layer
            self.layer_order.insert(z,layer.name)
            return True
        return False

    def add_process(self, process):
        process.set_id(self.process_id_c)

        #setup process
        process.setup(self.layers)
        self.processes.append(process)
        return True

    def add_actor(self, actor):
        #provide actor id
        actor.set_id(self.actor_id_c)
        self.actor_id_c = self.actor_id_c + 1

        #setup actor
        actor.setup(self.layers)

        #register actor to position layer
        self.layers['actor'].set(actor.location[0], actor.location[1], True)

        self.actors.append(actor)
        return True

    def step_processes(self):
        for process in self.processes:
            process.step(self.layers)

    def step_actors(self):
        for actor in self.actors:
            actor.step(self.layers)

        #Update actor position layer
        self.layers['actor'].reset()

        for actor in self.actors:
            self.set_data('actor', actor.location[0], actor.location[1], True)

        return True

    def step_all(self):
        self.step_actors()
        self.step_processes()

    def get_layer_ids(self):
        return self.layer_order

    def num_layers(self):
        return len(self.layers)

    def get_data(self, layer_id, x, y):
        if layer_id in self.layers:
            return self.layers[layer_id].get(x,y)
        return None

    def set_data(self, layer_id, x, y, v):
        if layer_id in self.layers:
            return self.layers[layer_id].set(x,y,v)
        return False

    def render_to_curses(self, layer_id, screen):
        screen.clear()
        screen.border()
        if layer_id in self.layers:
            layer = self.layers[layer_id]
            for y in range(self.height):
                vy = y + 1
                for x in range(self.width):
                    vx = x + 1
                    layer_v = layer.get(x,y)
                    if layer.render_hint == None:
                        if layer_v is not None:
                            screen.addch(vy,vx,'X')
                    elif layer.render_hint == "numeric":
                        if layer_v > 0 and layer_v < 10:
                            screen.addch(vy,vx,str(layer_v)[0])
                        elif layer_v >= 10 :
                            screen.addch(vy,vx,'+')


    def render_to_string(self, layer_id):
        output = ""
        if layer_id in self.layers:
            layer = self.layers[layer_id]

            if layer.render_hint == None or layer.render_hint=="numeric":
                for x in range(self.width+2):
                    output = output + '-'
                output = output+"\n"
                for y in range(self.height):
                    output = output + '|'
                    for x in range(self.width):
                        char = ' '
                        if layer.render_hint == None:
                            if layer.get(x,y) is not None:
                                char = 'X'
                        elif layer.render_hint == "numeric":
                            value = layer.get(x,y)
                            if value == 0:
                                char = ' '
                            elif value > 9:
                                char = '+'
                            else:
                                char = str(value)

                        output = output + char

                    output = output + '|'
                    if y is not self.height -1:
                        output = output + '\n'

                output = output + "Rendering layer: " + layer_id

        return output
