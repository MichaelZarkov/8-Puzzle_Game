from pathlib import Path

from q_learning import QLearning

if __name__ == '__main__':
    """
    Trains the q-agent.
    Finds a board arrangement which takes the most moves and prints it to the console.
    Saves the resulting state-action map in "q_tables/table_1.pkl".
    
    With these training parameters:
        learning_rate=1.0,
        discount_factor=0.92,
        generations=2000000,
        max_steps=40,
        exploration_probability=1.0
    it takes about 7 minutes to run.

    Note that with the above training parameters 2000000 generations (games played) is probably overkill.
    I speculate that the optimal solution for every board arrangement can be found in 1000000 generations,
    and very close to optimal can be found in 500000 generations.
    """

    agent = QLearning(
        learning_rate=1.0,
        discount_factor=0.92,
        generations=2000000,
        max_steps=40,
        exploration_probability=1.0
    )

    agent.train()
    print(agent.test())

    folder_path = Path(__file__).parent.parent
    file_path = Path(folder_path, 'q_tables\\table_1.pkl')

    agent.save(file_path)