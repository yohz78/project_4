from typing import List
from models.round import Round
from models.player import Player
from datetime import datetime
from operator import attrgetter


class Tournament:
    """Objet tournois"""

    def __init__(self, name, place, date, time_management, description, rounds_number):
        self.name = name
        self.place = place
        self.date = date
        self.players: List[Player] = []
        self.time_management = time_management
        self.description = description
        self.rounds = rounds_number
        self.rounds_list: List[Round] = []

    def serialized(self):
        """ Return a dictionary of the tournament attributes"""
        players = self.get_players()
        round_list = self.get_round_list()
        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "players": players,
            "time_management": self.time_management,
            "description": self.description,
            "round_number": self.rounds,
            "round_list": round_list
        }
        return serialized_tournament

    def get_round_list(self):
        """Return the list of serialized rounds of the tournament"""
        serialized_rounds = [round.serialized() for round in self.rounds_list]
        return serialized_rounds

    def get_players(self):
        """Return the list of serialized players of the tournament"""
        serialized_players = [player.serialized() for player in self.players]
        return serialized_players

    def recover_players(self, players):
        "recreate the player list based on players dictionary list"
        player_list = []
        for player in players:
            player = Player(player["surname"], player["name"],
                            player["birthdate"], player["gender"], player["ranking"])
            player_list.append(player)
        return player_list

    def recover_rounds(self, rounds):
        """Return the list of rounds objects based on the list of rounds dictionaries"""
        rounds = []
        for round in rounds:
            matches = []
            serialized_matches = round["matches"]
            for match in serialized_matches:
                player_1_serialized = match["player_1"]
                player_1 = Player(player_1_serialized["surname"], player_1_serialized["name"],
                                  player_1_serialized["birthdate"], player_1_serialized["gender"], player_1_serialized["ranking"])
                player_2_serialized = match["player_2"]
                player_2 = Player(player_2_serialized["surname"], player_2_serialized["name"],
                                  player_2_serialized["birthdate"], player_2_serialized["gender"], player_2_serialized["ranking"])
                new_match = ([player_1, match["result_player_1"]], [player_2, match["result_player_2"]])          
                matches.append(new_match)               
            new_round = Round(
                round["round_number"], round["start_time"], round["end_time"], matches)
            rounds.append(new_round)
        return rounds

    def get_round_number(self):
        """return the number of round expected for the tournament"""
        return self.rounds

    def get_name(self):
        """Return tournament's name"""
        return self.name

    def get_rounds(self):
        """return the number of round expected for the tournament"""
        return self.rounds_list

    def get_playersrank(self):
        """return the player list of the tournament ordered by rank"""    
        self.players.sort(key=attrgetter("ranking"))
        count = 1
        for player in self.players:
            player_name = player.get_name()
            player_surname = player.get_surname()
            player_ranking = player.get_ranking()
            print(
            f"{count} -- Rank {player_ranking} : {player_name} {player_surname}")
            count += 1

    def get_player_list(self):
        """return the player list of the tournament"""
        self.players.sort(key=attrgetter("surname"))
        count = 1
        for player in self.players:
            player_name = player.get_name()
            player_surname = player.get_surname()
            print(
            f"{count} --  {player_name} {player_surname}")
            count += 1

    def add_round(self, round):
        """Append a round of matches to the inner list of a tournament"""
        self.rounds_list.append(round)

    def set_players(self, players):
        """Update the player list of the tournament"""
        self.players = players

    def set_rounds(self, rounds):
        """Update the round list of the tournament"""
        self.rounds_list = rounds

    def create_a_round(self, round_number):
        """Return an object round"""
        now = datetime.now()
        start_time = now.strftime("%d/%m/%Y %H:%M:%S")
        round = Round(round_number, start_time)
        return round

    def save_pairs(self, pairs, saved_pairs):
        """Save a list of names pair for the players in the input list of players
        in the list saved_pairs given in input"""
        for pair in pairs:
            player_1 = pair[0]
            player_2 = pair[1]
            player_1_name = player_1.get_surname()
            player_2_name = player_2.get_surname()
            pair_names = [player_1_name, player_2_name]
            saved_pairs.append(pair_names)
        return saved_pairs

    def choose_players(self, players):
        """Allow to choose the tournament's player based on players in the input list"""
        print("Choisissez 8 joueurs dans la liste ci dessous:")
        count = 1
        for player in players:
            player_name = player.get_name()
            player_surname = player.get_surname()
            print(f"Joueur{count} : {player_name} {player_surname}")
            count += 1
        choice = 0
        player_list = []
        while choice < 8:
            player_number = int(
                input("please choose a player using his number:"))
            player_index = player_number-1
            player = players[player_index]
            player.reset_score()
            player_list.append(player)
            choice += 1
        self.set_players(player_list)


    def run_tournament(self):
        """Run the tournament"""
        total_rounds = self.get_round_number()
        current_round = 0
        saved_pairs = []
        while current_round != total_rounds:
            new_round = self.create_a_round(current_round+1)
            if current_round == 0:
                pairs = new_round.create_pairs(self.players)
                saved_pairs = self.save_pairs(pairs, saved_pairs)
            else:
                pairs = new_round.create_new_pairs(self.players, saved_pairs)
                saved_pairs = self.save_pairs(pairs, saved_pairs)
            new_round.save_matches(pairs)
            self.add_round(new_round)
            current_round += 1
