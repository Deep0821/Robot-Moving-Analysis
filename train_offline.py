from demo import Demonstration, load_all_demos
from utils import ACTION_TO_ID
from trainer import Trainer
from tqdm import tqdm
import os
import argparse
import numpy as np

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--base_model', required=True)
    parser.add_argument('-d', '--demo_dir', required=True, help='path to dir with demos')
    parser.add_argument('-i', '--iterations', default=250, type=int, help='how many training steps')
    parser.add_argument('-s', '--seed', default=1234, type=int)
    parser.add_argument('-t', '--task_type', default='stack', help='stack/row/unstack/vertical_square')
    args = parser.parse_args()

    # define workspace_limits (Cols: min max, Rows: x y z (define workspace limits in robot coordinates))
    workspace_limits = np.asarray([[-0.724, -0.276], [-0.224, 0.224], [-0.0001, 0.5]])

    # seed np.random
    np.random.seed(args.seed)

    # first load the demo(s)
    demos = load_all_demos(args.demo_dir, check_z_height=False,
            task_type=args.task_type)
    num_demos = len(demos)

    # now load the trainer
    model_path = os.path.abspath(args.base_model)
    place_common_sense = (args.task_type != 'unstack')
    if args.task_type == 'stack':
        place_dilation = 0.00
    else:
        place_dilation = 0.05

    trainer = Trainer(method='reinforcement', push_rewards=False,
            future_reward_discount=0.65, is_testing=False, snapshot_file=args.base_model,
            force_cpu=False, goal_condition_len=0, place=True, pretrained=True,
            flops=False, network='densenet', common_sense=True,
            place_common_sense=place_common_sense, show_heightmap=False,
            place_dilation=place_dilation, common_sense_backprop=True,
            trial_reward='spot', num_dilation=0)

    # store losses, save model if it has smaller loss
    losses = []
    best_model = None

    for i in tqdm(range(args.iterations)):
        # generate random number between 0 and 1, and another between 0 and 5 (inclusive)
        demo_num = np.random.randint(0, 2)
        progress = np.random.randint(1, 4)
        action_str = ['grasp', 'place'][np.random.randint(0, 2)]

        # get imgs
        d = demos[demo_num]
        color_heightmap, valid_depth_heightmap = d.get_heightmaps(action_str,
                d.action_dict[progress][action_str + '_image_ind'], use_hist=True)

        # get action info

        action_vec = d.action_dict[progress][ACTION_TO_ID[action_str]]

        # convert rotation angle to index
        best_rot_ind = np.around((np.rad2deg(action_vec[-2]) % 360) * 16 / 360).astype(int)

        # convert robot coordinates to pixel
        workspace_pixel_offset = workspace_limits[:2, 0] * -1 * 1000

        # need to index with (y, x) downstream, so swap order in best_pix_ind
        best_action_xy = ((workspace_pixel_offset + 1000 * action_vec[:2]) / 2).astype(int)
        best_pix_ind = [best_rot_ind, best_action_xy[1], best_action_xy[0]]

        # get next set of heightmaps for reward computation
        if action_str == 'grasp':
            next_action_str = 'place'
            next_progress = progress
        else:
            next_action_str = 'grasp'
            next_progress = progress + 1

        if next_progress > 3:
            print("HACK, NEEDS PROPER FIX")
            reward = 6
        else:
            next_color_heightmap, next_depth_heightmap = d.get_heightmaps(next_action_str,
                    d.action_dict[next_progress][action_str + '_image_ind'], use_hist=True)

            # compute reward
            grasp_success = (action_str == 'grasp')
            place_success = (action_str == 'place')
            reward, old_reward = trainer.get_label_value(action_str, push_success=False,
                    grasp_success=grasp_success, change_detected=True, prev_push_predictions=None,
                    prev_grasp_predictions=None, next_color_heightmap=next_color_heightmap,
                    next_depth_heightmap=next_depth_heightmap, color_success=None, goal_condition=None,
                    place_success=place_success, prev_place_predictions=None, reward_multiplier=1)

        # training step
        trainer.backprop(color_heightmap, valid_depth_heightmap, action_str,
                best_pix_ind, reward)
