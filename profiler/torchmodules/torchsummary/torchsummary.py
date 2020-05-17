# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import torch
import torch.nn as nn
from torch.autograd import Variable

from collections import OrderedDict


def hook_modules(register_fn, module, module_whitelist):
    sub_modules = module.__dict__['_modules']

    for name, sub_module in sub_modules.items():
        # nn.Module is the only thing we care about.
        if sub_module is None or isinstance(sub_module, torch.nn.Module) is False:
            continue

        sub_module_name = sub_module.__class__.__name__
        sub_sub_modules = sub_module.__dict__['_modules']
        if len(sub_sub_modules) > 0 and sub_module_name not in module_whitelist:
            #
            # Recursively visit this module's descendants.
            #
            hook_modules(register_fn, sub_module, module_whitelist)
        else:
            register_fn(sub_module)


def summary(model, module_whitelist, model_input, verbose, device="cuda"):
    mapping = {}
    module_last_idx = 0
    def register_hook(module):
        def hook(module, input, output):
            class_name = str(module.__class__).split('.')[-1].split("'")[0]
            module_idx = module_last_idx
            module_last_idx += 1

            curr_layer = OrderedDict()
            curr_layer['layer_name'] = module
            curr_layer['input_shape'] = list(input[0].size())
            if isinstance(output, (list,tuple)):
                curr_layer['output_shape'] = []
                for o in output:
                    if isinstance(o, (list,tuple)):
                        curr_layer['output_shape'].extend(
                            [list(o_elem.size()) for o_elem in o])
                    else:
                        curr_layer['output_shape'].append(list(o.size()))
            else:
                curr_layer['output_shape'] = list(output.size())

            params = 0
            for name, param in module.named_parameters():
                if 'weight' in name:
                    params += torch.prod(torch.LongTensor(list(param.size())))
                    curr_layer['trainable'] = param.requires_grad
                elif 'bias' in name:
                    params += torch.prod(torch.LongTensor(list(param.size())))
            curr_layer['nb_params'] = params
            curr_layer['forward_time'] = 0.0
            curr_layer['backward_time'] = 0.0
            summary.append(curr_layer)
            print(curr_layer['nb_params'], module_idx)

        hooks.append(module.register_forward_hook(hook))
                
    device = device.lower()
    assert device in ["cuda", "cpu"], "Input device is not valid, please specify 'cuda' or 'cpu'"

    if device == "cuda" and torch.cuda.is_available():
        dtype = torch.cuda.FloatTensor
    else:
        dtype = torch.FloatTensor

    summary = []
    hooks = []
    # register hook
    hook_modules(register_hook, model, module_whitelist)
    # make a forward pass
    model(*model_input)
    # remove these hooks
    for h in hooks:
        h.remove()

    if verbose:
        print('----------------------------------------------------------------')
        line_new = '%s\t%s\t%s' % ('Layer Type', 'Output Shape', 'Param #')
        print(line_new)
        print('================================================================')
    total_params = 0
    trainable_params = 0
    for layer_id in range(len(summary)):
        # input_shape, output_shape, trainable, nb_params
        print(layer_id)
        line_new = '%s\t%s\t%s' % (summary[layer_id]['layer_name'], str(summary[layer_id]['output_shape']), '{0:,}'.format(summary[layer_id]['nb_params']))
        total_params += summary[layer_id]['nb_params']
        if 'trainable' in summary[layer_id]:
            if summary[layer_id]['trainable'] == True:
                trainable_params += summary[layer_id]['nb_params']
        if verbose:
            print(line_new)
    if verbose:
        print('================================================================')
        print('Total params: {0:,}'.format(total_params))
        print('Trainable params: {0:,}'.format(trainable_params))
        print('Non-trainable params: {0:,}'.format(total_params - trainable_params))
        print('----------------------------------------------------------------')

    return summary
