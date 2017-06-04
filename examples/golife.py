import neonforest as nf

class life(nf.blocks.Process):

    def step(self, layers):
        base = layers['cell']
        work = layers['work']
        for cell,x,y in base.iter_all():
            neighbors = base.get_neighbors(x,y)
            n_alive = neighbors.count(True)

            if cell is True:
                if n_alive == 2 or n_alive == 3:
                    work.set(x,y,True)
                else:
                    work.set(x,y,False)

            else:
                if n_alive == 3:
                    work.set(x,y,True)

        base.overwrite(work)
        work.reset(False)

#setup workspace
width = 100
height = 100
ws = nf.base.Workspace(width,height)

#create layers
cell_layer = nf.base.Layer(width,height,'cell',default=False,render_hint="bool")
work_layer = nf.base.Layer(width,height,'work',default=False,render_hint="bool")

#set initial cell positions
cell_layer.set_batch(0,True,0,[24])
cell_layer.set_batch(0,True,1,[22,24])
cell_layer.set_batch(0,True,2,[12,13,20,21,34,35])
cell_layer.set_batch(0,True,3,[11,15,20,21,34,35])
cell_layer.set_batch(0,True,4,[0,1,10,16,20,21])
cell_layer.set_batch(0,True,5,[0,1,10,14,16,17,22,24])
cell_layer.set_batch(0,True,6,[10,16,24])
cell_layer.set_batch(0,True,7,[11,15])
cell_layer.set_batch(0,True,8,[12,13])


#attach layers and process
ws.add_layer(cell_layer,0)
ws.add_layer(work_layer,0)
ws.add_process(life())

#create display
disp1 = nf.display.CursesDisplay(ws, 'cell', start_paused=True, dt=0.1)

#run simulation
disp1.display()
