import torch

import utility
import data
import model
import loss
from option import args
from trainer import Trainer

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

if args.data_test == 'video':
    from videotester import VideoTester
    model = model.Model(args, checkpoint)
    t = VideoTester(args, model, checkpoint)
    t.test()
else:
    if checkpoint.ok:
        loader = data.Data(args)
        model = model.Model(args, checkpoint)
        print('    Total params: %.2fM' % (sum(p.numel() for p in model.parameters())/1000000.0))
        loss = loss.Loss(args, checkpoint) if not args.test_only else None
        t = Trainer(args, loader, model, loss, checkpoint)
        while not t.terminate():
            t.train()
            t.test()

        checkpoint.done()

