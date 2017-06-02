import workspace as mf
from ants import Ant, PDecay
import time
import shutil
term_size = shutil.get_terminal_size((80, 20))
wx = term_size.columns - 2
hy = term_size.lines - 3
ws1 = mf.Workspace(wx,hy)
ptrail_lay = mf.Layer(wx,hy,'ptrail',default=0,render_hint="numeric")
ws1.add_layer(ptrail_lay, 0)

ws1.set_data('base',3,4,1)
ws1.set_data('base',1,4,1)

print(ws1.render_to_string('base'))

for x in range(10):
    new_ant = Ant(80)
    ws1.add_actor(new_ant)

pdecay1 = PDecay(1)
ws1.add_process(pdecay1)

while(True):
    print(ws1.render_to_string('ptrail'))
    ws1.step_all()
    time.sleep(0.1)
