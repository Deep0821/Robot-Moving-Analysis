# "Good Robot!" Efficient Reinforcement Learning for Multi-Step Visual Tasks via Reward Shaping

[Andrew Hundt](http://ahundt.github.io/), Benjamin Killeen, Heeyeon Kwon, Chris Paxton, and Gregory D. Hager

Click the image to watch the video:

[!["Good Robot!": Efficient Reinforcement Learning for Multi Step Visual Tasks via Reward Shaping](https://img.youtube.com/vi/p2iTSEJ-f_A/0.jpg)](https://youtu.be/p2iTSEJ-f_A)

## Paper, Abstract, and Citations

```
@misc{hundt2019good,
    title={"Good Robot!": Efficient Reinforcement Learning for Multi-Step Visual Tasks via Reward Shaping},
    author={Andrew Hundt and Benjamin Killeen and Heeyeon Kwon and Chris Paxton and Gregory D. Hager},
    year={2019},
    eprint={1909.11730},
    archivePrefix={arXiv},
    primaryClass={cs.RO},
    url={https://arxiv.org/abs/1909.11730}
}
```

Abstract— In order to learn effectively, robots must be able to extract the intangible context by which task progress and mistakes are defined. In the domain of reinforcement learning, much of this information is provided by the reward function. Hence, reward shaping is a necessary part of how we can achieve state-of-the-art results on complex, multi-step tasks. However, comparatively little work has examined how reward shaping should be done so that it captures task context, particularly in scenarios where the task is long-horizon and failure is highly consequential. Our Schedule for Positive Task (SPOT) reward trains our Efficient Visual Task (EVT) model to solve problems that require an understanding of both task context and workspace constraints of multi-step block arrangement tasks. In simulation EVT can completely clear adversarial arrangements of objects by pushing and grasping in 99% of cases vs an 82% baseline in prior work. For random arrangements EVT clears 100% of test cases at 86% action efficiency vs 61% efficiency in prior work. EVT + SPOT is also able to demonstrate context understanding and complete stacks in 74% of trials compared to a base- line of 5% with EVT alone. To our knowledge, this is the first instance of a Reinforcement Learning based algorithm successfully completing such a challenge. Code is available at https://github.com/jhu-lcsr/costar visual stacking.

## Training CoSTAR Visual Stacking

Details of our specific training and test runs, command line commands, pre-trained models, and logged data with images are on the [costar visual stacking github releases page](https://github.com/jhu-lcsr/costar_visual_stacking/releases).

### Starting the V-REP Simulation

[Download V-REP](http://www.coppeliarobotics.com/index.html) and run it to start the simulation. Uou may need to adjust the paths below to match your V-REP folder, and it should be run from the costar_visual_stacking repository directory:

```bash
~/src/V-REP_PRO_EDU_V3_6_2_Ubuntu16_04/vrep.sh -gREMOTEAPISERVERSERVICE_19997_FALSE_TRUE -s simulation/simulation.ttt
```

### Cube Stacking

![A stack of 4 cubes](https://user-images.githubusercontent.com/55744/64198714-cb032100-ce56-11e9-9f6d-acb3101ff786.png)

#### Cube Stack Training

```bash
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 4 --push_rewards --experience_replay --explore_rate_decay --place
```

To use trial SPOT also add `--trial_reward` to this command.

#### Cube Stack Testing

Remember to first train the model or download the snapshot file from the release page (ex: [v0.12 release](https://github.com/jhu-lcsr/costar_visual_stacking/releases/tag/v0.12.0)) and update the command line `--snapshot_file FILEPATH`:

```bash
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 4  --push_rewards --experience_replay --explore_rate_decay --place --load_snapshot --snapshot_file ~/Downloads/snapshot.reinforcement-best-stack-rate.pth --random_seed 1238 --is_testing --save_visualizations --disable_situation_removal
```

### Row of 4 Cubes

![001057 1 color row](https://user-images.githubusercontent.com/55744/65455899-31f07600-de16-11e9-9808-bb75226fa58d.png)

Row Testing Video:

[![CoSTAR Visual Stacking v0.12 rows test run video](https://img.youtube.com/vi/Ti3mSGvbc7w/0.jpg)](https://youtu.be/Ti3mSGvbc7w)

[Row v0.12 release page and pretrained models](https://github.com/jhu-lcsr/costar_visual_stacking/releases/tag/v0.12.0).

#### Row Training

```bash
export CUDA_VISIBLE_DEVICES="1" && python3 main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 4 --push_rewards --experience_replay --explore_rate_decay --place --check_row
```

#### Row Testing

```bash
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 4  --push_rewards --experience_replay --explore_rate_decay --trial_reward --future_reward_discount 0.65 --place --check_row --is_testing  --tcp_port 19996 --load_snapshot --snapshot_file '/home/costar/Downloads/snapshot-backup.reinforcement-best-stack-rate.pth' --random_seed 1238 --disable_situation_removal --save_visualizations
```

### Push + Grasp

We provide backwards compatibility with the [Visual Pushing Grasping (VPG) GitHub Repository](https://github.com/andyzeng/visual-pushing-grasping), and evaluate on their pushing and grasping task as a baseline from which to compare our algorithms.

#### Push + Grasp Training

```bash
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/toys' --num_obj 10  --push_rewards --experience_replay --explore_rate_decay
```

You can also run without `--trial_reward` and with the default `--future_reward_discount 0.5`.

#### Push + Grasp Random Object Location Testing

![000040 0 color heightmap](https://user-images.githubusercontent.com/55744/63808939-16fe1500-c8ef-11e9-9dfa-8dc5ed53cd00.png)

```bash
 export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/toys' --num_obj 10  --push_rewards --experience_replay --explore_rate_decay --load_snapshot --snapshot_file '/home/costar/src/costar_visual_stacking/logs/2019-08-17.20:54:32-train-grasp-place-split-efficientnet-21k-acc-0.80/models/snapshot.reinforcement.pth' --random_seed 1238 --is_testing --save_visualizations
```

#### Push + Grasp Adversarial Object Location Testing

![Push grasp adversarial viz](https://user-images.githubusercontent.com/55744/64275313-4aeec100-cf13-11e9-9a04-3f56e2de79d5.png)

[Adversarial pushing and grasping release v0.3.2](https://github.com/jhu-lcsr/costar_visual_stacking/releases/tag/push_grasp_v0.3.2) video:

[![CoSTAR Visual Stacking v0.3.2 test run video](https://img.youtube.com/vi/F85d9xGCDnY/0.jpg)](https://youtu.be/F85d9xGCDnY)

```bash
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/toys' --num_obj 10  --push_rewards --experience_replay --explore_rate_decay --trial_reward --future_reward_discount 0.65 --tcp_port 19996 --is_testing --random_seed 1238 --load_snapshot --snapshot_file '/home/ahundt/src/costar_visual_stacking/logs/2019-09-12.18:21:37-push-grasp-16k-trial-reward/models/snapshot.reinforcement.pth' --max_test_trials 10 --test_preset_cases
```

After Running the test you need to summarize the results:

```bash
python3 evaluate.py --session_directory /home/ahundt/src/costar_visual_stacking/logs/2019-09-16.02:11:25  --method reinforcement --num_obj_complete 6 --preset
```

## Costar Visual Stacking Execution Details

### Running Multiple Simulations in Parallel

It is possible to do multiple runs on different GPUs on the same machine. First, start an instance of V-Rep as below,

```bash
~/src/V-REP_PRO_EDU_V3_6_2_Ubuntu16_04/vrep.sh -gREMOTEAPISERVERSERVICE_19997_FALSE_TRUE -s simulation/simulation.ttt
```

being careful to use V-Rep 3.6.2 wherever it is installed locally. The port number, here 19997 which is the usual default, is the important point, as we will cahnge it in subsequent runs.

Start the simulation as usual, but now specify `--tcp_port 19997`.

Start another V-Rep session.

```bash
~/src/V-REP_PRO_EDU_V3_6_2_Ubuntu16_04/vrep.sh -gREMOTEAPISERVERSERVICE_19996_FALSE_TRUE -s simulation/simulation.ttt
```

For some reason, the port number is important here, and should be selected to be lower than already running sessions.

When you start training, be sure to specify a different GPU. For example, if previously you set

```bash
export CUDA_VISIBLE_DEVICES="0"
```

then you should likely set

```bash
export CUDA_VISIBLE_DEVICES="1"
```

and specify the corresponding tcp port `--tcp_port 19996`.

Additional runs in parallel should use ports 19995, 19994, etc.

## Generating plots

To run jupyter lab or a jupyter notebook in the `costar_visual_stacking/plot_success_rate` folder use the following command:

```bash
jupyter lab ~/src/costar_visual_stacking/plot_success_rate
```

Open jupyter in your favorite browser and there you will also find instructions for generating the plots.

## "Good Robot!" is forked from the Visual Pushing and Grasping Toolbox

[Original Visual Pushing Grasping (VPG) Repository](https://github.com/andyzeng/visual-pushing-grasping). Edits have been made to the text below to reflect some configuration and code updates needed to reproduce the previous VPG paper's original behavior:

Visual Pushing and Grasping (VPG) is a method for training robotic agents to learn how to plan complementary pushing and grasping actions for manipulation (*e.g.* for unstructured pick-and-place applications). VPG operates directly on visual observations (RGB-D images), learns from trial and error, trains quickly, and generalizes to new objects and scenarios.

<img src="images/teaser.jpg" height=228px align="left"/>
<img src="images/self-supervision.gif" height=228px align="left"/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>

This repository provides PyTorch code for training and testing VPG policies with deep reinforcement learning in both simulation and real-world settings on a UR5 robot arm. This is the reference implementation for the paper:

### Learning Synergies between Pushing and Grasping with Self-supervised Deep Reinforcement Learning

[PDF](https://arxiv.org/pdf/1803.09956.pdf) | [Webpage & Video Results](http://vpg.cs.princeton.edu/)

[Andy Zeng](http://andyzeng.github.io/), [Shuran Song](http://vision.princeton.edu/people/shurans/), [Stefan Welker](https://www.linkedin.com/in/stefan-welker), [Johnny Lee](http://johnnylee.net/), [Alberto Rodriguez](http://meche.mit.edu/people/faculty/ALBERTOR@MIT.EDU), [Thomas Funkhouser](https://www.cs.princeton.edu/~funk/)

IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) 2018

Skilled robotic manipulation benefits from complex synergies between non-prehensile (*e.g.* pushing) and prehensile (*e.g.* grasping) actions: pushing can help rearrange cluttered objects to make space for arms and fingers; likewise, grasping can help displace objects to make pushing movements more precise and collision-free. In this work, we demonstrate that it is possible to discover and learn these synergies from scratch through model-free deep reinforcement learning. Our method involves training two fully convolutional networks that map from visual observations to actions: one infers the utility of pushes for a dense pixel-wise sampling of end effector orientations and locations, while the other does the same for grasping. Both networks are trained jointly in a Q-learning framework and are entirely self-supervised by trial and error, where rewards are provided from successful grasps. In this way, our policy learns pushing motions that enable future grasps, while learning grasps that can leverage past pushes. During picking experiments in both simulation and real-world scenarios, we find that our system quickly learns complex behaviors amid challenging cases of clutter, and achieves better grasping success rates and picking efficiencies than baseline alternatives after only a few hours of training. We further demonstrate that our method is capable of generalizing to novel objects.

<!-- ![Method Overview](method.jpg?raw=true) -->
<img src="images/method.jpg" width=100%/>

#### Citing

If you find this code useful in your work, please consider citing:

```
@inproceedings{zeng2018learning,
  title={Learning Synergies between Pushing and Grasping with Self-supervised Deep Reinforcement Learning},
  author={Zeng, Andy and Song, Shuran and Welker, Stefan and Lee, Johnny and Rodriguez, Alberto and Funkhouser, Thomas},
  booktitle={IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year={2018}
}
```

#### Demo Videos

Demo videos of a real robot in action can be found [here](http://vpg.cs.princeton.edu/).

#### Contact

The contact for CoSTAR Visual Stacking is [Andrew Hundt](http://ahundt.github.io/).
The contact for the original [Visual Pushing Grasping repository](https://github.com/andyzeng/visual-pushing-grasping) is [Andy Zeng](http://www.cs.princeton.edu/~andyz/) andyz[at]princeton[dot]edu

## Installation

This implementation requires the following dependencies (tested on Ubuntu 16.04.4 LTS):

* Python 2.7 or Python 3
* [NumPy](http://www.numpy.org/), [SciPy](https://www.scipy.org/scipylib/index.html), [OpenCV-Python](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html), [Matplotlib](https://matplotlib.org/). You can quickly install/update these dependencies by running the following (replace `pip` with `pip3` for Python 3):

  ```bash
  pip3 install numpy scipy opencv-python matplotlib
  ```

* [PyTorch](http://pytorch.org/) version 1.2:

  ```bash
  pip3 install torch==1.2 torchvision==0.4.0
  ```

* [V-REP](http://www.coppeliarobotics.com/) (simulation environment)

### (Optional) GPU Acceleration
Accelerating training/inference with an NVIDIA GPU requires installing [CUDA](https://developer.nvidia.com/cuda-downloads) and [cuDNN](https://developer.nvidia.com/cudnn). You may need to register with NVIDIA for the CUDA Developer Program (it's free) before downloading. This code has been tested with CUDA 8.0 and cuDNN 6.0 on a single NVIDIA Titan X (12GB). Running out-of-the-box with our pre-trained models using GPU acceleration requires 8GB of GPU memory. Running with GPU acceleration is **highly recommended**, otherwise each training iteration will take several minutes to run (as opposed to several seconds). This code automatically detects the GPU(s) on your system and tries to use it. If you have a GPU, but would instead like to run in CPU mode, add the tag `--cpu` when running `main.py` below.

## A Quick-Start: Demo in Simulation

<img src="images/simulation.gif" height=200px align="right" />
<img src="images/simulation.jpg" height=200px align="right" />

This demo runs our pre-trained model with a UR5 robot arm in simulation on challenging picking scenarios with adversarial clutter, where grasping an object is generally not feasible without first pushing to break up tight clusters of objects.

### Instructions

1. Checkout this repository and download our pre-trained models.

    ```shell
    git clone https://github.com/jhu-lcsr/costar_visual_stacking.git visual-pushing-grasping
    cd visual-pushing-grasping/downloads
    ./download-weights.sh
    cd ..
    ```

1. Run V-REP (navigate to your V-REP directory and run `./vrep.sh`). From the main menu, select `File` > `Open scene...`, and open the file `visual-pushing-grasping/simulation/simulation.ttt` from this repository.

1. In another terminal window, run the following (simulation will start in the V-REP window):

    ```shell
    python main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 10 \
        --push_rewards --experience_replay --explore_rate_decay \
        --is_testing --test_preset_cases --test_preset_file 'simulation/test-cases/test-10-obj-07.txt' \
        --load_snapshot --snapshot_file 'downloads/vpg-original-sim-pretrained-10-obj.pth' \
        --save_visualizations --nn densenet
    ```

Note: you may get a popup window titled "Dynamics content" in your V-REP window. Select the checkbox and press OK. You will have to do this a total of 3 times before it stops annoying you.

## Training

To train a regular VPG policy from scratch in simulation, first start the simulation environment by running V-REP (navigate to your V-REP directory and run `./vrep.sh`). From the main menu, select `File` > `Open scene...`, and open the file `visual-pushing-grasping/simulation/simulation.ttt`. Then navigate to this repository in another terminal window and run the following:

```shell
python main.py --is_sim --push_rewards --experience_replay --explore_rate_decay --save_visualizations
```

Data collected from each training session (including RGB-D images, camera parameters, heightmaps, actions, rewards, model snapshots, visualizations, etc.) is saved into a directory in the `logs` folder. A training session can be resumed by adding the flags `--load_snapshot` and `--continue_logging`, which then loads the latest model snapshot specified by `--snapshot_file` and transition history from the session directory specified by `--logging_directory`:

```shell
python main.py --is_sim --push_rewards --experience_replay --explore_rate_decay --save_visualizations \
    --load_snapshot --snapshot_file 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE/models/snapshot-backup.reinforcement.pth' \
    --continue_logging --logging_directory 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE' \
```

Various training options can be modified or toggled on/off with different flags (run `python main.py -h` to see all options):

```shell
usage: main.py [-h] [--is_sim] [--obj_mesh_dir OBJ_MESH_DIR]
               [--num_obj NUM_OBJ] [--num_extra_obj NUM_EXTRA_OBJ]
               [--tcp_host_ip TCP_HOST_IP] [--tcp_port TCP_PORT]
               [--rtc_host_ip RTC_HOST_IP] [--rtc_port RTC_PORT]
               [--heightmap_resolution HEIGHTMAP_RESOLUTION]
               [--random_seed RANDOM_SEED] [--cpu] [--flops] [--method METHOD]
               [--push_rewards]
               [--future_reward_discount FUTURE_REWARD_DISCOUNT]
               [--experience_replay] [--heuristic_bootstrap]
               [--explore_rate_decay] [--grasp_only] [--check_row]
               [--random_weights] [--max_iter MAX_ITER] [--place]
               [--no_height_reward] [--grasp_color_task]
               [--grasp_count GRASP_COUT] [--transfer_grasp_to_place]
               [--check_z_height] [--trial_reward]
               [--check_z_height_goal CHECK_Z_HEIGHT_GOAL]
               [--disable_situation_removal] [--is_testing]
               [--evaluate_random_objects] [--max_test_trials MAX_TEST_TRIALS]
               [--test_preset_cases] [--test_preset_file TEST_PRESET_FILE]
               [--test_preset_dir TEST_PRESET_DIR]
               [--show_preset_cases_then_exit] [--load_snapshot]
               [--snapshot_file SNAPSHOT_FILE] [--nn NN] [--continue_logging]
               [--logging_directory LOGGING_DIRECTORY] [--save_visualizations]

Train robotic agents to learn how to plan complementary pushing, grasping, and placing as well as multi-step tasks
for manipulation with deep reinforcement learning in PyTorch.

optional arguments:
  -h, --help            show this help message and exit
  --is_sim              run in simulation?
  --obj_mesh_dir OBJ_MESH_DIR
                        directory containing 3D mesh files (.obj) of objects
                        to be added to simulation
  --num_obj NUM_OBJ     number of objects to add to simulation
  --num_extra_obj NUM_EXTRA_OBJ
                        number of secondary objects, like distractors, to add
                        to simulation
  --tcp_host_ip TCP_HOST_IP
                        IP address to robot arm as TCP client (UR5)
  --tcp_port TCP_PORT   port to robot arm as TCP client (UR5)
  --rtc_host_ip RTC_HOST_IP
                        IP address to robot arm as real-time client (UR5)
  --rtc_port RTC_PORT   port to robot arm as real-time client (UR5)
  --heightmap_resolution HEIGHTMAP_RESOLUTION
                        meters per pixel of heightmap
  --random_seed RANDOM_SEED
                        random seed for simulation and neural net
                        initialization
  --cpu                 force code to run in CPU mode
  --flops               calculate floating point operations of a forward pass
                        then exit
  --method METHOD       set to 'reactive' (supervised learning) or
                        'reinforcement' (reinforcement learning ie Q-learning)
  --push_rewards        use immediate rewards (from change detection) for
                        pushing?
  --future_reward_discount FUTURE_REWARD_DISCOUNT
  --experience_replay   use prioritized experience replay?
  --heuristic_bootstrap
                        use handcrafted grasping algorithm when grasping fails
                        too many times in a row during training?
  --explore_rate_decay
  --grasp_only
  --check_row           check for placed rows instead of stacks
  --random_weights      use random weights rather than weights pretrained on
                        ImageNet
  --max_iter MAX_ITER   max iter for training. -1 (default) trains
                        indefinitely.
  --place               enable placing of objects
  --no_height_reward    disable stack height reward multiplier
  --grasp_color_task    enable grasping specific colored objects
  --grasp_count GRASP_COUT
                        number of successful task based grasps
  --transfer_grasp_to_place
                        Load the grasping weights as placing weights.
  --check_z_height      use check_z_height instead of check_stacks for any
                        stacks
  --trial_reward        Experience replay delivers rewards for the whole
                        trial, not just next step.
  --check_z_height_goal CHECK_Z_HEIGHT_GOAL
                        check_z_height goal height, a value of 2.0 is 0.1
                        meters, and a value of 4.0 is 0.2 meters
  --disable_situation_removal
                        Disables situation removal, where rewards are set to 0
                        and a reset is triggerd upon reveral of task progress.
  --is_testing
  --evaluate_random_objects
                        Evaluate trials with random block positions, for
                        example testing frequency of random rows.
  --max_test_trials MAX_TEST_TRIALS
                        maximum number of test runs per case/scenario
  --test_preset_cases
  --test_preset_file TEST_PRESET_FILE
  --test_preset_dir TEST_PRESET_DIR
  --show_preset_cases_then_exit
                        just show all the preset cases so you can have a look,
                        then exit
  --load_snapshot       load pre-trained snapshot of model?
  --snapshot_file SNAPSHOT_FILE
  --nn NN               Neural network architecture choice, options are
                        efficientnet, densenet
  --continue_logging    continue logging from previous session?
  --logging_directory LOGGING_DIRECTORY
  --save_visualizations
                        save visualizations of FCN predictions?

```

Results from our baseline comparisons and ablation studies in our [paper](https://arxiv.org/pdf/1803.09956.pdf) can be reproduced using these flags. For example:

* Train reactive policies with pushing and grasping (P+G Reactive); specify `--method` to be `'reactive'`, remove `--push_rewards`, remove `--explore_rate_decay`:

    ```shell
    python main.py --is_sim --method 'reactive' --experience_replay --save_visualizations
    ```

* Train reactive policies with grasping-only (Grasping-only); similar arguments as P+G Reactive above, but add `--grasp_only`:

    ```shell
    python main.py --is_sim --method 'reactive' --experience_replay --grasp_only --save_visualizations
    ```

* Train VPG policies without any rewards for pushing (VPG-noreward); similar arguments as regular VPG, but remove `--push_rewards`:

    ```shell
    python main.py --is_sim --experience_replay --explore_rate_decay --save_visualizations
    ```

* Train shortsighted VPG policies with lower discount factors on future rewards (VPG-myopic); similar arguments as regular VPG, but set `--future_reward_discount` to `0.2`:

    ```shell
    python main.py --is_sim --push_rewards --future_reward_discount 0.2 --experience_replay --explore_rate_decay --save_visualizations
    ```

To plot the performance of a session over training time, run the following:

```shell
python plot.py 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE'
```

Solid lines indicate % grasp success rates (primary metric of performance) and dotted lines indicate % push-then-grasp success rates (secondary metric to measure quality of pushes) over training steps. By default, each point in the plot measures the average performance over the last 200 training steps. The range of the x-axis is from 0 to 2500 training steps. You can easily change these parameters at the top of `plot.py`.

To compare performance between different sessions, you can draw multiple plots at a time:

```shell
python plot.py 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE' 'logs/ANOTHER-SESSION-DIRECTORY-NAME-HERE'
```

## Evaluation

We provide a collection 11 test cases in simulation with adversarial clutter. Each test case consists of a configuration of 3 - 6 objects placed in the workspace in front of the robot. These configurations are manually engineered to reflect challenging picking scenarios, and remain exclusive from the training procedure. Across many of these test cases, objects are laid closely side by side, in positions and orientations that even an optimal grasping policy would have trouble successfully picking up any of the objects without de-cluttering first. As a sanity check, a single isolated object is additionally placed in the workspace separate from the configuration. This is just to ensure that all policies have been sufficiently trained prior to the benchmark (*i.e.* a policy is not ready if fails to grasp the isolated object).

<img src="images/test-cases.jpg" width=100% align="middle" />

The [demo](#a-quick-start-demo-in-simulation) above runs our pre-trained model multiple times (x30) on a single test case. To test your own pre-trained model, simply change the location of `--snapshot_file`:

<!-- ```shell
python main.py --is_sim --obj_mesh_dir 'objects/blocks' --num_obj 10 \
    --push_rewards --experience_replay --explore_rate_decay \
    --is_testing --test_preset_cases --test_preset_file 'simulation/test-cases/test-10-obj-07.txt' \
    --load_snapshot --snapshot_file 'YOUR-SNAPSHOT-FILE-HERE' \
    --save_visualizations
``` -->

```
export CUDA_VISIBLE_DEVICES="0" && python3 main.py --is_sim --obj_mesh_dir 'objects/toys' --num_obj 10  --push_rewards --experience_replay --explore_rate_decay --load_snapshot --snapshot_file '/home/$USER/Downloads/snapshot.reinforcement.pth' --random_seed 1238 --is_testing --save_visualizations --test_preset_cases --test_preset_dir 'simulation/test-cases/' --max_test_trials 10
```

Data from each test case will be saved into a session directory in the `logs` folder. To report the average testing performance over a session, run the following:

```shell
python evaluate.py --session_directory 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE' --method SPECIFY-METHOD --num_obj_complete N
```

where `SPECIFY-METHOD` can be `reactive` or `reinforcement`, depending on the architecture of your model.

`--num_obj_complete N` defines the number of objects that need to be picked in order to consider the task completed. For example, when evaluating our pre-trained model in the demo test case, `N` should be set to 6:

```shell
python evaluate.py --session_directory 'logs/YOUR-SESSION-DIRECTORY-NAME-HERE' --method 'reinforcement' --num_obj_complete 6
```

Average performance is measured with three metrics (for all metrics, higher is better):
1. Average % completion rate over all test runs: measures the ability of the policy to finish the task by picking up at least `N` objects without failing consecutively for more than 10 attempts.
1. Average % grasp success rate per completion.
1. Average % action efficiency: describes how succinctly the policy is capable of finishing the task. See our [paper](https://arxiv.org/pdf/1803.09956.pdf) for more details on how this is computed.

### Creating Your Own Test Cases in Simulation

To design your own challenging test case:

1. Open the simulation environment in V-REP (navigate to your V-REP directory and run `./vrep.sh`). From the main menu, select `File` > `Open scene...`, and open the file `visual-pushing-grasping/simulation/simulation.ttt`.
1. In another terminal window, navigate to this repository and run the following:

    ```shell
    python create.py
    ```

1. In the V-REP window, use the V-REP toolbar (object shift/rotate) to move around objects to desired positions and orientations.
1. In the terminal window type in the name of the text file for which to save the test case, then press enter.
1. Try it out: run a trained model on the test case by running `main.py` just as in the demo, but with the flag `--test_preset_file` pointing to the location of your test case text file.

## Running on a Real Robot (UR5)

The same code in this repository can be used to train on a real UR5 robot arm (tested with UR Software version 1.8). To communicate with later versions of UR software, several minor changes may be necessary in `robot.py` (*e.g.* functions like `parse_tcp_state_data`). Tested with Python 2.7 (not fully tested with Python 3).

### Setting Up Camera System

The PrimeSense Camera can be used with the [perception packages from the Berkeley Automation Lab](https://berkeleyautomation.github.io/perception/install/install.html).

Alternatively, the latest version of our system uses RGB-D data captured from an [Intel® RealSense™ D415 Camera](https://click.intel.com/intelr-realsensetm-depth-camera-d415.html). We provide a lightweight C++ executable that streams data in real-time using [librealsense SDK 2.0](https://github.com/IntelRealSense/librealsense) via TCP. This enables you to connect the camera to an external computer and fetch RGB-D data remotely over the network while training. This can come in handy for many real robot setups. Of course, doing so is not required -- the entire system can also be run on the same computer.

#### Installation Instructions:

1. Download and install [librealsense SDK 2.0](https://github.com/IntelRealSense/librealsense)
1. Navigate to `visual-pushing-grasping/realsense` and compile `realsense.cpp`:

    ```shell
    cd visual-pushing-grasping/realsense
    cmake .
    make
    ```

1. Connect your RealSense camera with a USB 3.0 compliant cable (important: RealSense D400 series uses a USB-C cable, but still requires them to be 3.0 compliant to be able to stream RGB-D data).
1. To start the TCP server and RGB-D streaming, run the following:

    ```shell
    ./realsense
    ```

Keep the executable running while calibrating or training with the real robot (instructions below). To test a python TCP client that fetches RGB-D data from the active TCP server, run the following:

```shell
cd visual-pushing-grasping/real
python capture.py
```

### Calibrating Camera Extrinsics

<img src="images/calibration.gif" height=200px align="right" />
<img src="images/checkerboard.jpg" height=200px align="right" />

We provide a simple calibration script to estimate camera extrinsics with respect to robot base coordinates. To do so, the script moves the robot gripper over a set of predefined 3D locations as the camera detects the center of a moving 4x4 checkerboard pattern taped onto the gripper. The checkerboard can be of any size (the larger, the better).

#### Instructions:

1. Predefined 3D locations are sampled from a 3D grid of points in the robot's workspace. To modify these locations, change the variables `workspace_limits` and `calib_grid_step` at the top of `calibrate.py`.

1. Measure the offset between the midpoint of the checkerboard pattern to the tool center point in robot coordinates (variable `checkerboard_offset_from_tool`). This offset can change depending on the orientation of the tool (variable `tool_orientation`) as it moves across the predefined locations. Change both of these variables respectively at the top of `calibrate.py`.

1. The code directly communicates with the robot via TCP. At the top of `calibrate.py`, change variable `tcp_host_ip` to point to the network IP address of your UR5 robot controller.

1. With caution, run the following to move the robot and calibrate:

    ```shell
    python calibrate.py
    ```

The script also optimizes for a z-scale factor and saves it into `real/camera_depth_scale.txt`. This scale factor should be multiplied with each depth pixel captured from the camera. This step is more relevant for the RealSense SR300 cameras, which commonly suffer from a severe scaling problem where the 3D data is often 15-20% smaller than real world coordinates. The D400 series are less likely to have such a severe scaling problem.

### Training

To train on the real robot, simply run:

```shell
python main.py --tcp_host_ip 'XXX.XXX.X.XXX' --tcp_port 30002 --push_rewards --experience_replay --explore_rate_decay --save_visualizations
```

where `XXX.XXX.X.XXX` is the network IP address of your UR5 robot controller.

### Additional Tools

* Use `touch.py` to test calibrated camera extrinsics -- provides a UI where the user can click a point on the RGB-D image, and the robot moves its end-effector to the 3D location of that point
* Use `debug.py` to test robot communication and primitive actions


### ROS Based Image Collection Setup

Install ROS Melodic [Build ros from source](http://wiki.ros.org/melodic/Installation/Source) from source with python3, so you'll need to ensure `export ROS_PYTHON_VERSION=3` is set for the build.

```
export ROS_PYTHON_VERSION=3 && rosinstall_generator desktop_full --rosdistro melodic --deps --tar > melodic-desktop-full.rosinstall && wstool init -j8 src melodic-desktop-full.rosinstall
```

For the primesense camera add in the [openni2_launch](https://github.com/ros-drivers/openni2_launch), and [rgbd_launch](https://github.com/ros-drivers/rgbd_launch) repositories:

```
cd ~/src/catkin_ros_ws
git clone https://github.com/ros-drivers/openni2_camera.git
git clone https://github.com/ros-drivers/rgbd_launch.git
```

Run the build and install.

```
rosdep install --from-paths src --ignore-src --rosdistro melodic -y && ./src/catkin/bin/catkin_make_isolated --install
```
<!-- 
Then install the primesense image pipeline:

```bash
sudo apt-get install ros-melodic-openni2-launch ros-melodic-image-pipeline python3-rospkg python3-catkin-pkg
``` -->

Running ROS with depth image processing:

```bash
roslaunch openni2_launch openni2.launch depth_registration:=true
```

In a separate tab run our small test script, which currently only supports python2:

```bash
python test_ros_images.py
```

Running RVIZ to look at the images:

```
rosrun rviz rviz
```

The correct images, as done in the [JHU costar dataset](https://sites.google.com/site/costardataset) class [collector](https://github.com/jhu-lcsr/costar_plan/blob/d469d62d72cd405ed07b10c62eb24391c0af1975/ctp_integration/python/ctp_integration/collector.py), are from the following ROS topics:

```

        self.rgb_topic = "/camera/rgb/image_rect_color"
        # raw means it is in the format provided by the openi drivers, 16 bit int
        self.depth_topic = "/camera/depth_registered/hw_registered/image_rect"
```

Calibration:

```
roslaunch aruco_detect aruco_detect.launch
```

```
python3 calibrate_ros.py
```
