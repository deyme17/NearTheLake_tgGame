# NearTheLake_tgGame - A Business Simulation Game

**Overview**

Near the Lake is a simulation-based business game designed to model the dynamics of self-organization, decision-making, and systemic interactions within an economic environment.  
Participants act as directors of enterprises located around a lake, making monthly decisions that affect both their own profits and the ecological state of the shared water resource.

This educational game is intended for use in training, research, and classroom settings to study system thinking, environmental responsibility, group dynamics, and strategic cooperation.

**Objective**

Players aim to maximize their total profit over 48 game periods (each representing one month).  
At each step, participants choose one of four actions that balance economic gain with environmental impact and social responsibility.

**Game Mechanics**

1. **Environment**
   - Up to 8 enterprises (players) are situated around a shared lake.
   - The lake provides water for industrial use, and also receives wastewater.
   - Water quality degrades with pollution and improves naturally during seasonal floods.

2. **Possible Actions Each Turn:**
   - **Discharge Untreated Wastewater**
     * High immediate profit  
     * Degrades lake water quality for all players
   - **Treat Wastewater**
     * Lower profit in the short term  
     * Maintains water quality
   - **Impose Fines**
     * Player sacrifices their own profit to penalize polluters
   - **Reward Clean Enterprises**
     * Player sacrifices their own profit to reward those who treat wastewater

3. **Environmental Dynamics**
   - The lake has position and level metrics which affect scoring.
   - Water quality directly impacts the reward/penalty values of actions.
   - Scores for pollution/treatment are dynamic and depend on lake state.

**Gameplay Structure**

- The game spans **48 rounds (months)**, simulating 4 years.
- Every **8 months**, a **3-minute negotiation round (meeting)** occurs, where players may discuss and vote to end early.
- Every **12 months**, a **flood event** happens, automatically improving water quality.

**New Features**

- ✅ **Telegram Bot Integration**: Full gameplay via Telegram messages and inline keyboards.
- ✅ **Flexible Game Settings**: All game parameters configurable (player count, duration, intervals, bonuses/penalties).
- ✅ **State-Based Command Handling**: Each user state (idle, waiting, in-game) has its own command dispatcher.
- ✅ **Interactive Meeting Rounds**: Players can exchange messages or voice (optional), and vote to end meetings early.
- ✅ **Automated Turn Processing**: Game progresses automatically when all players select actions.
- ✅ **End Game Voting**: Players can democratically end the game before 48 rounds.
- ✅ **Dynamic Scoring**: Action scores depend on environmental conditions, incentivizing long-term thinking.
- ✅ **Action History Reset**: After each turn, player states and scores are cleared/prepared for the next round.
- ✅ **Modular Architecture**: Commands, services, events, and game logic separated into independent modules for scalability.
- ✅ **Voice Message Relay (optional)**: Supports forwarding player voice messages during meetings.

