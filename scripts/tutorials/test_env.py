# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.

from tqdm import trange

import pandemic_simulator as ps
from pandemic_simulator.environment.interfaces import InfectionSummary
from pandemic_simulator.environment.done import ORDone, DoneFunctionFactory, DoneFunctionType 
import random


def run_pandemic_gym_env() -> None:
    """Here we execute the gym envrionment wrapped simulator using austin regulations,
    a small town config and default person routines."""

    print('\nA tutorial that runs the OpenAI Gym environment wrapped simulator', flush=True)

    # init globals
    ps.init_globals(seed=2)

    # select a simulator config
    sim_config = ps.sh.small_town_config
    done_threshold = sim_config.max_hospital_capacity # 
    done_fn = ORDone(
            done_fns=[
                DoneFunctionFactory.default(
                    DoneFunctionType.INFECTION_SUMMARY_ABOVE_THRESHOLD,
                    summary_type=InfectionSummary.CRITICAL,
                    threshold=done_threshold,
                ),
                DoneFunctionFactory.default(DoneFunctionType.NO_PANDEMIC, num_days=40),
                # InfectionSummaryAboveThresholdDone, 
            ]
        )

    # make env
    # env = ps.env.PandemicGymEnv3Act.from_config(sim_config=sim_config, 
    #     pandemic_regulations=ps.sh.austin_regulations,
    #     done_fn=done_fn)
    env = ps.env.PandemicGymEnv.from_config(sim_config = sim_config, 
        pandemic_regulations=ps.sh.austin_regulations,
        done_fn=done_fn)

    # run stage-0 action steps in the environment
    env.reset()
    Reward = 0
    print('''You will manually change the stage of response to the simulated pandemic. Wait till 75%''')

    #Once you feel more comfortable change 30->100 and 40->120
    for i in trange(120, desc='Simulating day'):
        # if i>15:
        #     action = input('Enter a Stage number from 0-4. 0 is no restrictions, 4 is most strict lockdown.\n')
        # else:
        action = 0
        obs, reward, done, aux = env.step(action=int(action))  # here the action is the discrete regulation stage identifier
        print("reward is ", reward, ", done is ", done)
        Reward += reward

    # generate plots
    print('Return:'+str(Reward))


if __name__ == '__main__':
    run_pandemic_gym_env()

