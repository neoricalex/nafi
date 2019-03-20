import time
from core.envs.griduniverse_env import GridUniverseEnv


def run_griduniverse_from_text_file():
    """
    Run a random agent on an environment that was save via ascii text file.
    Check core/envs/maze_text_files for examples or the _create_custom_world_from_text() function within the environment
    """
    print('\n' + '*' * 20 + 'Creating a pre-made GridUniverse from text file and running random agent on it' + '*' * 20 + '\n')
    env = GridUniverseEnv(custom_world_fp='./core/envs/maze_text_files/mundo.txt')
    for i_episode in range(1):
        observation = env._reset()
        for t in range(10000):
            env._render(mode='graphic')
            action = env.action_space.sample()
            #print('go ' + env.action_descriptors[action])
            #time.sleep(1.5) # uncomment to watch slower
            observation, reward, done, info = env._step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break


if __name__ == '__main__':
    # Run random agent on environment variations
    run_griduniverse_from_text_file()

