'''
test file
'''

import time
import numpy as np

from dataset.fdataset import FDataSet
from net.unet2d import *
from net.pspnet2d import *
from net.channet2d import *
from net.resnet2d import *
from solver.solver2d import Solver2D
from utils.augmentation import *
from solver.combinesolver2d import CombineSolver2D

def test_file(solve, file_name):
    data = np.fromfile(file_name, dtype=np.float32)
    start = time.time()
    predict = solve.forward(data)
    duration = time.time()-start
    predict.shape = [data.shape[0]]
    print('testing cost %f seconds.'%(duration))
    print predict
    return predict

common_params = {}
common_params['batch_size'] = 16
common_params['test_batch_size'] = 32
common_params['dimension'] = 2
common_params['width'] = 512
common_params['height'] = 512
common_params['channel'] = 1
common_params['testing'] = True
common_params['label_type'] = 'binary'

dataset_params = {}
dataset_params['dtype'] = np.uint16
dataset_params['random'] = True
dataset_params['data_path'] = '/media/E/Documents/VesselData/TrainData/patches2D512'
dataset_params['label_path'] = '/media/E/Documents/VesselData/TrainLabel/binary2D512'
dataset_params['test_data_path'] = '/media/E/Documents/VesselData/TrainData/testpatches2D512'
dataset_params['test_label_path'] = '/media/E/Documents/VesselData/TrainLabel/testbinary2D512'


net_params = {}
net_params['weight_true'] = 0
net_params['weight_false'] = 1
net_params['layers'] = 101
solver_params = {}
solver_params['train_dir'] = 'models'
#solver_params['model_name'] = 'relu'
#solver_params['model_name'] = 'lrelu'
#solver_params['model_name'] = 'selu'
#solver_params['model_name'] = 'swish'
solver_params['model_name'] = 'binres'
#solver_params['pretrain_model_path'] = 'models/binres.cpkt-30000'
solver_params['max_iterators'] = 30000
learning_rate = np.zeros(30000, dtype=np.float32)
learning_rate[0:10000] = 0.001
learning_rate[10000:20000] = 0.0005
learning_rate[20000:30000] = 0.0001
#learning_rate[70000:100000] = 0.0001
solver_params['learning_rate'] = learning_rate
solver_params['beta1'] = 0.9
solver_params['beta2'] = 0.999
eval_names = []
eval_names.append('accuracy')
eval_names.append('precision')
eval_names.append('recall')
eval_names.append('f1')
solver_params['eval_names'] = eval_names
plot_params = {}
plot_params['max_iterations'] = solver_params['max_iterators']
plot_params['eval_names'] = eval_names
#plot_params['save_name'] = 'output/relu.png'
#plot_params['save_name'] = 'output/lrelu.png'
#plot_params['save_name'] = 'output/selu.png'
plot_params['save_name'] = 'output/binres.png'
plot_params['interactive'] = False
plot_params['loss_max'] = 5.0
solver_params['plot'] = False
solver_params['plot_params'] = plot_params
solver_params['keep_prob'] = 0.5
net_input = {}
net_input['training'] = True
net_input['former_train'] = True
net_input['pretrain'] = True
solver_params['net_input'] = net_input
aug = Augmentations('scaling', div=1024, bias=-1)
solver_params['aug'] = aug

dataset = FDataSet(common_params, dataset_params)
#net = Unet2D(common_params, net_params)
#net = UnetLReLU2D(common_params, net_params)
#net = UnetSeLU2D(common_params, net_params)
net = ResNet2D4(common_params, net_params, name='binres')
#net = PSPnet2DCombine(common_params, net_params)
#solver = CombineSolver2D(dataset, net, common_params, solver_params)
solver = Solver2D(dataset, net, common_params, solver_params)
solver.initialize()
solver.solve()
predict1 = test_file(solver, '/media/E/Documents/VesselData/TrainData/0015/oridata.dat')
predict2 = test_file(solver, '/media/E/Documents/VesselData/TrainData/0049/oridata.dat')
predict3 = test_file(solver, '/media/E/Documents/VesselData/TrainData/0322/oridata.dat')
predict4 = test_file(solver, '/media/E/Documents/VesselData/TrainData/1008/oridata.dat')
predict5 = test_file(solver, '/media/E/Documents/VesselData/TrainData/1015/oridata.dat')