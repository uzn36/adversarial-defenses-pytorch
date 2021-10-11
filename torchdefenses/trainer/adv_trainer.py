import os
import torch

from .trainer import Trainer

r"""
Base class for adversarial trainers.

Functions:
    self.record_rob : function for recording standard accuracy and robust accuracy against FGSM, PGD, and GN.

"""

class AdvTrainer(Trainer):
    def __init__(self, name, model):
        super(AdvTrainer, self).__init__(name, model)
        self._flag_record_rob = False
    
    def record_rob(self, train_loader, val_loader, eps, alpha, steps, std=0.1, n_limit=1000):
        self.record_keys += ['Clean(Tr)', 'FGSM(Tr)', 'PGD(Tr)', 'GN(Tr)',
                             'Clean(Val)', 'FGSM(Val)', 'PGD(Val)', 'GN(Val)',]    
        self._flag_record_rob = True    
        self._train_loader_rob = train_loader
        self._val_loader_rob = val_loader
        self._eps_rob = eps
        self._alpha_rob = alpha
        self._steps_rob = steps
        self._std_rob = std
        self._n_limit_rob = n_limit
    
    # Update Records
    def _update_record(self, records):
        if self._flag_record_rob:
            rob_records = []
            for loader in [self._train_loader_rob, self._val_loader_rob]:
                rob_records.append(self.eval_accuracy(loader,
                                                      n_limit=self._n_limit_rob))
                rob_records.append(self.eval_rob_accuracy_fgsm(loader,
                                                               eps=self._eps_rob,
                                                               n_limit=self._n_limit_rob))
                rob_records.append(self.eval_rob_accuracy_pgd(loader,
                                                              eps=self._eps_rob,
                                                              alpha=self._alpha_rob,
                                                              steps=self._steps_rob,
                                                              n_limit=self._n_limit_rob))
                rob_records.append(self.eval_rob_accuracy_gn(loader,
                                                             std=self._std_rob,
                                                             n_limit=self._n_limit_rob))
            
            self.rm.add([*records,
                         *rob_records,
                         self.optimizer.param_groups[0]['lr']])
        else:
            self.rm.add([*records,
                         self.optimizer.param_groups[0]['lr']])

