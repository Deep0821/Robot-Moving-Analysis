import numpy as np
import cv2
import os
from utils import ACTION_TO_ID

class Demonstration():
    def __init__(self, path, demo_num, check_z_height, task_type='stack'):
        # path is expected to be <logs/exp_name>
        self.action_log = np.loadtxt(os.path.join(path, 'transitions',
            'executed-actions-0.log.txt'))
        self.rgb_dir = os.path.join(path, 'data', 'color-heightmaps')
        self.depth_dir = os.path.join(path, 'data', 'depth-heightmaps')
        self.demo_num = demo_num
        self.check_z_height = check_z_height
        self.task_type = task_type

        if self.task_type == 'stack':
            # populate actions in dict keyed by stack height {stack_height : {action : (x, y, z, theta)}}
            self.action_dict = {}
            for s in range(3):
                # store push, grasp, and place actions for demo at stack height s
                # TODO(adit98) figure out how to incorporate push actions into this paradigm
                # TODO(adit98) note this assumes perfect demo
                # if stack height is 0, indices 0 and 1 of the action log correspond to grasp and place respectively
                demo_first_ind = 2 * s
                self.action_dict[s] = {ACTION_TO_ID['grasp'] : self.action_log[demo_first_ind],
                        ACTION_TO_ID['place'] : self.action_log[demo_first_ind + 1]}

        elif self.task_type == 'unstack':
            # get number of actions in demo
            self.num_actions = len(os.listdir(self.rgb_dir))

            # populate actions in dict keyed by stack height {stack_height : {action : (x, y, z, theta)}}
            self.action_dict = {}
            for s in range(1, 5):
                # store push, grasp, and place actions for demo at stack height s
                demo_ind = -2 * (5 - s)
                self.action_dict[s] = {ACTION_TO_ID['grasp'] : self.action_log[demo_ind],
                        ACTION_TO_ID['place'] : self.action_log[demo_ind + 1],
                        'demo_ind': demo_ind}

    def get_heightmaps(self, action_str, stack_height):
        # e.g. initial rgb filename is 000000.orig.color.png, only for stack demos
        if action_str != 'orig' and self.task_type == 'stack':
            action_str = str(stack_height) + action_str

        rgb_filename = os.path.join(self.rgb_dir,
                '%06d.%s.color.png' % (stack_height, action_str))
        depth_filename = os.path.join(self.depth_dir,
                '%06d.%s.depth.png' % (stack_height, action_str))

        rgb_heightmap = cv2.cvtColor(cv2.imread(rgb_filename), cv2.COLOR_BGR2RGB)
        depth_heightmap = cv2.imread(depth_filename, -1).astype(np.float32)/100000

        return rgb_heightmap, depth_heightmap

    # TODO(adit98) figure out how to get primitive action
    # TODO(adit98) this will NOT work for novel tasks, worry about that later
    def get_action(self, trainer, workspace_limits, primitive_action, stack_height):
        # TODO(adit98) clean up the way demo heightmaps are saved to reduce confusion
        # set action_str based on primitive action
        # heightmap_height is the height we use to get the demo heightmaps
        if self.task_type == 'stack':
            if not self.check_z_height:
                # if we completed a stack, prev_stack_height will be 4, but we want the imitation actions for stack height 1
                # TODO(adit98) switched this to get nonlocal_variables['stack_height'] now, so see how it is different
                stack_height = (stack_height - 1) if stack_height < 4 else 0
            else:
                # TODO(adit98) check but stack_height is going to be number of blocks on top of base block
                stack_height = np.round(stack_height).astype(int)
                # TODO(adit98) figure out how to reset stack height if check_z_height is set
                stack_height = (stack_height - 1) if stack_height < 4 else 0

            # TODO(adit98) deal with push
            if primitive_action == 'push':
                return -1

            if stack_height == 0 and primitive_action == 'grasp':
                action_str = 'orig'
            elif primitive_action == 'grasp':
                # if primitive action is grasp, we need the previous place heightmap and grasp action
                action_str = 'place'
                heightmap_height -= 1
            else:
                # if primitive action is place, get the previous grasp heightmap
                action_str = 'grasp'

        else:
            action_str = primitive_action
            if primitive_action == 'grasp':
                # offset is 2 for stack height 4, 4 for stack height 3, ...
                offset = 6 - stack_height

            elif primitive_action == 'place':
                # offset is 1 for stack height 4, 3 for stack height 3, ...
                # this is because place is always 1 action after grasp
                offset = 5 - stack_height

        if self.task_type == 'stack':
            color_heightmap, valid_depth_heightmap = self.get_heightmaps(action_str, stack_height)
        elif self.task_type == 'unstack':
            color_heightmap, valid_depth_heightmap = self.get_heightmaps(action_str, self.num_actions - offset)

        # to get vector of 64 vals, run trainer.forward with get_action_feat
        push_preds, grasp_preds, place_preds = trainer.forward(color_heightmap,
                valid_depth_heightmap, is_volatile=True, keep_action_feat=True, use_demo=True)

        # get demo action index vector
        action_vec = self.action_dict[stack_height][ACTION_TO_ID[primitive_action]]

        # convert rotation angle to index
        best_rot_ind = np.around((np.rad2deg(action_vec[-2]) % 360) * 16 / 360).astype(int)

        # convert robot coordinates to pixel
        workspace_pixel_offset = workspace_limits[:2, 0] * -1 * 1000
        best_action_xy = ((workspace_pixel_offset + 1000 * action_vec[:2]) / 2).astype(int)

        # need to swap x and y coordinates for best_action_xy
        best_action_xy = [best_action_xy[1], best_action_xy[0]]

        # TODO(adit98) figure out if we want more than 1 coordinate
        # TODO(adit98) add logic for pushing here
        if primitive_action == 'grasp':
            # TODO(adit98) figure out if we need to swap xy coordinates
            # we do y coordinate first, then x, because cv2 images are row, column indexed
            best_action = grasp_preds[best_rot_ind, :, best_action_xy[0], best_action_xy[1]]

        # TODO(adit98) find out why place preds inds were different before
        elif primitive_action == 'place':
            best_action = place_preds[best_rot_ind, :, best_action_xy[0], best_action_xy[1]]

        return best_action, ACTION_TO_ID[primitive_action]
