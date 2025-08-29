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
        def max_n(state, depth, player):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation_list(node)
                scores = state.get_scores()
                return [scores.get(chr(ord('A') + i), 0) for i in range(state.get_num_of_players())]

            score_list = [-math.inf for i in range(state.get_num_of_players())]  # get_player_count()
            i = player  # player.get_index()

            for action in state.get_legal_actions():  # for succ in node.successors()
                successor = state.generate_successor_state(action)
                next_player = successor.get_on_move_ord()  # get_next(player)
                child_score_list = max_n(successor, depth - 1, next_player)

                # score_list = score_list if score_list[i] >= child_score_list[i] else child_score_list
                if score_list[i] < child_score_list[i]:
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
            next_player = successor.get_on_move_ord()
            scores = max_n(successor, max_depth - 1, next_player)

            if best_scores is None or scores[current_player] > best_scores[current_player]:
                best_action = action
                best_scores = scores

        return best_action


class MinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def minimax(state, depth, player):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation(node)
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                return agent_score - opponent_score

            actions = state.get_legal_actions()

            if player == Player.MAX:
                score = -math.inf
                for action in actions:  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = max(score, minimax(successor, depth - 1, Player.MIN))
                return score
            else:  # player == Player.MIN
                score = +math.inf
                for action in actions:  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = min(score, minimax(successor, depth - 1, Player.MAX))
                return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            # Always start as MAX player
            score = minimax(successor, max_depth - 1, Player.MIN)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action


class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def minimax_alpha_beta(state, depth, player, alpha, beta):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation(node)
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                return agent_score - opponent_score

            actions = state.get_legal_actions()

            if player == Player.MAX:
                score = -math.inf
                for action in actions:  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = max(score, minimax_alpha_beta(successor, depth - 1, Player.MIN, alpha, beta))
                    alpha = max(alpha, score)
                    if alpha >= beta:  # alpha-cut
                        break
                return score
            else:  # player == Player.MIN
                score = +math.inf
                for action in actions:  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = min(score, minimax_alpha_beta(successor, depth - 1, Player.MAX, alpha, beta))
                    beta = min(beta, score)
                    if alpha >= beta:  # beta-cut
                        break
                return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            # Always start as MAX player
            score = minimax_alpha_beta(successor, max_depth - 1, Player.MIN, alpha, beta)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, score)

        return best_action


class NegamaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def switch(player):
            return Player.MIN if player == Player.MAX else Player.MAX

        def negamax(state, player, depth):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation(node) * (-1 if player == Player.MIN else 1)
                scores = state.get_scores()
                current_player_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_scores = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                evaluation = current_player_score - opponent_scores
                return evaluation * (-1 if player == Player.MIN else 1)

            score = -math.inf
            for action in state.get_legal_actions():  # for succ in node.successors()
                successor = state.generate_successor_state(action)
                score = max(score, -negamax(successor, switch(player), depth - 1))
            return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            score = -negamax(successor, Player.MIN, max_depth - 1)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action


class NegamaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def switch(player):
            return Player.MIN if player == Player.MAX else Player.MAX

        def negamax_alpha_beta(state, player, alpha, beta, depth):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation(node) * (-1 if player == Player.MIN else 1)
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                evaluation = agent_score - opponent_score
                return evaluation * (-1 if player == Player.MIN else 1)

            score = -math.inf
            for action in state.get_legal_actions():  # for succ in node.successors()
                successor = state.generate_successor_state(action)
                val = -negamax_alpha_beta(successor, switch(player), -beta, -alpha, depth - 1)
                score = max(score, val)
                alpha = max(alpha, score)
                if alpha >= beta:  # break
                    break
            return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            # Always start as MAX player
            score = -negamax_alpha_beta(successor, Player.MIN, -beta, -alpha, max_depth - 1)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, score)

        return best_action


class IterativeDeepeningMinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def id_minimax(state, player, depth, MAX_DEPTH):
            if depth == MAX_DEPTH or state.is_goal_state():  # depth == MAX_DEPTH or is_terminal_node(node)
                # node_evaluation(node)
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                return agent_score - opponent_score

            if player == Player.MAX:
                score = -math.inf
                for action in state.get_legal_actions():  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = max(score, id_minimax(successor, Player.MIN, depth + 1, MAX_DEPTH))
                return score
            else:  # player == Player.MIN
                score = +math.inf
                for action in state.get_legal_actions():  # for succ in node.successors()
                    successor = state.generate_successor_state(action)
                    score = min(score, id_minimax(successor, Player.MAX, depth + 1, MAX_DEPTH))
                return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None

        # Iterative Deepening
        for current_depth in range(1, max_depth + 1):
            current_best_action = None
            current_best_score = -math.inf

            for action in actions:
                successor = state.generate_successor_state(action)
                # Always start as MAX player, depth starts from 1
                score = id_minimax(successor, Player.MIN, 1, current_depth)

                if score > current_best_score:
                    current_best_score = score
                    current_best_action = action

            best_action = current_best_action

        return best_action


class NegaScoutAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        class Player:
            MAX = "MAX"
            MIN = "MIN"

        our_player = state.get_on_move_ord()

        def switch(player):
            return Player.MIN if player == Player.MAX else Player.MAX

        def negascout(state, player, alpha, beta, depth):
            if state.is_goal_state() or depth == 0:  # is_terminal_node(node)
                # node_evaluation(node) * (-1 if player == Player.MIN else 1)
                scores = state.get_scores()
                agent_score = scores.get(chr(ord('A') + our_player), 0)
                opponent_score = sum(score for key, score in scores.items() if key != chr(ord('A') + our_player))
                evaluation = agent_score - opponent_score
                return evaluation * (-1 if player == Player.MIN else 1)

            score = -math.inf
            actions = state.get_legal_actions()
            first_child = True

            for action in actions:  # for succ in node.successors()
                successor = state.generate_successor_state(action)

                if first_child:  # if succ is node.first_child()
                    val = -negascout(successor, switch(player), -beta, -alpha, depth - 1)
                    first_child = False
                else:
                    val = -negascout(successor, switch(player), -alpha - 1, -alpha, depth - 1)

                    if alpha < val < beta:
                        val = -negascout(successor, switch(player), -beta, -alpha, depth - 1)

                score = max(score, val)
                alpha = max(alpha, score)

                if alpha >= beta:
                    break

            return score

        actions = state.get_legal_actions()
        if not actions:
            return None

        best_action = None
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for action in actions:
            successor = state.generate_successor_state(action)
            # Always start as MAX player
            score = -negascout(successor, Player.MIN, -beta, -alpha, max_depth - 1)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, score)

        return best_action