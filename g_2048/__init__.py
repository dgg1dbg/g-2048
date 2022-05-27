from gym.envs.registration import register

register(
    id='2048-v0',
    entry_point='g_2048.envs:GameBoardEnv',
)