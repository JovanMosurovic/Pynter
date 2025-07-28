import math
import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action


class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        def max_n(state, depth):
            if state.is_goal_state() or depth == 0:
                scores = state.get_scores()
                # Return a list of scores for all agents
                return [scores.get(chr(ord('A') + i), 0) for i in range(state.get_num_of_players())]

            # Initialize score_list with -inf for all players
            score_list = [-math.inf for i in range(state.get_num_of_players())]
            current_player = state.get_on_move_ord()
            actions = state.get_legal_actions()

            for action in actions:
                successor = state.generate_successor_state(action)
                child_score_list = max_n(successor, depth - 1)

                # Poredi trenutni score_list sa child_score_list za trenutnog igrača
                if score_list[current_player] < child_score_list[current_player]:
                    score_list = child_score_list

            return score_list

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_scores = None
        current_player = state.get_on_move_ord()

        for action in actions:
            successor = state.generate_successor_state(action)
            scores = max_n(successor, max_depth - 1)

            if best_scores is None or scores[current_player] > best_scores[current_player]:
                best_action = action
                best_scores = scores

        return best_action


class MinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        # Identify which player is on the move
        our_player = state.get_on_move_ord()

        def minimax(state, depth, is_maximizing):
            if state.is_goal_state() or depth == 0:
                # Funkcija procene kao razlika rezultata agenta i protivnika
                # Evaluation function as the difference between agent's score and opponent's score
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                return agent_score - opponent_score

            actions = state.get_legal_actions()
            current_player = state.get_on_move_ord()

            if is_maximizing:  # Naš agent
                max_eval = -math.inf
                for action in actions:
                    successor = state.generate_successor_state(action)
                    # Sledeći igrač je maximizing ako je naš igrač
                    # The next player is maximizing if it's our player
                    eval_score = minimax(successor, depth - 1, successor.get_on_move_ord() == our_player)
                    max_eval = max(max_eval, eval_score)
                return max_eval
            else:  # Oponent
                min_eval = math.inf
                for action in actions:
                    successor = state.generate_successor_state(action)
                    # Sledeći igrač je maximizing ako je naš igrač
                    # The next player is maximizing if it's our player
                    eval_score = minimax(successor, depth - 1, successor.get_on_move_ord() == our_player)
                    min_eval = min(min_eval, eval_score)
                return min_eval

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            # Početni poziv je uvek maximizing jer je naš red
            # The initial call is always maximizing since it's our turn
            score = minimax(successor, max_depth - 1, successor.get_on_move_ord() == our_player)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action


class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        # Identify which player is on the move
        our_player = state.get_on_move_ord()

        def minimax_alpha_beta(state, depth, alpha, beta, is_maximizing):
            if state.is_goal_state() or depth == 0:
                # Funkcija procene kao razlika rezultata agenta i protivnika
                # Function evaluation as the difference between agent's score and opponent's score
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                return agent_score - opponent_score

            actions = state.get_legal_actions()

            if is_maximizing:  # Our agent
                max_eval = -math.inf
                for action in actions:
                    successor = state.generate_successor_state(action)
                    eval_score = minimax_alpha_beta(successor, depth - 1, alpha, beta,
                                                    successor.get_on_move_ord() == our_player)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
                return max_eval
            else:  # Opponent
                min_eval = math.inf
                for action in actions:
                    successor = state.generate_successor_state(action)
                    eval_score = minimax_alpha_beta(successor, depth - 1, alpha, beta,
                                                    successor.get_on_move_ord() == our_player)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
                return min_eval

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            score = minimax_alpha_beta(successor, max_depth - 1, alpha, beta,
                                       successor.get_on_move_ord() == our_player)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, score)

        return best_action
