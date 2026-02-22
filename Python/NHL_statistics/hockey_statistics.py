import json
    
class FileHandler:
    def __init__(self, filename):
        self.__filename = filename
        
    def read(self) -> list[dict]:
        """
        Reads JSON data from file and returns it as a list of dictionaries.

        Raises:
            ValueError: If file name is incorrect or JSON format is invalid.
        """
        try:
            with open(self.__filename) as file:
                content = file.read()
        except:
            raise ValueError("Error with file name")
        return json.loads(content)
    
class Player:
    """Represents a single NHL player and their statistics."""

    def __init__(self, name, nationality, assists, goals, penalties, team, games):
        self.name = name
        self.nationality = nationality
        self.team = team
        self.assists = assists
        self.goals = goals
        self.penalties = penalties
        self.games = games
    
    def __str__(self) -> str:
        """Returns formatted string representation of player stats."""
        return f"{self.name:20} {self.team:3} {self.goals:>3} + {self.assists:>2} = {self.goals+self.assists:>3}"
    
    
class Stats:
    """Stores and manages player statistics."""
    def __init__(self):
        self.__players = []
        
    def add_player(self, name, nationality, assists, goals, penalties, team, games) -> None:
        """Adds a Player object to the statistics collection."""
        self.__players.append(Player(name, nationality, assists, goals, penalties, team, games))
    
    def search(self, name) -> list[Player]:
        """Returns players matching the given name."""
        return [player for player in self.__players if player.name.lower() == name.lower()]
    
    def all_entries(self) -> list[Player]:
        """Returns a copy of all stored players."""
        return list(self.__players)
    
    def players_by_team(self, team: str) -> list[Player]:
        """Returns all players belonging to a specific team."""
        return [player for player in self.__players if player.team.lower() == team.lower()]

    def players_by_country(self, country: str) -> list[Player]:
        """Returns all players from a specific country."""
        return [player for player in self.__players if player.nationality.lower() == country.lower()]
    
    
class StatsApplication:
    def __init__(self):
        self.__stats = Stats()
        
    def search(self):
        name = input("name: ")
        players = self.__stats.search(name)
        if len(players) == 0:
            print("no player found")
            return
        for player in players:
            print(player)
            
    def list_teams(self):
        teams = sorted(set([player.team for player in self.__stats.all_entries()]))
        for team in teams:
            print(team)
            
    def list_countries(self):
        countries = sorted(set([player.nationality for player in self.__stats.all_entries()]))
        for country in countries:
            print(country)
            
    def sort_by_points(self, players: list) -> list[Player]:
        """Returns players sorted by points and goals."""
        return sorted(players, key=lambda p:(p.goals + p.assists, p.goals), reverse=True)
    
    def team_players(self) -> None:
        team = input("team: ")
        players = self.__stats.players_by_team(team)
        if len(players) == 0:
            print(f"no players in {team}")
            return
        for player in self.sort_by_points(players):
            print(player)
            
    def country_players(self) -> None:
        country = input("country: ")
        players = self.__stats.players_by_country(country)
        if len(players) == 0:
            print(f"no players in {country}")
            return
        for player in self.sort_by_points(players):
            print(player)
            
    def most_points(self) -> None:
        try:
            n = int(input("how many: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        for player in self.sort_by_points(self.__stats.all_entries())[:n]:
            print(player)
            
    def most_goals(self) -> None:
        try:
            n = int(input("how many: "))
        except ValueError:
            print("Please enter a valid number.")
            return      
        players = sorted(self.__stats.all_entries(), key=lambda p:(-p.goals, p.games))
        for player in players[:n]:
            print(player)
            
    def help(self) -> None:
        """Displays available commands."""
        print("commands:")
        print("0 quit")
        print("1 search for player")
        print("2 teams")
        print("3 countries")
        print("4 players in team")
        print("5 players from country")
        print("6 most points")
        print("7 most goals")
        
    def load_players(self) -> None:
        filename = input("file name: ")
        handler = FileHandler(filename)
        players = handler.read()
        for player in players:
            self.__stats.add_player(player["name"], player["nationality"], player["assists"], player["goals"], player["penalties"], player["team"], player["games"])
        print(f"read the data of {len(players)} players")
        print()
        
    def execute(self):
        """Starts the command-line application."""
        self.load_players()
        self.help()
        
        while True:
            print()
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.search()
            elif command == "2":
                self.list_teams()
            elif command == "3":
                self.list_countries()
            elif command == "4":
                self.team_players()
            elif command == "5":
                self.country_players()
            elif command == "6":
                self.most_points()
            elif command == "7":
                self.most_goals()
            else:
                self.help()
        
        
            
if __name__ == "__main__":
    application = StatsApplication()
    application.execute()