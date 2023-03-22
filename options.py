import sys

lbfgs_opts = {"maxcor": 100, 'ftol':0.0, 'gtol':0.0, 'maxfun': 10000, "maxiter": 10000, "maxls": 50}

nn_opts = {'num_hidden_layers':4, 'num_neurons_per_layer':64, 'resnet': False, 'userbf' : False}

weights = {'res':1.0, 'resl1':None, 'geomse':None, 'petmse': None, 'bc':1.0, 'dat':None, 
    'plfcor':None,
    'area1':None, 'area2':None,'mreg':None,'seg1':None, 'seg2':None, 'seglower1':None, 'seglower2':None}

opts = {
   "tag" : '',
    "model_dir": '',
    "num_init_train" : 100000, # initial traning iteration
    "N" : 20000, # number of residual point
    "Ntest":20000,
    "Ndat":20000,
    "Ndattest":20000,
    "nn_opts": nn_opts,
    "print_res_every" : 100, # print residual
    "save_res_every" : None, # save residual
    "weights" : weights, # weight of data, weight of res is 1
    "ckpt_every": 20000,
    "patience":1000,
    "file_log":True,
    "saveckpt":True,
    "D0":1.0,
    "trainD":True,
    "RHO0":1.0,
    "trainRHO":True,
    "M0":1.0,
    "trainM":False,
    "m0":1.0,
    "trainm":False,
    "datmask":'u1',
    "mrange":[0.8,2.0],
    "A0":0.0,
    "trainA":False,
    "x0":0.0,
    "y0":0.0,
    "z0":0.0,
    "th1":0.25,
    "th2":0.7,
    "trainth1":False,
    "trainth2":False,
    "trainx0":False,
    'inv_dat_file': '',
    "lbfgs_opts":lbfgs_opts,
    "randomt": -1.0,
    "activation":'tanh',
    "optimizer":'adam',
    "restore": '',
    "trainnnweight":None,
    "resetparam":False,
    "exactfwd":False,
    "lr": 1e-3,
    "smalltest":False,
    "useupred": None,
    "synthetic": False,
    "gradnorm":False,
    "outputderiv":False,
    "usegeo":False,
    "patient":False,
    "monitor":['total'],
    "weightopt": {'method': 'constant','window': 100, 'whichloss': 'res', 'factor':0.001}
    }


def update_nested_dict(nested_dict, key, value):
    """
    Recursively updates a nested dictionary by finding the specified key and assigning the new value to it.
    
    Args:
    - nested_dict (dict): the nested dictionary to update
    - key (str): the key to find and update
    - value (any): the new value to assign to the key
    
    Returns:
    - None
    """
    for k, v in nested_dict.items():
        if k == key:
            nested_dict[k] = value
        elif isinstance(v, dict):
            update_nested_dict(v, key, value)

def get_nested_dict(nested_dict, key):
    """
    get value from nested dict
    """
    for k, v in nested_dict.items():
        if k == key:
            return nested_dict[k]
        elif isinstance(v, dict):
            get_nested_dict(v, key)

class Options(object):
    def __init__(self, opts = opts):
        self.opts = opts
            
    def parse_args(self, *args):
        # parse args according to dictionary
        i = 0
        while i < len(args):
            key = args[i]
            
            default_val = get_nested_dict(self.opts, key)
            if isinstance(default_val,str):
                val = args[i+1]
            else:
                val = eval(args[i+1])
            update_nested_dict(self.opts, key, val)
            i +=2
        
        self.preprocess_option()
    
    def preprocess_option(self):
        
        # trim weights
        self.opts['weights'] = {k: v for k, v in self.opts['weights'].items() if v is not None}
        
        # exact fix trainable paramter
        if self.opts['exactfwd'] == True:
            self.opts['trainD'] = False
            self.opts['trainRHO'] = False
            self.opts['trainM'] = False
            self.opts['trainm'] = False
            self.opts['trainA'] = False
            self.opts['trainx0'] = False
            self.opts['trainth1'] = False
            self.opts['trainth2'] = False
            for wkey in self.opts['weights']:
                if wkey == 'res' or wkey == 'bc' or wkey == 'dat' or wkey == 'geomse':
                    continue
                else:
                    self.opts['weights'][wkey] = None
        
        # quick test
        if self.opts['smalltest'] == True:
            self.opts['file_log'] = False
            self.opts['num_init_train'] = 500
            self.opts['lbfgs_opts']['maxfun'] = 200
        
        # inference with synthetic data
        if self.opts['synthetic'] == True:
            self.opts['trainD'] = True
            self.opts['trainRHO'] = True
            self.opts['trainM'] = False
            self.opts['trainm'] = False
            self.opts['trainA'] = False
            self.opts['trainx0'] = False
            self.opts['trainth1'] = False
            self.opts['trainth2'] = False
            self.opts['weights']['res'] = 1.0
            self.opts['weights']['dat'] = 1.0
            self.opts['weights']['bc'] = 1.0
        
        if self.opts['patient'] is not False:
            w = self.opts['patient']
            self.opts['trainD'] = True
            self.opts['trainRHO'] = True
            self.opts['trainm'] = True
            self.opts['trainA'] = True
            self.opts['trainx0'] = True
            self.opts['trainth1'] = True
            self.opts['trainth2'] = True
            self.opts['weights']['res'] = 1.0
            self.opts['weights']['bc'] = 1.0
            self.opts['weights']['petmse'] = w
            self.opts['weights']['seg1'] = w
            self.opts['weights']['seg2'] = w
            self.opts['weights']['Areg'] = 1.0
            self.opts['weights']['mreg'] = 1.0
            self.opts['weights']['th1reg'] = 1.0
            self.opts['weights']['th2reg'] = 1.0
            self.opts['monitor'] = ['pdattest']

        


            


    
if __name__ == "__main__":
    
    
    opts = Options()
    opts.parse_args(*sys.argv[1:])

    print(opts.opts)


